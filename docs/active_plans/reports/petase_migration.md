# PETase migration report

Path note (2026-10-22): paths and command examples below use the current repository layout.
Recorded observations belong to their stated snapshots; renamed output manifests retain their
original contents until the final rebuild and verification refresh.

[petase_1_linear_regression.md](../../../tutorial_data/petase/petase_1_linear_regression.md) is a complete
illustrative Bradford regression lesson, **not a recovered original experiment**. All seeded numbers
are synthetic teaching data, stated in the title, introduction, worksheet name, column headers, and
instructions. The coordinator authorized that approach after recovery found no original measurements.

## Source coverage and recovery

The original
[PETase_1_Linear_Regression_Tutorial_Fall_2025.md](../../../2025_Artifacts/PETase_1_Linear_Regression_Tutorial_Fall_2025.md)
is unchanged. Its SHA-256 is
`b508e35304561e07e80eb0e157af1dbe9dbb628f55bc03e2845209e4ffe6b7a6`.

| Original material | Replacement and reason |
| --- | --- |
| Title, lines 1-3 | Regression identity retained; illustrative status explicit. |
| PET background, lines 7-14 | Packaging, recycling motivation, discovery, and images retained with scientific scope qualified. |
| Yeast engineering, lines 16-28 | All three expression strategies and purification stages retained as a fictional scenario; unsupported performance claims become proposed goals. |
| Production task, lines 30-34 | Bradford standards, unknowns, regression, R squared, and comparison retained; total protein distinguished from PETase. |
| Bradford mechanism, lines 36-42 | Dye binding, 595 nm signal, BSA standards, and limited linear range retained and clarified. |
| Regression, lines 44-46 | Least squares, scatter, calibration, equation, and interpolation retained; residuals added. |
| Setup, lines 48-57 | Unavailable BSA data replaced with explicit synthetic table. Worksheet name avoids the original illegal XLSX colon and excessive length. |
| Steps 2-9, lines 59-171 | Unrelated Busse Woods t-test/degrees-of-freedom/p-value/IF material replaced with regression, residuals, dilution, mass, interpretation. |
| Base64 images | Extracted byte-identically into local PNG companions. |

On 2026-10-22 the
[original linked workbook](https://docs.google.com/spreadsheets/d/1cAlU997q8IazW6wJhBwYRrrO2l6ls0yCAo3Rx9BlUY0/edit)
was publicly exported as XLSX. All nonblank cells were inspected. Its tabs are
`Part 1 and 2 Busse Woods 2024`, `Part 3 and 4 Busse Woods 2014 a`, and `Part 5 ANOVA Data`.
They contain Shannon indices, no BSA standards and no PETase absorbances. No false Google tab mapping
is supplied for the new lesson. File searches across the repository, `/Users/vosslab/nsh`, and the
adjacent teaching directories found another copy of the PETase Markdown and unrelated older BSA
laboratory spreadsheets; those data were not reused as PETase measurements.

Both original images were inspected locally: packaging examples and PET polymer structure. The
original source does not identify external creators or image licenses; that limitation is preserved.
The extracted bytes match the base64 payloads exactly:

| Companion | SHA-256 |
| --- | --- |
| [petase_01.png](../../../tutorial_data/petase/assets/petase_01.png) | `ac18ea8fdb0ecf2729e226f8a8cb2cc256e8df7152d22f2dcf58603a52553a7d` |
| [petase_02.png](../../../tutorial_data/petase/assets/petase_02.png) | `d954d55629e392d10e847a8b23c47107bfc26a668b5a4db669b1ad4d5b6083f1` |

## Scientific corrections and primary sources

Yoshida et al., 2016,
[A bacterium that degrades and assimilates poly(ethylene terephthalate)](https://doi.org/10.1126/science.aad6359),
with the [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/26965627/) checked on 2026-10-22,
supports the discovery description. The lesson makes no general remediation claim from that result.

Bio-Rad's
[Quick Start Bradford manual](https://www.bio-rad.com/webroot/web/pdf/lsr/literature/4110065A.pdf)
was checked on 2026-10-22. Sections 1.1-1.2 describe dye chemistry, interference, protein-dependent
response, and relative standards. Section 2.1 supports matching sample buffers and replicate readings.
Section 3 supports blank subtraction, concentration on the horizontal axis, absorbance on the vertical
axis, and multiplication by dilution factor. The synthetic lesson follows these principles while
explicitly acknowledging single readings and protocol-specific calibration bounds.

Bradford measures total protein, not PETase specifically. BSA-equivalent concentration, recovered
total protein mass, PETase abundance, enzyme activity, purification losses, and fermentation
productivity are distinguished. Concentration times volume estimates recovered total protein mass;
it is not a batch productivity or PETase-specific measurement. R squared alone does not establish
accuracy, linearity, or purity. Residual inspection and interpolation checks are taught.

Google's [trendline instructions](https://support.google.com/docs/answer/6075154?hl=en), checked on
2026-10-22, support Customize > Series, equation labels, and the legend requirement for R squared.
No Google import, editing, or formula calculation was performed.

## Independent numerical checks

Least squares calculations run through `source source_me.sh && python3` give slope
`0.7982857142857143`, intercept `0.0002142857142856669`, and R squared `0.9999410777343518`.
This check does not add a formula evaluator to the converter.

| Preparation | Diluted mg/mL | Original mg/mL | Recovered mg |
| --- | --- | --- | --- |
| Strain A | 0.3003758053 | 1.5018790265 | 4.5056370795 |
| Strain B | 0.5033106657 | 5.0331066571 | 10.0662133142 |
| Strain C | 0.4005905512 | 2.0029527559 | 8.0118110236 |

All unknown corrected absorbances fall within the nonzero teaching standards. Student calculation
cells are blank initially; data and headers alone are seeded. Formula destinations and anchors are
explicit. The exercise does not need a hypothesis test or p-value for calibration interpolation.

## Integration validation

Initial lint reached the shared compiler but failed with `UnboundLocalError` in `compile_source`
at its `tutorial_lib.parser.parse_source` call, caused by a local import binding. The coordinator
was notified; this content owner did not modify shared code. Final lint and generated DOCX/XLSX/PDF
inspection require the integrating agent's repaired implementation. Numerical checks, image-byte
comparisons, and source recovery are independently verified. Google behavior remains unverified.

After the shared compiler repair, PETase lint passed with no errors or warnings; the only note is
`google-unmapped`, intentionally retained because the original link points to unrelated data.
Independent SciPy `linregress` reference cells were supplied to the formula-validation owner in
`/private/tmp/sheets_expectations_petase.json` for calibration and all three unknown preparations.


## Post-freeze startup correction

Added a short workbook-opening step before dataset inspection: upload the generated XLSX to
Google Drive, open in Google Sheets, make and rename a personal copy, and locate the exact
`Bradford illustrative` worksheet. No synthetic data, formula, or scientific claim changed.

Validation: `source source_me.sh && python3 make_tutorial.py lint tutorial_data/petase_1_linear_regression.md`
passed with zero errors and zero warnings; the existing unmapped-Google note remains. Reviewed
the source step for complete instructions and exact sheet naming. This is an authored workflow,
not evidence of live Google import. Final PDF rebuild and visual verification belong to the
render-validation workstream.
