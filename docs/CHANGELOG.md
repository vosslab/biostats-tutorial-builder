# Changelog

## 2026-11-04

### Refreshed authoring documentation

- Introduce biology tutorial authoring without a course-specific audience label. Update the guides
  and runnable examples for the refined heading hierarchy, complete Contents, equations, inline
  reflections, green formula-entry borders, menu paths, and proportional captioned figures.
- Refresh all native documentation capture sets and guide exports, including retained checkpoint
  examples. Separate Contents from the title crop and add math and inline-reflection views.
- Remove live Google upload instructions from the current usage path; retain local-only validation.

### Accessible regression notation and figures

- Use a, b, c and the familiar quadratic equation throughout Part 3 and all shared workbook
  declarations; retain beta notation only in one later-study note.
- Pair hypothesis names with their subscripted symbols in active tutorial sources, matching the
  human's null/alternative terminology example.
- Make values-only copying the first route for transferring linear results and explain the sheet
  separator `!` in the optional linked-formula route.
- Add a reproducible Matplotlib figure command using canonical observations, readable label sizes,
  and gridlines behind data points. Record the corresponding human guidance.

### Complete contents navigation

- Include every Step and Substep in a native linked TOC with subordinate indentation and hanging
  indents. Show a single Part in a title-area Subtitle while preserving its body heading; retain
  Part entries when a document has multiple Parts. Exclude the Contents label from the outline.

### Workbook filename presentation

- Record the human-approved standalone workbook filename line used in all three Caffeine introductions.

### Part identity and guidance review

- Synchronize single-Part document headings and contents with shared-build reflection identities;
  declare Caffeine Parts 1, 2, and 3 explicitly for standalone builds too.
- Reconcile superseded numbering and Google-access instructions, and record the human's caption,
  proportional figure bounds, and inline reflection preferences in the guidance.

### Remove assignment labels

- Remove student section-assignment names from the Caffeine warm-up heading.

### Caffeine narrative refinement

- Restore Caffeine's shared proportional figure maximum after removing temporary pagination-only
  image caps; natural sparse print pages are not a release defect.
- Justify ordinary narrative paragraphs without local line-count guesses while leaving specialized
  lists, equations, figures, captions, and prompt callouts left aligned. Give long Caffeine
  workbook filenames their own visible code lines without inserting hidden characters.
- Split every Caffeine reflection into its exact identifier, workbook question, and answer-tab
  destination; retain surrounding explanation as ordinary prose outside the modest native callout.

### Formula-entry displays

- Render every semantic Enter or Replace formula as an individually copyable, destination-labeled
  display line. Restructure Caffeine Part 3's linked formula groups into one readable action per
  target cell while retaining the authored formula bytes.
- Replace full-width shaded formula cards with compact native green run borders around display
  text. Keep reflection callouts shaded; local DOCX/PDF rendering is verified separately from any
  future Google Docs import behavior.

### Consistent heading weight

- Let unmarked inline text inherit paragraph bold styling so plain and Markdown-bold headings
  render consistently. Preserve explicit emphasis and defer rebuilding during the formatting queue.

### Menu path formatting

- Style bold or code-formatted menu paths and Choose actions with bold Roboto Mono, dark text,
  and a light gray background. Normalize menu arrows while preserving formulas and comparisons.

### Page margins

- Set all document margins to 0.6 inches and derive the usable Letter-page width from that margin.
  Defer artifact rebuilds while queued formatting changes continue.

### Workbook tab sequence

- Keep common data first, then place each lesson's work tabs immediately before its reflection tab.

### Descriptive Caffeine captions

- Replace generic illustration captions with descriptions based on direct image inspection.
  Distinguish fictional comic annotations from the actual sleep dataset and fitted results.

### Behavior or Interface Changes

- Group the twelve tutorial sources and every topic asset beneath `tutorial_data/babies/`,
  `tutorial_data/caffeine/`, `tutorial_data/microbes/`, and `tutorial_data/petase/`. Recursive
  discovery and documentation commands now use topic-qualified paths.

### Part 2 structural consistency

- Make research-question and hypothesis labels real headings, flatten peer relationship definitions,
  and separate regression calculations and prediction into numbered substeps with ordered actions.

### Part 1 instructional flow

- Organize descriptive-statistics calculations into numbered mean, median, sample-standard-deviation,
  and summary substeps, with ordered learner actions. Preserve the existing formulas and prose.

### Workflow scope

- Record standing human guidance: Google Drive uploading is always out of scope. Deliver local
  artifacts without uploading to Drive or importing into Google Docs or Google Sheets.

