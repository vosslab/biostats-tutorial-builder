# Usage

Google Drive uploading is always out of scope for this repository. Builds and delivery produce
local files only. Do not upload artifacts to Google Drive or import them into Google Docs or
Google Sheets as part of this workflow. Google-compatible output does not authorize uploading.

For the student authoring path, see [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md). This page is for building
and maintaining tutorial files.

Follow [INSTALL.md](INSTALL.md) to download the project and install its requirements. In Terminal,
open the project folder, then start Bash and load its shell environment:

```bash
bash
source source_me.sh
```

If you created `.venv` using [INSTALL.md](INSTALL.md#if-pip-reports-externally-managed-environment),
run `source .venv/bin/activate` after `source source_me.sh` and before any Python commands.

Run subsequent commands in this same Bash shell.

To regenerate the two Caffeine data figures from the canonical observations, install the
development requirements and run:

```bash
python3 devel/render_caffeine_figures.py
```

The command uses NumPy least-squares polynomial fits and Matplotlib, with larger axis text and
gridlines drawn behind the points. Rebuild the release afterward to embed the updated images.

Choose a lesson from [TUTORIAL_CATALOG.md](TUTORIAL_CATALOG.md), including the explicitly
synthetic PETase calibration example.

## Validate and build

Lint checks one source without writing output files:

```bash
python3 make_tutorial.py lint tutorial_data/babies/babies_1_z_test.md
```

Build DOCX, XLSX, and PDF into `tutorial_output/<source-stem>/`:

```bash
python3 make_tutorial.py build tutorial_data/babies/babies_1_z_test.md
```

PDF output is reopened with a PDF reader and must contain pages before the bundle is published.

Use `--format` to build a supported subset. `docx,xlsx` skips PDF conversion; `docx` and `xlsx`
build one file. `all` is the default. `--output-dir` selects a different bundle directory.

```bash
python3 make_tutorial.py build tutorial_data/babies/babies_1_z_test.md --format docx,xlsx
python3 make_tutorial.py build tutorial_data/babies/babies_1_z_test.md --format xlsx --output-dir /tmp/babies-workbook
```

The bundle contains the requested deliverables and `validation.json`. The report describes offline
checks and does not claim Google import, link navigation, or formula calculation. Warnings are
reported while a build may still complete; validation errors stop publication. Existing generated
files are protected by the bundle manifest, and edited outputs must be preserved before rebuilding.

Pass several sources to build their DOCX/PDF files beside one compatible shared workbook. The source
order controls the workbook tab order:

```bash
python3 make_tutorial.py build tutorial_data/caffeine/caffeine_1_descriptive_statistics.md \
  tutorial_data/caffeine/caffeine_2_linear_regression.md \
  tutorial_data/caffeine/caffeine_3_quadratic_regression.md \
  --output-dir tutorial_output/caffeine_release
```

Use `--workbook-name` when students must receive a specifically named workbook:

```bash
python3 make_tutorial.py build tutorial_data/caffeine/caffeine_1_descriptive_statistics.md \
	tutorial_data/caffeine/caffeine_2_linear_regression.md \
	tutorial_data/caffeine/caffeine_3_quadratic_regression.md \
	--output-dir tutorial_output/caffeine_release \
	--workbook-name Dr_Caffeines_All_Nighter_Academy_Student_Workbook.xlsx
```

Shared data tabs come first. Each source's work tabs are followed immediately by its generated
reflection tab, in source order. The tab name and
question identifiers follow the resolved Part identity; see [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

For real local formula execution, generate independent expectations and run the final workbook
states through LibreOffice Calc:

```bash
python3 devel/check_tutorial_calculations.py -o tutorial_output/validation/local_calc
python3 devel/validate_libreoffice.py tutorial_data/*/*.md \
  -e tutorial_output/validation/local_calc/tutorial_expectations.json \
  -o tutorial_output/validation/local_calc/calc
```

This compares Calc's saved results with independent expectations after all authored assignments.
It does not verify intermediate steps or Google Sheets behavior. See
[local_calculation_readiness.md](active_plans/reports/local_calculation_readiness.md) for current
engine evidence.

## Import a workbook

Create a Markdown draft from a simple XLSX workbook:

```bash
python3 make_tutorial.py import-xlsx template.xlsx --output draft.md
```

The destination must not already exist. The draft contains workbook data and a Tutorial scaffold;
author the instructions before building. See [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) and the
[tutorial specification](TUTORIAL_SPEC.md) for supported content and limits.

## Maintain a worksheet after a layout decision

Students write ordinary Markdown and ordinary Excel formulas. They do not need this command for
normal tutorial authoring. Use it only when an author has deliberately changed an existing layout
and wants the compiler to update the associated workbook coordinates, formula operands, action
links, and explicit cell instructions together.

The command prints a preview and leaves the source unchanged by default:

```bash
python3 make_tutorial.py worksheet-edit tutorial_data/caffeine/caffeine_3_quadratic_regression.md \
  --sheet "Quadratic Regression" insert-columns --at A --count 1
```

Review the entire diff. If every change is intended, rerun the same command with `--write` to
atomically replace an unchanged source file. `--write` may appear before or after the edit operation.
The command recompiles its
candidate before it can write. It supports familiar
worksheet maintenance operations:

```bash
python3 make_tutorial.py worksheet-edit lesson.md --sheet Data insert-rows --at 2 --count 1
python3 make_tutorial.py worksheet-edit lesson.md --sheet Data move-range \
  --range H1:M26 --destination J1
python3 make_tutorial.py worksheet-edit lesson.md --sheet Data resize-observations \
  --data-range A1:B26 --rows 50
```

The editor coordinates declared worksheet geometry, semantic action targets, explicit cell/range
instructions, and formulas marked as spreadsheet formulas. Observation resizing updates both the
visible range and semantic target of a Fill link. Use uppercase letters for standalone column
references (`column D`, `columns D-F`); ordinary words following `column` remain prose. Review the
complete diff before applying it, then follow the rebuild checklist in
[reference/CHANGES.md](reference/CHANGES.md).

The preview also reports ambiguous coordinates for review. Use an explicit `cell`, `range`, action
link, or code-formatted spreadsheet formula when a reference must be maintained, and verify the
proposed result. A resize prints review notices for nearby numerical
explanations; authors remain responsible for checking whether those examples and interpretations
still make sense. If a reference only partly overlaps a moved range, or the resulting source does
not compile, the command stops without writing anything.

## Check numerical expectations

Generate independent SciPy/NumPy expectations for all 12 lessons, then prepare the optional
Google Sheets execution cases without API requests:

```bash
python3 -m devel.check_tutorial_calculations
python3 -m devel.validate_google_sheets tutorial_data/*/*.md --dry-run \
  --expectations tutorial_output/validation/tutorial_expectations.json --output tutorial_output/validation/sheets
```

With authorized Application Default Credentials available, replace `--dry-run` with `--live`
and choose a separate output directory. The live runner creates fresh test workbooks and records
their IDs; it does not modify linked original spreadsheets. See
[GOOGLE_SHEETS_VALIDATION.md](GOOGLE_SHEETS_VALIDATION.md) for credentials, evidence, and limits.
An unavailable-credentials result is not a successful calculation check.

## Refresh documentation screenshots

After changing renderer styles, rebuild the documentation screenshots so the examples show the
current output. From the repository root, run:

```bash
source source_me.sh && python3 devel/refresh_documentation.py
```

The refresh renders the documentation capture sets from native outputs and anchors crops to
semantic content, so a style change can be reviewed in the affected images. It also records a
machine-readable capture receipt. Review the refreshed images and receipt alongside the lesson
pages that use them. For the three guide Parts, the refresh combines the guide text with the
workbook from [examples/authoring_features.md](examples/authoring_features.md), then runs the normal
compiler. This workbook supports native export; it is not a project students must complete.
The guides remain ordinary Markdown with literal source in fenced code blocks;
they are not direct build sources. Review rendered GFM documentation separately from the PDFs.

This optional documentation workflow uses the existing application environment and Pillow,
Poppler (`pdftotext`, `pdftoppm`), WebP (`cwebp`), librsvg (`rsvg-convert`), LibreOffice, and the
required fonts. See [INSTALL.md](INSTALL.md) for `brew bundle` and font requirements.
