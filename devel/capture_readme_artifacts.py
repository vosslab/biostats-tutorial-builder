#!/usr/bin/env python3
"""Refresh README artifact views; run outside the macOS sandbox (LibreOffice)."""

# Standard Library
import re
import json
import math
import shutil
import pathlib
import hashlib
import argparse
import datetime
import tempfile
import subprocess

# PIP3 modules
import openpyxl
import PIL.Image
import PIL.ImageChops
import openpyxl.worksheet.page
import openpyxl.worksheet.properties
import defusedxml.ElementTree

# Local modules
import tutorial_lib.compiler
import tutorial_lib.formula_io
import sheets_validation_lib


#============================================
def digest(path: pathlib.Path) -> str:
	"""Return a file's SHA-256 fingerprint."""
	result = hashlib.sha256(path.read_bytes()).hexdigest()
	return result


#============================================
def encode_webp(image: PIL.Image.Image, destination: pathlib.Path) -> None:
	"""Encode a temporary PNG with the documentation workflow's quality-90 cwebp."""
	with tempfile.TemporaryDirectory(prefix="documentation-webp-") as directory:
		temporary = pathlib.Path(directory)
		png = temporary / "capture.png"
		webp = temporary / "capture.webp"
		image.save(png, "PNG")
		subprocess.run(["cwebp", "-q", "90", str(png), "-o", str(webp)],
			check=True, capture_output=True, text=True)
		destination.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(webp, destination)


#============================================
def pdf_layout(pdf: pathlib.Path) -> list[dict]:
	"""Read Poppler text lines in PDF point coordinates, retaining page dimensions."""
	# ASVS 1.2.5: use argument arrays, never interpolate paths into a shell command.
	process = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"],
		check=True, capture_output=True, text=True)
	root = defusedxml.ElementTree.fromstring(process.stdout)
	pages = []
	for page in root.findall(".//{*}page"):
		lines = []
		for line in page.findall(".//{*}line"):
			text = " ".join(word.text or "" for word in line.findall("{*}word"))
			lines.append({"text": text, **{key: float(line.attrib[key])
				for key in ("xMin", "xMax", "yMin", "yMax")}})
		pages.append({"width": float(page.attrib["width"]),
			"height": float(page.attrib["height"]), "lines": lines})
	return pages


#============================================
def find_anchor(pages: list[dict], anchor: str, occurrence: int = 1) -> tuple[int, dict]:
	"""Find literal text across wrapped lines, allowing ordinary whitespace changes."""
	words = []
	locations = []
	for index, page in enumerate(pages):
		for line in page["lines"]:
			for word in line["text"].split():
				words.append(word)
				locations.append((index, line))
	text = " ".join(words)
	needle = " ".join(anchor.split())
	matches = list(re.finditer(re.escape(needle), text))
	if occurrence < 1 or occurrence > len(matches):
		raise ValueError(f"PDF anchor occurrence {occurrence} missing: {anchor!r}")
	position = len(text[:matches[occurrence - 1].start()].split())
	return locations[position]


