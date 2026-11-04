# Microbes migration report

Path note (2026-10-22): paths and command examples below use the current repository layout.
Recorded observations belong to their stated snapshots; renamed output manifests retain their
original contents until the final rebuild and verification refresh.

## Coverage

All five complete Microbes tutorials have been migrated to single-source Markdown. Their source
files are [microbes_1_z_test.md](../../../tutorial_data/microbes/microbes_1_z_test.md),
[microbes_2_t_test.md](../../../tutorial_data/microbes/microbes_2_t_test.md),
[microbes_3_two_sample_t_test.md](../../../tutorial_data/microbes/microbes_3_two_sample_t_test.md),
[microbes_4_f_test.md](../../../tutorial_data/microbes/microbes_4_f_test.md), and
[microbes_5_anova.md](../../../tutorial_data/microbes/microbes_5_anova.md).

| Tutorial | Original instruction steps | Preserved embedded images | Seeded source cells |
| --- | --- | --- | --- |
| Z-test | 8, including all three tail substeps | 2 | 52 |
| Benchmark t-test | 9, including all three tail substeps | 1 | 52 |
| Two-sample t-test | 9, including all three tail substeps | 2 | 88 |
| Two-sample F-test | 9, including all three tail substeps | 1 | 88 |
| ANOVA | 13 | 2 | 146 |

These are full migrations, retaining scenarios, statistical explanations, distribution diagrams,
formula-method comparisons, decision and interpretation exercises, practice tasks, key takeaways,
and next-part narrative. Repetitive copy/setup steps were adapted to opening the generated workbook,
with the original Google workbook retained as provenance and a manual Copy to workflow preserved.
Cell-entry instructions became Label/Enter actions; preseeded conflicting template labels use Replace.
Alternative methods here use different destination columns, so no competing destination branches are
necessary. Headings retain their original standalone part numbers. Worksheet names are valid XLSX
names without the original colon punctuation.

All nonempty cells of each corresponding original XLSX sheet were compared, by original row/column
address and value, against the compiled Markdown model. Exact dictionaries match, including multiline
headers, numeric observations, incomplete early-year columns, existing template labels, and the dot
separator at G1 on the ANOVA template. Styled-only rows through 100/101 were not authored as data.
Only rows 1 through 25 are seeded. The formula ranges deliberately extend through 101 for practice,
and the tutorial explicitly explains that blank capacity is not an observation.

There are 24 observations in the 2024 one-sample data and each of the two-year comparison columns.
ANOVA sample sizes are 10, 15, 20, 24, 24 for 1994, 2004, 2009, 2014, 2024. Crucially, the ANOVA
2014 series differs from the two-year workbook's 2014 series. Both original datasets remain unchanged;
the ANOVA source warns against silently substituting one for the other.

## Scientific corrections

- Align the initial Z-test scenario alternative with its planned lower-tail question; keep the
  separately explained two-sided and upper-sided comparisons for teaching.
- Identify 4.0 and the Z-test population SD 0.6 as stipulated teaching values, not independently
  established Busse Woods population parameters. Shannon index has no universal 1.5-to-4.5 bound.
- Correct the Z-test explanation of the normal CDF versus upper tail, weight/index copy error,
  and stale D13 alpha references (actual alpha is D14).
- Correct one-sample t CDF cumulative argument description from FALSE to TRUE; avoid claiming
  T.TEST is a one-sample benchmark function. Upper-tail complements/symmetry allow negative t.
- Use T.TEST type 3 to match Welch formulas, rather than original type 2 equal variance.
  Explain that the signed statistic is 2024 minus 2014 and use sign-aware directional IF formulas.
- Keep Welch example calculations; their six rounded degrees-of-freedom examples were independently
  checked. Replace misleading pooled-DF wording with approximate Welch DF.
- Use F ratio 2024 variance / 2014 variance, with numerator DF E14 and denominator DF E13.
  Correct two-tailed F p-value to twice the smaller tail capped at one. Preserve reciprocal-ratio
  comparison with the corresponding swapped DF. Directional F.TEST cross-check chooses the half
  or its complement using the actual CDF rather than assuming the observed direction.
- Correct F-distribution asymptotic wording: it concentrates around one, rather than simply
  becoming a normal distribution. Distinguish a p-value calculation from the F-statistic.
- Preserve the original ANOVA sum-of-squares decomposition with unequal group sizes; use bounded
  data ranges rather than whole columns, correct I10 to I11 grand mean, and M3 to M2 p-value.
- Explain independent sampling assumptions for the two-year methods despite identical site names.
  If they are matched repeated measurements, an independence-based test is not justified.
- Add normality/common-variance assumptions for classical F/ANOVA, warning about F-test sensitivity.
  Lower variance of Shannon values does not establish taxonomic homogenization.
- Explain that a p-value conditions on the null model, that failure to reject does not establish
  equivalence, and that these comparisons alone establish neither causality nor a time trend.
