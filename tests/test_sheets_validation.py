"""Local spreadsheet cases preserve typed values and scientific comparisons."""

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
