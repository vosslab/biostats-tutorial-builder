# Microbes 1-3 voice restoration

## Result

The three tutorial openings again follow the Fall 2025 narrative: Busse Woods and the Shannon Index
establish the first question, Part 2 explains why the unknown population SD calls for a t-test, and
Part 3 returns to the advisor's suggestion to compare 2014 with 2024. Original tutorial titles and
the descriptive **Why Use a T-Test Now?** and **Why Use a Two Sample T-Test Now?** headings are
restored. Spreadsheet directions use numbered prose with semantic cell links around their original
visible values and formulas.

The restored student story remains a teaching scenario. Statistical outcomes are stated as evidence
about population means under the working model, not proof of urbanization, climate change, or another
environmental cause.

## Source-specific restorations and exceptions

| Lesson | Restored original material | Necessary exception or correction |
| --- | --- | --- |
| [Microbes 1 Z-test](../../../tutorial_data/microbes/microbes_1_z_test.md) | The Fall 2025 opening about Busse Woods, soil samples, SSU rRNA sequencing, the Shannon Index, and the reason for the Z-test (original lines 7-13). The original title and student-facing spreadsheet setup cadence are retained. | The 4.0 value is called a **stipulated benchmark**; the original's claim that it represents an established average for similar ecosystems is not verified by the supplied artifacts. The known SD of 0.6 is stipulated for this exercise. The two-tail and higher-tail comparisons are stated alongside the actual lower-tail research question. Shannon Index descriptions retain richness and evenness but omit the unsupported typical range of 1.5-4.5. Urbanization remains a motivating hypothesis, not a demonstrated cause. |
| [Microbes 2 one-sample t-test](../../../tutorial_data/microbes/microbes_2_t_test.md) | The "more realistic challenge" opening, the two spreadsheet goals, and the **Why Use a T-Test Now?** explanation follow original lines 7-21. The narrative now distinguishes this Part 2 estimate from Part 1's stipulated known SD. | The original says the t-test is specifically for small samples and provides a more accurate result. The restored explanation instead identifies the relevant reason: the population SD is unknown and estimated from the sample, adding uncertainty. It does not claim this makes a small sample representative. The lower-tail alternative remains the main question; neither test is treated as evidence of environmental cause. |
| [Microbes 3 two-sample t-test](../../../tutorial_data/microbes/microbes_3_two_sample_t_test.md) | The original transition from the benchmark result to the advisor's 2014-vs-2024 suggestion and **Why Use a Two Sample T-Test Now?** heading follow original lines 7-13. | The source's repeated 24 location names are disclosed. Independence is a hypothetical exercise assumption because the source cannot establish whether the named observations are independent or repeated site measurements. If matched sites are repeated, a paired mean method is needed; the later variance exercise also cannot treat the classical independent F-test as a paired variance test. Welch's unequal-variance method is used for the hypothetical independent-samples exercise. The original causal wording is qualified, and the lower-tail conclusion is limited to the model. |

## Workbook directions

The originals ask students to create worksheets and copy tabs from a Google workbook. The current
canonical sources provide a generated XLSX with the observations already present, so those actions
were updated to opening that workbook in Google Sheets and inspecting its named worksheet. Calculation
rows remain student work; no answers were added to preseeded result cells. Existing data, formulas,
cell coordinates, alternate calculations, and interpretation locations were preserved.

Action annotations were converted from repeated `Label` and `Enter` bullets to ordered student
directions such as `In cell C2, type [Population Mean](label:C2)` and `In cell D2, enter
[4.0](enter:D2)`. The visible words and formulas are the authored lesson text; semantic links carry
the cell operation. The current sample-size and formula ranges remain 2:101 to allow later practice,
while the original 24 observations occupy rows 2:25.
