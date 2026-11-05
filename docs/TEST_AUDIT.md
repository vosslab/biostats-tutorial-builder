# Permanent-test simplicity audit

Date: 2026-11-04. All six independent passes completed: Plan, Test, Style, Docs, Legacy, and
Comment. Review covered project-specific tutorial, workbook-editing, calculation-preparation,
and documentation tests and their source owners. Mandatory vendored hygiene guards were excluded.
The Comment pass reported no findings.

## Remaining findings

1. **Medium: decimal image bounds fail despite the documented positive-inch syntax.**
   [validation.py](../tutorial_lib/validation.py) accepts decimal inches, but the current Markdown
   attribute path rejects an override such as `{width=5.5in}`. A permanent test previously required
   this rejection. That case was removed; accepting fractional bounds remains a parser follow-up.
   Do not restore a test that treats this limitation as intended behavior.

2. **Medium: generic final-paragraph pairing remains a print-oriented rule.**
   [docx_renderer.py](../tutorial_lib/docx_renderer.py) keeps the last pair of paragraphs together
   regardless of their instructional relationship. Plan and Test reviewers questioned this under
   the current screen-first guidance. Comment review found an earlier explicit design decision
   supporting it. The test freezing the rule was removed; renderer behavior was preserved because
   changing that contested policy exceeds low-risk audit cleanup.

## Resolved after audit

**High: the out-of-scope live Google workflow was removed on 2026-11-05.** The runner
`devel/validate_google_sheets.py`, its API-only helpers, fake transport test, and Google dependencies
were deleted at the human's request. Local Calc case preparation and typed comparison functions remain.
Current instructions are in [LOCAL_VALIDATION.md](LOCAL_VALIDATION.md).
After removal, `source ./source_me.sh && pytest tests/` passed 2,222 tests without warnings.
All four retained local helper functions are unchanged. Additional Calc execution exposed three
Part 3 links that depended on completed Part 2 results. The tutorial now provides same-sheet
SLOPE, INTERCEPT, and RSQ formulas for a fresh workbook, while retaining values-only copying for
students continuing from Part 2.
The corrected sources passed all 254 local Calc comparisons across 13 scenarios; pytest remained
clean at 2,222 tests. No new permanent test or validation mechanism was added for that correction.

## Applied simplifications

- Delete `test_final_body_paragraph_stays_with_its_predecessor` and
  `test_tall_images_fit_native_printable_page_without_cropping`. The former freezes generic page
  tails; the latter duplicates proportional-bound checks using artificial print geometry.
- Remove duplicate `keepNext`, `keep_together`, and `cantSplit` assertions from broader DOCX
  content tests. Preserve their editable content, links, tables, formulas, and menu checks.
- Remove exact default worksheet widths, reflection row heights, and repeated font assertions
  from integrity tests. Keep blank answers, unchanged values, question identifiers, ordering, and
  reflection exclusion from the document.
- Remove the negative test case requiring fractional inch bounds to fail.
- Correct remaining documentation that permitted or directed Google importing.
- Replace figure-generation runtime assertions with explicit errors and add the standard import
  group headings. This leaves validation active under optimized Python.

## Retained contracts and disagreement

The Test pass also proposed deleting label-to-entry grouping tests. The Plan pass distinguished
semantic adjacency from generic page-tail handling; Comment review found the grouping policy
documented. Retain these two tests because keeping a label with its value or formula is a useful
instructional relationship, unlike grouping arbitrary final paragraphs.

Retain native PAGE and TOC field checks: those are documented output features, and cached visible
Contents alone cannot prove the field will refresh over the intended heading levels. Retain
requested heading geometry, image proportions and bounds, workbook identities and tab order,
formula preservation, input validation, and source-editing/data-loss protections. The documentation
composition test earns its place by keeping fenced examples literal while supplying a compilable
practice workbook; it does not freeze guide wording.

No new permanent tests, temporary test files, gates, or configuration were added. Remaining
parser and page-tail changes are findings, not prerequisites for the completed audit. Local
validation supplies no evidence of Google execution or import fidelity.

## Verification

- Baseline: `source source_me.sh && python3 -m pytest tests/ -q --durations=8` passed 2,232 tests
  in about five seconds. No slow project-specific test or live service was found in this lane.
- After cleanup: `source source_me.sh && python3 -m pytest tests/ -q` passed 2,235 cases in
  5.05 seconds with no warnings. Two project test functions were removed; the new report itself
  adds five automatically parameterized checks under the existing shared hygiene guards.
- `MPLCONFIGDIR=/Users/vosslab/.cache/matplotlib python3 -O devel/render_caffeine_figures.py`
  completed successfully in the repository's sourced Python environment.
- No LibreOffice rendering or Google operations are needed for this test-only cleanup.

Authority: [PYTEST_STYLE.md](PYTEST_STYLE.md), [REPO_STYLE.md](REPO_STYLE.md),
[TESTS_README.md](../tests/TESTS_README.md), and [DEVEL_README.md](../devel/DEVEL_README.md).
