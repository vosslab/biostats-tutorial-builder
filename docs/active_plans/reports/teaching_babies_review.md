# Babies tutorials teaching review

## Scope and evidence

This review compared all three editable sources in `tutorial_data/` with the matching 2025 Fried
Foods Markdown, DOCX, and PDF artifacts. I read the generated DOCX files, extracted text from the
generated and source PDFs, and rendered every generated PDF page for visual inspection. I also
inspected the actual generated XLSX cell contents and tab names. The source and generated PDFs have
these page counts: Z test, 6 and 6; one-sample t test, 5 and 6; two-sample t test, 4 and 4.

The generated workbook data match the lesson instructions: the national-test workbooks contain 24
weights in rows 2-25 on both tabs; the two-sample workbook contains 24 observations in each group
in rows 2-25. Calculation areas are blank for student entry, apart from the provided D1/E1 headers
in the national-test sheets and `E3 = not used` in the t-test sheet. The two-sample statistical
area is blank. Therefore the prescribed cell-entry sequence can be followed against the starting
files.

## Z test: national average

The original [Fried Foods Z-Test guide](../../../2025_Artifacts/Fried_Foods_1_Z-Test_Tutorial_Guide_Fall_2025.md),
[DOCX](../../../2025_Artifacts/Fried_Foods_1_Z-Test_Tutorial_Guide.docx), and [PDF](../../../2025_Artifacts/Fried_Foods_1_Z-Test_Tutorial_Guide.pdf)
teach setup, population values, sample summaries, the Z statistic, both tail choices, decisions,
interpretation, practice, and the transition to the t-test. Those parts fall on source PDF pp. 1,
2, 3, 4, 5, and 6 respectively. The generated [babies_1_z_test source](../../../tutorial_data/babies/babies_1_z_test.md)
preserves that sequence and the 24 observations. It retains the normal-curve figure, practice
prompts, and Joe's comic award story. Generated `tutorial_output/babies_1_z_test/babies_1_z_test.pdf`
pp. 1-6 and `tutorial_output/babies_1_z_test/babies_1_z_test.docx` carry the same
instructional content: the opener/scenario is p. 1, setup/population values p. 2, sample values/Z
statistic p. 3, p-values/decisions p. 4, interpretation/practice/story start p. 5, and story finish
p. 6.

The old Z guide's instructional screenshots (source PDF pp. 2-3) show the former instructor
Google Sheet, including its three-tab layout and copy/paste setup. They are absent from the new
lesson, whose generated workbook has different tabs and already contains the working data. The
cell-by-cell prose and expected-values table replace those stale screenshots; this is a reasonable
fidelity choice, though a new screenshot of the generated workbook could help students recognize
the tabs. The normal-curve image and protest illustration remain. The story's criticism of using
fewer than 30 observations as a categorical reason to reject a Z test is rewritten around the
unknown population standard deviation and small-sample assumptions, preserving the plot while
correcting its statistical lesson.

The new opener (generated p. 1) gives students the known-sigma condition and appropriately cautions
that a small sample needs an approximately normal population. The setup (generated p. 2) updates
the old three-tab directions to the generated two-tab workbook and gives a safe reset operation.
Students can proceed in order: D2/E2 and D3/E3; D5/E5, D6/E6, D7/E7; D9/E9; choose D11/E11 or
D12/E12; D14/E14 and E16/E17; then write E19. Formula ranges match the workbook's data in B2:B25
and its stated extension space through B40. The step-by-step cell labels, formulas, tail labels,
and decision formulas survive. The original incorrectly implied that fewer than 30 observations
alone made a Z test unsuitable; the generated copy corrects that reasoning.

**Low severity: the tail choice is stated but not operationally gated.** The scenario names Joe's
right-tailed claim, then offers a two-tailed comparison and tells students to choose before seeing
results. Yet the guide proceeds to calculate both p-values and both decisions, and the sample data
are already in the workbook. A novice can read this as permission to choose whichever result looks
better. Keep both formulas as practice, but explicitly say which alternative is the assigned
reporting choice, and tell students to record their choice before looking at either p-value; if
students may choose, require them to report only the preselected branch. Generated pp. 1 and 4-5.