- Preserve the culture/plate/staining narrative while explaining identification limits and
  method-confounding when culture-based and sequencing diversity measures are compared.

Primary references checked for the corrections:
[Google T.TEST](https://support.google.com/docs/answer/6055837?hl=en),
[Google T.DIST](https://support.google.com/docs/answer/9369014?hl=en),
[Google T.DIST.2T](https://support.google.com/docs/answer/9368252?hl=en),
[Google F.DIST](https://support.google.com/docs/answer/6055706?hl=en), and
[NIST F-test](https://www.itl.nist.gov/div898/handbook/eda/section3/eda359.htm).
Google's T.DIST documentation opening description conflicts with its own CDF examples; the
cumulative argument and worked examples support the left-CDF interpretation used here.

## Verification

Commands used (all Python invocations follow the required environment bootstrap):

```bash
source source_me.sh && python3 make_tutorial.py lint tutorial_data/microbes_1_z_test.md
source source_me.sh && python3 make_tutorial.py build tutorial_data/microbes_1_z_test.md --format docx,xlsx --output-dir output_microbes/microbes_1_z_test
```

The same build command was run successfully for all five basenames. Generated DOCX/XLSX bundles
are under the ignored output_microbes directory. A direct compile_document loop verified zero
semantic errors in all five files. A source-workbook versus compiled-seed dictionary assertion
passed for every nonempty cell in all five tutorials.

A separate NumPy/SciPy calculation used original XLSX numeric observations, independently of the
spreadsheet formula implementation. It checked mean/sample variance/count, Z/one-sample t/Welch
statistics and tails, the variance-ratio tails, and all ANOVA intermediate quantities. It also
swapped two-year arrays to test the opposite sign/direction logic. A 93-output oracle was supplied
at /tmp/sheets_expectations_microbes.json to the spreadsheet-validation workstream for integration.

| Outcome | Independent numerical result |
| --- | --- |
| 2024 mean | 3.7969166666666667 |
| 2024 sample SD | 0.900872375107531 |
| Z statistic | -1.6581684731007231 |
| Z lower p | 0.048641733142320315 |
| One-sample t | -1.1043751716126042 |
| One-sample t lower p | 0.14042528409399224 |
| Welch t | -1.914518063545092 |
| Welch DF | 39.49523704154586 |
| Welch lower p | 0.03140902938960033 |
| Variance F ratio | 0.42264785040073066 |
| F lower p | 0.022066402601674674 |
| ANOVA grand mean | 4.142440860215054 |
| ANOVA DF between / within / total | 4 / 88 / 92 |
| ANOVA SS between / within | 4.739368541397847 / 118.62880838333331 |
| ANOVA F | 0.8789273813982056 |
| ANOVA right-tail p | 0.47999149550466147 |

These outcomes are report-only verification evidence, not prefilled student workbook answers.

## Remaining review and limitations

The parent requested a fresh independent content correction pass after freeze. Its reviewer has
flagged an empty upper-tail explanatory fragment in the Z-test source and malformed F-test prose;
those findings are intentionally handed off, not edited concurrently with the next reviewer.
The initial migration should not be described as final editorial acceptance until that pass ends.

Current lint advisories concern deliberate spare-range blanks/overshoot, forward references in
explanatory prose and free-response destinations, missing Google tab mappings, and unverified
SUMPRODUCT compatibility. All actual local image references resolve. Spreadsheet URLs lack gid,
so no cell-tab mapping was invented. The independent oracle uses real-valued Welch DF; spreadsheet
engines may differ in fractional-DF handling and live discrepancies need explicit reporting.
No Google import/calculation/navigation, PDF visual inspection, or browser execution is claimed by
this migration workstream. No original 2025 artifact was changed by this workstream.


## Post-freeze content corrections

Restored the Z-test upper-tail explanation: the complement of the standard-normal CDF gives the
higher-tail p-value. Corrected the supervisor email and its two follow-up paragraphs to explain
that estimating an unknown population standard deviation motivates the t-test. Small sample size
alone does not invalidate a Z-test with known population SD and a normal model. Independence,
normality, and outlier cautions remain explicit. This distinction follows the primary
[NIST one-sample mean guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc22.htm),
checked on 2026-10-22. Repaired the broken F.DIST sentence to explain its lower-tail CDF and the
need for the subsequent tail calculations. No data or formulas changed.

Validation: `source source_me.sh && python3 make_tutorial.py lint tutorial_data/microbes_1_z_test.md` and
`source source_me.sh && python3 make_tutorial.py lint tutorial_data/microbes_4_f_test.md` each passed with
zero errors. Existing spare-range, free-response, and forward-reference warnings remain. Reviewed
the changed source paragraphs for complete sentences and balanced inline formatting. Final PDF
rebuild and visual verification belong to the render-validation workstream.
