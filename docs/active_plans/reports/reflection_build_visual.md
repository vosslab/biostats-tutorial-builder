# Reflection build and visual review

## Build evidence

On 2026-11-04, all 12 canonical Markdown sources built through
`tutorial_lib.build.build_documents(..., formats="all")` into their normal
`tutorial_output/<source-stem>/` bundles. The descriptive-statistics example built into
`tutorial_output/descriptive_statistics_reflection/`. The three Caffeine sources built together
into `tutorial_output/caffeine_release/`. Every LibreOffice operation ran outside the sandbox,
with `source source_me.sh && python3`. No production code changed in this workstream.

The Caffeine Part 2 stale worksheet instruction was corrected by the source workstream, then
its single bundle and the complete shared bundle were rebuilt.

`tutorial_output/validation/reflection_artifact_checks.json` records source/output SHA-256
fingerprints and checks of all 13 single-source bundles (30 corpus questions plus five example
questions). Every DOCX has exactly one appended Reflection Questions heading; its final question
paragraphs exactly match the literal question cells in its workbook. All generated reflection
question and answer rows have wrapped text and height at least 47.25 points, and column A has
width 124. Answer cells contain `answer here`. The shared workbook has the four ordinary tabs
followed by Part 1 Reflection, Part 2 Reflection, and Part 3 Reflection. Shared DOCX/workbook
question identifiers match (1.1 through 1.3, 2.1 through 2.7, 3.1 through 3.7).

The five example question texts compare verbatim with cells A2/A4/A6/A8/A10 of Part 1 Reflection
in `Nov_4_Artifacts/Copy_This-Descriptive_Statistics_Tutorial.xlsx`. Frozen originals were read
only and were not edited.

## Actual Calc execution

The runtime command compiled the three Caffeine sources, merged them using
`tutorial_lib.build.merge_documents`, prepared the baseline final state with
`devel.sheets_validation_lib.prepare_cases`, derived all 103 independent expectations using
`devel.tutorial_oracles.caffeine_release`, and passed the case to
`devel.validate_libreoffice.run_case`. All 103 comparisons passed, with zero Calc errors or
missing formula caches. The report at `tutorial_output/validation/reflection_shared_calc.json`
keeps the engine version, source/oracle/validator fingerprints, calculated workbook path and
hash, expected and actual values, and source line attribution. This checks native Calc final
states; it makes no claim about Google Sheets or intermediate classroom edits.

## Visual inspection

All captures are fresh native DOCX-to-PDF or actual generated XLSX-to-Calc-PDF output, rendered
with `pdftoppm` and inspected with `view_image`. Named screenshots are quality-90 WebP files in
`tutorial_output/validation/reflection_visual/`. `pdf_pages.json` enumerates the exact PDF pages.

| Bundle | Reflection pages | Boundary pages |
| --- | --- | --- |
| babies_1_z_test | 6 | 5 |
| babies_2_t_test | 6 | 5 |
| babies_3_two_sample_t_test | 5 | 4 |
| caffeine_1_descriptive_statistics | 3 | 2 |
| caffeine_2_linear_regression | 9 | 8 |
| caffeine_3_quadratic_regression | 8 | 7 |
| microbes_1_z_test | 9 | 8 |
| microbes_2_t_test | 9 | 8 |
| microbes_3_two_sample_t_test | 12 | 11 |
| microbes_4_f_test | 11 | 10 |
| microbes_5_anova | 10 | 9 |
| petase_1_linear_regression | 6 | 5 |
| shared caffeine_release, Parts 1/2/3 | 3/9/8 | 2/8/7 |
| descriptive_statistics_reflection | 1-2 | 1 |

The appended questions are legible, numbered, complete, and separated from surrounding prose.
No new reflection-page clipping, overlapping text, or detached headings appeared. The example
naturally continues questions 3-5 on its second page; all five are visible. The seven linear
questions fit on the last page, including question 7 above the footer.

Four actual workbook tabs were printed with the existing
`devel.capture_readme_artifacts.render_workbook(source, name, temporary, destination, area,
sheet_name)` helper. Only disposable print copies received active-tab/hidden-tab/print settings;
student workbooks retain their normal sheet visibility and blank answer spaces. Inspected views:

- `descriptive_statistics_reflection_reflection_workbook.webp`: all five original long prompts.
- `babies_1_z_test_reflection_workbook.webp`: single Joe question and its tall answer row.
- `microbes_3_two_sample_t_test_reflection_workbook.webp`: both long, wrapped prompts.
- `caffeine_release_reflection_workbook.webp`: seven Part 3 prompts labeled 3.1 through 3.7.

All text and answer placeholders are readable; long prompts wrap within their rows. The large
answer spaces remain visible. The workbook receipt is `workbook_captures.json` in the same folder.

## Documentation refresh

The additional native documentation refresh completed successfully with the existing commands:

```bash
source source_me.sh && python3 devel/refresh_documentation.py
source source_me.sh && python3 devel/capture_authoring_course.py
```

Both commands ran outside the sandbox and exited 0. The first refreshed the shared release,
Microbes Parts 4/5, four README screenshots, 21 syntax/authoring screenshots, and all three
illustrated guides. The second built all eight authored course stages, passed its independent
Calc checks, published root_statistics.md/.docx/.pdf/.xlsx, and refreshed 16 native course views.
All 41 final named documentation screenshots were opened with view_image and inspected: crops
preserve their complete intended content, formula text and worksheet labels are readable, and
workbook starters remain visibly blank. Receipt timestamps are 2026-11-04 18:40:16 UTC (README),
18:40:35 UTC (syntax), and 18:41:47 UTC (course).

After these refreshes, every reflection PDF page and boundary was recaptured; all 32 final WebP
files were pixel-identical to their already inspected versions. Final source hashes match both
artifact and Calc reports. The final shared workbook reflection capture was refreshed as well.
No temporary runner script was added. The final source/output fingerprints cover all 46 student
artifacts, and no frozen original changed.

## Verification limits

Root reports the final full-suite result as 2145 passed with one baseline Podman-unavailable
failure; that suite was not rerun by this workstream. Legacy PDF pages outside the reflection
sections and their immediate boundaries were not exhaustively inspected. Live Google import,
navigation, editing, and calculation remain unverified.