**Low severity: a sentence is split across a page turn.** On generated p. 5, the award letter ends
mid-sentence at "variation in hospital"; p. 6 begins with "practices and diets." Keep that short
paragraph together or move the letter to the next page. The rest of the PDF is readable, and the
normal curve and closing illustration remain visible. Generated pp. 5-6.

## One-sample t test: national average

The original [Fried Foods t-Test guide](../../../2025_Artifacts/Fried_Foods_2_T-Test_Tutorial_Guide_Fall_2025.md),
[DOCX](../../../2025_Artifacts/Fried_Foods_2_T-Test_Tutorial_Guide.docx), and [PDF](../../../2025_Artifacts/Fried_Foods_2_T-Test_Tutorial_Guide.pdf)
cover the changed assumption, setup, sample size/mean/SD, t statistic, degrees of freedom,
tail-specific p-values, decision, interpretation, practice, and Joe's redemption ending. In the
source PDF, these run from scenario/setup on p. 1, through setup/sample size on p. 2, summaries and
degrees of freedom on p. 3, tail choices and p-values on p. 4, and decisions/practice/conclusion on
p. 5. The generated [babies_2_t_test source](../../../tutorial_data/babies/babies_2_t_test.md) preserves
these topics, all 24 data values, the national benchmark, and the story voice. It adds explicit
null and alternative statements, cautions about independence/normality/outliers, and correctly
states that sample size alone does not invalidate a Z test. These are useful corrections to the
original. Generated `tutorial_output/babies_2_t_test/babies_2_t_test.pdf` pp. 1-6
and `tutorial_output/babies_2_t_test/babies_2_t_test.docx` carry the lesson: opener
and scenario p. 1, setup/summary calculations pp. 2-3, degrees-of-freedom/p-value work pp. 4-5,
and takeaways/story p. 6.

The original t-test's second figure (source PDF p. 2) is a screenshot of the old workbook's
population-value table. The generated lesson replaces it with an editable cell/contents table that
matches the new XLSX. That preserves the instructional information and is easier to reuse. The
award-story voice remains, but its ending changes: the original claims significance and reinstatement;
the generated lesson reports the calculated right-tail p of about 0.154 and Joe's failure to reject.
That change is warranted by the supplied data. The cover art remains; the source has no separate
t-distribution figure to preserve.

The actual workbook has `Datas for Part 1 and 2` and `Part 2 National T-Test`, with the supplied
`E3 = not used`. Students can follow the stated order: D2/E2, inspect D3/E3; D5/E5, D6/E6, D7/E7;
D9/E9; D10/E10; choose D12/E12 or D13/E13; D15/E15 and E17/E18; then write E20. The formulas use
B2:B101, and all data are initially in B2:B25. The generated PDF's formulas and labels agree with
the starting workbook and no step depends on a value that students were not first asked to enter.

**Low severity: the optional workbook-copy path is underspecified.** Step 2 says students may copy
the two generated tabs into their Part 1 workbook, but gives no steps for copying tabs. The main
path, opening the generated XLSX and making a copy, is complete. Either remove the side path or
identify the exact tab-copy operation and destination. Generated p. 2.

**Low severity: the tail branch needs the same explicit reporting instruction as Part 1.** The
scenario states both alternatives and the p-value cells are clearly labeled, including the right
tail. It also calculates both p-values and both decisions. Tell students to preselect one alternative
and report only its result so the two available outputs are not treated as post hoc choices.
Generated pp. 1-2 and 4-5.

Visually, the cover figure and closing section are intact. Page turns split a list item and the
setup step (pp. 1-3), the nested p-value explanation (pp. 4-5), and the last practice bullet from
the rest of the practice task (pp. 5-6). The text remains readable, but keeping those units together
would make a first-time walk-through easier. These are layout refinements, not missing content.

## Two-sample t test: hospitals

