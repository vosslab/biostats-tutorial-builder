# Babies tutorial migration

Path note (2026-10-22): paths and command examples below use the current repository layout.
Recorded observations belong to their stated snapshots; renamed output manifests retain their
original contents until the final rebuild and verification refresh.

Status: source migration and offline DOCX/XLSX builds complete. This report
records source evidence and independent numerical checks, not a live Google Sheets calculation.

## Sources and completeness

The complete Fall 2025 Markdown exports supply the prose, scenario, formulas, explanation,
practice tasks, and takeaways. The two one-sample t-test Markdown variants are byte-identical.
The corresponding DOCX documents corroborate the lessons and image counts (z: 10 images;
one-sample t: 2; two-sample t: none). No source artifact was modified.

The migrated files are:

- [babies_1_z_test.md](../../../tutorial_data/babies/babies_1_z_test.md): 7 numbered steps, 2 substeps,
  23 scalar assignments, 10 original PNG companions.
- [babies_2_t_test.md](../../../tutorial_data/babies/babies_2_t_test.md): 10 numbered steps, 3 substeps,
  24 scalar assignments, 2 original PNG companions.
- [babies_3_two_sample_t_test.md](../../../tutorial_data/babies/babies_3_two_sample_t_test.md): 9 numbered
  steps, numbered 0-8, 3 substeps, 20 scalar assignments including two explicit alternatives.

National lessons retain the entire original data sheet and seed the same data on their respective
working sheets. They retain the copying exercise as an optional reset of the data region. This
avoids silently requiring a copy before later formulas can reference data. The generated workbooks
replace the original external template as the main starting point. Original template URLs remain
as provenance links; neither supplies a verified gid, so no Google tab mapping is invented.
The original three-tab screenshot remains, with an explicit explanation of the split workbooks.

All 12 extracted image files were compared byte-for-byte with their original embedded base64
payloads. Screenshot examples are identified as historical, particularly where formulas or tab
names have been corrected. All substantial instructional topics and story beats remain, including
the award committee letter, protest scene, degrees-of-freedom explanation, practice changes to
sample size and weights, interpretation prompts, and Joe's hoped-for redemption. The duplicate
Step 6.3/Step 7 decision assignment in the two-sample original is consolidated into a preview and
one actual assignment; its instructional purpose remains.

## Dataset evidence

The current authoritative XLSX files have these SHA256 fingerprints:

- National workbook: `3d82cd9e268255c251985c262338d39d2ff0542922b203487b2b53b0d1c86de7`.
- Two-sample workbook: `99744e93e9b5d0fe9426479e2fed2e44d9d0d42b5ff7b7dfb6d1d38654dd43b2`.

National source: `Datas for Part 1 and 2!A1:B25`; 24 observations. Two-sample source:
`Part 3 Fried Foods vs. Green Ve!A1:C25`; 24 observations per hospital. The original workbook's
row-101 used extent includes formatting, not 100 observations. No empty formatting rows were
migrated as fictional infants. All five migrated dataset tables were independently parsed from
the authored Markdown and compared, cell by cell, with their respective XLSX source: identical.

The national and two-sample Joe datasets differ (for example, second weight 7.88 versus 8.88).
Each tutorial uses its own original dataset; one was not substituted for the other.
The z-test intentionally retains `B2:B40`, and the t-tests intentionally retain ranges ending at
row 101. The prose explains these blank practice slots. This is deliberate spare capacity, not
missing data. COUNT, AVERAGE, and STDEV.S ignore blank cells. Meaningful original coordinates for
calculation cells are preserved. Formula/output cells and student-written labels start blank;
only table headers and the original Part 2 `E3` text "not used" are seeded.

## Scientific corrections

