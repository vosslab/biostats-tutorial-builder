# Tutorial collection

These 12 editable Markdown sources combine student instructions and starting workbook data.
Build one source from the repository root:

```bash
source source_me.sh && python3 make_tutorial.py build tutorial_data/babies_1_z_test.md
```

The bundle appears in `tutorial_output/babies_1_z_test/` with DOCX, XLSX, PDF, and `validation.json`.
Use `--format docx,xlsx` to skip PDF conversion. Student answer cells start blank;
the instructions carry formulas and assignments. See [USAGE.md](USAGE.md) and
[AUTHORING_GUIDE.md](AUTHORING_GUIDE.md).

## Babies and fried foods

The hospital scenarios teach comparisons against a national benchmark and between hospitals.

| Source | Method |
| --- | --- |
| [babies_1_z_test.md](../tutorial_data/babies_1_z_test.md) | One-sample Z; known population SD |
| [babies_2_t_test.md](../tutorial_data/babies_2_t_test.md) | One-sample t; estimated SD |
| [babies_3_two_sample_t_test.md](../tutorial_data/babies_3_two_sample_t_test.md) | Welch two-sample t |

## Microbial diversity

The Busse Woods lessons analyze Shannon diversity indices with explicit directional tails.

| Source | Method |
| --- | --- |
| [microbes_1_z_test.md](../tutorial_data/microbes_1_z_test.md) | One-sample Z |
| [microbes_2_t_test.md](../tutorial_data/microbes_2_t_test.md) | One-sample t |
| [microbes_3_two_sample_t_test.md](../tutorial_data/microbes_3_two_sample_t_test.md) | Welch two-sample t |
| [microbes_4_f_test.md](../tutorial_data/microbes_4_f_test.md) | Two-sample variance F test |
| [microbes_5_anova.md](../tutorial_data/microbes_5_anova.md) | One-way ANOVA; right-tail F probability |

## Dr. Caffeine

The three Caffeine Parts use the same shared six-tab workbook and release together.

| Source | Method |
| --- | --- |
| [caffeine_1_descriptive_statistics.md](../tutorial_data/caffeine_1_descriptive_statistics.md) | Mean, median, sample SD |
| [caffeine_2_linear_regression.md](../tutorial_data/caffeine_2_linear_regression.md) | Linear fit, prediction, two-tailed slope test |
| [caffeine_3_quadratic_regression.md](../tutorial_data/caffeine_3_quadratic_regression.md) | Quadratic fit, curvature test, model comparison |

Build their shared release with the three sources in order. The bundle contains one `workbook.xlsx`
and one DOCX/PDF pair for each source:

```bash
source source_me.sh && python3 make_tutorial.py build \
  tutorial_data/caffeine_1_descriptive_statistics.md \
  tutorial_data/caffeine_2_linear_regression.md \
  tutorial_data/caffeine_3_quadratic_regression.md \
  --output-dir tutorial_output/caffeine_release
```

## Illustrative PETase calibration

[petase_1_linear_regression.md](../tutorial_data/petase_1_linear_regression.md) uses **synthetic teaching data**.
It repairs a contaminated legacy lesson with a Bradford calibration, interpolation, dilution
correction, and recovered total protein estimates. It does not represent recovered experimental
measurements or establish PETase-specific protein abundance or enzyme activity.

## Validation evidence

Local build and review evidence is recorded in
[implementation_validation.md](active_plans/reports/implementation_validation.md),
[pdf_validation.md](active_plans/reports/pdf_validation.md), and
[calculation_validation.md](active_plans/reports/calculation_validation.md).
Independent numerical expectations are distinct from formula execution in Google Sheets;
live Google import, calculation, and link behavior remain unverified without observed results.