### Fixes and Maintenance

- Restore the native DOCX teaching hierarchy: Part, Step, Substep, and body/task text use
  0, 0.1, 0.2, and 0.3-inch edges; lists, continuations, formulas, prompts, captions, and quotes
  derive from that context while figures stay centered.
- Lead Caffeine regression instruction with familiar linear and quadratic equations, map only the
  needed workbook coefficients, and clarify the quadratic-coefficient reflection prompt.
- Regenerate the Caffeine scientific scatter and fit-comparison figures from the authored data
  without standalone plot titles, while preserving axes, fitted curves, R-squared values, and panel labels.
- Anchor the Caffeine screenshot capture to stable Step titles rather than shifted generated numbers.
- Highlight full contextual reflection prompts with native paragraph shading and borders while
  keeping the workbook list as the single question source.
- Unify DOCX heading, body, list, continuation, formula, quote, figure-caption, and table-caption
  indentation around one native list and quote hierarchy.
- Center standalone DOCX figures in a 6.5-inch-wide by 3-inch-tall proportional fit box, reserve
  caption room, and split line-break-separated figures from their surrounding prose.
- Select the instructional heading occurrences after the generated contents field when refreshing
  syntax-example screenshots.
- Render Caffeine figures from recovered full-proportion artwork, add native figure captions and
  table titles, clarify shared-workbook reflection labels, and name the released student workbook.
- Add native Word contents fields and editable TeX/Office Math for explanatory equations while
  preserving literal spreadsheet formulas.

### Additions and New Features

- Keep the required Workbook reflection list and generated reflection tab per source, while
  repeating each full prompt in the relevant Tutorial prose instead of appending a duplicate DOCX
  section. Shared builds assign Part IDs automatically without step mapping.
- Clarify reflection output: shared workbook tabs use spaced names such as `Part 2 Reflection`,
  question identifiers are literal editable text in the workbook, and the compiler normalizes
  source list starts to 1 without making that author recommendation a lint gate.
- Adapt the three Dr. Caffeine sources around one shared six-tab workbook. Build multiple existing
  Markdown sources into one compatible XLSX and separate Google Docs-ready DOCX/PDF documents.

### Behavior or Interface Changes

- Use the regression dataset throughout the Caffeine warm-up, linear regression, and quadratic
  regression. Preserve the frozen student artifacts as the source reference while correcting their
  inconsistent warm-up dataset and spreadsheet formulas.

### Fixes and Maintenance

- Extend independent numerical expectations to support one tutorial whose formula results span
  multiple worksheets. Update Caffeine catalog and build guidance for the shared release.

### Developer Tests and Notes

- Final shared-workbook execution in LibreOffice Calc matches all 103 independent formula
  expectations. The complete numerical inventory covers 254 formulas across 12 tutorials.
  Reflection corpus/template/example sources compile (12 corpus sources and 30 questions); 13
  single-source plus shared outputs match all 46 source/output hashes. Calc passes 103 checks with
  zero errors. Native visual review inspected 41 documentation images, including the generated
  reflection preview, and the latest receipt records 14 source and 22 image hashes. The final
  repository suite reports 2,146 passed and one failure: the existing unavailable Podman VM
  connection. Google import remains unverified.
- The baseline full suite reported 2,115 passing tests and one pre-existing Podman disk check
  failure because the local Podman VM connection at localhost:54395 was refused.

## 2026-10-23

### Additions and New Features

- Rebuild all three authoring-guide Parts around document formatting, Excel workbook construction,
  and building/refining files. Add a visual feature index and one runnable Roots formatting source
  with actual Word/Excel crops, including an unchanged instructor z-test excerpt.
- Define BIOL 318 student authorship and the open-pedagogy/Student-Generated Content purpose in the
  landing page, authoring guide, and specification. Use labeled placeholders for original content.

- Add the three-part Roots authoring course: one student project source, eight comparison
  checkpoints, six Markdown topic references, a student hub, and a published Markdown/DOCX/PDF/XLSX
  capstone. The starter supplies labels and leaves calculation cells blank.
- Add the [student guide](AUTHORING_GUIDE.md) as the primary course hub and route the README's first
  tutorial path through it.
- Document the one-command documentation screenshot refresh workflow and its separate course capture
  receipt.

- Expand [FORMATTING_GUIDE.md](FORMATTING_GUIDE.md) with a worksheet-address map and worked
  examples adding a calculation column and an observation row. Add a runnable source showing
  supplied headers, blank calculation cells, and matching Enter/Fill instructions.

