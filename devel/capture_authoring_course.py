#!/usr/bin/env python3
"""Build and capture native course artifacts; run outside the macOS sandbox."""

# Standard Library
import json
import math
import shutil
import pathlib
import argparse
import datetime
import statistics
import subprocess

# PIP3 modules
import openpyxl
import PIL.Image

# Local modules
import capture_readme_artifacts


#============================================
def annotated_formula_map(native: pathlib.Path, metadata: dict,
		temporary: pathlib.Path, destination: pathlib.Path) -> dict:
	"""Add a clearly separate teaching overlay to an unchanged native starter view."""
	pages = capture_readme_artifacts.pdf_layout(pathlib.Path(metadata["native_pdf"]))
	lines = pages[0]["lines"]
	first = next(line for line in lines if line["text"] == "12.000")
	last = next(line for line in lines if line["text"] == "25.000")
	column = next(line for line in lines if line["text"] == "E")
	row = next(line for line in lines if line["text"] == "3")
	left, top = metadata["bbox_pixels"][:2]
	scale = metadata["scale"]
	x1 = (first["xMin"] * 2 - left - 9) * scale
	y1 = (first["yMin"] * 2 - top - 5) * scale
	x2 = (last["xMax"] * 2 - left + 6) * scale
	y2 = (last["yMax"] * 2 - top + 5) * scale
	ex = ((column["xMin"] + column["xMax"]) - left) * scale
	ey = ((row["yMin"] + row["yMax"]) - top) * scale
	with PIL.Image.open(native) as image:
		width, height = image.size
		canvas = PIL.Image.new("RGB", (width, height + 120), "white")
		canvas.paste(image, (0, 120))
		native_png = temporary / "formula_map_native.png"
		canvas.save(native_png)
	svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height+120}">'
	svg += '<rect width="100%" height="110" fill="#f1f5f9"/>'
	svg += '<g font-family="sans-serif" fill="#172554">'
	svg += '<text x="16" y="28" font-size="19" font-weight="bold">'
	svg += 'ANNOTATED TEACHING VIEW - blank student starter</text>'
	svg += '<text x="16" y="57" font-size="19">'
	svg += 'Blue: A2:A6 inputs | Orange: E3 result destination</text>'
	svg += '<text x="16" y="88" font-size="20">'
	svg += 'Enter =AVERAGE(A2:A6) in E3 to calculate the mean.</text></g>'
	svg += f'<rect x="{x1}" y="{y1+120}" width="{x2-x1}" height="{y2-y1}" '
	svg += 'rx="4" fill="none" stroke="#0057a6" stroke-width="4"/>'
	svg += f'<rect x="{ex-48}" y="{ey+120-14}" width="96" height="28" '
	svg += 'rx="4" fill="none" stroke="#b45309" stroke-width="4"/>'
	svg += '</svg>'
	overlay = temporary / "formula_map_overlay.svg"
	overlay.write_text(svg, encoding="ascii")
	overlay_png = temporary / "formula_map_overlay.png"
	subprocess.run(["rsvg-convert", "-o", str(overlay_png), str(overlay)], check=True)
	with PIL.Image.open(native_png) as base, PIL.Image.open(overlay_png) as layer:
		result = PIL.Image.alpha_composite(base.convert("RGBA"), layer.convert("RGBA"))
		capture_readme_artifacts.encode_webp(
			result.convert("RGB"), destination / "course_formula_map.webp")
	metadata = {"native_asset": native.name, "native_asset_sha256": capture_readme_artifacts.digest(native),
		"annotation": "Separate SVG overlay and labeled caption; native cells remain blank",
		"input_range": "A2:A6", "destination": "E3", "formula": "=AVERAGE(A2:A6)"}
	return metadata


