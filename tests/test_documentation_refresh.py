"""Keep displayed lesson source literal while compiling the guide's practice workbook.

If this fails, fix documentation composition before refreshing published guide artifacts.
"""

# Standard library
import pathlib

# Local modules
import refresh_documentation
import tutorial_lib.compiler


#============================================
def test_guide_uses_checkpoint_without_executing_fenced_source(tmp_path: pathlib.Path) -> None:
	guide = tmp_path / "guide.md"
	checkpoint = tmp_path / "checkpoint.md"
	destination = tmp_path / "derived" / "guide.md"
	example = "## Workbook\n\n### Sheet: Displayed only\n\n![Example](image.svg)\n"
	guide.write_text("# Author a lesson\n\n```markdown\n" + example
		+ "```\n\n### Part 1: Practice\n\n- **Worksheet:** Roots\n\n"
		+ "#### Step: Inspect\n\n[Checkpoint](checkpoint.md)\n", encoding="utf-8")
	checkpoint.write_text("# Lesson\n\n## Workbook\n\n### Sheet: Roots\n\n"
		+ "| Root length |\n| --- |\n| 12 |\n\n### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n"
		+ "### Part: Observe\n\n#### Step: Read\n\nRead the length.\n", encoding="utf-8")
	refresh_documentation.compose_guide(guide, checkpoint, destination)
	document = tutorial_lib.compiler.compile_document(destination)
	assert not document.has_errors
	assert [sheet.name for sheet in document.worksheets] == ["Roots", "Reflection Questions"]
	assert document.worksheets[0].cells[(2, 1)].scalar.value == 12
	fences = [token.content for token in document.tokens if token.type == "fence"]
	assert fences == [example]
	assert "[Checkpoint](../checkpoint.md)" in destination.read_text(encoding="utf-8")