### Fixes and Maintenance

- Fix worksheet-editor source corruption found by the independent authoring walkthrough:
  distinguish uppercase column notation from ordinary prose and synchronize visible Fill ranges
  with their semantic targets. Add two focused regressions and retain preview/write validation.
  Remove the temporary limitation text after reproducing the corrected preview, write, and build.

- Add a seven-dimension authoring-guide rubric and commission an independent documentation-only
  walkthrough, separating expert inspection from evidence of actual student learning.
- Correct the optional worksheet editor's prose-preservation promise after the independent
  walkthrough reproduced unintended capitalization and a stale visible fill range in a resize
  preview. Initially document manual revision as an alternative; the subsequent narrow editor
  repair above resolves these defects.
- Clarify dependent Fill diagnostics and the DOCX/XLSX-only build option in Part 3 following the
  independent review. Preserve the reviewer's original scores and document corrections separately.

- Make the README welcoming to first-time Markdown authors and explain how original student
  tutorials contribute to open pedagogy and a shared resource for classmates and future students.

- Consolidate the student hub into the authoring guide, revise the six topic references, and keep
  advanced worksheet editing optional. Separate technical validation from advisory quality review.
  Refresh the existing capture workflow for the feature source and preserve literal fenced snippets.

- Show literal student source in fenced examples and refresh the illustrated course by composing
  practice source from the existing Roots checkpoints before the normal compiler runs. Correct
  worksheet editing at its source and compiled-table owner, give interpretation response rows a
  shared eight-line / 123-point minimum while preserving taller regions, and clarify novice setup.
  Keep five humanizer edits restrained and grounded in existing lesson content. The initial native
  PDF review found that the Part 1 instructional table lost its five data rows; a DOCX renderer
  header-cell keep-with-next fix resolves the loss. Final PDF inspection confirms all five rows
  together and all 106 cells across six tables. The [native visual report](active_plans/reports/pipeline_quality_followup_visual.md)
  records the initial failure and final proof. The GFM baseline found two source/output mismatches
  and setup gaps; current sources now match accepted actual GitHub GFM renders. Fresh SPEC,
  QUALITY, and [integration](active_plans/reports/pipeline_quality_followup_integration.md)
  reviews accept the follow-up, including the Git checkout and Homebrew pip recovery route.
  All 20 canonical lesson/checkpoint sources remain unchanged; all 102 bundle and 131 receipt
  comparisons match. Final full-suite verification passes 2,054 tests after closeout edits.
  Google behavior and student outcomes remain unverified.
- Record the course structure and capture design in the decision and human-guidance ledgers.
- Reorganize the README around a BIOL 318 student reading path, starting examples, and a plain-language
  explanation of Workbook and Tutorial sections. Keep build commands and advanced examples later.
- Rebuild the ANOVA bundle and refresh README and formatting-guide screenshots using the
  three-decimal numerical display. Inspect both workbook views and refresh capture receipts.
- Correct the illustrated course overview crop so it includes the complete first inspection Step;
  merge its redundant Locate step into Inspect sources to avoid a two-bullet orphan. Fit images to
  printable page bounds while preserving aspect ratio, keep code blocks together, validate local
  WebP captures, and convert image data to PNG in memory at the DOCX boundary. Final screenshots and
  the one-page published capstone are refreshed. Final PDF visual and fresh teaching-quality reviews
  accept the course; fresh SPEC, QUALITY, and integration reviews accept the final course state.
  The full suite passes 2,036 tests; Google behavior and student outcomes remain unverified.

### Decisions and Failures

- Retire the required Roots checkpoint course: it taught introductory spreadsheet/statistics work
  instead of the authoring system. Keep Roots as a formatting example without a prescribed scenario.
  Earlier checkpoint artifacts and their review history remain available.

### Developer Tests and Notes

- Verify 31 student-facing pages through GitHub's Markdown API and local desktop/narrow browser
  inspection. Match 26 source excerpts to their demonstrated inputs; inspect all 13 native guide
  PDF pages and current screenshot/workbook output. A separate content-transfer and error-repair
  walkthrough passes. The repository suite passes 2,105 tests. See the
  [authoring review](active_plans/reports/authoring_visual_reference_review.md) for evidence and
  limits; Google import and student learning remain untested.

## 2026-10-22

### Additions and New Features

- Add [FORMATTING_GUIDE.md](FORMATTING_GUIDE.md), pairing copyable ASCII Markdown with cropped
  native document and spreadsheet output. Include a runnable example and capture script.
  Verify the source excerpts, native renders, and 917 documentation/script checks.
