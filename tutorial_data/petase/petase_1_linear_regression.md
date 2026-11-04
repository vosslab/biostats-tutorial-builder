# Enzyme Expression Linear Regression Tutorial for BIOL 318/418

![PET packaging examples from the original tutorial](assets/petase_01.png)

### Part: Scenario

#### Background: PET and Plastic Waste

**Polyethylene terephthalate (PET)** is the clear plastic used in water bottles, food packaging,
and synthetic fibers. It is lightweight and convenient, but it breaks down very slowly in the
environment. Global plastic accumulation has created landfills and "plastic oceans" that are
difficult to clean up with traditional methods.

You have just been hired at a small biotechnology startup that has one big goal: to help solve the
plastic waste problem using **engineered microbes**. The company focuses on PET because it is
durable and cheap, but that same durability means it persists in landfills and oceans for decades.
Your team is working on an enzyme called **PETase** that can cut PET into smaller, more manageable
molecules and may become the core of an industrial plastic recycling process.

![PET polymer structure from the original tutorial](assets/petase_02.png)

In 2016, researchers described a bacterium, *Ideonella sakaiensis*, that can use PET as a carbon
source. One of its key enzymes is PETase, which binds to PET and cuts it into smaller molecules
that other enzymes can finish processing. This discovery suggested a new approach to plastic waste
that uses **biocatalysts** rather than mechanical or chemical treatment alone.

#### Engineering Yeast to Produce PETase

The startup's scientists have spent the last year building *Saccharomyces cerevisiae* strains that
can produce PETase. Instead of using the wild type PETase gene from *I. sakaiensis*, they designed
a **synthetic PETase variant** that combines several mutations known to improve activity and
stability. The coding sequence was **codon optimized** for yeast and carries engineered
substitutions in the active site region and surface loops that increase catalytic activity on PET
fragments, improve thermal stability, and reduce aggregation during expression.

This PETase variant has shown severalfold higher **enzyme activity** than the wild type enzyme in
test reactions and remains active at temperatures that are closer to realistic industrial
conditions. For that reason the entire **fermentation project** now focuses on producing this
improved mutant rather than the original enzyme.

After many rounds of tinkering with promoters, secretion signals, and growth conditions, the team
had a breakthrough shortly before you were hired. Three yeast strains now look very promising:

* **Strain A** carries a single copy of the yeast codon optimized PETase variant integrated at the
  HO locus under the TEF1 constitutive promoter, producing cytosolic His tagged PETase at moderate
  but stable levels.
* **Strain B** carries the same PETase variant on a high copy 2&micro; plasmid under a
  strengthened PGK1 promoter with a LEU2 marker, driving very high intracellular expression and
  placing heavy load on the translation machinery.
* **Strain C** expresses PETase from a low copy CEN plasmid under the GPD promoter, fused to the
  &alpha; factor prepro secretion signal and a C terminal His tag so that PETase is secreted
  directly into the culture medium for easier recovery.

Each strain is grown in baffled flasks to late log phase, then cells are harvested by
centrifugation. For Strains A and B, the pellets are kept; for Strain C, the supernatant is saved
because PETase is secreted. For the intracellular strains, pellets are resuspended in a cold lysis
buffer and broken in a bead beater, and the crude lysate is clarified by high speed refrigerated
centrifugation to obtain a clear soluble fraction. Solid ammonium sulfate is then added to this
fraction to precipitate protein, the mixture is centrifuged again, and the resulting protein
pellet is resuspended in a smaller volume of Ni NTA binding buffer. The enriched solution is
loaded onto a small gravity flow column packed with Ni&sup2;<sup>+</sup> charged resin, washed, and
PETase is eluted with an imidazole containing buffer, followed by SDS PAGE to identify and pool
the best fractions. The pooled Ni eluate is concentrated using a centrifugal concentrator and run
over a size exclusion chromatography column to remove remaining aggregates and contaminants. The
main PETase peak fractions are pooled to yield a **partially purified PETase preparation** for
each strain, which is then aliquoted and stored at 4 &deg;C for immediate use and frozen for
longer term experiments.

#### Your Task: Quantifying PETase Production

Your first assignment is to help evaluate these three strains. Each one has been grown in a small
fermentation flask, and the team has prepared three partially purified PETase samples. However, no
one yet knows how **concentrated** these samples are, so the team must quantify how much total
protein is present in each sample before comparing yields or planning scale up.

You will perform a **Bradford protein assay** using bovine serum albumin (BSA) standards to create
a standard curve. You will measure absorbance at 595 nm for the standards and for the three
unknown PETase samples, then use **linear regression** in Google Sheets to fit a straight line to
the standard data, obtain a regression equation and R&sup2; value, and convert absorbance values
for Strain A, Strain B, and Strain C into protein concentrations. In other words, your regression
model will turn blue color in a cuvette into hard numbers that tell the startup how much
BSA-equivalent total protein was recovered in each preparation.

