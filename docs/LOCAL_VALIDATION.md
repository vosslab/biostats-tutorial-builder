# Local calculation validation

Generate independent expected results and execute tutorial calculations locally. Google Drive
uploading and Google Docs/Sheets importing are always out of scope. The Google runner has been
removed; no credentials or Google API packages are needed.

## Generate expected results

From the repository root:

```bash
source ./source_me.sh
python3 -m devel.check_tutorial_calculations
```

The command compiles the tutorial sources and derives expected results independently with NumPy
and SciPy. It writes `tutorial_expectations.json` and `independent_oracles.json` under
`tutorial_output/validation/`. This checks formula destinations and expected values; it does not
execute spreadsheet formulas.

## Execute formulas in LibreOffice Calc

```bash
python3 -m devel.validate_libreoffice tutorial_data/*/*.md \
  --expectations tutorial_output/validation/tutorial_expectations.json
```

The runner applies each lesson's instructions to a disposable local workbook, recalculates it
using an isolated LibreOffice profile, and compares saved results with the independent
expectations. On this macOS host, agents must run this command outside the sandbox.

Cases cover the baseline and each alternative branch independently, changing one choice group
at a time. They preserve typed numbers, booleans, formulas, literal strings, and instruction order.
This does not exhaust combinations of unrelated choices.

Each invocation creates a separate directory under `tutorial_output/validation/libreoffice/`.
Its `report.json` records the engine, source fingerprints, results, and comparisons. Missing
calculated values and spreadsheet errors fail validation. Numbers use the expectation's numeric
tolerances; text and booleans require matching values and types. Exit code 0 means all cases
passed; exit code 1 means a calculation or comparison failed.

Inspect the failed case and its disposable workbook, correct the source or independent expectation
as appropriate, regenerate expectations, and rerun. Preserve original teaching workbooks.

## Evidence limits

These checks cover final workbook states, not intermediate student actions, scientific accuracy,
or Google Docs/Sheets behavior. Local case preparation and comparison helpers remain in
[sheets_validation_lib.py](../devel/sheets_validation_lib.py), shared by Calc validation,
calculation checks, and screenshot capture.

The per-source checker starts each lesson with its own blank workbook. Part 3 calculates its linear
comparison from the observations on its own sheet, so it does not depend on completed Part 2 cells.
Students continuing from Part 2 may copy those results instead.

Earlier execution evidence is recorded in
[local_calculation_readiness.md](active_plans/reports/local_calculation_readiness.md).

## Publication review

Every tutorial requires the two LLM author review checks in
[AUTHORING_GUIDE.md](AUTHORING_GUIDE.md#required-llm-author-review-before-publishing): add a data point at the bottom
and delete one from the middle, verifying the final result without formula changes.
No human review or approval is required. Passing the original dataset's calculation checks does not establish adaptability.

One-time checks of the current babies, microbes, and Caffeine sources passed 24 Calc cases:
append a bottom observation or clear a middle observation, preserving every completed formula.
Reports are under `tutorial_output/validation/variable_n/`. These experiments left canonical data
unchanged and excluded PETase's separate, fully occupied calibration and unknown blocks.
They provide supporting evidence, not a generic test runner or publication gate.
