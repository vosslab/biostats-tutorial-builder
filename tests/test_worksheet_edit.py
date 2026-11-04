"""Focused contracts for coordinated source-coordinate maintenance."""

import pathlib

import pytest
import make_tutorial
import tutorial_lib.compiler
import tutorial_lib.worksheet_edit


#============================================
def lesson() -> str:
	"""Create one valid, deliberately ordinary student-authored lesson."""
	rows = "".join(f"| {number} | {number + 10} |\n" for number in range(1, 26))
	source = "# Coordinate practice\n\n## Workbook\n\n### Sheet: Data\n\n"
	source += "| Hours | Score |\n| --- | --- |\n" + rows
	source += "\n- **Region A1:B26:** source\n- **Region C1:C26:** calculation\n"
	source += ("\n### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part: Spreadsheet practice\n\n#### Step: Calculate\n\n")
	source += "In cell C2, enter [=A2^2](enter:C2), then [fill down through C26](fill:C2:C26). "
	source += "Use =AVERAGE(A2:A26), but retain =COUNT(B2:B101) for future rows.\n"
	return source


#============================================
def write_lesson(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Write a source file only for the edit command's normal file API."""
	path = tmp_path / "lesson.md"
	path.write_text(lesson(), encoding="utf-8")
	return path


#============================================
def test_insert_column_updates_visible_targets_and_formulas_without_writing(tmp_path: pathlib.Path) -> None:
	"""A layout shift updates prose, action URLs, fills, and formula operands together."""
	path = write_lesson(tmp_path)
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=3, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert path.read_text(encoding="utf-8") == result.source
	assert "cell D2" in result.updated_source
	assert "(enter:D2)" in result.updated_source
	assert "fill:D2:D26" in result.updated_source
	assert "=A2^2" in result.updated_source


#============================================
def test_insert_before_implicit_data_table_makes_shifted_geometry_explicit(tmp_path: pathlib.Path) -> None:
	"""A whole-sheet shift does not silently leave the supplied table at A1."""
	path = write_lesson(tmp_path)
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "#### At: B1\n\n| Hours | Score |" in result.updated_source
	assert "**Region B1:C26:** source" in result.updated_source
	assert "(enter:D2)" in result.updated_source


#============================================
def test_layout_edit_does_not_rewrite_unmarked_scientific_or_biology_prose(tmp_path: pathlib.Path) -> None:
	"""A1-looking prose is not a worksheet reference without technical Markdown context."""
	path = write_lesson(tmp_path)
	path.write_text(path.read_text(encoding="utf-8")
		+ "The model is y-hat = b0 + b1 x + b2 x^2. Vitamin B12 supports biology.\n",
		encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "y-hat = b0 + b1 x + b2 x^2" in result.updated_source
	assert "Vitamin B12 supports biology" in result.updated_source


#============================================
def test_layout_edit_leaves_unmarked_biology_sentences_unchanged(tmp_path: pathlib.Path) -> None:
	"""Cell-shaped biology terms remain prose without a technical marker."""
	path = write_lesson(tmp_path)
	path.write_text(path.read_text(encoding="utf-8")
		+ "The vitamin B12 is required. A mutation in TP53 is serious. "
		+ "B12 contains a cofactor.\n", encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "The vitamin B12 is required." in result.updated_source
	assert "A mutation in TP53 is serious." in result.updated_source
	assert "B12 contains a cofactor." in result.updated_source


#============================================
def test_layout_edit_updates_explicit_uppercase_column_syntax(tmp_path: pathlib.Path) -> None:
	"""An uppercase column coordinate remains an intentional worksheet reference."""
	path = write_lesson(tmp_path)
	path.write_text(path.read_text(encoding="utf-8")
		+ "The calculation column C contains reader work.\n"
		+ "[Fill C2:C26](fill:C2:C26) down.\n", encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "The calculation column D contains reader work." in result.updated_source
	assert "[Fill D2:D26](fill:D2:D26) down." in result.updated_source


#============================================
def test_layout_edit_updates_explicit_technical_range_and_notices_for_bare_cells(tmp_path: pathlib.Path) -> None:
	"""A natural range is safe, but unmarked individual cells need author review."""
	path = write_lesson(tmp_path)
	path.write_text(path.read_text(encoding="utf-8")
		+ "Write the fitted equation using I2:I4. Compare the results in M4 and I5.\n",
		encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "using J2:J4" in result.updated_source
	assert "in M4 and I5" in result.updated_source
	assert any("coordinate-looking text" in notice for notice in result.notices)


#============================================
def test_cli_accepts_write_after_the_edit_operation(tmp_path: pathlib.Path) -> None:
	"""The explicit confirmation flag works in the order authors naturally type."""
	path = write_lesson(tmp_path)
	status = make_tutorial.main(["worksheet-edit", str(path), "--sheet", "Data",
		"insert-columns", "--at", "C", "--count", "1", "--write"])
	assert status == 0
	assert "cell D2" in path.read_text(encoding="utf-8")


#============================================
def test_cli_reports_invalid_column_as_one_line_author_error(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
	"""An invalid column is a usable command error instead of a Python traceback."""
	path = write_lesson(tmp_path)
	status = make_tutorial.main(["worksheet-edit", str(path), "--sheet", "Data",
		"insert-columns", "--at", "ZZZ", "--count", "1"])
	captured = capsys.readouterr()
	assert status == 1
	assert captured.err == "worksheet-edit: Column must be between A and XFD\n"
	assert "Traceback" not in captured.err
#============================================
def test_move_range_updates_layout_coordinates_and_preserves_formula_anchors(tmp_path: pathlib.Path) -> None:
	"""A compact calculation block moves as an author-directed table, not a new design."""
	path = write_lesson(tmp_path)
	source = path.read_text(encoding="utf-8")
	source = source.replace("#### Step: Calculate\n\n", "#### Step: Calculate\n\n"
		"In cell H1, label [Result](label:H1). In cell I2, enter [=$A$2](enter:I2). "
		"In cell H3, enter [=I2](enter:H3). Use the table H1:I3.\n\n")
	path.write_text(source, encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("move-range", "Data",
		source_range="H1:I3", destination="J1")
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "cell J1" in result.updated_source
	assert "(label:J1)" in result.updated_source
	assert "(enter:K2)" in result.updated_source
	assert "(enter:J3)" in result.updated_source
	assert "=K2" in result.updated_source
	assert "=$A$2" in result.updated_source
	assert "J1:K3" in result.updated_source


#============================================
def test_resize_observations_extends_exact_ranges_but_preserves_spare_capacity(tmp_path: pathlib.Path) -> None:
	"""Growing supplied data updates dependent endpoints without shrinking row 101 capacity."""
	path = write_lesson(tmp_path)
	request = tutorial_lib.worksheet_edit.WorksheetEdit("resize-observations", "Data",
		data_range="A1:B26", rows=50)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "**Region A1:B51:** source" in result.updated_source
	assert "**Region C1:C51:** calculation" in result.updated_source
	assert "fill:C2:C51" in result.updated_source
	assert "=AVERAGE(A2:A51)" in result.updated_source
	assert "=COUNT(B2:B101)" in result.updated_source
	assert result.updated_source.count("| | |\n") == 25
	assert any("review numerical explanation" in notice for notice in result.notices)


#============================================
def test_resize_observations_can_shrink_the_declared_data_table(tmp_path: pathlib.Path) -> None:
	"""A smaller source table removes trailing supplied rows and updates its ranges."""
	path = write_lesson(tmp_path)
	request = tutorial_lib.worksheet_edit.WorksheetEdit("resize-observations", "Data",
		data_range="A1:B26", rows=10)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "**Region A1:B11:** source" in result.updated_source
	assert "**Region C1:C11:** calculation" in result.updated_source
	assert "fill:C2:C11" in result.updated_source
	assert "=AVERAGE(A2:A11)" in result.updated_source
	assert "| 11 | 21 |" not in result.updated_source


#============================================
def test_resize_observations_preserves_prose_and_syncs_visible_fill_range(
	tmp_path: pathlib.Path) -> None:
	"""A resize changes deliberate coordinates but leaves prose untouched."""
	path = write_lesson(tmp_path)
	source = path.read_text(encoding="utf-8")
	source += "The blank calculation column is where readers record their results.\n"
	source += "[Fill C2:C26](fill:C2:C26) down.\n"
	path.write_text(source, encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("resize-observations", "Data",
		data_range="A1:B26", rows=50)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	assert "The blank calculation column is where readers record their results." in result.updated_source
	assert "[Fill C2:C51](fill:C2:C51) down." in result.updated_source


#============================================
def test_write_requires_source_to_match_preview_and_does_not_apply_partial_edit(tmp_path: pathlib.Path) -> None:
	"""A stale preview cannot overwrite concurrent author work."""
	path = write_lesson(tmp_path)
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-rows", "Data", at=2, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	path.write_text(result.source + "\nAuthor revision.\n", encoding="utf-8")
	with pytest.raises(tutorial_lib.worksheet_edit.WorksheetEditError, match="changed after preview"):
		tutorial_lib.worksheet_edit.write_edit(path, result)
	assert path.read_text(encoding="utf-8").endswith("Author revision.\n")


#============================================
@pytest.mark.parametrize("kind,at,value_cell,target", [
	("insert-columns", 1, (1, 6), "F2"),
	("insert-columns", 5, (1, 6), "F2"),
	("insert-rows", 1, (2, 5), "E3"),
	("insert-rows", 2, (1, 5), "E3"),
])
def test_insert_preserves_all_anchored_table_geometry(tmp_path: pathlib.Path, kind: str,
	at: int, value_cell: tuple[int, int], target: str) -> None:
	"""Every supplied table moves or expands with its matching student action."""
	source = "# Tables\n\n## Workbook\n\n### Sheet: Data\n\n#### At: B1\n\n"
	source += "| Observation |\n| --- |\n| 12 |\n| 15 |\n"
	source += "\n#### At: D1\n\n| Statistic | Value |\n| --- | --- |\n| Mean | |\n"
	source += ("\n### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part: Calculate\n\n#### Step: Mean\n\n")
	source += "In cell E2, enter [`=AVERAGE(B2:B3)`](enter:E2).\n"
	path = tmp_path / "tables.md"
	path.write_text(source, encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit(kind, "Data", at=at, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	document = tutorial_lib.compiler.compile_source(result.updated_source, path)
	sheet = document.worksheets[0]
	assert sheet.cells[value_cell].scalar.value == "Value"
	assert document.actions[0].target.address == target
	assert sheet.cells[(document.actions[0].target.start_row,
		document.actions[0].target.start_column)].scalar.kind == "blank"


#============================================
def test_legacy_target_and_nested_formula_shift_once_but_code_examples_stay_literal(
	tmp_path: pathlib.Path) -> None:
	"""Executable fenced formulas follow the same edit as their legacy target."""
	source = "# Formula\n\n## Workbook\n\n### Sheet: Data\n\n"
	source += "| Observation |\n| --- |\n| 12 |\n| 15 |\n"
	source += ("\n### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part: Calculate\n\n#### Step: Count\n\n")
	source += "- **Enter E2:**\n\n  ```sheets\n  =COUNT(A2:A3)\n  ```\n"
	source += "\n```text\nIn cell E2, use `=COUNT(A2:A3)`.\n```\n"
	path = tmp_path / "formula.md"
	path.write_text(source, encoding="utf-8")
	request = tutorial_lib.worksheet_edit.WorksheetEdit("insert-columns", "Data", at=1, count=1)
	result = tutorial_lib.worksheet_edit.prepare_edit(path, request)
	document = tutorial_lib.compiler.compile_source(result.updated_source, path)
	assert "**Enter F2:**" in result.updated_source
	assert document.actions[0].scalar.value == "=COUNT(B2:B3)"
	assert "In cell E2, use `=COUNT(A2:A3)`." in result.updated_source