#============================================
def capture_pdf(pdf: pathlib.Path, start: str | None, end: str | None, name: str,
		temporary: pathlib.Path, destination: pathlib.Path, occurrence: int = 1,
		end_occurrence: int = 1) -> dict:
	"""Capture start-inclusive/end-exclusive text regions across genuine PDF pages."""
	pages = pdf_layout(pdf)
	first_page, first_line = find_anchor(pages, start, occurrence) if start else (0, None)
	last_page, last_line = find_anchor(pages, end, end_occurrence) if end else (len(pages)-1, None)
	if (last_page, last_line["yMin"] if last_line else math.inf) <= (
		first_page, first_line["yMin"] if first_line else 0):
		raise ValueError(f"PDF end anchor precedes start anchor: {name}")
	images = []
	segments = []
	for index in range(first_page, last_page + 1):
		page = pages[index]
		# Locate actual page-number text rather than assuming a fixed footer pixel band.
		footers = [line for line in page["lines"] if line["text"].strip().isdigit()
			and line["yMin"] > page["height"] * 0.85]
		footer_top = min(line["yMin"] for line in footers) - 8 if footers else page["height"]
		top = first_line["yMin"] if index == first_page and first_line else 0
		bottom = last_line["yMin"] if index == last_page and last_line else footer_top
		lines = [line for line in page["lines"] if top <= line["yMin"] < bottom]
		if not lines:
			continue
		# Bound padding by adjacent text so a neighboring heading never appears sliced.
		previous = [line["yMax"] for line in page["lines"] if line["yMax"] <= top]
		y1 = max(0, top - 8, (max(previous) + top) / 2 if previous else 0)
		last_text = max(line["yMax"] for line in lines)
		y2 = min(footer_top, bottom - 0.5,
			max(bottom - 8, (last_text + bottom) / 2))
		# Raster the page width so figures wider than nearby text are preserved.
		x1 = 0
		x2 = page["width"]
		# Starting at the document top preserves native illustrations between the text.
		if index == first_page and first_line is None:
			y1 = max(0, min(line["yMin"] for line in lines) - 8)
		bounds = [math.floor(x1*2), math.floor(y1*2), math.ceil((x2-x1)*2),
			math.ceil((y2-y1)*2)]
		stem = temporary / f"{name}_page_{index + 1}"
		subprocess.run(["pdftoppm", "-f", str(index+1), "-l", str(index+1), "-r", "144",
			"-x", str(bounds[0]), "-y", str(bounds[1]), "-W", str(bounds[2]),
			"-H", str(bounds[3]), "-singlefile", "-png", str(pdf), str(stem)], check=True)
		with PIL.Image.open(stem.with_suffix(".png")) as rendered:
			rgb = rendered.convert("RGB")
			ink = PIL.ImageChops.difference(rgb, PIL.Image.new("RGB", rgb.size, "white"))
			bbox = ink.getbbox()
			if bbox is None:
				continue
			trim = (max(0, bbox[0]-12), max(0, bbox[1]-12),
				min(rgb.width, bbox[2]+12), min(rgb.height, bbox[3]+12))
			images.append(rgb.crop(trim))
		segments.append({"page": index+1, "bbox_points": [
			(bounds[0]+trim[0])/2, (bounds[1]+trim[1])/2,
			(bounds[0]+trim[2])/2, (bounds[1]+trim[3])/2]})
	if not images:
		raise ValueError(f"PDF region has no rendered content: {name}")
	width = max(image.width for image in images)
	height = sum(image.height for image in images) + 24 * (len(images)-1)
	composite = PIL.Image.new("RGB", (width, height), "#e5e7eb")
	offset = 0
	for image in images:
		composite.paste(image, (0, offset))
		offset += image.height + 24
	destination.mkdir(parents=True, exist_ok=True)
	asset = destination / f"{name}.webp"
	original_size = list(composite.size)
	composite.thumbnail((1920, 1920), PIL.Image.Resampling.LANCZOS)
	encode_webp(composite, asset)
	result = {"asset": str(asset), "source": str(pdf), "start_anchor": start,
		"end_anchor": end, "segments": segments, "dpi": 144, "webp_quality": 90,
		"page_separator_pixels": 24 if len(images) > 1 else 0,
		"original_dimensions": original_size, "dimensions": list(composite.size)}
	return result


#============================================
def libreoffice_executable() -> str:
	"""Locate the installed LibreOffice executable without a skill dependency."""
	executable = shutil.which("libreoffice") or shutil.which("soffice")
	macos = pathlib.Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
	if executable is None and macos.is_file():
		executable = str(macos)
	if executable is None:
		raise RuntimeError("LibreOffice is required for native artifact captures")
	return executable


