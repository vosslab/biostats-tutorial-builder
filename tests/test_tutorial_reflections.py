"""Authoritative reflection lists stay aligned across editable exports and bundles."""

import copy
import pathlib

import docx
import pytest
import openpyxl

import tutorial_lib.build
import tutorial_lib.compiler
import tutorial_lib.workbook
import tutorial_lib.docx_renderer


def source(questions: str = "1. Why does the result matter?", part: str = "Part: Analyze") -> str:
	text = "# Example\n\n## Workbook\n\n### Sheet: Data\n\n"
	text += "| Result |\n| --- |\n| 4 |\n\n### Reflection Questions\n\n"
	text += questions + "\n\n## Tutorial\n\n### " + part
	text += "\n\n#### Step: Observe\n\nCompare the results.\n"
	return text


@pytest.mark.parametrize("broken", [
	source().replace("### Reflection Questions\n\n1. Why does the result matter?\n\n", ""),
	source(""),
	source("1. "),
	source("1.\n2. Question\n\n   Extra paragraph."),
	source("- Why?"),
	source("1. Why?\n   - Nested question"),
	source("1. Why?\n\n   Extra paragraph."),
	source("1. What does ![plot](figure.png) show?"),
	source("1. Use [4](enter:A1) to explain."),
	source("1. Why <span>this</span>?"),
	source().replace("### Reflection Questions", "### Reflection Questions (optional)"),
	source().replace("### Reflection Questions", "#### Reflection Questions"),
	source().replace("## Workbook", "## Workbook\n\n### Reflection Questions\n\n1. Extra?"),
	source().replace("### Reflection Questions\n\n1. Why does the result matter?\n\n", "")
		+ "\n### Reflection Questions\n\n1. Wrong section?\n",
])
def test_invalid_reflection_authoring_blocks_exports(broken: str, tmp_path: object) -> None:
	document = tutorial_lib.compiler.compile_source(broken)
	assert any(item.category == "reflection-questions" for item in document.diagnostics)
	with pytest.raises(ValueError):
		tutorial_lib.workbook.write_workbook(document, tmp_path / "invalid.xlsx")


@pytest.mark.parametrize("part,prefix", [("Part: Analyze", ""), ("Part 3: Analyze", "3.")])
def test_matching_question_order_and_identifiers_in_exports(
	part: str, prefix: str, tmp_path: object) -> None:
	prompts = ["Second idea **first**?", "=Literal prompt " + "long words " * 160]
	document = tutorial_lib.compiler.compile_source(source(
		"1. " + prompts[0] + "\n2. " + prompts[1], part))
	assert not document.has_errors
	xlsx_path, docx_path = tmp_path / "questions.xlsx", tmp_path / "questions.docx"
	tutorial_lib.workbook.write_workbook(document, xlsx_path)
	tutorial_lib.workbook.verify_workbook(document, xlsx_path)
	tutorial_lib.docx_renderer.write_document(document, docx_path)
	book = openpyxl.load_workbook(xlsx_path)
	sheet = book["Reflection Questions"]
	assert sheet["A2"].value == f"{prefix}1. Second idea first?"
	assert sheet["A4"].value.startswith(f"{prefix}2. =Literal prompt")
	assert sheet["A4"].data_type == "s"
	assert sheet["A3"].value == "answer here"
	assert sheet.column_dimensions["A"].width == 124
	assert sheet.row_dimensions[3].height == 47.25
	assert sheet.row_dimensions[4].height > 47.25
	assert sheet["A3"].font.name == "PT Sans"
	paragraphs = [item.text for item in docx.Document(docx_path).paragraphs]
	assert "Reflection Questions" not in paragraphs
	assert sheet["A2"].value not in paragraphs
	assert sheet["A4"].value not in paragraphs
	book.close()


@pytest.mark.parametrize("part,number", [("Part: Analyze", 2), ("Part 3: Analyze", 3)])
def test_merge_resolves_shared_identity_without_mutating_sources(
	part: str, number: int, tmp_path: object) -> None:
	first_path, second_path = tmp_path / "one.md", tmp_path / "three.md"
	first_path.write_text(source(), encoding="utf-8")
	second_path.write_text(source(part=part), encoding="utf-8")
	first = tutorial_lib.compiler.compile_document(first_path)
	second = tutorial_lib.compiler.compile_document(second_path)
	original = copy.deepcopy([first, second])
	merged = tutorial_lib.build.merge_documents([first, second])
	assert [sheet.name for sheet in merged.worksheets] == [
		"Data", "Part 1 Reflection", f"Part {number} Reflection"]
	assert merged.worksheets[1].cells[(2, 1)].scalar.value.startswith("1.1. ")
	assert merged.worksheets[2].cells[(2, 1)].scalar.value.startswith(f"{number}.1. ")
	bundle = tmp_path / "bundle"
	tutorial_lib.build.build_documents([first, second], bundle, "docx,xlsx")
	paragraphs = [item.text for item in docx.Document(bundle / "three.docx").paragraphs]
	assert f"Part {number}: Analyze" in paragraphs
	assert "Part 1: Analyze" not in paragraphs
	assert "Reflection Questions" not in paragraphs
	assert not any(item.startswith("3.1. ") for item in paragraphs)
	book = openpyxl.load_workbook(bundle / "workbook.xlsx")
	assert book.sheetnames == ["Data", "Part 1 Reflection", f"Part {number} Reflection"]
	book.close()
	assert [first, second] == original


def test_multiple_local_parts_use_whole_tutorial_fallback() -> None:
	text = source(part="Part 1: Begin") + "\n### Part 2: Continue\n\n#### Step: Finish\n\nExplain.\n"
	document = tutorial_lib.compiler.compile_source(text)
	assert not document.has_errors
	assert document.reflection_part_number is None
	assert document.worksheets[-1].cells[(2, 1)].scalar.value.startswith("1. ")


def test_generated_names_and_part_identities_cannot_collide() -> None:
	first = tutorial_lib.compiler.compile_source(source(part="Part 2: Analyze"), "two.md")
	second = tutorial_lib.compiler.compile_source(source(), "implicit.md")
	with pytest.raises(ValueError, match="two.md and implicit.md"):
		tutorial_lib.build.merge_documents([first, second])
	text = source().replace("### Sheet: Data", "### Sheet: Reflection Questions")
	assert tutorial_lib.compiler.compile_source(text).has_errors
	first = tutorial_lib.compiler.compile_source(source().replace(
		"### Sheet: Data", "### Sheet: Part 2 Reflection"), "reserved.md")
	with pytest.raises(ValueError, match="collision"):
		tutorial_lib.build.merge_documents([first, second])


def test_shared_lesson_work_precedes_its_reflection() -> None:
	root = pathlib.Path(__file__).resolve().parents[1]
	paths = sorted((root / "tutorial_data/caffeine").glob("*.md"))
	documents = [tutorial_lib.compiler.compile_document(path) for path in paths]
	merged = tutorial_lib.build.merge_documents(documents)
	assert [sheet.name for sheet in merged.worksheets] == [
		"Data", "Sample Mean", "Part 1 Reflection", "Linear Regression",
		"Part 2 Reflection", "Quadratic Regression", "Part 3 Reflection"]
