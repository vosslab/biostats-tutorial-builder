"""Protect published teaching bundles from failed builds and user-edit loss.

Failures mean publication protection regressed: fix staging/ownership before releasing.
Conversion is replaced locally so these integrity checks stay offline and fast.
"""

# Standard library
import json
import io
import pathlib
import subprocess

# Third-party modules
import docx
import openpyxl
import pytest
import pypdf

# Local modules
import tutorial_lib.build
import tutorial_lib.model
import tutorial_lib.pdf_export


#============================================
def make_document(directory: pathlib.Path) -> tutorial_lib.model.Document:
	"""Create a minimal compiled model for publication integrity tests."""
	source = directory / "lesson.md"
	source.write_text("A tutorial\n", encoding="utf-8")
	document = tutorial_lib.model.Document(source, source.read_text(encoding="utf-8"))
	span = tutorial_lib.model.SourceSpan(str(source), 1, 1)
	sheet = tutorial_lib.model.Worksheet("Data", span)
	sheet.cells[(1, 1)] = tutorial_lib.model.CellSeed(
		1, 1, tutorial_lib.model.Scalar("text", "Value"), span
	)
	document.worksheets.append(sheet)
	return document


#============================================
def make_named_document(directory: pathlib.Path, name: str, sheet_name: str,
	value: str) -> tutorial_lib.model.Document:
	"""Create a second minimal source for shared-workbook publication tests."""
	source = directory / f"{name}.md"
	source.write_text(f"{name} tutorial\n", encoding="utf-8")
	document = tutorial_lib.model.Document(source, source.read_text(encoding="utf-8"))
	span = tutorial_lib.model.SourceSpan(str(source), 1, 1)
	sheet = tutorial_lib.model.Worksheet(sheet_name, span)
	sheet.cells[(1, 1)] = tutorial_lib.model.CellSeed(
		1, 1, tutorial_lib.model.Scalar("text", value), span
	)
	document.worksheets.append(sheet)
	return document


#============================================
def write_docx(document: tutorial_lib.model.Document, path: pathlib.Path) -> None:
	"""Provide a valid local package without exercising the independent renderer."""
	output = docx.Document()
	output.add_paragraph(document.source)
	output.save(path)


#============================================
def write_pdf(source: pathlib.Path, destination: pathlib.Path) -> None:
	"""Stand in for conversion without invoking LibreOffice in pytest."""
	if not source.is_file():
		raise FileNotFoundError(source)
	destination.write_bytes(b"%PDF-1.4\nMock conversion evidence only\n")


#============================================
def fail_pdf(source: pathlib.Path, destination: pathlib.Path) -> None:
	"""Represent a converter failure after other staged artifacts exist."""
	raise RuntimeError("conversion failed")


#============================================
def test_failed_conversion_preserves_bundle_and_subset_replaces_it(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	document = make_document(tmp_path)
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.docx_renderer, "write_document", write_docx)
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.pdf_export, "export_pdf", write_pdf)
	destination = tmp_path / "published"
	tutorial_lib.build.build_document(document, destination)
	before = {path.name: path.read_bytes() for path in destination.iterdir()}
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.pdf_export, "export_pdf", fail_pdf)
	with pytest.raises(RuntimeError, match="conversion failed"):
		tutorial_lib.build.build_document(document, destination)
	assert {path.name: path.read_bytes() for path in destination.iterdir()} == before
	tutorial_lib.build.build_document(document, destination, "xlsx")
	assert set(path.suffix for path in destination.iterdir()) == {".xlsx", ".json"}
	report = json.loads((destination / "validation.json").read_text(encoding="utf-8"))
	assert report["external_behavior"]["google_import"] == "unchecked"


#============================================
def test_modified_artifact_and_foreign_directory_are_preserved(tmp_path: pathlib.Path) -> None:
	document = make_document(tmp_path)
	destination = tmp_path / "published"
	tutorial_lib.build.build_document(document, destination, "xlsx")
	workbook = destination / "lesson.xlsx"
	workbook.write_bytes(b"user edits")
	with pytest.raises(ValueError, match="modified"):
		tutorial_lib.build.build_document(document, destination, "xlsx")
	assert workbook.read_bytes() == b"user edits"
	foreign = tmp_path / "foreign"
	foreign.mkdir()
	(foreign / "notes.txt").write_text("keep", encoding="utf-8")
	with pytest.raises(ValueError, match="not an owned"):
		tutorial_lib.build.build_document(document, foreign, "xlsx")
	assert (foreign / "notes.txt").read_text(encoding="utf-8") == "keep"