#============================================
def render_workbook(source: pathlib.Path, name: str, temporary: pathlib.Path,
		destination: pathlib.Path, print_area: str, sheet_name: str) -> dict:
	"""Print a disposable XLSX copy through native Calc, retaining complete print content."""
	workspace = pathlib.Path(tempfile.mkdtemp(prefix="workbook_", dir=temporary))
	print_copy = workspace / f"{name}.xlsx"
	prepare_workbook(source, print_copy, print_area, sheet_name)
	profile = workspace / "profile"
	process = subprocess.run([libreoffice_executable(),
		f"-env:UserInstallation={profile.as_uri()}", "--headless", "--convert-to",
		"pdf:calc_pdf_Export", "--outdir", str(workspace), str(print_copy)],
		check=True, capture_output=True, text=True, timeout=120)
	pdf = print_copy.with_suffix(".pdf")
	if not pdf.is_file():
		raise RuntimeError(f"Calc produced no PDF: {process.stdout} {process.stderr}")
	stem = workspace / "rendered"
	subprocess.run(["pdftoppm", "-r", "144", "-singlefile", "-png", str(pdf), str(stem)],
		check=True)
	with PIL.Image.open(stem.with_suffix(".png")) as image:
		rgb = image.convert("RGB")
		ink = PIL.ImageChops.difference(rgb, PIL.Image.new("RGB", rgb.size, "white"))
		bbox = ink.getbbox()
		if bbox is None:
			raise ValueError(f"Calc rendered an empty print area: {print_area}")
		bounds = (max(0, bbox[0]-12), max(0, bbox[1]-12),
			min(rgb.width, bbox[2]+12), min(rgb.height, bbox[3]+12))
		destination.mkdir(parents=True, exist_ok=True)
		asset = destination / f"{name}.webp"
		view = rgb.crop(bounds)
		original_size = list(view.size)
		view.thumbnail((1920, 1920), PIL.Image.Resampling.LANCZOS)
		encode_webp(view, asset)
	result = {"asset": str(asset), "source": str(source), "print_area": print_area,
		"renderer": "LibreOffice Calc PDF export and Poppler", "page": 1,
		"bbox_pixels": list(bounds), "dpi": 144, "webp_quality": 90,
		"native_pdf": str(pdf), "scale": view.width / original_size[0],
		"original_dimensions": original_size, "dimensions": list(view.size)}
	return result


#============================================
def prepare_workbook(source: pathlib.Path, destination: pathlib.Path, print_area: str,
		sheet_name: str) -> None:
	"""Change only print settings in a disposable copy of the actual workbook."""
	workbook = openpyxl.load_workbook(source)
	sheet = workbook[sheet_name]
	workbook.active = workbook.index(sheet)
	for other in workbook:
		other.sheet_state = "visible" if other is sheet else "hidden"
	sheet.print_area = print_area
	sheet.page_setup.orientation = "landscape"
	sheet.page_setup.paperSize = sheet.PAPERSIZE_A3
	sheet.page_setup.fitToWidth = 1
	sheet.page_setup.fitToHeight = 1
	sheet.sheet_properties.pageSetUpPr = (
		openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True))
	sheet.page_margins = openpyxl.worksheet.page.PageMargins(
		left=0.25, right=0.25, top=0.25, bottom=0.25)
	sheet.print_options.gridLines = True
	sheet.print_options.headings = True
	workbook.save(destination)
	workbook.close()


#============================================
def completed_workbook(source: pathlib.Path, lesson: pathlib.Path, destination: pathlib.Path) -> None:
	"""Apply the baseline authored actions to a styled disposable student workbook."""
	document = tutorial_lib.compiler.compile_document(lesson)
	cases = sheets_validation_lib.prepare_cases(document)
	case = next(item for item in cases if item["scenario"] == "baseline")
	workbook = openpyxl.load_workbook(source)
	for write in case["writes"]:
		cell = workbook[write["sheet"]][write["address"]]
		value = write["value"]
		if "formulaValue" in value:
			cell.value = tutorial_lib.formula_io.serialize_formula(value["formulaValue"])
		elif "stringValue" in value:
			cell.value = value["stringValue"]
			cell.data_type = "s"
		elif "numberValue" in value:
			cell.value = value["numberValue"]
		elif "boolValue" in value:
			cell.value = value["boolValue"]
		else:
			cell.value = None
	workbook.calculation.fullCalcOnLoad = True
	workbook.calculation.forceFullCalc = True
	workbook.save(destination)
	workbook.close()


