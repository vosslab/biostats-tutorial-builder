#!/usr/bin/env python3
"""Rebuild all documentation artifacts and native screenshots; run outside the sandbox."""

# Standard Library
import sys
import os.path
import pathlib
import subprocess
import urllib.parse

# Local modules
import tutorial_lib.build
import tutorial_lib.compiler
import tutorial_lib.parser


#============================================
def compose_guide(source: pathlib.Path, checkpoint: pathlib.Path,
	destination: pathlib.Path) -> pathlib.Path:
	"""Combine guide instructions with one explicit practice-workbook checkpoint."""
	guide = source.read_text(encoding="utf-8")
	lines = guide.splitlines(keepends=True)
	tokens = tutorial_lib.parser.markdown_parser().parse(guide)
	# Rebase rendered links and images only; fenced student source stays literal.
	for token in tokens:
		if token.type != "inline" or token.map is None:
			continue
		start, end = token.map
		block = "".join(lines[start:end])
		for child in token.children:
			attribute = "src" if child.type == "image" else "href"
			if child.type not in ("image", "link_open"):
				continue
			target = child.attrGet(attribute)
			url = urllib.parse.urlsplit(target)
			if url.scheme or url.netloc or not url.path:
				continue
			relative = os.path.relpath(source.parent / url.path, destination.parent)
			rebased = urllib.parse.urlunsplit(("", "", relative, url.query, url.fragment))
			block = block.replace(f"]({target})", f"]({rebased})")
		lines[start:end] = block.splitlines(keepends=True)
	# The existing checkpoint owns the workbook; guide fences are never executed.
	checkpoint_text = checkpoint.read_text(encoding="utf-8")
	workbook = checkpoint_text.split("\n## Workbook\n", 1)[1].split("\n## Tutorial\n", 1)[0]
	workbook = workbook.split("\n### Reflection Questions\n", 1)[0]
	workbook += "\n### Reflection Questions\n\n"
	workbook += "1. Which design choice in your tutorial supports its learning goal, "
	workbook += "and how will you check that it helps a reader?\n"
	first_part = next(token.map[0] for token in tokens
		if token.type == "heading_open" and token.tag == "h3")
	lines.insert(first_part, f"## Workbook\n{workbook}\n## Tutorial\n\n")
	destination.parent.mkdir(parents=True, exist_ok=True)
	destination.write_text("".join(lines), encoding="utf-8")
	return destination


#============================================
def build(sources: list[pathlib.Path], destination: pathlib.Path,
	workbook_name: str | None = None) -> None:
	"""Refresh an owned output bundle with the current native renderer styles."""
	print("Build documentation artifact: " + ", ".join(source.name for source in sources),
		flush=True)
	documents = [tutorial_lib.compiler.compile_document(source) for source in sources]
	for document in documents:
		if document.has_errors:
			messages = [item.message for item in document.diagnostics if item.severity == "error"]
			raise ValueError(f"Cannot build {document.path}: {messages}")
	tutorial_lib.build.build_documents(documents, destination, "all", workbook_name)


#============================================
def main() -> None:
	"""Run LibreOffice stages sequentially, capturing images before illustrated Part builds."""
	root = pathlib.Path(__file__).resolve().parent.parent
	# Keep canonical outputs current; the build API preserves manually edited bundles.
	caffeine = [root / "tutorial_data" / "caffeine" / f"caffeine_{part}_{name}.md" for part, name in (
		("1", "descriptive_statistics"), ("2", "linear_regression"),
		("3", "quadratic_regression"))]
	build(caffeine, root / "tutorial_output" / "caffeine_release",
		"Dr_Caffeines_All_Nighter_Academy_Student_Workbook.xlsx")
	for stem in ("microbes_4_f_test", "microbes_5_anova"):
		build([root / "tutorial_data" / "microbes" / f"{stem}.md"], root / "tutorial_output" / stem)
	for script in ("capture_readme_artifacts.py", "capture_syntax_examples.py",
		"capture_authoring_course.py"):
		print(f"Capture documentation: {script}", flush=True)
		# ASVS 1.2.5: executable and script paths remain distinct argv values.
		subprocess.run([sys.executable, str(root / "devel" / script)], cwd=root, check=True)
	for stem in ("PART_1_CREATE", "PART_2_STATISTICS", "PART_3_IMPROVE"):
		source = compose_guide(root / "docs" / "learn" / f"{stem}.md",
			root / "docs" / "examples" / "authoring_features.md",
			root / "tutorial_output" / "authoring_course" / "sources" / f"{stem}.md")
		build([source],
			root / "tutorial_output" / "authoring_course" / "parts" / stem)
	print("Documentation artifacts and all screenshot receipts refreshed.", flush=True)


if __name__ == "__main__":
	main()