The original [Fried Foods two-sample guide](../../../2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial_Fall_2025.md),
[DOCX](../../../2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial.docx), and [PDF](../../../2025_Artifacts/Fried_Foods_3_Two-Sample_T-Test_Tutorial.pdf)
move from the prior one-sample scenario through two-group summaries, hypothesis choice, `T.TEST`,
decision, and interpretation. In the source PDF, the scenario/setup are on p. 1, summaries and the
start of hypothesis choice on p. 2, remaining hypotheses and p-value work on p. 3, and decision /
interpretation on p. 4. The generated
[babies_3_two_sample_t_test source](../../../tutorial_data/babies/babies_3_two_sample_t_test.md) keeps
that sequence and story setup, plus all 24 values for both groups. Generated PDF pages 1-4 retain
the introduction/setup, summaries/hypotheses, p-value work, and decision/interpretation respectively;
the `tutorial_output/babies_3_two_sample_t_test/babies_3_two_sample_t_test.pdf` and
`tutorial_output/babies_3_two_sample_t_test/babies_3_two_sample_t_test.docx` contain
the same lesson text. The actual XLSX has one sheet, `Fried Foods vs Green Veggies`, with the data
in A1:C25 and an empty F:H calculation area as the instructions expect.

Neither the original nor generated two-sample lesson includes figures. Both preserve the playful
Joe/Alex rivalry. The generated version changes Joe from having already regained the award to
hoping to regain it, which fits the calculation outcome and keeps the story moving without claiming
an unsupported win.

The cell sequence is coherent: F1:H1 headers; F2 and G2/H2 means; F3 and G3/H3 sample SDs; F4 and
G4/H4 sizes; then choose the alternative and enter the corresponding p-value formula in G5; enter
F6/G6 alpha, F7/G7 decision, and F8/G8 interpretation. Both branches are described. The generated
two-tailed formula uses type 3 (Welch unequal-variance); the one-tailed formula adjusts for which
group mean is larger so it returns the right-tail probability for Joe-greater, including p > 0.5
when the observed means point in the other direction. This repairs the source's incorrect claim
that type 2 is Welch and its use of type 2 in the worked test. The current workbook data give Joe
mean 8.058 lb, Green Veggies mean 7.657 lb, and Welch two-tailed p about 0.244; the right-tail p
for Joe greater is about 0.122. These agree with the prose's intended interpretation and support
the directional adjustment.

**Medium severity: students are asked to choose a tail after calculating and seeing both means.**
Step 6.1 appears after steps 3-5 have students calculate both means and standard deviations from
the visible data. Later prose says to choose the alternative before examining data. This conflicts
with the actual order and can teach students to pick direction after seeing which group is higher.
Move the hypothesis-selection prompt before the workbook summary steps, or clearly require students
to state and record the alternative before opening/viewing the data. Keep both supported branches:
two-tailed difference with `=T.TEST(B2:B101, C2:C101, 2, 3)` and right-tailed Joe-greater with the
provided sign-adjusted formula. Generated pp. 1-3; the same order appears in the DOCX.

**Low severity: the source's duplicated decision directions were simplified successfully.** The
2025 guide repeats the significance-level and IF-decision cells in both Steps 6.3 and 7. The
generated guide names the planned decision in 6.3, then enters it once in Step 7. This removes
redundancy without omitting a needed workbook action. Generated p. 4.

Generated PDF pp. 1-4 are visually clean and readable; p. 4 has open space after the short final
interpretation, which is acceptable for this brief lesson. The p-value formula on p. 3 wraps across
several lines but remains legible.

## Overall assessment

All three generated lessons retain their essential workflow and practice activities, and the
starting XLSX files match the cell references in the prose. The major teaching improvements are
the repaired sample-size explanation in the one-sample t lesson, clearer tail and hypothesis
language, and the corrected Welch test and directional one-tail formula in the two-sample lesson.
The main follow-up should address preselecting/reporting the tail, especially moving that choice
before students calculate the two-sample summaries. Remaining findings concern minor alternate-path
and page-break clarity; no missing calculation step or data mismatch was found.

The existing 2025 DOCX/PDF artifacts corroborate the original lesson content and page sequence. I
did not modify any source, workbook, or generated product file and did not launch LibreOffice.