#### Concept: How the Bradford BSA Assay Works

The **Bradford protein assay** is a colorimetric method that turns protein amount into blue color.
The reagent contains the dye Coomassie Brilliant Blue G-250 in an acidic solution. In acid, the
dye is mostly in a reddish or brownish form that absorbs around 465-470 nm. When it binds to
proteins, especially basic and aromatic residues, the dye shifts into a blue anionic form that
absorbs strongly at **595 nm**. The more protein present, the more dye switches to the blue form,
and the higher the absorbance you measure at 595 nm.

To turn this color change into an actual concentration, you mix the dye with a set of **protein
standards** of known concentration, usually bovine serum albumin (BSA). Each standard is treated
exactly like an unknown, and you record the absorbance at 595 nm for all of them. Across a certain
working range, the amount of bound dye is approximately proportional to the amount of protein, so
the standards form an approximately straight line relationship between BSA concentration and
absorbance.

Your PETase samples are then handled in the same way: you add Bradford reagent, wait for the color
to develop, and measure absorbance at 595 nm. Since you do not know their concentrations, you use
the **standard curve** from the BSA series to infer them. Different proteins can produce different
dye responses, so these estimates are BSA-equivalent total protein concentrations. In the next
section, you will fit that curve with a linear regression so that a single equation can translate
absorbance values from your unknown PETase samples into estimated protein concentrations.

#### Why Use Linear Regression Now?

In the Bradford assay, you are relying on a **standard curve** that links BSA concentration to
absorbance at 595 nm, but your data points will never fall perfectly on a straight line because of
pipetting error, instrument noise, and natural variation. **Linear regression** is the
mathematical tool that finds the single "best fit" line through those scattered points by
minimizing the sum of squared vertical distances between the data and the line. This line is not
just a sketch; it is defined by an equation and a slope that quantify how much absorbance changes
per unit of protein. Once you have that equation and its R&sup2; value, you can plug in absorbance
values from your unknown PETase samples and interpolate their protein concentrations in a
consistent way, instead of guessing from the graph or relying on a single pair of points.

**This lesson uses synthetic teaching data** to practice a Bradford calibration and compare three
protein preparations. No earlier tutorial or laboratory measurements are required.

## Workbook

### Sheet: Bradford illustrative

- **Region A1:B8:** source
- **Region A12:D15:** source
- **Region C1:C8:** calculation
- **Region E13:F15:** calculation
- **Region I1:J8:** calculation
- **Region F1:G4:** results
- **Region G13:G15:** results
- **Region I12:J13:** interpretation

| Synthetic BSA concentration (mg/mL) | Synthetic raw A595 | Blank corrected A595 |
| --- | --- | --- |
| 0 | 0.052 | |
| 0.125 | 0.153 | |
| 0.250 | 0.249 | |
| 0.375 | 0.354 | |
| 0.500 | 0.452 | |
| 0.625 | 0.550 | |
| 0.750 | 0.651 | |

#### At: F1

| Calibration statistic | Student value |
| --- | --- |

#### At: A12

| Synthetic sample | Synthetic raw A595 | Synthetic dilution factor | Synthetic recovered volume (mL) | Diluted protein (mg/mL) | Original protein (mg/mL) | Recovered protein (mg) |
| --- | --- | --- | --- | --- | --- | --- |
| Strain A | 0.292 | 5 | 3 | | | |
| Strain B | 0.454 | 10 | 2 | | | |
| Strain C | 0.372 | 5 | 4 | | | |

#### At: I12

| Interpretation | |
| --- | --- |
|  |  |

### Reflection Questions

1. Compare the ranking in G13:G15 with the concentration ranking and explain why volume matters for recovered mass.

## Tutorial

### Part: Prepare the calibration

- **Worksheet:** Bradford illustrative

#### Step: Open your workbook

1. Upload this tutorial's generated XLSX workbook to Google Drive and open it in Google Sheets.
2. Choose File > Make a copy and add your name to the spreadsheet name.
3. Open the `Bradford illustrative` sheet in your copy.

#### Step: Inspect the dataset

`A2:B8` holds the BSA standards, including the zero-protein reagent blank in row 2; `A13:D15` holds the three unknown preparations and their
dilution information. Each absorbance is a single illustrative reading. A real assay should
include replicate standards and samples, matching buffers, consistent timing, and a validated
working range for the specific reagent and format. The nonzero teaching standards span 0.125 to
0.750 mg/mL; those bounds describe this dataset, not a universal Bradford linear range.

#### Step: Subtract the blank

In C2, enter [=B2-$B$2](enter:C2), then fill [C2:C8](fill:C2:C8) down: select the range, including C2,
and press Ctrl+D (Windows) or Command+D (Mac). You can also drag the blue fill handle from C2 to C8.