#============================================
def workbook_values(source: pathlib.Path, moved: bool, expanded: bool, completed: bool) -> dict:
	"""Verify blank starters or independently calculated native Calc results."""
	workbook = openpyxl.load_workbook(source, data_only=True)
	sheet = workbook["Roots"]
	data_column = "B" if moved else "A"
	result_column = "F" if moved else "E"
	deviation_column = "C" if moved else "B"
	values = [12, 15, 18, 20, 25] + ([30] if expanded else [])
	actual_data = [sheet[f"{data_column}{row}"].value for row in range(2, len(values) + 2)]
	if actual_data != values:
		raise ValueError(f"Unexpected source observations in {source}: {actual_data}")
	expected = [len(values), statistics.mean(values), statistics.stdev(values)]
	actual = [sheet[f"{result_column}{row}"].value for row in range(2, 5)]
	if completed:
		if any(not isinstance(value, (int, float)) for value in actual):
			raise ValueError(f"Calc returned nonnumeric summary cells: {actual}")
		if any(not math.isclose(value, target, rel_tol=1e-12) for value, target in zip(actual, expected)):
			raise ValueError(f"Calc summary {actual} differs from Python statistics {expected}")
	elif actual != [None, None, None]:
		raise ValueError(f"Starter result cells must be blank: {actual}")
	deviations = []
	if expanded:
		deviations = [sheet[f"{deviation_column}{row}"].value for row in range(2, 8)]
		targets = [value - statistics.mean(values) for value in values]
		if completed and deviations != targets:
			raise ValueError(f"Incorrect deviations: {deviations}; expected {targets}")
		if not completed and deviations != [None] * 6:
			raise ValueError(f"Starter deviation cells must be blank: {deviations}")
	numeric_addresses = [f"{data_column}{row}" for row in range(2, len(values) + 2)]
	numeric_addresses += [f"{result_column}{row}" for row in range(2, 5)]
	if expanded:
		numeric_addresses += [f"{deviation_column}{row}" for row in range(2, 8)]
	formats = {address: sheet[address].number_format for address in numeric_addresses}
	if any(value != "0.000" for value in formats.values()):
		raise ValueError(f"Expected three-decimal display in {source}: {formats}")
	workbook.close()
	result = {"observations": actual_data, "summary": actual,
		"independent_expected_summary": expected, "deviations": deviations,
		"numeric_display_formats": formats,
		"state": "completed authored baseline" if completed else "blank student starter"}
	return result


#============================================
def protected_hashes(root: pathlib.Path) -> dict[str, str]:
	"""Protect canonical lessons and built teaching artifacts during isolated capture."""
	paths = sorted((root / "tutorial_data").rglob("*.md"))
	for lesson in (root / "tutorial_data").rglob("*.md"):
		paths += [path for path in (root / "tutorial_output" / lesson.stem).glob("*") if path.is_file()]
	result = {str(path.relative_to(root)): capture_readme_artifacts.digest(path) for path in paths}
	return result


