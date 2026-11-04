# Reflection migration

## M1: Content map before editing

The revised contract is one flat `### Reflection Questions` list under Workbook per source.
Ordinary Tutorial directions preserve activity timing by referring to local question numbers.
The frozen Nov_4_Artifacts descriptive-statistics PDF/XLSX are evidence only and stay unchanged.
The current corpus has 12 sources; archived course material is outside this migration.

| Source | Existing question wording or activity | What stays inline | Intended timing |
| --- | --- | --- | --- |
| babies_1_z_test | "Discuss how changing the dataset size or individual baby weights affects the hypothesis test results and your interpretation." | E19 original-result interpretation/examples; add/modify-weight practice actions | After practice edits |
| babies_2_t_test | "Discuss when the t-test results start to resemble the z-test."; "Discuss how the flexibility in sample size affects the results of the t-test and compare this to their earlier z-test results." | E20 original-result interpretation; change/add-weight actions | After adding weights; end of practice |
| babies_3_two_sample_t_test | "For the right-tailed alternative, state whether the data provide sufficient evidence that Joe's population mean is greater." | G8 chosen-test interpretation and sentence example; equality/causality limitations | After interpreting the two-hospital test |
| caffeine_1_descriptive_statistics | "Based on your result, do students appear to be getting enough sleep? Is the average higher or lower than you expected?"; "Is the median similar to your mean?"; "Write two sentences for Dr. Caffeine: one about typical sleep and its variability, and one about typical exam performance and its variability. Include the six calculated values and their units." | All six calculations, units, worked descriptions of center/spread; remove duplicated D6 response table in all three shared workbook declarations | After mean; after median; after standard deviation |
| caffeine_2_linear_regression | Existing seven-row Linear Regression Reflection table: prediction, slope/causation, intercept/observed range, seven-hour prediction, R-squared, p-value/decision, overall straight-line adequacy | Equations, worked slope/intercept explanations, prediction calculation, hypothesis tests; replace equivalent inline reflection requests with local directions | Prediction before calculations; slope/intercept/prediction after calculation; R-squared after fit; decision after test; model adequacy at end |
| caffeine_3_quadratic_regression | Existing seven-row Quadratic Regression Reflection table: missed pattern, sign of b2, R-squared comparison, quadratic-term p-value, exploratory selection, causation, 16-hour extrapolation | All calculations and worked explanations; retain richer residual/new-data model-check question because it asks a different task | After straight-line check; after coefficients; after test and exploratory caveat; after comparison; final limitations |
| microbes_1_z_test | "Think about how both changing the dataset size and modifying individual Shannon Index values impacts the hypothesis test results." | D19 interpretation/examples; add/modify-index actions; explanatory caveats on sample size and extreme values | After practice edits; minimally change Think about to Discuss |
| microbes_2_t_test | "Discuss how the t reference distribution approaches the normal distribution as degrees of freedom increase; this does not make the population SD known or guarantee a smaller p-value."; "Discuss how the flexibility in sample size affects the results of the one-sample T-test and compare this to your earlier z-test results. Specifically, observe how a larger sample size reduces uncertainty, impacting the p-value and overall hypothesis test results." | D19 original-result interpretation/examples; change/add-index actions | After adding samples; end of practice |
| microbes_3_two_sample_t_test | "Discuss how the t reference distribution approaches the normal distribution as degrees of freedom increase; this does not make the population variances known or guarantee a smaller p-value."; "Discuss how the flexibility in sample size affects the results of the two-sample T-test and compare this to your earlier z-test results. Focus on how a larger sample size reduces uncertainty and impacts the p-value, degrees of freedom, and overall results." | Original-result interpretation/examples; change/add-index actions | After adding samples; end of practice |
| microbes_4_f_test | "Discuss how sample size affects the F-test results and compare this to earlier T-test results. Focus on how a larger sample size can reduce uncertainty under the model and change the F-distribution, without guaranteeing a smaller p-value." | Original-result interpretation/examples; change/add-index actions | End of practice |
| microbes_5_anova | "Observe how the sample means, F-statistic, and p-value change."; "Discuss how sample size influences the ANOVA test and compare this to earlier F-test results." | I16 interpretation/example; practice copy, modify and add-data actions | After modification; after sample-size experiment; minimally adapt Observe to Describe |
| petase_1_linear_regression | "Compare the ranking in G13:G15 with the concentration ranking and explain why volume matters for recovered mass." | Calibration/calculations; original synthetic-data report; J13 PETase-specific interpretation and limits | After recovered-mass calculation |

Both manually declared Caffeine reflection sheets are removed from all three sources. Each source
keeps only its own question list. All three retain identical four ordinary sheet declarations.
Warmup questions preserve the current source, rather than borrowing unrelated frozen questions.

## Migration result and checks

| Source | Questions |
| --- | --- |
| babies_1_z_test | 1 |
| babies_2_t_test | 2 |
| babies_3_two_sample_t_test | 1 |
| caffeine_1_descriptive_statistics | 3 |
| caffeine_2_linear_regression | 7 |
| caffeine_3_quadratic_regression | 7 |
| microbes_1_z_test | 1 |
| microbes_2_t_test | 2 |
| microbes_3_two_sample_t_test | 2 |
| microbes_4_f_test | 1 |
| microbes_5_anova | 2 |
| petase_1_linear_regression | 1 |

Total: 30 questions across 12 sources. Each has one nonempty Workbook list and authored local
question directions. Caffeine slope/intercept directions jointly reference questions 2 and 3.
The seven linear and seven quadratic table prompts retain their exact source wording. Warmup
retains its three existing interpretation requests. Equivalent inline answer requests become
local directions; worked explanations and distinct interpretation/calculation tasks remain.
Removing the warmup D6 response table from all three declarations avoids a second response
location for its summary question. The four ordinary Caffeine Workbook declarations compare
identically after migration. Joe's/Microbes original-result cell examples and PETase J13 remain.

Verification (2026-11-04):

```bash
source source_me.sh && python3 - <<'PY'
import pathlib
import subprocess
import sys
for path in sorted(pathlib.Path('tutorial_data').glob('*.md')):
    result = subprocess.run([sys.executable, 'make_tutorial.py', 'lint', str(path)],
                            capture_output=True, text=True)
    print(path.name, 'PASS' if result.returncode == 0 else 'FAIL')
    if result.returncode:
        print(result.stdout, result.stderr)
        raise SystemExit(result.returncode)
PY
```

All 12 offline lints passed. Direct `compiler.compile_document(path)` calls also compiled all
12 sources. Compiler worksheet totals include the new generated reflection worksheet: Caffeine
has five sheets (four ordinary plus one reflection), Joe's national comparisons three, and the
remaining sources two. A temporary source inspection confirmed exactly one Workbook reflection
heading per source, the question counts above, valid local numeric references, and identical
Caffeine ordinary workbook declarations. Existing Google mapping notes and INDEX/LINEST
compatibility warnings remain; offline lint does not verify live Google behavior or calculations.
No LibreOffice command, generated output build, visual review, or frozen-file edit occurred in
this content workstream. The integration workstream owns generated-output inspection.

Correction (2026-11-04): Updated the caffeine linear-regression chart instruction to name its
actual **Linear Regression** worksheet tab. `FindHours...` now points to that tab; no Caffeine
source retains the stale **Sleep and scores** name. The source compiled with zero errors.