- Add student-oriented calculated-column, statistical-summary, and ANOVA Markdown templates.
  Templates keep spreadsheet coordinates and ordinary Excel formulas visible while separating
  supplied Workbook content from learner-entered Tutorial actions.

### Behavior or Interface Changes

- Display spreadsheet numbers and formulas with three decimal places by default, including
  formulas students later enter in blank work cells. Preserve stored precision and blank answers.
  Refresh the formatting-guide workbook capture; 934 focused workbook and documentation checks pass.
- Lint Markdown tutorial files as ASCII source, allow readable named scientific entities, and
  reject numeric character references with source-located corrections. Preserve Unicode handling
  for in-memory parser and renderer callers.
- Diagnose an explicit `In cell C2, enter ...` instruction when its visible destination conflicts
  with the semantic action target.

### Fixes and Maintenance

- Repair two historical report links to the removed blank-workspace screenshot, preserving the
  original review history and noting why that image was later removed.
- Remove the unlabeled Caffeine grid from the showcase after the human clarified that authors
  establish labels first and tutorial users do not generally enter headings. Keep the completed
  ANOVA demonstration explicitly separate from claims about the starting worksheet.
- Correct the README changelog entries to use this approved category. Record the capture agent's
  `py_compile` cache-writing mistake and the manager's agent-reuse mistake in the verification
  report; retain the existing Python environment settings and absence of cache ignore rules.
- Refresh the landing page around student authors, preserved prose, professional document styling,
  blank learner workbooks, three starter templates, and preview-first worksheet maintenance.
- Replace stale numeric entities in the authoring excerpt. Verify the template quick start in
  DOCX/XLSX and PDF, the complete runnable example, and the worksheet-edit preview. Explain the
  preview's actual fill-wording review notice rather than implying complete prose synchronization.
- Refresh four native output captures, with three featured in the README. Add the prominent
  F-statistic formula and a focused completed ANOVA demonstration. The latter uses a disposable
  styled workbook populated from authored actions and recalculated in Calc; student starters stay
  blank. All 48 canonical source/product fingerprints remain unchanged.
- Extend the existing capture harness and record reproducible provenance in the
  [screenshot receipt](screenshots/README.md). See the
  [README verification report](active_plans/reports/readme_capabilities_showcase.md) for checks and
  the editorial before/after score.

- Normalize active lesson punctuation and scientific notation to ASCII, named entities, and
  ordinary `sub`/`sup` markup without changing lesson wording or archived originals.
- Repair worksheet editing for column insertion, data growth and shrinkage, and ANOVA column moves;
  real previews, writes, and exports pass while preserving learner prose and formulas. Accepted
  presentation updates cover workbook future headers, rules, and response panels, plus DOCX step
  headings with zero left indent, native indents, long-prose justification, and left-aligned hard
  breaks. All 12 bundles and 36 outputs pass manifest and source/output SHA-256 verification; the
  94-page PDF review and final two-page correction review are accepted. The full suite passes 1,828
  tests and Calc passes 13 scenarios / 254 comparisons. Final editor specification-quality and
  integration reviews are accepted; see the
  [student publishing integration review](active_plans/reports/student_publishing_integration.md).
  Google import and student outcomes remain unverified; ambiguous unmarked references still receive
  author review, and line counts are estimates.

### README showcase refresh

- Put three reviewed output screenshots immediately after the opening, followed by the verified
  DOCX/XLSX quick start, Caffeine 3 source excerpt, full runnable example, and curated documentation
  routes. State the unverified Google Docs/Sheets import and execution limits before Quick start.
- Capture the actual illustrated opening, complete fill-down instruction, and full blank workbook
  with `devel/capture_readme_artifacts.py`. The 48 source/product hashes remain unchanged; capture
  hygiene passes 511 checks. See the [screenshot receipt](screenshots/README.md).
- Pass independent SPEC recheck, QUALITY review, and INTEGRATION review with ACCEPT and no material
  issues. The subjective README rubric is 100/100 (15, 15, 20, 15, 10, 10, 5, 10); this is an
  editorial README score, not a product-quality claim. The [showcase report](active_plans/reports/readme_showcase_refresh.md)
  records evidence and limits.
- Caffeine 3 lint and isolated DOCX/XLSX and all-formats builds pass; 155 focused documentation
  tests and the 1,549-test repository suite pass. Canonical lesson text and outputs remain unchanged;
  no live Google verification or student study is claimed.

### Instructional voice restoration

