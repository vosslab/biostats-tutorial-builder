# Caffeine figure corrections

## Scope and result

The active linear lesson now shows an accurate scatterplot of the supplied 25 students before
students fit a model. The quadratic lesson now compares straight and downward-curving fitted
models on those same observations. Their axes describe sleep hours and exam scores, and their
reported R-squared values agree with the workbook data.

- Replace active use of `caffeine_06.png` with
  [caffeine_sleep_score_scatter.png](../../../tutorial_data/caffeine/assets/caffeine_sleep_score_scatter.png).
  No trendline or coefficient appears before the initial shape prediction.
- Replace active use of `caffeine_13.png` with
  [caffeine_sleep_score_model_comparison.png](../../../tutorial_data/caffeine/assets/caffeine_sleep_score_model_comparison.png).
  Both panels use identical axis limits and the same 25 points. The quadratic fit bends downward.
- Remove active references to `caffeine_04.png` and `caffeine_09.png`, whose embedded scenario
  labels conflict with the actual sleep/score observations. Their original files remain retained.
- Remove the explanation excusing the old comic's 0.88 R-squared. Brief captions now identify the
  actual data and tell students to check their chart and calculations.
- Add explicit "Open chart: Double-click your scatterplot" before returning to the chart editor
  after spreadsheet work in both regression lessons and the PETase lesson.

Neutral story illustrations and the classroom voice remain. This change does not alter dataset
pairs, spreadsheet formula math, hypothesis directions, or the teaching sequence. Applying the
Humanizer skill yielded short factual captions without extra framing or motivational prose.

## Scientific computation

The one-time generator is `/tmp/caffeine_scientific_plots.py`, run from the repository root with
`source source_me.sh && python3 /tmp/caffeine_scientific_plots.py`. It creates new scientific plots
with Matplotlib; it does not edit, crop, or overwrite any retained illustration. No permanent plot
pipeline or test infrastructure was introduced.

Inputs come from `tutorial_lib.compiler.compile_document()` for both current lesson sources.
`tutorial_oracles.observations(sheet, column, end=26)` extracts numeric workbook seeds in row
order. The generator verifies that both sources have exactly the same 25 sleep/score pairs.
Reproduction of the statistical calculation is:

```python
document = tutorial_lib.compiler.compile_document(
    "tutorial_data/caffeine_2_linear_regression.md")
x = tutorial_oracles.observations(document.worksheets[0], 1, end=26)
y = tutorial_oracles.observations(document.worksheets[0], 2, end=26)
linear = numpy.polyfit(x, y, 1)
quadratic = numpy.polyfit(x, y, 2)
total_ss = numpy.sum((y - y.mean()) ** 2)
linear_r2 = 1 - numpy.sum((y - numpy.polyval(linear, x)) ** 2) / total_ss
quadratic_r2 = 1 - numpy.sum((y - numpy.polyval(quadratic, x)) ** 2) / total_ss
```

Observed sleep range is 3 to 11.5 hours. Fitted lines are drawn only within that range, using
300 equally spaced x coordinates. Axis limits are x = 2.7 to 11.8 and y = 45 to 105; this small
margin keeps endpoint observations visible and does not extend the fitted curves.

| Quantity | Computed value |
| --- | --- |
| Linear slope | 3.179071152129 |
| Linear intercept | 58.077850550759 |
| Linear R-squared | 0.346638667858 |
| Quadratic b2 | -1.520250341702 |
| Quadratic b1 | 24.993237896554 |
| Quadratic b0 | -12.004603985325 |
| Quadratic R-squared | 0.847164660392 |

Matplotlib renders the scatterplot at 8 by 5.4 inches and the two-panel comparison at 11 by
5.4 inches, both at 200 dpi. Blue circular observations use `#185c91`; fitted models use
`#a33a13`. White backgrounds, light grids, direct panel headings, explicit units, and rounded
R-squared values keep the comparison readable without relying on color alone.

## Validation and boundaries

- Opened both new PNG files and inspected the complete images: labels and titles are readable,
  all 25 observations are visible, the linear fit rises, and the quadratic fit rises then falls.
- Offline lint passes for both Caffeine regression sources and PETase. Existing Google mapping
  notes and INDEX/LINEST compatibility warnings remain; lint does not execute Google Sheets.
- Root coordinates the subsequent full artifact rebuild and independent rendered-page review.
  This report records source and scientific-figure verification, not PDF layout acceptance.
- No LibreOffice command was run in this workstream.