#============================================
def main() -> None:
	"""Build eight stages, verify starters and Calc results, and publish native crops."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args()
	repo = subprocess.run(["git", "rev-parse", "--show-toplevel"],
		check=True, capture_output=True, text=True)
	root = pathlib.Path(repo.stdout.strip())
	lessons = sorted((root / "docs/examples/authoring_course").glob("root_*.md"))
	if len(lessons) != 8:
		raise ValueError("All eight authored course stages must exist before capture")
	before = protected_hashes(root)
	output = root / "tutorial_output/authoring_course"
	temporary = output / "capture_work"
	temporary.mkdir(parents=True, exist_ok=True)
	destination = root / "docs/screenshots"
	builds = {}
	for lesson in lessons:
		build = output / lesson.stem
		subprocess.run(["python3", "make_tutorial.py", "build", str(lesson),
			"--format", "all", "--output-dir", str(build)], cwd=root, check=True)
		builds[lesson.stem] = build
	provenance = {}
	checks = {}
	document_views = [
		("root_05_variation", "course_overview_document", "Exploring root lengths", "Reflection Questions"),
		("root_05_variation", "course_overview_excerpt", "Exploring root lengths", "Part 2: Summarize root lengths"),
		("root_02_write", "course_markdown", "Exploring root lengths", "Reflection Questions"),
		("root_04_calculate", "course_count_action", "Step 1: Count the observations", "Step 2: Calculate the mean"),
		("root_04_calculate", "course_mean_action", "Step 2: Calculate the mean", "Reflection Questions"),
		("root_05_variation", "course_variation_action", "Step 3: Describe the spread", "Reflection Questions"),
		("root_06_grow", "course_fixed_formula", "Step 1: Subtract the mean", "Reflection Questions"),
		("root_07_move", "course_moved_action", "Step 1: Subtract the mean", "Reflection Questions"),
	]
	for stem, name, start, stop in document_views:
		provenance[name] = capture_readme_artifacts.capture_pdf(
			builds[stem] / f"{stem}.pdf", start, stop, name, temporary, destination)
	workbook_views = [
		("root_05_variation", "course_overview_starter", "A1:E6", False),
		("root_03_layout", "course_layout", "A1:E6", False),
		("root_05_variation", "course_statistics", "D1:E4", True),
		("root_06_grow", "course_expanded_starter", "A1:E7", False),
		("root_06_grow", "course_expanded_complete", "A1:E7", True),
		("root_07_move", "course_moved_starter", "B1:F7", False),
		("root_07_move", "course_moved_complete", "B1:F7", True),
	]
	for stem, name, area, completed in workbook_views:
		source = builds[stem] / f"{stem}.xlsx"
		if completed:
			case_directory = temporary / name
			if case_directory.exists():
				shutil.rmtree(case_directory)
			case_directory.mkdir()
			disposable = case_directory / f"{stem}_authored.xlsx"
			capture_readme_artifacts.completed_workbook(source,
				root / f"docs/examples/authoring_course/{stem}.md", disposable)
			source = case_directory / f"{stem}_completed.xlsx"
			capture_readme_artifacts.recalculate_workbook(disposable, source, case_directory)
		checks[name] = workbook_values(source, stem == "root_07_move",
			stem in ("root_06_grow", "root_07_move"), completed)
		rendered = capture_readme_artifacts.render_workbook(source, name, temporary, destination, area, "Roots")
		provenance[name] = {**rendered, "native_xlsx": str(source.relative_to(root)), "print_area": area,
			"state": checks[name]["state"], "source_sha256": capture_readme_artifacts.digest(source)}
	provenance["course_formula_map"] = annotated_formula_map(
		destination / "course_overview_starter.webp", provenance["course_overview_starter"],
		temporary, destination)
	published = root / "docs/examples/authoring_course/published"
	published.mkdir(exist_ok=True)
	for suffix in (".md", ".docx", ".pdf", ".xlsx"):
		source = (root / "docs/examples/authoring_course/root_05_variation.md" if suffix == ".md"
			else builds["root_05_variation"] / f"root_05_variation{suffix}")
		shutil.copyfile(source, published / f"root_statistics{suffix}")
	after = protected_hashes(root)
	if before != after:
		raise RuntimeError("A canonical source or teaching artifact changed during capture")
	assets = {}
	for name in provenance:
		path = destination / f"{name}.webp"
		with PIL.Image.open(path) as view:
			width, height = view.size
		if max(width, height) > 1920:
			raise ValueError(f"Capture exceeds 1920-pixel edge limit: {path}: {width}x{height}")
		assets[path.name] = {"sha256": capture_readme_artifacts.digest(path),
			"width": width, "height": height, "quality": 90, **provenance[name]}
	receipt = {
		"captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
		"renderer": "devel/capture_readme_artifacts.py", "assets": assets,
		"course_sources_sha256": {str(path.relative_to(root)): capture_readme_artifacts.digest(path)
			for path in lessons}, "protected_sha256": after, "protected_files_unchanged": True,
		"independent_calc_checks": checks,
		"published_sha256": {path.name: capture_readme_artifacts.digest(path)
			for path in sorted(published.iterdir())},
		"native_provenance": "Project DOCX-to-PDF; styled XLSX copies rendered by LibreOffice Calc",
		"completed_scenario": "baseline authored action replay; no synthetic screenshot content",
	}
	(destination / "course_capture_receipt.json").write_text(
		json.dumps(receipt, indent=2) + "\n", encoding="ascii")
	print(f"Captured {len(assets)} native course views; receipt: {destination / 'course_capture_receipt.json'}")


if __name__ == "__main__":
	main()
