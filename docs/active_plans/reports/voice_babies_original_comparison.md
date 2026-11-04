# Babies original-voice comparison

## Finding

The three current lessons retain their scenarios, datasets, core analysis sequence, humor beats, and
most source explanations. They do not retain the original instructional voice consistently. In all
three, the source's numbered actions and explanatory sentences were transformed into repeated
`Label`, `Enter`, `Inspect`, `Method`, and `Instruction` list entries. PDF extraction confirms these
labels are visible to students; this is not just a source-authoring detail. The resulting workbook
transcription reads like an operation log and fragments the source's natural numbered groups.
Restore the original sentence-led numbered groups and explanation paragraphs, adapting only the
cell names, ranges, dataset facts, formulas, and verified scientific errors.

Evidence reviewed: all three Fall 2025 Markdown originals, the three original DOCX and PDFs, all
three current Markdown sources and PDFs, and all three current XLSX workbooks. The national XLSX
files each have separate data and working sheets; the two-sample file has one combined sheet. The
2025 DOCX/PDFs corroborate the same authorship, story, explanations, and list grouping;
the Fall 2025 Markdown files are the most precise paragraph anchors. The z and one-sample t originals
also have an additional `Fried_Foods_2_T-Test_Tutorial_Guide.md` copy; its opening is truncated, so
use the complete Fall 2025 file for paragraph restoration.

## Restore these source passages and groupings

### National z-test

In [the original z guide](../../../2025_Artifacts/Fried_Foods_1_Z-Test_Tutorial_Guide_Fall_2025.md),
restore the explanatory paragraph at lines 7 and 51, the scene-setting and tutorial cadence in
`Part 1 Scenario` (lines 9-15), and the explanatory prose beneath Steps 2-5 and 7 (lines 34, 51,
71-75, 79, 95, 119-127, 131-133). Keep the source's `Step 1` through `Step 7`, `Practice Task`,
`Key Takeaways`, and `Part 2 Setup` hierarchy; a separate `Workbook` section and explicit
`Part 1: National z-test` part are warranted by the standalone generated workbook, but do not replace
the original lesson headings or number-group structure.

At current [babies_1_z_test.md](../../../tutorial_data/babies/babies_1_z_test.md):

- Lines 125-165 replace the original nine-item population setup and six-item sample-values steps
  with a `Label`/`Enter` log and nested `Method`/`Instruction` labels. Restore the original numbered
  items and complete explanatory sentences. Keep the correction `Population parameter` for the
  source's `Population statistic`; correct the source's sample-mean typo in the STDEV explanation;
  retain `STDEV.S` and the current D/E references.
- Lines 169-180 add `Instruction` labels to formula/explanation text that was already naturally
  written. Preserve the original Z-statistic note in its original paragraph form. The source's
  `standard deviations away` is a genuine technical error: the statistic standardizes the sample
  mean by its standard error. Keep that correction.
- Lines 203-215 and 225-253 fragment source list steps and explanation paragraphs with labels.
  Restore numbered substeps for the two p-value branches and numbered decision/interpretation
  entries. The supported `NORM.DIST` formula, explicit right-tail label, and sign behavior may stay.
- Lines 257-272 turn the source's three unnumbered practice bullets and three numbered takeaways
  into `Instruction` and bold-label bullets. Restore the source grouping and wording, changing only
  ranges/function references if needed.
- Lines 274-288 retell the comic opener and committee letter. Keep the revised scientific reason
  (unknown population SD calls for estimating variability; n<30 alone does not invalidate z), and
  keep the correction that the data do not support Joe's claimed victory. Restore source scene
  beats/phrasing where compatible: `Joe was ecstatic...`, the stern letter, and the protest scene.
  Do not restore the false assertion in the original letter that fewer than 30 automatically makes
  a z-test invalid, or a false significance claim.

Source setup used copied tabs from a combined instructor workbook; the current student XLSX is a
separate standalone tutorial workbook and contains its own data. Upload/open/copy/rename is therefore
a legitimate workflow adaptation. Keeping the source's playful copy exercise as an optional reset is
also reasonable. The added tab inventory and historical-template note are factual bridge text, not
author voice to preserve.

### National one-sample t-test

In [the original one-sample t guide](../../../2025_Artifacts/Fried_Foods_2_T-Test_Tutorial_Guide_Fall_2025.md),
restore the original opening explanation at lines 7-8 from the corroborating DOCX, the paired
committee-issues list and scenario paragraphs under `The New Challenge` and `The New Scenario`
(lines 11-25), numbered Steps 1-10, explanatory `Why Do We Use Degrees of Freedom?`, substeps 8.1-8.3,
and the grouped practice/takeaways/`Joe's Redemption` story (lines 27-150). These contain much of the
lesson's personality and statistical scaffolding. Source exact opening DOCX wording begins: "A
T-test is a statistical test used when you want to know if the average of your sample is meaningfully
different from a known value, but you cannot assume the population standard deviation is known."

At current [babies_2_t_test.md](../../../tutorial_data/babies/babies_2_t_test.md):

