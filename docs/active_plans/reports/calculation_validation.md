# Independent calculation validation

Historical snapshot: the Google runner was removed on 2026-11-05. Use
[LOCAL_VALIDATION.md](../../LOCAL_VALIDATION.md) for the current local-only workflow.

Path note (2026-10-22): paths and command examples below use the current repository layout.
Recorded observations belong to their stated snapshots; renamed output manifests retain their
original contents until the final rebuild and verification refresh.

All 12 migrated tutorials have reproducible independent numerical expectations. There are
13 execution scenarios (the babies two-sample lesson has two alternatives), covering all
254 final formula cells across those scenarios. Eight synthetic checks exercise both signs of
Z, one-sample t and Welch t statistics, and both variance-ratio orientations with unequal degrees
of freedom. No Google Sheets formula execution is claimed by this report.

## Method and boundaries

[devel/tutorial_oracles.py](../../../devel/tutorial_oracles.py) reads numeric seeds from the compiled
worksheet models and numeric population-parameter assignments. It never parses or evaluates a
spreadsheet formula. Explicit curriculum mappings associate intended statistical outputs with cells.
SciPy supplies one-sample t, Welch t, one-way ANOVA and distribution probabilities. NumPy supplies
sample summaries, SVD least-squares coefficients, and QR-based coefficient covariance. The
ANOVA sums of squares independently center raw observations rather than reusing summary-cell
formulas. PETase blanks, dilution factors and sample volumes come from the actual seed table.

[devel/check_tutorial_calculations.py](../../../devel/check_tutorial_calculations.py) requires exactly
12 input lessons and fails on an unknown lesson, compilation error, missing expected formula cell,
or expected cell without an authored formula. It checks every prepared alternative separately and
records each result's source line. This validates the expectation mapping and intended mathematics;
it does not establish that Google Sheets evaluates the authored formula to that result.

Google runner expectations are emitted to `tutorial_output/validation/tutorial_expectations.json`, using
`tutorials -> basename -> common/scenarios -> Sheet!Cell -> value`. Full precision numerical and
decision outputs, source lines, scenario counts and synthetic check results are also recorded in
`tutorial_output/validation/independent_oracles.json`. Numeric comparisons use relative tolerance `1e-7`
and absolute tolerance `1e-10`; string decisions require equality. Common values apply to every
scenario; scenario values override common ones. Generated files are reproducible ignored outputs.

## Numerical results

Values below are rounded for reading; JSON preserves full precision. All reported tails follow the
authored direction. Two-sample microbial statistics use 2024 minus 2014; babies use Joe minus Green
Veggies. Variance ratios use 2024 variance over 2014 variance.

| Tutorial | Independent result |
| --- | --- |
| Babies Z | Z = 1.00565162218; two-tail p = 0.314583182343; right-tail p = 0.157291591172 |
| Babies one-sample t | t = 1.04305170965; right-tail p = 0.153882184989; two-tail p = 0.307764369979 |
| Babies Welch t | Two-tail p = 0.244097584233; Joe-greater p = 0.122048792117 |
| Caffeine descriptive | Means: sleep 7.16, score 80.84; medians 7 and 83; sample SDs 2.36607973943 and 12.7758887493 |
| Caffeine linear | Slope = 3.17907115213; intercept = 58.0778505508; R squared = 0.346638667858; slope p = 0.00196019030045 |
| Caffeine quadratic | b2 = -1.52025034170; b1 = 24.9932378966; b0 = -12.0046039853; R squared = 0.847164660392; quadratic-term p = 2.17800441157e-8 |
| Microbes Z | Z = -1.65816847310; two-tail p = 0.0972834662846; lower p = 0.0486417331423; higher p = 0.951358266858 |
| Microbes one-sample t | t = -1.10437517161; two-tail p = 0.280850568188; lower p = 0.140425284094; higher p = 0.859574715906 |
| Microbes Welch t | t = -1.91451806355; df = 39.4952370415; two-tail p = 0.0628180587792; lower p = 0.0314090293896; higher p = 0.968590970610 |
| Microbes F | F = 0.422647850401; df = 23, 23; two-tail p = 0.0441328052033; lower p = 0.0220664026017; higher p = 0.977933597398 |
| Microbes ANOVA | F = 0.878927381398; df = 4, 88; right-tail p = 0.479991495505 |
| PETase calibration | Slope = 0.798285714286; intercept = 0.000214285714286; R squared = 0.999941077734 |

The ANOVA degrees of freedom reflect the actual unequal group sizes, not filled-down blank rows.
At alpha 0.05 the microbial lower Z, lower Welch t, and two-tailed/lower variance comparisons reject;
the other displayed microbial comparisons and all babies comparisons fail to reject. Synthetic
opposite signs preserve two-tail probabilities and reverse directional probabilities. The F
synthetic checks also swap numerator/denominator degrees of freedom under reciprocation.

## Verification evidence

Commands run from the repository root:

```bash
source source_me.sh && python3 -m devel.check_tutorial_calculations
source source_me.sh && python3 -m devel.validate_google_sheets tutorial_data/*.md \
  -n -e tutorial_output/validation/tutorial_expectations.json -o tutorial_output/validation/sheets
source source_me.sh && python3 -m pytest -q tests/test_tutorial_oracles.py \
  tests/test_function_typing.py tests/test_pyflakes_code_lint.py \
  tests/test_import_requirements.py
```

The generator completed all 12 lessons, 13 scenarios, 254 expected formula cells and eight synthetic
checks. The actual Google runner accepted the merged expectations and prepared all 13 cases without
API requests. A separate comparison against the earlier caffeine, PETase and microbial numerical
expectation files checked 200 overlapping cells with zero discrepancies. The focused oracle tests
and typing, lint and dependency checks passed: 128 tests. The two permanent oracle tests protect
directional sign behavior and quadratic coefficient ordering/standard error, which directly affect
student inferences. Failure means repair the independent model before trusting its expected values.

An expanded hygiene run including ASCII, indentation, shebang and whitespace checks produced
434 passes and two ASCII failures in unchanged historical source artifacts: zero-width spaces in
`2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial_Fall_2025.md` and a superscript plus in
`2025_Artifacts/PETase_1_Linear_Regression_Tutorial_Fall_2025.md`. Neither failure concerns the new
oracle files or migrated tutorials; the original source artifacts were preserved.

Application Default Credentials are unavailable in this environment. Thus live Sheets numerical
comparison, Sheets formula compatibility, effective-value errors, and real spill results remain
unverified here. The Google runner must execute the generated expectations with authorized ADC to
close that evidence gap; dry-run preparation is not a substitute for that execution.
