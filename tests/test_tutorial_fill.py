"""Protect concise fill teaching, spreadsheet translation, and branch safety."""

import pathlib
import zipfile

import openpyxl
import defusedxml.ElementTree

import sheets_validation_lib
import tutorial_lib.compiler
import tutorial_lib.workbook
import tutorial_lib.docx_renderer


def compile_fill(instructions: str) -> object:
	source = "# Fill example\n\n## Workbook\n\n### Sheet: Data\n\n"
	source += "| A | B |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |\n| 5 | 6 |\n\n"
	source += ("### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part: Calculate\n\n#### Step: Fill formulas\n\n")
	document = tutorial_lib.compiler.compile_source(source + instructions)
	return document


def test_fill_translation_replay_and_blank_concise_outputs(tmp_path: pathlib.Path) -> None:
	"""Filled calculations must remain executable without expanding the student handout."""
	instructions = '- **Enter E2:** `=A2+$B2+A$2+$B$2`\n'
	instructions += '- **Enter F2:** `=E2+\'Data\'!A2+IF(A2=1,"A2",0)`\n'
	instructions += '- **Fill E2:F4:** Down\n- **Enter G2:** `=SUM(E2:F4)`\n'
	document = compile_fill(instructions)
	assert not document.has_errors
	assert not any(item.category.endswith("input") for item in document.diagnostics)
	writes = sheets_validation_lib.prepare_cases(document)[0]["writes"]
	assert [(write["address"], write["value"]["formulaValue"]) for write in writes[2:6]] == [
		("E3", "=A3+$B3+A$2+$B$2"),
		("F3", '=E3+\'Data\'!A3+IF(A3=1,"A2",0)'),
		("E4", "=A4+$B4+A$2+$B$2"),
		("F4", '=E4+\'Data\'!A4+IF(A4=1,"A2",0)'),
	]
	workbook_path = tmp_path / "student.xlsx"
	tutorial_lib.workbook.write_workbook(document, workbook_path)
	book = openpyxl.load_workbook(workbook_path)
	assert all(book["Data"][write["address"]].value is None for write in writes)
	book.close()
	docx_path = tmp_path / "student.docx"
	tutorial_lib.docx_renderer.write_document(document, docx_path)
	with zipfile.ZipFile(docx_path) as archive:
		root = defusedxml.ElementTree.fromstring(archive.read("word/document.xml"))
	texts = "".join(root.itertext())
	assert texts.count("Fill E2:F4:") == 1
	assert "Enter E3:" not in texts and "Enter F4:" not in texts


def test_fill_rejects_invalid_sources_directions_ranges_and_overwrites() -> None:
	cases = [
		('- **Fill C2:C4:** Down', "fill-source"),
		('- **Enter C2:** 3\n- **Fill C2:C4:** Down', "fill-source"),
		('- **Enter C2:** `=A2`\n- **Fill C2:C4:** Up', "action-syntax"),
		('- **Enter C2:** `=A2`\n- **Fill C2:D2:** Down', "action-target"),
		('- **Enter C2:** `=A2`\n- **Fill C4:C2:** Down', "action-target"),
		('- **Enter C2:** `=A2`\n- **Enter C3:** 9\n- **Fill C2:C4:** Down',
			"assignment-conflict"),
	]
	for instructions, category in cases:
		document = compile_fill(instructions)
		assert document.has_errors
		assert any(item.category == category for item in document.diagnostics)
	malformed = compile_fill('- **Enter C2:** `=A2)`\n- **Fill C2:C3:** Down')
	assert malformed.has_errors
	fill_diagnostic = next(item for item in malformed.diagnostics
		if item.category == "fill-formula")
	assert fill_diagnostic.span.start_line > 0
	assert "pop from empty list" in fill_diagnostic.message
	assert any(item.category == "formula-syntax" for item in malformed.diagnostics)


def test_fill_respects_possible_branch_sources_and_selected_execution() -> None:
	instructions = '- **Alternative: First**\n  - **Enter C2:** `=A2`\n'
	instructions += '- **Alternative: Second**\n  - **Enter C2:** `=A2`\n\n'
	instructions += '- **Fill C2:C4:** Down\n- **Enter D2:** `=SUM(C2:C4)`\n'
	document = compile_fill(instructions)
	assert not document.has_errors
	cases = sheets_validation_lib.prepare_cases(document)
	assert len(cases) == 2
	assert all([write["address"] for write in case["writes"]] == ["C2", "C3", "C4", "D2"]
		for case in cases)
	for replacement in ('  - **Enter C2:** `=B2`', '  - **Explain:** No formula.'):
		invalid = compile_fill(instructions.replace('  - **Enter C2:** `=A2`', replacement, 1))
		assert any(item.category == "fill-source" for item in invalid.diagnostics)
	branch_fills = instructions.replace('  - **Enter C2:** `=A2`',
		'  - **Enter C2:** `=A2`\n  - **Fill C2:C4:** Down')
	branch_fills = branch_fills.replace('\n- **Fill C2:C4:** Down', '')
	branch_fills = branch_fills.replace('**Alternative: Second**\n  - **Enter C2:** `=A2`',
		'**Alternative: Second**\n  - **Enter C2:** `=B2`')
	branch_document = compile_fill(branch_fills)
	assert not branch_document.has_errors
	branch_cases = sheets_validation_lib.prepare_cases(branch_document)
	assert branch_cases[0]["writes"][2]["value"] == {"formulaValue": "=A4"}
	assert branch_cases[1]["writes"][2]["value"] == {"formulaValue": "=B4"}