- Lines 103-129 convert the original paired issue list and narrative into `Instruction` bullets and
  append standalone hypothesis prose. Restore the source paragraphs/list grouping and wording; retain
  the correction that a small sample alone does not invalidate z, the explicit assumptions, and the
  prespecified right-tail claim.
- Lines 143-168 replace the original eleven-item setup with the repeated action labels. Preserve the
  source numbering and parent/child sequence, including the warm aside "^ this is our representative
  mean baby weight of the population." Adapt the old "Return to your spreadsheet" operation to
  opening this separately generated workbook; the self-contained workbook plus optional data-copy
  reset is a valid product change.
- Lines 173-218 split the source's concise formula steps and degree-of-freedom explanation into
  label/enter pairs and short bold-led fragments. Restore the source's Step 3-7 grouping and its
  explanatory prose. Correct only the source's mistaken P-value cell references (`D5`/`D6` should be
  the t statistic/df cells `E9`/`E10`) and explain that `T.DIST.RT` expects a signed statistic, so
  the right-tail result must remain correct for a negative t value.
- Lines 224-260 fragment source 8.1-8.3 into nested action logs. Restore those numbered substeps
  and prose. Retain the important qualification that doubling a one-tail p-value only applies when
  the observed statistic points in the prespecified direction; keep the `ABS` two-tail calculation
  and explicit right-tail direction.
- Lines 275-310 convert decision, interpretation, practice, and takeaway blocks to repetitive
  labels. Restore the source's paired numbered decision entries, narrative interpretation direction,
  three practice bullets and three takeaways. Lines 311-324 rewrite the redemption ending; preserve
  only the data-supported conclusion that Joe does not reject the null. The original "T-test shows
  ... significantly larger"/reinstatement is unsupported and should remain corrected.

### Two-sample t-test

In [the original two-sample guide](../../../2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial_Fall_2025.md),
restore the original headings `Part 3: Two-Sample T-Test Scenario`, `Step 0`-`Step 8`, and
`6.1`/`6.2` hierarchy; restore the voice in the two scenario paragraphs (lines 7-13), Step 0's
three numbered reasons (17-19), the explanatory hypothesis paragraphs (64-75), the function
walkthrough (77-99), notes (100-103), and interpretation example (120-127).
The original is already numbered and explanatory; current introductory `Before calculating
summaries` content is a legitimate teaching improvement, but its timing-specific placement may be
retained under the original Step 6 hypothesis-selection subsection.

At current [babies_3_two_sample_t_test.md](../../../tutorial_data/babies/babies_3_two_sample_t_test.md):

- Lines 60-68 reduce the three numbered Step 0 reasons to label bullets and add qualifications.
  Restore the original numbered group, retaining the clarifications about independence, small-sample
  assumptions, Welch unequal variance, and infant numbers not indicating paired observations.
- Lines 72-78 are legitimate standalone-workbook steps and data/range bridge text, but leave them as
  short setup steps, not as a pattern to impose on the rest of the lesson.
- Lines 93-113 translate the original cell instruction sequences into terse `Label`/`Enter` pairs.
  Restore original numbered actions with the current F:H cells and row ranges.
- Lines 117-138 rewrite and compress the original nested 6.1/6.2 hypothesis/function walkthrough.
  Restore the authored explanation and hierarchy while preserving necessary fixes: `T.TEST` type 3
  (Welch), valid B2:B101/C2:C101 ranges, and the signed directional guard because Sheets' one-tailed
  T.TEST uses the magnitude and does not encode Joe-greater from range order. Keep the improved
  preselection instruction before summary work; the source currently makes students inspect group
  means first, then choose a tail, which risks post-hoc choice.
- Lines 150-160 add a "Preview" substep and convert the duplicated decision directions to a single
  action. Keep that actual de-duplication: original 6.3 and 7 repeat F6/G6 and the decision formula.
  Reattach the preview naturally to the original Step 6 instead of creating a new pseudo-step.
- Lines 164-176 fragment interpretation/example text and append appropriate limits. Restore the
  original numbered F8/G8 action and example paragraph; retain the evidence-based explanation and
  no-causality limits.
- The scenario at current lines 53-56 changes Joe from "feeling confident after reinstating his
  eligibility" to hoping to reinstate it. That is required because the previous supplied-data result
  is not significant. Keep the story beat and voice around that factual correction.

## Change boundary

Keep standalone XLSX setup, workbook/table inventory, updated sheet names, retained blank practice
ranges, exact formulas, corrected cell references, and concise references needed to explain source
differences. These details connect the original learning experience to the actual generated
workbooks. Do not expand them into a complete workbook transcription before each tutorial or repeat
every action as a bold action label. Preserve the original heading specificity, paragraph wording,
numbered groups, substep nesting, jokes, and explanations verbatim wherever the workbook conversion
does not make a statement false or confusing. Existing source typos and formatting quirks are not
themselves a mandate for prose rewrites; fix a typo only when it obstructs understanding or touches a
corrected scientific statement.
