#!/usr/bin/env python3
"""Build and capture native formatting-demo evidence outside the macOS sandbox."""

# Standard Library
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import tempfile

# PIP3 modules
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

# Local modules
import capture_readme_artifacts


#============================================
def digest(path: pathlib.Path) -> str:
	"""Return a file's SHA-256 fingerprint."""
	result = hashlib.sha256(path.read_bytes()).hexdigest()
	return result


#============================================
def protected_hashes(root: pathlib.Path) -> dict[str, str]:
	"""Fingerprint the example source and all pre-existing canonical teaching inputs."""
	protected = [root / "docs" / "examples" / name for name in
		("formatting_demo.md", "authoring_features.md")]
	protected += sorted((root / "tutorial_data").rglob("*.md"))
	result = {str(path.relative_to(root)): digest(path) for path in protected}
	return result


#============================================
def build_example(root: pathlib.Path, temporary: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
	"""Build the example into an isolated output directory with native DOCX and XLSX renderers."""
	source = root / "docs" / "examples" / "formatting_demo.md"
	output = temporary / "build"
	command = [
		"python3", "make_tutorial.py", "build", str(source), "--format", "all", "--output-dir", str(output),
	]
	subprocess.run(command, cwd=root, check=True)
	stem = source.stem
	pdf = output / f"{stem}.pdf"
	xlsx = output / f"{stem}.xlsx"
	if not pdf.is_file() or not xlsx.is_file():
		raise RuntimeError("The native build did not produce both PDF and XLSX artifacts")
	return pdf, xlsx


#============================================
def compare_source(source: str, output: pathlib.Path, destination: pathlib.Path) -> None:
	"""Pair selectable-source equivalent text with an unchanged native output crop."""
	font_paths = (
		pathlib.Path.home() / "Library/Fonts/RobotoMono[wght].ttf",
		pathlib.Path("/System/Library/Fonts/Menlo.ttc"),
		pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
	)
	font_path = next(path for path in font_paths if path.is_file())
	font = PIL.ImageFont.truetype(str(font_path), 22)
	label = PIL.ImageFont.truetype(str(font_path), 24)
	lines = source.strip().splitlines()
	left_width = max(round(font.getlength(line)) for line in lines) + 48
	with PIL.Image.open(output) as native:
		crop = native.convert("RGB")
	width = left_width + crop.width + 48
	height = max(len(lines) * 33 + 86, crop.height + 86)
	canvas = PIL.Image.new("RGB", (width, height), "white")
	draw = PIL.ImageDraw.Draw(canvas)
	draw.rectangle((0, 0, left_width, height), fill="#f0f4f8")
	draw.text((24, 18), "You type", font=label, fill="#243b53")
	draw.text((left_width + 24, 18), "Word output", font=label, fill="#243b53")
	for index, line in enumerate(lines):
		draw.text((24, 66 + index * 33), line, font=font, fill="#172b4d")
	canvas.paste(crop, (left_width + 24, 66))
	capture_readme_artifacts.encode_webp(canvas, destination)


#============================================
def capture_authoring_features(root: pathlib.Path, temporary: pathlib.Path,
	destination: pathlib.Path) -> tuple[list[dict], dict[str, str]]:
	"""Capture the feature reference from one runnable source, without a practice course."""
	source = root / "docs/examples/authoring_features.md"
	output = temporary / "authoring_features"
	subprocess.run(["python3", "make_tutorial.py", "build", str(source),
		"--format", "all", "--output-dir", str(output)], cwd=root, check=True)
	pdf = output / "authoring_features.pdf"
	xlsx = output / "authoring_features.xlsx"
	views = [
		("Roots formatting examples", "Part 1: Format the document", "title"),
		("Part 1: Format the document", "Explanation: Mark up scientific text", "headings"),
		("Explanation: Mark up scientific text", "Step 2: Show a document table", "text"),
		("Step 2: Show a document table", "Step 3: Include an image", "table"),
		("Step 3: Include an image", "Step 4: Link to a section", "image"),
		("Step 4: Link to a section", "Part 2: Connect a workbook", "links"),
		("Step 1: Enter a formula", "Step 2: Fill a column", "enter"),
		("Step 2: Fill a column", "Step 3: Select a range", "fill"),
		("Step 3: Select a range", "Step 4: Replace a supplied value", "select"),
		("Step 4: Replace a supplied value", "Part 3: Offer alternatives", "replace"),
		("Step 1: Provide a choice", "Reflection Questions", "alternatives"),
	]
	captures = [capture_readme_artifacts.capture_pdf(pdf, start, end,
		f"authoring_{name}", temporary, destination) for start, end, name in views]
	for name, area in (("workbook", "A1:E6"), ("results", "D1:E3"), ("response", "D8:E9")):
		captures.append(capture_readme_artifacts.render_workbook(xlsx, f"authoring_{name}",
			temporary, destination, area, "Roots"))
	captures.append(capture_readme_artifacts.render_workbook(xlsx, "authoring_reflection",
		temporary, destination, "A1:A3", "Reflection Questions"))
	text = source.read_text(encoding="ascii")
	excerpt = "#### Step: Enter a formula\n" + text.split(
		"#### Step: Enter a formula\n", 1)[1].split("\n#### Step:", 1)[0]
	comparison = destination / "authoring_comparison.webp"
	compare_source(excerpt, destination / "authoring_enter.webp", comparison)
	captures.append({"asset": str(comparison), "source": str(source),
		"source_excerpt": excerpt.strip(), "native_crop": "authoring_enter.webp",
		"description": "Literal source beside the actual DOCX-to-PDF crop"})
	hashes = {str(source.relative_to(root)): digest(source)}
	instructor = root / "tutorial_data/microbes/microbes_1_z_test.md"
	instructor_output = temporary / "instructor_example"
	subprocess.run(["python3", "make_tutorial.py", "build", str(instructor),
		"--format", "all", "--output-dir", str(instructor_output)], cwd=root, check=True)
	captures.append(capture_readme_artifacts.capture_pdf(
		instructor_output / "microbes_1_z_test.pdf", "Step 4: Calculate the Z-Statistic",
		"Explanation:", "authoring_instructor", temporary, destination))
	hashes[str(instructor.relative_to(root))] = digest(instructor)
	return captures, hashes


#============================================
def main() -> None:
	"""Capture five tightly cropped proof views without changing canonical outputs."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args()
	repo_result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True,
	)
	root = pathlib.Path(repo_result.stdout.strip())
	destination = root / "docs" / "screenshots"
	before = protected_hashes(root)
	temporary = pathlib.Path(tempfile.mkdtemp(prefix="syntax_capture_"))
	pdf, xlsx = build_example(root, temporary)
	views = [
		("Part 1: Explore a curved relationship", "Explanation: Why square a value?",
			"syntax_headings"),
		("Explanation: Why square a value?", "Step 2: Calculate squared sleep hours",
			"syntax_text"),
		("Step 2: Calculate squared sleep hours",
			"Explanation: Read a formula before copying it", "syntax_actions"),
		("Step 3: Compare the model features", "Reflection Questions", "syntax_table"),
	]
	metadata = [capture_readme_artifacts.capture_pdf(pdf, start, end, name, temporary, destination)
		for start, end, name in views]
	metadata.append(capture_readme_artifacts.render_workbook(xlsx, "syntax_workbook",
		temporary, destination, "A1:F4", "Sleep and scores"))
	feature_captures, feature_hashes = capture_authoring_features(root, temporary, destination)
	metadata.extend(feature_captures)
	assets = [pathlib.Path(item["asset"]) for item in metadata]
	after = protected_hashes(root)
	if after != before:
		raise RuntimeError("A protected source changed during syntax capture")
	receipt = {
		"captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
		"source": "docs/examples/formatting_demo.md",
		"authoring_sources_sha256": feature_hashes,
		"protected_sha256": after,
		"assets_sha256": {asset.name: digest(asset) for asset in assets},
		"renderer": "repository-owned LibreOffice and Poppler",
		"captures": metadata,
		"native_artifacts": {
			"document": "DOCX rendered to PDF by the project build, then cropped from PDF",
			"workbook": "generated XLSX printed through repository-owned LibreOffice Calc helper",
		},
		"protected_sources_unchanged": True,
		"build_output": "isolated temporary directory; canonical tutorial_output is not used",
	}
	receipt_path = destination / "syntax_capture_receipt.json"
	receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="ascii")
	print(f"Capture receipt: {receipt_path}")


if __name__ == "__main__":
	main()