The `$` anchor keeps the zero-protein reading fixed. C2 should be zero, and C8 should contain
`=B8-$B$2` and show 0.599. Do not subtract the blank again from an already corrected reading.

#### Step: Plot the standards

1. Select [A1:A8](select:A1:A8), then choose Insert > Chart.
2. In Chart editor > Setup, choose Scatter chart. Set `A2:A8` as the concentration X-axis and
   add `C2:C8` as the only absorbance series; remove any automatically selected raw absorbance
   series.
3. In Chart editor > Customize > Chart and axis titles, name the chart "Illustrative Bradford
   calibration", label the horizontal axis "BSA concentration (mg/mL)", and label the vertical
   axis "Blank corrected A595".

Check that concentration is the horizontal numeric axis. A line chart with categories is not the
intended graph. Look for curvature or isolated outliers.

#### Step: Fit a regression line

1. In F2, label [Slope (A595 per mg/mL)](label:F2); in G2, enter
   [=SLOPE(C2:C8,A2:A8)](enter:G2). In F3, label [Intercept (A595)](label:F3); in G3, enter
   [=INTERCEPT(C2:C8,A2:A8)](enter:G3). In F4, label [R squared](label:F4); in G4, enter
   [=RSQ(C2:C8,A2:A8)](enter:G4).
2. Double-click your scatterplot, then choose Chart editor > Customize > Series > Trendline. Use a
   linear trendline, show its equation as the label, enable a legend, and show R squared.

The chart equation should agree with G2:G3 after allowing for displayed rounding. Use spreadsheet
coefficients in calculations to retain precision. R squared describes the fitted variation in
absorbance explained by concentration for these standards. A value near 1 does not establish
correct units, absence of systematic error, sample purity, or validity outside the calibration
interval. Do not force the intercept to zero solely because you subtracted a blank.

#### Step: Examine residuals

1. In I1, label [Fitted A595](label:I1); in J1, label [Residual A595](label:J1).
2. In I2, enter [=$G$2*A2+$G$3](enter:I2); in J2, enter [=C2-I2](enter:J2). Fill
   [I2:J8](fill:I2:J8) down. The `$G$2` and `$G$3` references stay on the calibration coefficients.
3. Insert a second scatter chart with `A2:A8` as the concentration X-axis and `J2:J8` as the
   residual series.

Look for residuals scattered around zero. A curved pattern suggests that one straight line is
inadequate; a high R squared alone would not resolve that problem. These few synthetic readings do
not provide replicate-based measurement uncertainty.

### Part: Estimate sample protein

- **Worksheet:** Bradford illustrative

#### Step: Check interpolation limits

Subtract B2 from each unknown raw reading in B13:B15. Confirm that each corrected result falls
between the corrected nonzero standards in C3:C8. If a real unknown lies outside the validated
range, repeat the assay at a suitable dilution and record its new reading and dilution factor.
Extrapolation can give a plausible number without reliable calibration support.

#### Step: Calculate diluted concentrations

In E13, enter [=(B13-$B$2-$G$3)/$G$2](enter:E13), then fill [E13:E15](fill:E13:E15) down.
Subtract the blank once from each raw sample reading, subtract the fitted intercept, and divide
by the slope. The result is BSA-equivalent total protein in the diluted sample before dye addition,
in mg/mL.

#### Step: Correct for dilution

In F13, enter [=E13*C13](enter:F13), then fill [F13:F15](fill:F13:F15) down. A dilution factor
of 5 means one volume of original preparation brought to five total volumes before the assay.
Multiply the diluted concentration by that factor once. Rank F13:F15 as concentrations of the
original recovered preparations; do not rank raw absorbances alone when dilution factors differ.

#### Step: Calculate recovered total protein

In G13, enter [=F13*D13](enter:G13), then fill [G13:G15](fill:G13:G15) down. Multiplying
concentration in mg/mL by the recovered preparation volume in mL gives BSA-equivalent recovered
total protein in mg. This is the original undiluted preparation volume, not the diluted assay
aliquot volume. Answer reflection question 1 in the reflection tab.

#### Step: Interpret the limits

The slope should be about 0.7983 A595 per mg/mL. The dilution-corrected concentrations should be
about 1.50, 5.03, and 2.00 mg/mL for strains A, B, and C. If they differ substantially, check
blank subtraction, anchored coefficients, and dilution factors. Write a short report naming the
calibration slope, intercept, and R squared, then the three diluted concentrations, dilution-
corrected concentrations, and recovered masses. Give units and identify the data as synthetic.

Explain why the preparation with the most recovered total protein is not necessarily the
preparation with the most PETase. To compare PETase production per fermentation batch, measure
PETase abundance or independently establish purity, account for recovery losses and culture
volumes, and use independent biological replicates. To compare catalytic performance, measure
enzyme activity under defined conditions. Total protein concentration alone answers neither
question. Write the interpretation in `J13`; include both charts and the calculation cells, and
preserve the formulas so the calculation can be checked.
