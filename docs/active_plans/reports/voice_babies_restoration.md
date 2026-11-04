# Babies instructional voice restoration

## Finding

The three Babies sources now follow the Fall 2025 lessons' sentence-led instructions, descriptive
section titles, numbered groups, humor, and story beats. Semantic links attach workbook operations to
the visible original instructions. Generated workbook data, cell addresses, formulas, and statistical
outcomes remain in their existing locations.

The wording comparison uses the read-only [Fall 2025 z-test guide](../../../2025_Artifacts/Fried_Foods_1_Z-Test_Tutorial_Guide_Fall_2025.md),
[Fall 2025 one-sample t-test guide](../../../2025_Artifacts/Fried_Foods_2_T-Test_Tutorial_Guide_Fall_2025.md),
and [Fall 2025 two-sample t-test guide](../../../2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial_Fall_2025.md),
with the original DOCX files as corroboration. The current source and the
[original-to-current comparison report](voice_babies_original_comparison.md) were also checked. No
original 2025 artifact was changed.

## Restored content

### National z-test

In [babies_1_z_test.md](../../../tutorial_data/babies/babies_1_z_test.md), the source's scenario, population
and sample explanations, numbered setup and calculation instructions, Z-statistic note, 5.1/5.2
p-value grouping, decision explanation, interpretation examples, practice bullets, numbered
takeaways, and Joe's committee scene are restored. The standalone workbook instructions describe
opening its generated file and its supplied sheets; copying the data is retained as an optional
reset. The committee still sends Joe a stern letter, and the protest scene and signs remain.

Scientific exceptions retained: the population description says **parameter** rather than
**statistic**; the sample standard deviation uses `STDEV.S` and the source's mean/standard-deviation
mix-up is corrected; the Z statistic is described as the sample mean's distance from the null mean
in standard errors. The tutorial states that a z-test requires known population SD, while a sample
size below 30 is not a magic invalidity cutoff. The right-tailed alternative is recorded before
examining results, and the prose does not treat a higher sample mean as significant evidence.

### National one-sample t-test

In [babies_2_t_test.md](../../../tutorial_data/babies/babies_2_t_test.md), the original t-test opening,
committee issues, scenario, numbered setup and Steps 1-10, degrees-of-freedom explanation, p-value
substeps, decision pair, interpretation, three practice bullets, three takeaways, and redemption
ending are restored. The parenthetical population-mean aside is nested under its original numbered
entry. Workbook setup describes the standalone XLSX and keeps the source's copy action as an
optional reset.

Scientific exceptions retained: small sample size alone does not invalidate a z-test; independence,
approximate normality, and influential outliers matter for the small-sample model. The hypothesis is
chosen before calculating p-values, and the fictional 7.5 lb value is identified as a teaching
benchmark. The source's right-tail formula references the signed t statistic and its degrees of
freedom (`E9` and `E10`), not the source's mistaken `D5`/`D6`. The formula therefore returns a
right-tail p-value above 0.5 when the statistic is negative; doubling a one-tail p-value is
qualified by the statistic's direction. With the supplied observations, the one-tailed p-value is
about 0.154, so the committee does not reinstate Joe's eligibility. The original humility and
fried-food-awards joke remain around that corrected outcome.

### Two-sample t-test

In [babies_3_two_sample_t_test.md](../../../tutorial_data/babies/babies_3_two_sample_t_test.md), the two
original scenario paragraphs, Step 0's three reasons, setup/calculation sequence, hypothesis
explanation, `T.TEST` walkthrough, important notes, and interpretation example are restored. The
corrected story says Joe hopes to regain eligibility; it does not claim he has already been
reinstated. A short preselection instruction stays before the summaries to prevent choosing a test
after seeing the group means.

Scientific exceptions retained: the groups are independent despite matching infant identifiers;
the small sample calls for attention to independence, approximate normality, and outliers. `T.TEST`
uses Welch type 3 and the current `B2:B101`/`C2:C101` ranges. Google Sheets' one-tail result uses
the absolute statistic, so the Joe-greater formula includes a signed mean-difference guard. The
source's duplicated decision block is consolidated into one decision formula. The two-tailed
alternative formula remains visible in its alternative branch; only the prespecified Joe-greater
formula writes to `G5` in its branch. Each branch contains one formula action.

## Workbook bindings and regions

The three sources contain 64 semantic operations: 32 label operations and 32 enter operations. Of
the enters, 26 assign formulas and 6 assign scalar values. The two-tail and right-tail `G5` formulas
are in explicit alternative branches, so they do not conflict. The workbook headers `D1:E1` in
Babies 1 and 2 and `F1:H1` in Babies 3 are seeded from the source instructions; no formula answers
are seeded and the already supplied header labels have no re-entry operation.

Each seeded data range has a `source` role. Babies 1 and 2 declare their matching `A1:B25` source
regions on both sheets; each working sheet declares disjoint calculation, results, and interpretation
regions. Babies 3 declares `A1:C25` as source, `F1:H4` as calculation, `F5:G7` as results, and
`F8:G8` as interpretation. All three workbook roles are disjoint within each worksheet.

## Validation status

All three sources pass offline compiler lint after the shared compiler fix for emphasized text inside
semantic links. Lint reports the intended practice-range extensions through row 40 or 101 because
the supplied tables contain 24 observations, and notes the absence of optional Google cell mappings.
No LibreOffice build or output review was performed here; those remain integration work.