- Complete the five-milestone instructional voice restoration across all 12 sources. Independent
  source reviews accept the original prose, humor, headings, and nested groups with narrow
  technical/scientific corrections; Caffeine retains good draft prose and adds missing instruction.
  The final rendering SPEC passes 177 checks, and fresh material review accepts all 92 PDF pages
  plus the actual workbook layouts. Prior failed restoration/material reports remain historical.
- Reconcile the earlier 1,528-passed / 1-failed full-suite checkpoint as historical. Its ignored
  image link was removed, and the report now links to the repository test code rather than an
  ignored output log. A fresh suite run remains for integration.
- Preserve the authoring example correction: the regression formula binds to F2; I2 is an unbound
  reflection response. Caffeine's visible E2/E3/E4 formulas and calculations retain their existing
  destinations. PETase's fictional strain-performance narrative remains a scenario premise, with
  three targeted corrections about Bradford total-protein limits, protein-specific response, and
  the least-squares objective.
- Rebuild all 36 DOCX/XLSX/PDF products after the final fixes: 92 PDF pages, with Calc passing 13
  scenarios / 254 comparisons against unchanged expectations. Integration matches all 60 source/
  product/validation fingerprints and both refreshed managed screenshot receipts. Fresh pages close
  the label markup, terminal break, adjacent formula, closing link, numeric alpha, and blank spacer
  findings. The [voice restoration ledger](active_plans/reports/voice_restoration_summary.md) links
  current evidence. Google behavior remains unverified; no student study was run.
- Keep the final-build report in `docs/active_plans/reports/` and preserve its original contents.
- Keep adjacent semantic label and entry instructions together in DOCX, including the first nested
  formula under the next numbered item, while leaving later explanations free to paginate. Remove
  redundant terminal list hardbreaks, preserve internal breaks, and keep a final body paragraph with
  its predecessor when those are consecutive paragraphs. Focused DOCX XML coverage passes 10 tests;
  fresh final PDF inspection accepts the resulting page groups.
- Correct the authoring example to name D5/E5 visibly and use a range-fill instruction. Distinguish
  Markdown-decoded semantic labels from JSON Enter/Replace scalars, and require visible destination
  cues. Move the untracked pagination report into the established reports directory and retain the
  completed plan at its stable referenced path. Final integration accepts all five milestones and
  the repository suite passes 1,548 tests after correcting two closing-document link labels.

### Automatic tutorial formatting

- Start the formatting work ledger for automatic formula styling and tighter list spacing across
  all 12 tutorials. The plan tracks parser ownership, focused checks, full rebuild and visual
  comparison, author-facing examples, and staged specification, quality, and integration reviews.
- Update the authoring guide and README to show bare formula entry. Specify contextual formula
  roles, literal-text and prose safeguards, preserved formula text, dark-green monospace output,
  and the accepted paragraph spacing. The literal-action correction passed specification recheck;
  independent review accepted all 65 rebuilt PDF pages, and final integration verified all source,
  product, and screenshot hashes. Scoped guidance-format and Markdown-link checks passed 111 tests;
  the complete suite passed 1,493 tests.
- Clarify that JSON-quoted formulas are literal only in Workbook and Enter/Replace scalar contexts;
  prose and ordinary Tutorial tables retain narrative formula styling for quoted examples.
- Complete the 12-tutorial rebuild and quality review: 65 PDF pages versus 70 baseline pages, all
  634 list paragraphs compacted, Calc passes 254 comparisons across 13 scenarios, and the full
  suite passes 1,493 tests. Final integration matched all 12 source hashes and 36 artifact hashes.
  Record scope and verification limits in the
  [formatting summary](active_plans/reports/automatic_formatting_summary.md).

### README screenshot rerun

- Refresh both managed README screenshots from the current canonical Caffeine 3 PDF and XLSX. The
  PDF excerpt shows the green formula and compact Fill instructions; the disposable workbook render
  changes print settings only, and all 75 answer cells remain blank. Inspect both WebPs and record
  canonical product/image hashes in [the screenshot receipt](screenshots/README.md). Live Google
  import remains unverified.

### Teaching-quality closeout evidence

