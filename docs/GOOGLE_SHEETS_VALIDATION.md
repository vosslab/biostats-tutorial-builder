# Google Sheets validation

The optional runner executes formulas in actual Google Sheets using fresh test workbooks.
It reads the compiled tutorial model, seeds typed workbook data, then applies assignments and
replacements in instruction order. Authored Google mapping URLs are never write targets.

## Prepare and execute

Run from the repository root using the Python bootstrap:

```bash
source source_me.sh && python3 -m devel.validate_google_sheets \
  --dry-run --output build/sheets-validation tutorial_data/babies/babies_1_z_test.md
```

Use actual tutorial paths such as [the babies z-test](../tutorial_data/babies/babies_1_z_test.md). Dry run writes
`execution-cases.json` and `report.json` locally and makes no Google requests. The report says
`not_run` for Google calculation and scientific oracle checks.

Install the [development dependencies](../pip_requirements-dev.txt) for live execution. Configure
Google Application Default Credentials separately with Sheets API access. The runner uses existing
ADC, including the standard `GOOGLE_APPLICATION_CREDENTIALS` mechanism; it never starts login or
prints credential contents. Missing ADC produces `unavailable` and exit code 2.

```bash
source source_me.sh && python3 -m devel.validate_google_sheets \
  --live --expectations tutorial_output/validation/tutorial_expectations.json \
  --output build/sheets-live tutorial_data/babies/babies_1_z_test.md
```

Each case creates a workbook titled `TUTORIAL VALIDATION - ...` with original worksheet names,
preserving cross-sheet references. Every created ID and URL is saved immediately in the report.
Test workbooks remain available for inspection; remove those specific workbooks manually afterward.
The runner cannot accept an existing spreadsheet ID and does not delete files.

## Branch coverage

`baseline` selects the lowest numbered branch in each alternative group. Additional cases named
`group-N-branch-M` change one group to a nonbaseline branch, leaving other groups at baseline.
This covers every branch independently without constructing an exponential product. It does not
claim to cover interactions among independent choice groups. Each case starts with a new workbook.

Assignments use typed `updateCells.userEnteredValue` values: numbers and booleans retain their
types, literal strings stay literal, and formulas use `formulaValue`. Formula checkpoints capture
intermediate results before later replacements. Final reads include every populated cell, capturing
spill errors as well as individual assignment errors.

## Scientific expectations

Expectations use tutorial basenames and unquoted worksheet names in cell keys:

```json
{
  "tutorials": {
    "example.md": {
      "common": {
        "Results!B2": {
          "value": 1.23,
          "relative_tolerance": 1e-7,
          "absolute_tolerance": 1e-9
        }
      },
      "scenarios": {
        "baseline": {"Results!C2": {"value": 0.05}},
        "group-1-branch-2": {"Results!C2": {"value": 0.025}}
      }
    }
  }
}
```

`common` applies to every case; `scenarios` overrides common cells for a named case. Both sections
are optional. Unknown tutorial or scenario names fail before any Google requests. Numbers use
`math.isclose` with the illustrated defaults; strings and booleans require exact values and types.
Compute scientific expectations independently, for example with SciPy and NumPy, and record their
provenance alongside the expectation file. Missing cells and Google errors fail comparisons.

For this collection, generate the complete 12-lesson expectation file first:

```bash
source source_me.sh && python3 -m devel.check_tutorial_calculations
```

The generated `tutorial_output/validation/tutorial_expectations.json` covers 13 execution scenarios and
254 final formula cells. See
[calculation_validation.md](active_plans/reports/calculation_validation.md) for the independent
method and its limits. Google execution remains a separate check.

## Read the evidence

`report.json` separates `sheets_status` (actual calculation errors) from `oracle_status` (agreement
with independent expected answers). Each result records typed `userEnteredValue`, `effectiveValue`,
formula checkpoints, Google error details, comparison results, and the test workbook URL.
No expectations means `not_provided`, never scientific success. An aggregate `incomplete` oracle
status means at least one case had no expectations. A clean Sheets result alone establishes that
the formulas calculated, not that the statistical model or tail was correct.

Exit code 0 means preparation succeeded or live execution completed without observed failures;
1 means a Sheets error or expectation mismatch; 2 means credentials were unavailable. API or
transport failures raise an error and leave the saved report in `running`, preserving created IDs
and completed results. Diagnose the external failure and run again into a separate output folder.
The offline pytest uses a fake transport only to verify requests and error reporting. It is not
Google compatibility evidence.

## Local formula execution

LibreOffice Calc can execute the final workbook state for each prepared scenario without Google
credentials. The repository runner uses a separate temporary profile and compares Calc's saved
results with the independent expectation file. It applies assignments in order and checks the final
cells; it does not test intermediate steps or student interaction.

On the current tutorial snapshot, Calc `26.2.6.3` passed all 254 values across 13 scenarios. The
report is [local_calculation_readiness.md](active_plans/reports/local_calculation_readiness.md),
and the detailed run is `tutorial_output/validation/local_calc_portable/calc/run-eehzg5wq/report.json`.
This is real local formula execution. It does not establish Google Sheets import or execution.
All 14 worksheet Google mappings remain absent, and Application Default Credentials were
unavailable for the live Google attempt. Offline static checks plus Calc execution are the
available local evidence; do not describe them as Google validation.

The implementation follows Google's official references for
[spreadsheet creation](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create),
[typed cell values and calculated results](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells),
and [batch updates](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate).