#============================================
def recalculate_workbook(source: pathlib.Path, destination: pathlib.Path,
		temporary: pathlib.Path) -> None:
	"""Use Calc to update formulas while preserving the styled disposable workbook."""
	output = temporary / "recalculated"
	output.mkdir()
	profile = temporary / "calc_profile"
	process = subprocess.run([
		libreoffice_executable(), f"-env:UserInstallation={profile.as_uri()}", "--headless",
		"--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(output), str(source),
	], check=True, capture_output=True, text=True, timeout=120)
	converted = output / source.name
	if not converted.is_file():
		raise RuntimeError(f"Calc did not write {converted}: {process.stdout}\n{process.stderr}")
	shutil.copyfile(converted, destination)


#============================================
def main() -> None:
	"""Capture four current views and preserve canonical teaching artifacts."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args()
	repo_result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True,
	)
	root = pathlib.Path(repo_result.stdout.strip())
	output = root / "tutorial_output"
	caffeine = "caffeine_3_quadratic_regression"
	caffeine_parts = ("caffeine_1_descriptive_statistics", "caffeine_2_linear_regression",
		"caffeine_3_quadratic_regression")
	microbes_f = "microbes_4_f_test"
	microbes_anova = "microbes_5_anova"
	caffeine_release = output / "caffeine_release"
	pdf = caffeine_release / f"{caffeine}.pdf"
	f_pdf = output / microbes_f / f"{microbes_f}.pdf"
	anova_xlsx = output / microbes_anova / f"{microbes_anova}.xlsx"
	destination = root / "docs" / "screenshots"
	# Fingerprint all canonical teaching sources and built student artifacts.
	canonical = sorted((root / "tutorial_data").glob("*.md"))
	protected = canonical + [caffeine_release / f"{stem}{suffix}"
		for stem in caffeine_parts for suffix in (".docx", ".pdf")] + [caffeine_release / "workbook.xlsx"] + [
		output / stem / f"{stem}{suffix}"
		for stem in (microbes_f, microbes_anova)
		for suffix in (".docx", ".pdf", ".xlsx")]
	before = {str(path.relative_to(root)): digest(path) for path in protected}
	temporary = pathlib.Path(tempfile.mkdtemp(prefix="readme_capture_"))
	views = [
		(pdf, None, "Step 1: Set Up Your Google Sheet", "caffeine_3_illustrated_opening"),
		(pdf, "Step 3: Create a SQUARED Sleep-Hours Column",
			"Step 4: Calculate Quadratic Regression", "caffeine_3_fill_down_instructions"),
		(f_pdf, "Step 4: Calculate the F-Statistic",
			"Step 5: Calculate the Degrees of Freedom", "microbes_4_formula_instruction"),
	]
	metadata = [capture_pdf(source, start, end, name,
		temporary, destination) for source, start, end, name in views]
	completed_source = temporary / "microbes_5_completed_anova_source.xlsx"
	completed_workbook(anova_xlsx, root / "tutorial_data" / f"{microbes_anova}.md", completed_source)
	completed = temporary / "microbes_5_completed_anova.xlsx"
	recalculate_workbook(completed_source, completed, temporary)
	metadata.append(render_workbook(completed,
		"microbes_5_completed_anova", temporary, destination, "H1:M16", "30 Year ANOVA Test"))
	after = {str(path.relative_to(root)): digest(path) for path in protected}
	if after != before:
		raise RuntimeError("A protected teaching source or canonical artifact changed")
	receipt = {
		"captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
		"protected_sha256": after,
		"assets_sha256": {pathlib.Path(item["asset"]).name: digest(pathlib.Path(item["asset"]))
			for item in metadata},
		"renderer": "repository-owned LibreOffice and Poppler",
		"captures": metadata,
		"canonical_files_unchanged": True,
		"completed_demo": {
			"asset": "microbes_5_completed_anova.webp",
			"source": "styled canonical student workbook plus baseline authored actions",
			"calculation": "LibreOffice Calc recalculation in a disposable workspace",
			"canonical_student_workbook": "unchanged and intentionally blank",
		},
	}
	receipt_path = temporary / "receipt.json"
	receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
	shutil.copyfile(receipt_path, destination / "capture_receipt.json")
	print(f"Capture receipt: {receipt_path}")


if __name__ == "__main__":
	main()