- Complete all-12 lesson source comparisons and expert workbook walkthroughs; the final rebuild
  contains 36 artifacts across 70 PDF pages, with matching source hashes, 254 passing Calc
  comparisons across 13 scenarios, and 1,464 passing repository tests at rebuild time. Final
  integration matched all 12 source hashes and 36 artifact hashes against the manifest, and the
  complete suite passed 1,474 tests. Fresh independent review
  accepted all 12 DOCX bundles and 70 PDF pages. A further style-quality review found no blocker
  across 48 source/artifact hashes, four native workbook/DOCX pairs, and 11 critical pages. These
  reviews do not establish student outcomes; Google Docs/Sheets import and live Google calculation
  remain unverified. The README now embeds current PDF and XLSX screenshots; their hashes and
  capture methods are in [the screenshot receipt](screenshots/README.md). Final integration
  acceptance is recorded in [the integration review](active_plans/reports/teaching_integration_review.md). See the
  [teaching quality summary](active_plans/reports/teaching_quality_summary.md) and
  [final style-quality review](active_plans/reports/teaching_final_style_quality.md).
- Clarify in the README that student workbooks retain starting data while leaving answer cells blank.

### Readiness implementation and current evidence

- Complete the focused result-label pagination SPEC review: the renderer meets the adjacent
  same-row, next-column Label/Enter-or-Replace contract; three affected DOCX exports carry
  `keep_with_next` only on the label paragraphs. The referenced standalone SPEC file was absent,
  so the review records the supplied contract and DOCX evidence in
  [the pagination review](active_plans/reports/teaching_pagination_spec.md). Rebuilt PDF visual
  verification remains pending.
- Consolidate the active executable layout and entry points: `make_tutorial.py`, `tutorial_lib/`,
  `tutorial_data/`, and ignored `tutorial_output/`; do not provide old-name aliases. Expand the
  README with a working quick start and links to the installation, usage, authoring, and format
  guides.
- Define the formula I/O boundary: recognized modern function tokens receive `_xlfn.` only for
  XLSX storage and are normalized on readback. This preserves authored formula math and text.
- Record local final-state formula execution separately from offline static checks and Google
  execution. LibreOffice Calc passed 254 independent expected values over 13 scenarios, including
  15 signed Welch probes. Fourteen Google worksheet mappings remain absent and live credentials
  were unavailable; this result is not Google validation.
- Refresh execution evidence after the coordinated rename: 12 lessons and all 36 DOCX/XLSX/PDF
  artifacts were checked. After final whitespace cleanup, the babies t-test DOCX/XLSX/PDF bundle was
  rebuilt from its current source; the source and all artifact fingerprints are current, and its six
  pages were re-rendered and reviewed. All 65 current PDF pages have no blocking visual findings.
  Calc passed 254 comparisons across 13 scenarios, the repository suite passed 1309 tests, and
  integrated implementation/content reviews accepted the result. Archive the completed plan; 14
  Google worksheet mappings remain absent and Google behavior remains unverified.
- Complete source corrections for all 12 lessons after direct original-to-generated
  comparisons; restore Babies task ordering and standalone setup, Microbes narrative and statistical
  boundaries, independently usable Caffeine lessons, and PETase's qualified synthetic Bradford task.
  A fresh visual review found four misleading Caffeine visuals and recurring label/step page splits;
  the source and pagination fixes are rebuilt across 36 current artifacts and 68 PDF pages. Calc
  passes all 254 comparisons across 13 scenarios. Fresh regression review accepted the corrected
  Caffeine figures and pagination; both HCI groups and all 12 workbook walkthroughs are complete.
  The final refresh rebuilt the Babies 1 story fix, renumbered Babies 3's moved substeps, and
  clarified PETase's chart path as Series > Add series. The pre-style source refresh produced 36
  artifacts over 68 PDF pages; Calc passed 254 comparisons across 13 scenarios and the full suite
  passed 1,458 tests. Final comparison found nondeterministic LibreOffice font resolution: identical
  Babies 3 DOCX exports produced three or four pages depending on the Carlito font resolved.
  The user confirmed the Google Docs Normal text, Title, Subtitle, and Heading 1-3 styles, plus PT Sans,
  PT Sans Narrow, and Roboto Mono. Map these styles to titles, optional metadata, parts, steps,
  substeps, and Normal text content. Use direct formatting for instructional emphasis and monospace;
  clear inherited theme font selectors. Render menu paths with bold Roboto Mono and ASCII ` > `
  separators. Require these fonts in the local PDF environment; do not install fonts or download
  fallbacks. Preserve existing sizes, spacing, and margins. The final style-integrated rebuild has 36
  artifacts across 70 PDF pages, current source hashes, 254 passing Calc comparisons across 13
  scenarios, and 1,464 passing repository tests. Repeated Babies 3 exports match in text layout,
  normalized fonts, and all four page pixel hashes. Fresh typography SPEC review accepted all 12
  DOCX/PDF bundles and 70 pages; final integration acceptance is recorded in
  [the integration review](active_plans/reports/teaching_integration_review.md). See the
  [teaching quality summary](active_plans/reports/teaching_quality_summary.md).
