"""Offline contracts protecting isolated Sheets execution and scientific comparison."""

import pathlib

import pytest

import tutorial_lib.model
import tutorial_lib.compiler
import sheets_validation_lib


def test_independent_branches_preserve_replacements_and_literal_types() -> None:
	"""Prevent branch leakage and accidental evaluation of literal text."""
	source = "# Example\n\n## Workbook\n\n### Sheet: Data\n\n"
	source += "| Header | Result |\n| --- | --- |\n| 2 | |\n\n"
	source += ("### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part: Calculate\n\n#### Step: Values\n\n")
	source += "- **Alternative: First**\n  - **Enter B2:** `=A2+1`\n"
	source += "- **Alternative: Second**\n  - **Enter B2:** `=A2+2`\n\n"
	source += "- **Replace B2:** `=A2+3`\n"
	document = tutorial_lib.compiler.compile_source(source)
	cases = sheets_validation_lib.prepare_cases(document)
	assert [case["scenario"] for case in cases] == ["baseline", "group-1-branch-2"]
	assert [write["value"] for write in cases[1]["writes"]] == [
		{"formulaValue": "=A2+2"}, {"formulaValue": "=A2+3"}]
	literal = tutorial_lib.model.Scalar("text", "=NOT_A_FORMULA")
	assert sheets_validation_lib.extended_value(literal) == {
		"stringValue": "=NOT_A_FORMULA"}


def test_oracles_reject_errors_and_coercions_but_allow_numeric_tolerance() -> None:
	cells = {"Data!A1": {"effectiveValue": {"numberValue": 1.000000001}},
		"Data!A2": {"effectiveValue": {"boolValue": True}},
		"Data!A3": {"effectiveValue": {"errorValue": {"type": "NAME"}}},
		"Data!A4": {"effectiveValue": {"stringValue": "text"}}}
	expected = {"Data!A1": {"value": 1}, "Data!A2": {"value": 1},
		"Data!A3": {"value": None}, "Data!A4": {"value": "Text"},
		"Data!A5": {"value": 0}, "Missing!Z999": {"value": None}}
	results = sheets_validation_lib.compare_expectations(cells, expected)
	assert [result["status"] for result in results] == [
		"passed", "failed", "failed", "failed", "failed", "failed"]


class FakeRequest:
	def __init__(self, result: dict) -> None:
		self.result = result

	def execute(self, num_retries: int) -> dict:
		return self.result


class FakeSheets:
	"""Inspect request structure only: this transport never evaluates a formula."""

	def __init__(self) -> None:
		self.created = []
		self.writes = []

	def spreadsheets(self) -> object:
		return self

	def create(self, body: dict, fields: str) -> FakeRequest:
		self.created.append(body)
		return FakeRequest({"spreadsheetId": "offline-fake-id", "spreadsheetUrl": "fake-url"})

	def batchUpdate(self, spreadsheetId: str, body: dict) -> FakeRequest:
		self.writes.append((spreadsheetId, body))
		return FakeRequest({})

	def get(self, spreadsheetId: str, ranges: list, includeGridData: bool,
		fields: str) -> FakeRequest:
		return FakeRequest({"sheets": [{"properties": {"title": "Other sheet"},
			"data": [{"startRow": 1, "startColumn": 1, "rowData": [{"values": [{
				"userEnteredValue": {"formulaValue": "='Other sheet'!A1+1"},
				"effectiveValue": {"errorValue": {"type": "NAME", "message": "fake error"}}}]}]}]}]})


def test_live_request_boundary_creates_only_new_workbooks_and_records_errors(
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	monkeypatch.setattr(sheets_validation_lib.time, "sleep", lambda seconds: None)
	service = FakeSheets()
	write = {"sheet": "Other sheet", "row": 2, "column": 2, "address": "B2", "line": 10,
		"value": {"formulaValue": "='Other sheet'!A1+1"}}
	case = {"tutorial": str(pathlib.Path("example.md")), "scenario": "baseline",
		"sheets": ["Other sheet"], "seeds": [], "writes": [write]}
	created = []
	result = sheets_validation_lib.run_case(service, case, {}, created.append)
	assert created == [{"spreadsheetId": "offline-fake-id", "spreadsheetUrl": "fake-url"}]
	assert service.writes[0][0] == "offline-fake-id"
	assert service.writes[0][1]["requests"][0]["updateCells"]["rows"][0]["values"][0] == {
		"userEnteredValue": write["value"]}
	assert result["sheets_status"] == "failed"
	assert result["oracle_status"] == "not_provided"
	# A successful HTTP response with no computed cells is not calculation success.
	monkeypatch.setattr(service, "get", lambda **kwargs: FakeRequest({}))
	missing = sheets_validation_lib.run_case(service, case, {}, created.append)
	assert missing["sheets_status"] == "failed"
	assert {error["error"]["type"] for error in missing["errors"]} == {"MISSING_RESULT"}
