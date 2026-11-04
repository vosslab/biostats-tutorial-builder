"""Keep student-authored tutorial files easy to type and maintain."""

import pathlib
import tutorial_lib.compiler


ROOT = pathlib.Path(__file__).resolve().parents[1]


def source() -> str:
	return """# Lesson

## Workbook

### Sheet: Data

| Value |
| --- |
| 1 |

### Reflection Questions

1. How do the results support your conclusion?

## Tutorial

### Part: Practice

- **Worksheet:** Data

#### Step: Calculate

In cell B2, enter [=A2^2](enter:B2).
"""


def test_file_compilation_requires_ascii_and_named_entities(tmp_path: pathlib.Path) -> None:
	"""Students receive actionable diagnostics for pasted source characters."""
	path = tmp_path / "lesson.md"
	path.write_text(source().replace("Calculate", "Calculate -- let's test &alpha;"), encoding="utf-8")
	document = tutorial_lib.compiler.compile_document(path)
	assert not document.has_errors
	path.write_text(source().replace("Calculate", "Calculate -- let's test \u03b1, &#945;, and &alpha;"),
		encoding="utf-8")
	document = tutorial_lib.compiler.compile_document(path)
	errors = [item for item in document.diagnostics if item.severity == "error"]
	assert [item.category for item in errors] == [
		"source-numeric-entity", "source-non-ascii"]
	assert "readable named entity" in errors[0].correction


def test_in_memory_compilation_keeps_renderer_unicode_support() -> None:
	"""The file-authoring rule does not narrow parser or renderer internals."""
	document = tutorial_lib.compiler.compile_source(
		source().replace("Calculate", "Calculate \u03b1 &alpha;"))
	assert not document.has_errors


def test_explicit_action_destination_must_match_binding_target() -> None:
	"""Catch a copied instruction whose visible destination is stale."""
	wrong = source().replace("enter:B2", "enter:C2")
	document = tutorial_lib.compiler.compile_source(wrong)
	assert any(item.category == "action-visible-target" for item in document.diagnostics)
	input_mention = source().replace("In cell B2, enter", "Use input cell A2, then enter")
	document = tutorial_lib.compiler.compile_source(input_mention)
	assert not any(item.category == "action-visible-target" for item in document.diagnostics)
	multiple = source().replace("In cell B2, enter [=A2^2](enter:B2).",
		"In cell B1, type [Squared](label:B1); in cell B2, enter [=A2^2](enter:B2).")
	document = tutorial_lib.compiler.compile_source(multiple)
	assert not any(item.category == "action-visible-target" for item in document.diagnostics)


def test_active_lessons_and_templates_are_ascii_without_numeric_entities() -> None:
	"""Starter content models the same keyboard-friendly source rule it teaches."""
	paths = sorted((ROOT / "tutorial_data").glob("*.md"))
	paths.extend(sorted((ROOT / "templates").glob("*.md")))
	assert paths
	for path in paths:
		text = path.read_text(encoding="utf-8")
		assert text.isascii(), path
		assert "&#" not in text, path