- Clarify the review standard: preserve established Babies/Microbes teaching experience and voice,
  correcting verified errors, typos, and format faults with minimal wording changes. Treat Caffeine
  as a draft foundation and complete all three parts as polished standalone classroom lessons.
- Complete focused Fill/layout specification reviews and the all-12 generated-XLSX walkthrough.
  Shared Fill handling reports malformed source formulas through controlled diagnostics; label
  sizing includes quoted formula text such as IF decisions while preserving blank answer cells.
  Final typography SPEC review accepted all rebuilt bundles; subsequent final integration acceptance
  is recorded in [the integration review](active_plans/reports/teaching_integration_review.md), and
  the plan is closed.
  Review reports name ignored `tutorial_output/`
  artifacts as code paths instead of broken links.
- Complete an independent established-teaching SPEC review of the current Babies 1-3 and Microbes
  1-5 DOCX/PDF/XLSX bundles. The report records direct source-to-output evidence, formula-free
  starting workbooks, and fresh renders of all current PDF pages; 45 pages were reviewed.

### Behavior or Interface Changes

- Apply the final user-selected layout: `make_tutorial.py`, `tutorial_lib/`, `tutorial_data/`,
  and default generated `tutorial_output/`. Move tracked sources with Git, retain prior staged
  edits, and move generated evidence intact. Update imports, discovery, defaults, active commands,
  documentation links, and readiness ownership without compatibility aliases. Historical changelog
  entries and archived plans retain their snapshot names. Existing generated manifest contents
  remain historical until the final rebuild.

### Readiness Contract and Status Reconciliation

- Clarify in the specification and authoring guide that labels are either seeded for inspection or
  left blank for student `Label` actions; preserve the existing warning for identical repeated
  assignments. Reject label-only instruction items from parsed structure, including cases where an
  empty child would otherwise obscure the missing instruction. Keep the existing authoring schema.
- Set the readiness output contract to freeze panes at A2, use a 12-character minimum width for
  columns including blank entry cells, and include a native Word PAGE footer field. Keep number
  formats as explicit authored menu tasks when needed; do not infer arbitrary styles or promise full
  spreadsheet formatting fidelity.
- Replace misleading worked examples with native editable tables while retaining original assets.
  Record focused preproduction decisions without adding compatibility paths or stubs.
- Earlier ledger status snapshot was superseded by current review evidence below and in the active
  readiness plan. Content, compiler, export, local formula execution, fresh builds, and visual review
  are complete; final repository-suite and closeout remain open.
- Verify documentation links with `tests/test_markdown_links.py` (71 passed) and run the repository
  character check on each edited Markdown file.

### Plan Scope and Execution

- Expand the tutorial converter plan from two pilots to all three Fried Foods/babies tutorials,
  five Microbes tutorials, and the three-part Dr Caffeine set; repair PETase with an explicitly
  synthetic Bradford dataset because the legacy source contains unrelated Microbes material.
- Add [tutorial_execution_ledger.md](archive/tutorial_execution_ledger.md) to track
  foundation, implementation, migration, and review work. Live Google calculation was attempted
  but unavailable without credentials; Google Docs/Sheets import remains unverified.
- Keep completion agent-led: focused DOCX/XLSX behavior checks and PDF visual assessment establish
  local evidence; Google import is optional and reported only with observed evidence. Agents resolve
  scientific migration issues from authoritative sources and document corrections.

### Additions and New Features

- Add [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) defining the single-source Markdown tutorial/workbook
  format, list actions, worksheet tables, numbering, validation, DOCX/XLSX/PDF outputs,
  simple XLSX import, and Google import acceptance boundaries.
- Add [tutorial_converter_plan.md](archive/tutorial_converter_plan.md) with component
  contracts, six implementation milestones, dependencies, verification, risks, and migration scope.
- Implement source-located compilation, static reference/assignment checks, native XLSX import
  and export, editable DOCX, LibreOffice PDF conversion, and staged three-output CLI bundles.
- Migrate all 12 lessons and extracted original images. Correct mean-test assumptions, signed
  t-test tails, Welch variance handling, F-test directions, ANOVA group sizes, regression ranges,
  coefficient ordering, and unsupported narrative conclusions; document provenance and corrections.
- Add independent SciPy/NumPy expectations and optional real Google Sheets developer tooling.
  Cover 12 lessons, 13 scenarios, 254 final formula values, and 8 synthetic directional checks.

