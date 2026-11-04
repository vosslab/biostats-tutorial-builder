# Microbes teaching restoration

Compared all five migrated sources with the direct Fall 2025 originals, including their scenario
openings, transitions, practice tasks, and Key Takeaways. Used the early and late teaching reviews
as findings to assess, rather than as authoritative descriptions of the originals.

## Changes

| Lesson | Before | After |
| --- | --- | --- |
| 1: Z-test | General comparison instructions; missing Busse Woods image and recap; short transition | Restored the student's soil-diversity task and Busse Woods image, a three-point recap, and a short supervisor message motivating unknown-SD reanalysis. Moved the normal lower-tail image beside the p-value instruction and retained its illustrative caption. |
| 2: One-sample t-test | Model statement without the student's continuing task or recap | Restored the original unknown-SD challenge, return to the spreadsheet, neutral Z-versus-t title art, four concise takeaways, and the advisor's proposal to compare years. |
| 3: Welch t-test | Generalized transition; missing forest illustration, distribution comparison, and recap | Restored the advisor's continuing comparison task, contextual forest illustration with a non-evidentiary caption, four takeaways, and the student's observation about spread leading to the F-test. Explicitly called independence a hypothetical assumption. |
| 4: F-test | Missing personal advisor task, title art, and recap; seeded D1/E1 implicit | Restored the student's observation and advisor's variance comparison, title art, four takeaways, and the older-theses bridge to ANOVA. Clarified that D1/E1 already contain headers. Explicitly called independence hypothetical. |
| 5: ANOVA | Generalized opening; missing title art and recap | Restored the return to older theses with the advisor, original ANOVA title art, and four concise takeaways about omnibus means, right-tail p, sample size, and scope. |

The new [t_distributions.png](../../../tutorial_data/microbes/assets/t_distributions.png) replaces the
original lesson 3 distribution image. The original labels implied a threshold near n = 30 and its
curves did not accurately represent the distributions. The replacement plots the standard normal
density and Student t densities at df = 3 and 23 using `scipy.stats.norm.pdf` and `scipy.stats.t.pdf`
on 1,601 points from -4 to 4. Solid, dashed, and dotted lines make the distributions distinguishable
without relying only on color. The figure was visually inspected at its saved resolution.

## Scientific boundaries retained

- Population SD is stipulated in lesson 1 and estimated in lesson 2. A small sample does not by
  itself prohibit a known-SD Z-test, and n = 30 is not a switch between tests.
- The one-sample t-test original mentions `T.TEST` but supplies no direct one-sample implementation.
  No direct `T.TEST` promise or formula was introduced in lesson 2.
- Welch comparisons retain fractional df, signed directional tails, and the hypothetical
  independent-samples model. Matching site labels still require an appropriate dependent-data
  method if they represent repeated measurements.
- F-tests compare index variances, not taxonomic homogenization, resilience, or causal mechanisms.
  The recap retains the sensitivity to nonnormality and numerator/denominator ordering in the steps.
- ANOVA compares means with a right-tail F probability. It neither locates differences nor
  establishes a monotonic trend. Historical method differences and the separate 2014 series remain
  explicit in lesson 5.
- Forest imagery supplies context; its caption explicitly excludes it as evidence about the data
  or their causes. No additional repeated caveat paragraphs were added.

## Verification

All five files passed `source source_me.sh && python3 make_tutorial.py lint <file>` with exit 0.
The files introduced no list-opening warnings. Existing notes and warnings concern unmapped Google
links, intentionally spare input ranges, student interpretation cells, and ANOVA `SUMPRODUCT`
compatibility. Full logs are in
  `tutorial_output/verification/teaching_review/microbes_fixes/`.

A direct before/after check confirmed that every `Enter` directive and the entire `Workbook`
section of each file remained byte-for-byte unchanged. Raw observations, formulas, numeric
benchmarks, worked results, and answer-cell addresses therefore remain unchanged in this pass.
No manual page breaks, renderer edits, or workbook generator changes were made.

This pass did not run LibreOffice, build the main bundle, inspect rebuilt PDFs, or validate live
Google Sheets behavior. The coordinated rebuild and fresh rendered-output review follow this
source restoration.