- Removed the false rule that a sample below 30 makes a z-test invalid. Known population SD and
  a suitable normal model for the sample mean determine the z-test assumptions; estimating SD
  calls for t. Independence, approximate normality and outliers are discussed for small samples.
  See [NIST process-mean tests](https://www.itl.nist.gov/div898/handbook/prc/section2/prc.htm).
- Described the z-statistic in standard errors, not individual-observation standard deviations.
  Changed "population statistic" to "population parameter" and fixed STDEV being described as
  calculating a sample mean. STDEV.S now explicitly calculates the sample SD.
- Made national benchmarks fictional teaching assumptions and hypotheses explicit. Replaced causal
  assertions about fried foods with limits appropriate to observational hospital comparisons.
- Corrected the one-sample t explanation's mistaken D5/D6 references to E9/E10. The right-tailed
  calculation uses `1 - T.DIST(E9, E10, TRUE)` so negative statistics retain the intended direction.
  See [Google T.DIST](https://support.google.com/docs/answer/9369014?hl=en).
- Corrected Welch's `T.TEST` type from 2 (equal variance) to 3 (unequal variance). Added a signed
  mean-difference guard to the one-tailed choice, because the function's one-tailed result alone
  uses an absolute statistic. See [Google T.TEST](https://support.google.com/docs/answer/6055837?hl=en).
  The two formulas are explicit sibling Alternative groups targeting G5.
- Limited the claim that a two-tailed p-value doubles a right-tailed p-value to a statistic pointing
  in the hypothesized direction. Failing to reject is not evidence that the means are equal.
- Corrected Joe's asserted significant national result. His redemption remains his hope; the supplied
  data at alpha 0.05 fail to reject. The story now acknowledges that result instead of overriding it.

## Independent numerical check

Executed with `source source_me.sh && python3`, using statistics.mean/stdev, manual standardized
statistics, scipy.stats.norm.sf, scipy.stats.t.sf, scipy.stats.ttest_1samp, and
scipy.stats.ttest_ind(equal_var=False). These are independent statistical expectations for later
spreadsheet calculation comparison. No student answer was filled into the authored workbook tables.

| Result | Expected value |
| --- | --- |
| National sample size | 24 |
| National mean | 7.807916666666666 |
| National sample SD | 1.446215388272218 |
| Z statistic | 1.0056516221759815 |
| Z two-tailed p | 0.31458318234311144 |
| Z right-tailed p | 0.15729159117155572 |
| One-sample t statistic | 1.0430517096531093 |
| One-sample df | 23 |
| One-sample t two-tailed p | 0.3077643699787132 |
| One-sample t right-tailed p | 0.1538821849893566 |
| Two-sample Joe mean / SD | 8.057916666666667 / 1.4763408913717155 |
| Two-sample Green Veggies mean / SD | 7.656666666666666 / 0.7558506101919454 |
| Welch two-tailed p | 0.24409758423304945 |
| Welch right-tailed p, Joe greater | 0.12204879211652472 |
| Welch right-tailed p with groups swapped | 0.8779512078834752 |

All supplied-data decisions at alpha 0.05 are "Fail to Reject the Null Hypothesis". The swapped
hospital check verifies that the right-tail formula must not simply divide the two-tail value by
two. The normal and one-sample t right-tail calculations likewise exceed 0.5 for negative statistics.
Numerical values were handed to the independent Sheets validation worker for its oracle manifest.

## Validation boundary

All three sources now pass compiler lint with zero errors. Remaining diagnostics are intentional:

| Tutorial | Unavailable-input warnings | Range-overshoot warnings | Google mapping notes |
| --- | --- | --- | --- |
| Z | 4 | 3 | 2 |
| One-sample t | 4 | 3 | 2 |
| Welch | 15 | 12 | 1 |

Input/range warnings refer to the deliberately blank practice rows, plus the student-written
interpretation cell. Missing Google mappings are explicit; no gid was invented. The initial
compile_source local-import error was reported to the compiler owner and has been resolved.

Built each lesson with `build_document(..., 'docx,xlsx')`, reopened the generated DOCX and XLSX,
and checked every working-sheet cell for prefilled formulas: none. E9/G5 checks are blank as
expected. Generated DOCX image counts are 10, 2 and 0, matching all original local companions;
paragraph counts are 105, 109 and 75. Bundles are under tutorial_output/babies_1_z_test,
tutorial_output/babies_2_t_test, and tutorial_output/babies_3_two_sample_t_test.

Google import, formula execution, link navigation, and visual DOCX/PDF review remain separate
external checks. Neither independent scipy results nor offline source checks claim these passed.


## Post-freeze tab-name correction

Corrected the one-sample Z lesson's setup prose from `Part 1: National Z-Test` to the declared
worksheet name `Part 1 National Z-Test`. No workbook content or calculation changed.
`source source_me.sh && python3 make_tutorial.py lint tutorial_data/babies_1_z_test.md` passed with zero
errors; the existing spare-range and free-response warnings and mapping notes remain. Final
PDF rebuild and visual verification belong to the render-validation workstream.
