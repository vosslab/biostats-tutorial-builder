# PETase source fidelity recovery

Compared the actual paragraphs in
[the Fall 2025 source](../../../2025_Artifacts/PETase_1_Linear_Regression_Tutorial_Fall_2025.md)
with [the current lesson](../../../tutorial_data/petase/petase_1_linear_regression.md).
Earlier restoration summaries did not establish prose fidelity: the current opening had still
shortened the engineering, purification, Bradford, and regression explanations. This pass restores
that wording, including the fictional startup's mutant activity, strain designs, and fermentation
premise.

## Original prose reconciliation

The useful original introduction ends after **Why Use Linear Regression Now?**, source line 46.
Its 14 prose blocks include the three-strain list as one block. After decoding HTML entities and
normalizing whitespace, 11 blocks are verbatim. Three blocks contain only these exceptions:

| Original wording | Current wording | Reason |
| --- | --- | --- |
| "In other words, your regression model will turn blue color in a cuvette into hard numbers that tell the startup which yeast strain is actually producing the most PETase per fermentation batch." | "In other words, your regression model will turn blue color in a cuvette into hard numbers that tell the startup how much BSA-equivalent total protein was recovered in each preparation." | Bradford measurements of partially purified samples measure total protein; they cannot establish PETase-specific production. The surrounding assay assignment remains verbatim. |
| "Since you do not know their concentrations, you use the **standard curve** from the BSA series to infer them. In the next section" | "Since you do not know their concentrations, you use the **standard curve** from the BSA series to infer them. Different proteins can produce different dye responses, so these estimates are BSA-equivalent total protein concentrations. In the next section" | Adds one sentence identifying the calibration's protein-response limitation. The rest of this paragraph remains verbatim. |
| "minimizing the overall vertical distance between the data and the line" | "minimizing the sum of squared vertical distances between the data and the line" | Corrects the least-squares objective. The rest of this paragraph remains verbatim. |

All other changes to the introduction are structural: the document title and Part heading follow
the repository syntax; extracted image paths replace embedded image references; paragraphs wrap
at about 98 columns; micro, degree, and superscript-plus characters use HTML entities. The original
2016 discovery paragraph, every strain description, the full purification paragraph, and the
severalfold-activity story paragraph retain their words. The existing single synthetic-data notice
follows the introduction. The duplicate notice before the dataset instructions is removed.

The original Step 1 depends on an external teaching spreadsheet. The current generated workbook
setup replaces that dependency. Starting at original Step 2, the source contains copied Microbes
population-mean, t-statistic, and Busse Woods instructions. Those instructions remain replaced by
the coherent Bradford calibration, residual, interpolation, dilution, and recovered-total-protein
workflow. They are not prose-restoration targets.

## Instruction cleanup

The blank correction now has one natural instruction: enter the formula in C2 and fill C2:C8,
with the keyboard and fill-handle alternatives in the same paragraph. It contains exactly one
`enter:C2` binding and one `fill:C2:C8` binding. The separate numbered selection/execution step
is gone. The other fill instructions already group their starting formulas and fill ranges;
they do not have a duplicate Fill/Do/Check action-log sequence. Source values, worksheet name,
cell locations, formulas, and declared region roles remain unchanged.

No new student checkpoint or challenge was added: this pass repairs fidelity and a duplicate
instruction. The existing residual and interpretation questions still ask students to explain
calibration limits and distinguish total protein from PETase production or activity.

## Verification

Ran `source source_me.sh && python3 make_tutorial.py lint tutorial_data/petase_1_linear_regression.md`.
Offline lint passes. It retains the unmapped-Google-sheet note and the `unavailable-input` warning
for J13, the free-text interpretation entry. These appeared before this pass. This check does
not establish Google import, navigation, or calculation behavior. No LibreOffice command ran.

A direct paragraph comparison independently checked the 11 unchanged original blocks and printed
the three changed block openings. The new text received a humanizer pass for plain wording;
the restored author's wording was not rewritten to satisfy that style. Rendered artifact review
belongs to the subsequent fresh review and rebuild.