#============================================
def test_successful_converter_with_unreadable_pdf_preserves_bundle(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""A converter's zero exit and PDF signature must not publish a corrupt bundle."""
	document = make_document(tmp_path)
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.docx_renderer, "write_document", write_docx)
	monkeypatch.setattr(tutorial_lib.pdf_export.shutil, "which", lambda name: "/mock/soffice")
	writer = pypdf.PdfWriter()
	writer.add_blank_page(width=100, height=100)
	buffer = io.BytesIO()
	writer.write(buffer)
	pdf_bytes = buffer.getvalue()

	def convert(command: list[str], **options: object) -> subprocess.CompletedProcess[str]:
		output = pathlib.Path(command[-2]) / pathlib.Path(command[-1]).with_suffix(".pdf").name
		output.write_bytes(pdf_bytes)
		return subprocess.CompletedProcess(command, 0, stdout="converted", stderr="")

	monkeypatch.setattr(tutorial_lib.pdf_export.subprocess, "run", convert)
	destination = tmp_path / "published"
	tutorial_lib.build.build_document(document, destination)
	before = {path.name: path.read_bytes() for path in destination.iterdir()}
	pdf_bytes = b"%PDF-"
	with pytest.raises(RuntimeError, match="unreadable PDF"):
		tutorial_lib.build.build_document(document, destination)
	assert {path.name: path.read_bytes() for path in destination.iterdir()} == before


#============================================
def test_multi_source_build_keeps_documents_separate_and_unites_sheets(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Several Markdown tutorials produce isolated documents and one workbook."""
	first = make_document(tmp_path)
	second = make_named_document(tmp_path, "follow_up", "Results", "Outcome")
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.docx_renderer, "write_document", write_docx)
	destination = tmp_path / "published"
	tutorial_lib.build.build_documents([first, second], destination, "docx,xlsx")
	assert {path.name for path in destination.iterdir()} == {
		"lesson.docx", "follow_up.docx", "workbook.xlsx", "validation.json"}
	assert docx.Document(destination / "lesson.docx").paragraphs[0].text == first.source
	assert docx.Document(destination / "follow_up.docx").paragraphs[0].text == second.source
	workbook = openpyxl.load_workbook(destination / "workbook.xlsx")
	assert workbook.sheetnames == ["Data", "Results"]
	assert workbook["Data"]["A1"].value == "Value"
	assert workbook["Results"]["A1"].value == "Outcome"
	workbook.close()


#============================================
def test_multi_source_merge_rejects_conflicting_cell_values(tmp_path: pathlib.Path) -> None:
	"""Two sources cannot silently assign different values to one shared cell."""
	first = make_document(tmp_path)
	second = make_named_document(tmp_path, "conflict", "Data", "Different")
	with pytest.raises(ValueError, match="Conflicting values"):
		tutorial_lib.build.merge_documents([first, second])


#============================================
def test_multi_source_merge_rebases_alternative_groups_without_mutating_sources(
	tmp_path: pathlib.Path,
) -> None:
	"""Source-local alternatives cannot collide in one shared workbook model."""
	first = make_document(tmp_path)
	second = make_named_document(tmp_path, "follow_up", "Results", "Outcome")
	span = tutorial_lib.model.SourceSpan(str(first.path), 1, 1)
	first.actions.append(tutorial_lib.model.Action("enter", span, 1, "first",
		alternative_group=1, alternative_branch=1,
		generated_actions=[tutorial_lib.model.Action("enter", span, 1, "fill",
			alternative_group=1, alternative_branch=1)]))
	second.actions.append(tutorial_lib.model.Action("enter", span, 1, "second",
		alternative_group=1, alternative_branch=1,
		generated_actions=[tutorial_lib.model.Action("enter", span, 1, "fill",
			alternative_group=1, alternative_branch=1)]))
	merged = tutorial_lib.build.merge_documents([first, second])
	assert [action.alternative_group for action in merged.actions] == [1, 2]
	assert [action.generated_actions[0].alternative_group for action in merged.actions] == [1, 2]
	assert first.actions[0].generated_actions[0].alternative_group == 1
	assert second.actions[0].generated_actions[0].alternative_group == 1


#============================================
def test_multi_source_merge_preserves_repeated_action_order(tmp_path: pathlib.Path) -> None:
	"""Later instructions remain meaningful even when they repeat an earlier value."""
	document = make_document(tmp_path)
	span = tutorial_lib.model.SourceSpan(str(document.path), 1, 1)
	for kind, value in (("enter", 1), ("replace", 2), ("enter", 1)):
		document.actions.append(tutorial_lib.model.Action(kind, span, 1, str(value),
			scalar=tutorial_lib.model.Scalar("number", value)))
	merged = tutorial_lib.build.merge_documents([document])
	assert [(action.kind, action.scalar.value) for action in merged.actions] == [
		("enter", 1), ("replace", 2), ("enter", 1)]


#============================================
def test_multi_source_failure_preserves_existing_bundle(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""A later document failure cannot replace an already verified release."""
	first = make_document(tmp_path)
	second = make_named_document(tmp_path, "follow_up", "Results", "Outcome")
	destination = tmp_path / "published"
	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.docx_renderer, "write_document", write_docx)
	tutorial_lib.build.build_documents([first, second], destination, "docx,xlsx")
	before = {path.name: path.read_bytes() for path in destination.iterdir()}

	def fail_later(document: tutorial_lib.model.Document, path: pathlib.Path) -> None:
		if document.path.stem == "follow_up":
			raise RuntimeError("later document failed")
		write_docx(document, path)

	monkeypatch.setattr(tutorial_lib.build.tutorial_lib.docx_renderer, "write_document", fail_later)
	with pytest.raises(RuntimeError, match="later document failed"):
		tutorial_lib.build.build_documents([first, second], destination, "docx,xlsx")
	assert {path.name: path.read_bytes() for path in destination.iterdir()} == before