### Implementation Documentation

- Start the [student publishing implementation ledger](active_plans/student_publishing_implementation.md)
  for worksheet edits, DOCX/XLSX presentation, and ASCII/template authoring with mismatch validation.
  Reviews, the full build, formula calculation, and visual verification remain pending.
- Add [INSTALL.md](INSTALL.md), [USAGE.md](USAGE.md), and [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md)
  for the current install and CLI workflow, plus a concise README description. Update
  [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) to reflect the available CLI and autonomous local completion
  policy. Keep the active execution ledger aligned with observed files and current workstream status.
- Add [TUTORIAL_CATALOG.md](TUTORIAL_CATALOG.md) with indexed links to all 12 sources, build outputs,
  and explicit synthetic PETase provenance. Consolidate observed evidence in
  [implementation_validation.md](active_plans/reports/implementation_validation.md).

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.

### Decisions and Failures

- Correct the voice-restoration scope after direct original-to-generated comparisons found that
  migrated lessons had been rewritten into action logs. Create
  [the restoration plan](active_plans/instructional_voice_restoration.md): preserve original wording,
  headings, humor, and compact numbered groups; keep only necessary technical/scientific changes;
  complete missing Caffeine material without replacing its good prose. Tests and prior approvals do
  not establish original-voice fidelity.
- Record the user's list-first authoring and Google import priorities in
  [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). Record the planned seed-data/student-action separation and
  source-located validation model in [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md). Keep the original
  artifacts and adjacent projects unchanged.

### Developer Tests and Notes

- Document the macOS sandbox restriction for every direct or indirect LibreOffice invocation,
  including PDF exports, conversion tests, and ODP imports; use repository scripts outside it.
- Validate the final naming layout with CLI help, a `tutorial_lib.compiler` import, explicit
  `pyflakes devel/validate_libreoffice.py`, and the full repository suite (1305 passed).

- Earlier naming experiment (superseded by the final layout recorded above): rename the application
  package from `tutorial_lib/` to `sheetlesson/` while retaining the
  `tutorial.py` executable, so shell completion distinguishes the library from the command.
  Update active imports, developer tools, tests, documentation, and the execution ledger; do not
  provide a compatibility alias. Compiler quality review accepted the secure XML parsing,
  flattened helper imports, malformed-formula diagnostics, and literal payload handling; record
  its seven behavior tests and 12 lint checks in the ledger. XML behavior review accepted 12 tests,
  pending hygiene review; workbook import checks passed 137 and 66 checks.
- Extend the repository bootstrap `PYTHONPATH` with both the repository root and `devel/` so the
  root package and shared flat developer-tool helpers import under the required sourced environment.
  Keep the extension after loading `~/.bashrc`, which clears `PYTHONPATH`.
- Reject converter output that has a PDF signature but cannot be parsed as a document with pages.
  Use the declared `pypdf` dependency before publication and retain the previous bundle on failure.
  The focused build tests pass with a regression for a successful converter writing only `%PDF-`.
- Document the macOS agent lane: invoke builds using the LibreOffice wrapper with
  `sandbox_permissions="require_escalated"`; human terminal commands remain ordinary commands.
- Google Docs/Sheets import verification has not been performed. Documentation checks for the
  implementation-facing updates passed local link and ASCII checks. The oversized human-guidance
  bullet is split into focused entries. Existing non-ASCII content in two legacy sources remains
  preserved; report it separately from changed-source verification.
- Build all 12 bundles and visually assess the initial 87 PDF pages. Repair nested-list and table
  pagination findings; final rebuilt-PDF verification remains in progress. Record exact evidence in
  [pdf_validation.md](active_plans/reports/pdf_validation.md).
- Prepare all 13 Sheets cases with independent expectations, then attempt authorized live execution.
  Missing ADC returns exit 2 and creates no Google files; no live calculation or import is claimed.
- Preserve original archival Unicode through an explicit ASCII-check scope rule for
  `2025_Artifacts/**` in the existing layered test registry. New tutorials, code, and documentation
  remain checked; all original SHA fingerprints match and the scoped ASCII checks pass (120).
- Earlier snapshot only: source-edit checks, failed-build preservation, and 12 PDF reviews were
  recorded with the then-current 1272-test suite. The later coordinated rename and readiness work
  require fresh verification; see current reports under `active_plans/reports/`.
- Historical review rasters and verification paths were moved with the selected output directory.
  Current evidence is under `tutorial_output/verification/`.
