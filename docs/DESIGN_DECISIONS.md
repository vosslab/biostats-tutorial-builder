# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

### Default spreadsheet numerical display

**Decision.** Apply `0.000` to numerical content and blank work cells in generated spreadsheets.

**Why.** Authors get a consistent three-decimal display without extra source syntax.

**Consequence.** Preserve stored values and student-entered calculations. Other displays remain
ordinary spreadsheet formatting tasks.

**Owner.** [tutorial_lib/workbook.py](../tutorial_lib/workbook.py).

### Visual syntax reference

**Decision.** Pair copyable Markdown excerpts with cropped native output from one runnable
documentation example.

**Why.** Students can see the formatting a convention produces before using it in a lesson.

**Consequence.** Refresh the example captures when rendering changes; show supplied worksheet labels
and blank student calculations separately from completed demonstrations.

**Owner.** [FORMATTING_GUIDE.md](FORMATTING_GUIDE.md).

### Temporary Graphify Cargo reconciliation

**Decision.** Reconcile exact Cargo aliases with their AST package twins before
reclustering; verify the resulting IDs against Graphify's loaded graph before writing.

**Why.** Graphify 0.9.80 compares normalized candidate counts with raw JSON counts,
and its original-link export otherwise drops links still pointing to removed aliases.

**Consequence.** Preserve all link records and the active shrinkage guard. Keep the
correction in one removable function; already reconciled upstream output is a no-op.

**Owner.** `normalize_cargo_twins` in
[devel/graphify_prune_tests.py](../devel/graphify_prune_tests.py)
and [devel/graphify_map_repo.py](../devel/graphify_map_repo.py).

Write each decision as a level-three heading with these four fields. `Owner` names the
authoritative code or contract document, rather than a person.

```markdown
### <decision title>

**Decision.** <the durable direction>

**Why.** <the reason it was chosen>

**Consequence.** <the constraint a future change preserves>

**Owner.** <the authoritative code or contract doc>
```

### Single-source tutorial and workbook contract

**Decision.** Use one Markdown file with a Workbook section of GFM tables and a Tutorial
section of list-authored instructions. Generate native DOCX and XLSX, then PDF from DOCX.

**Why.** Writers prefer lists for instructions and can represent these simple spreadsheets
as tables without maintaining a separate formula registry or workbook manifest.

**Consequence.** Workbook tables define initial values; student instruction actions retain
expected assignments for validation without filling student answers in the XLSX. Generated
files do not synchronize edits back to Markdown.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

### Required reflection question list

**Decision.** Require one ordinary numbered `### Reflection Questions` list under Workbook in each
source. Generate an appended DOCX reflection section and a separate workbook tab per source, using
matching literal, editable question identifiers and answer space. Use Normal text for those IDs and
retain native Heading styles for headings. Normalize the source ordered list to start at 1 regardless
of its authored start value. In shared builds, name tabs `Part {resolvedpart} Reflection`.

**Why.** A single authored list keeps question wording in the source of truth while Tutorial prose
can tell students when to answer each question.

**Consequence.** Authors use no parameters, citation IDs, or automatic activity associations.
Shared builds preserve one tab per source, named with spaces as in `Part 2 Reflection`. Resolve
each source using its single unique explicit Part identity, or its source position only when it
has no unique explicit Part identity. Duplicate resolved identities across sources fail before
publication rather than falling back to source position. DOCX and workbook identifiers remain
visible editable Normal text;
Word automatic list numbering and numbering fields do not generate them. Starting at 1 is author
guidance, while the compiler normalizes the source list and does not reject a different Markdown
start value.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

### Semantic actions stay attached to authored prose

**Decision.** Encode spreadsheet actions as semantic links around the natural student-facing words
and formulas already in a paragraph. Preserve ordinary GFM numbered and nested list grouping; do
not require bold action labels at the start of every list item.

**Why.** Action meaning needs to reach validation and the workbook without turning an instructional
paragraph into an operation log or duplicating a value or formula in visible text.

**Consequence.** Use destinations such as `[**Sample Mean**](label:D5)`,
`[=AVERAGE(B2:B26)](enter:E5)`, `[Select C2:C26](select:C2:C26)`, and
`[drag down](fill:C2:C26)`. The renderer shows the link text and hides the semantic destination;
multiple actions may be attached in source order within one paragraph. Legacy bold action openings
remain supported. Scalar decoding removes formatting wrappers from assigned values while preserving
authored emphasis in rendered prose; a same-instruction mention of its write target is not treated
as a missing input, while formula dependencies remain validated in action order.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md), [semantic_bindings.py](../tutorial_lib/semantic_bindings.py),
and [compiler.py](../tutorial_lib/compiler.py).

### ASCII source with rendered scientific typography

**Decision.** Lint authored Markdown files as ASCII and reject numeric character references while
allowing readable named scientific entities and ordinary `sub` and `sup` markup.

**Why.** BIOL 318 authors should be able to write source with an ordinary keyboard and read it
without memorizing numeric encodings. Renderers can still present scientific notation cleanly.

**Consequence.** File compilation reports source locations for pasted Unicode and numeric entities.
The parser and renderers continue accepting Unicode in in-memory callers, which keeps output and
test internals independent from the authoring-file contract.

**Owner.** [source_text.py](../tutorial_lib/source_text.py) and
[TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

### Restore authored Markdown boundaries

**Decision.** Preserve literal scalar payloads, authored emphasis, paragraph-terminal Markdown hard
breaks, and informational headings such as `Step-by-Step Tutorial:` at the parser/rendering
boundary. Require genuine structural numbering before treating a `Step` prefix as syntax.

**Why.** Source recovery exposed cases where parsing changed visible wording or formatting, or
misdiagnosed ordinary prose as malformed structure. Those repairs must preserve the authored lesson
while keeping formula-order and structural validation meaningful.

**Consequence.** Decode binding values separately from their Markdown presentation; restore a
terminal backslash-newline as a hard break only when the source line contains that break; retain
literal backslashes in code and scalar payloads; and keep hyphenated informational headings as prose.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md), [parser.py](../tutorial_lib/parser.py),
[semantic_bindings.py](../tutorial_lib/semantic_bindings.py), and [docx_inline.py](../tutorial_lib/docx_inline.py).

### Keep short instructional units together in DOCX

**Decision.** Use native DOCX `keepNext` for an immediately adjacent semantic label and its
same-row, next-column entry. A numbered instruction may place that entry in its first nested list
item. Keep the final body paragraph with its predecessor when both are consecutive paragraphs, and
trim a redundant hardbreak at the end of a list paragraph.

**Why.** Page breaks should not separate a spreadsheet result label from the next instruction, add
blank lines between compact list items, or strand a short closing prompt by itself. Later formula
explanations remain free to move independently.

**Consequence.** Match the adjacent list-token structure and validated cell targets; do not infer
page numbers or keep a whole list branch together. Preserve internal hardbreaks and the authored
paragraph text. Terminal paragraph pairing applies only when the final two document blocks are both
paragraphs.

**Owner.** [docx_renderer.py](../tutorial_lib/docx_renderer.py) and
[test_tutorial_docx.py](../tests/test_tutorial_docx.py).

### Shared meaning and explicit validation limits

**Decision.** Parse source once into a source-located semantic model consumed by validators
and native output renderers. Track static references and assignment history without evaluating
spreadsheet formulas or claiming statistical correctness.

**Why.** The legacy templates contain blank answer cells, and formula/range consistency
cannot be established merely by checking existing workbook formulas.

**Consequence.** Unsupported formula analysis remains visible as a coverage warning. Use
adjacent projects as implementation references, without importing their application schemas
or depending on their local checkouts.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) and
[tutorial_converter_plan.md](archive/tutorial_converter_plan.md).

### Readable PDF before bundle publication

**Decision.** Reopen LibreOffice output with `pypdf` in strict mode and require a nonempty page tree
before publication.

**Why.** A converter can report success while producing truncated output with a valid PDF header.
The Python reader checks document structure without adding a separate system executable.

**Consequence.** Invalid output fails the staged build and preserves the previous published bundle.
This check does not claim rendered layout or visual review.

**Owner.** [pdf_export.py](../tutorial_lib/pdf_export.py).

### Independent scientific expectations

**Decision.** Keep numerical curriculum checks in developer tooling using SciPy and NumPy,
separate from static source validation and the optional real Google Sheets runner.

**Why.** Formula syntax and reference consistency cannot establish the statistical model,
tail direction, or numerical answer. A locally computed expectation also cannot establish
Google Sheets compatibility.

**Consequence.** Compare live calculated values against independent expectations when credentials
exist. Report dry runs, unavailable credentials, and actual Google execution separately.

**Owner.** [tutorial_oracles.py](../devel/tutorial_oracles.py) and
[GOOGLE_SHEETS_VALIDATION.md](GOOGLE_SHEETS_VALIDATION.md).

### Shared workbook releases

**Decision.** A normal build accepts one or more Markdown sources. A multi-source build writes one
shared workbook and separate DOCX/PDF files for each source.

**Why.** Dr. Caffeine is assigned as three compact documents that work through the same six-tab
workbook. Keeping the source files separate preserves the ordinary authoring workflow.

**Consequence.** All sources must declare compatible sheets; conflicting supplied cells stop
publication. The bundle records every source and output in one manifest.

**Owner.** [build.py](../tutorial_lib/build.py) and [make_tutorial.py](../make_tutorial.py).

### Repaired PETase teaching data

**Decision.** Present the PETase lesson as an illustrative Bradford calibration using explicitly
synthetic standards and unknowns, retaining recoverable narrative and original images.

**Why.** The linked legacy workbook contains unrelated microbial diversity data and supplies no
original Bradford measurements.

**Consequence.** Keep synthetic provenance visible. Interpret Bradford as total protein relative
to a standard, rather than PETase-specific abundance, activity, or fermentation productivity.

**Owner.** [petase_1_linear_regression.md](../tutorial_data/petase_1_linear_regression.md) and
[petase_migration.md](active_plans/reports/petase_migration.md).

### User-selected tutorial layout

**Decision.** Use `make_tutorial.py` for the executable, `tutorial_lib/` for the application
package, `tutorial_data/` for authored lessons and assets, and `tutorial_output/` for default
generated bundles and verification evidence.

**Why.** The latest explicit user instruction selects this coordinated layout and supersedes
the earlier distinct-prefix naming decision.

**Consequence.** Update imports, command examples, source discovery, and default paths together.
Retain existing generated evidence under the renamed ignored output directory; rebuild manifests
after the rename before claiming current artifact provenance. Provide no old-name aliases.

**Owner.** [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md), [tutorial_lib](../tutorial_lib/),
[tutorial_data](../tutorial_data/), and [make_tutorial.py](../make_tutorial.py).

### Focused readiness contracts

**Decision.** Keep the authored schema unchanged while enforcing label ownership and rejecting
instruction items that contain only bold, colon-terminated labels and no substantive continuation,
valid action, nonempty fence, or substantive descendant.

**Why.** The 12-lesson readiness review exposed these gaps in existing source and AST handling; the
current `Label`, `Enter`, `Select`, and `Choose` actions already express the needed work.

**Consequence.** A seeded label is for inspection; a student `Label` assignment starts blank.
Identical repeated assignments continue to warn. An empty child does not make its parent
instruction substantive. Do not add directives or compatibility layers for these cases.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) and the compiler in
[tutorial_lib/compiler.py](../tutorial_lib/compiler.py).

### Targeted workbook and document readability

**Decision.** Freeze worksheet panes at `A2`, keep columns at least 12 characters wide, and add a
native Word `PAGE` footer field. Use the three-decimal default described above; teach other number
formats as explicit menu tasks when a lesson requires them.

**Why.** These defaults make entry worksheets easier to follow while preserving simple authored
tables and an honest boundary around native spreadsheet formatting.

**Consequence.** Do not infer arbitrary formats from cell values or claim full Excel/Sheets
formatting fidelity. Replace misleading worked-example screenshots with native editable tables;
preserve original image assets.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md),
[tutorial_lib/workbook.py](../tutorial_lib/workbook.py), and
[tutorial_lib/docx_styles.py](../tutorial_lib/docx_styles.py).

### XLSX formula token serialization

**Decision.** Add the OOXML `_xlfn.` prefix only to recognized modern formula-name tokens when
writing XLSX, and remove it on readback only for recognized tokens.

**Why.** Modern spreadsheet functions otherwise fail to calculate in some engines even though
the authored formula is valid. Prefixing the full formula or rewriting its math would alter the
source semantics.

**Consequence.** Keep authored whitespace, function arguments, strings, references, and
mathematical operations unchanged. Leave unknown functions untouched and report their validation
coverage honestly. Formula normalization is a storage-boundary operation, not calculation.

**Owner.** [formula_io.py](../tutorial_lib/formula_io.py) and [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

### Repository and developer import paths

**Decision.** Source both the repository root and `devel/` from `source_me.sh` after it loads
the user's shell configuration.

**Why.** The CLI and tests import the root `tutorial_lib` package, while developer tools and tests
share flat support modules from `devel/`.

**Consequence.** Keep the paths after `.bashrc` because it clears `PYTHONPATH`; run repository
Python commands through `source source_me.sh` so package and support imports resolve consistently.

**Owner.** [source_me.sh](../source_me.sh).

### Preserve archival source characters

**Decision.** Scope the ASCII-compliance check to exclude imported `2025_Artifacts/**` through
the existing layered test registry. Keep new tutorials, application code, and documentation checked.

**Why.** Historical exports contain Unicode characters that must remain unchanged as source
evidence. Editing them solely to satisfy a new implementation's hygiene run would damage provenance.

**Consequence.** This is an explicit archival scope rule, not an ASCII exception for new work.
Source fingerprints verify the original artifacts remain intact.

**Owner.** [conftest.py](../tests/conftest.py).

### Fill-down action and label sizing

**Decision.** Author a spreadsheet fill as one `Fill` action such as `Fill C2:C26: Down`; the range
includes its seeded first row, supports downward filling only, and expands through blank student cells.
Translate with the spreadsheet reference translator and report malformed source formulas through
controlled diagnostics. Estimate workbook widths and wrapping from authored labels and quoted
formula text, including IF decisions, while leaving answer cells blank.

**Why.** Students should enter a formula once and fill the intended range efficiently, while authored
labels and decision text provide evidence for estimating readable dimensions before answers exist.

**Consequence.** Keep this action distinct from repeated `Enter` instructions. Keep student answers
blank and treat dimensions as estimates, not font measurements or calculated formula results.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md), [compiler.py](../tutorial_lib/compiler.py), and
[workbook.py](../tutorial_lib/workbook.py).

### Standalone lesson numbering

**Decision.** Number each independently usable Caffeine lesson from Part 1. Caffeine 1 uses Steps 1-5;
Caffeine 2 uses Steps 1-7 with substeps 3.1-3.2 and 6.1-6.4; Caffeine 3 uses Steps 1-7.

**Why.** The three lessons are separate classroom materials, not sequential parts of one document.

**Consequence.** Preserve semantic Part, Step, and Substep markers in each source and render numbering
from that source structure; do not number the lessons as Parts 1, 2, and 3.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) and
[docx_numbering.py](../tutorial_lib/docx_numbering.py).

### DOCX Google Docs style mapping

**Decision.** In generated DOCX, use Google Docs' Normal text, Title, Subtitle, and Heading 1-3
paragraph styles. Map Title to document titles, Subtitle to optional metadata, and Heading 1-3 to
parts, steps, and substeps. Use Normal text for body, lists, formulas, quotes, tables, and the page
footer. Directly format emphasis, code, cell references, menus, and links. Set PT Sans for body text,
PT Sans Narrow for compact table text, and Roboto Mono for formulas, cells, and menus.

**Why.** LibreOffice exported byte-identical DOCX packages with different pagination when Carlito
font files with mismatched versions resolved on the host. The user confirmed these fonts and six
paragraph styles are available in Google Docs, matching the intended import workflow.

**Consequence.** Restrict emitted DOCX paragraph references to the six Google Docs styles and set font
names explicitly so PDF pagination does not depend on inherited theme fonts. Unused stock definitions
may remain in the template. Do not rely on custom tutorial paragraph or character styles; preserve
instructional emphasis through direct formatting. Keep XLSX font styling unchanged. Keep existing
point sizes, spacing, and margins unless rendered evidence requires a focused change.

**Owner.** [docx_styles.py](../tutorial_lib/docx_styles.py) and the PDF conversion contract in
[TUTORIAL_SPEC.md](TUTORIAL_SPEC.md).

### Automatic formula roles and paragraph spacing

**Decision.** Recognize formulas from Markdown structure and context, then pass a semantic formula
role to the DOCX renderer for Roboto Mono and dark-green (`188038`) presentation. Keep formula
recognition separate from rendering styles. Use 2 pt after, 0 pt before, and single spacing for list
paragraphs; retain 6 pt after and 1.08 line spacing for body paragraphs.

**Why.** Authors should be able to enter ordinary spreadsheet formulas without presentation markup,
while prose equations, URLs, and scalar literal text retain their intended meaning. Semantic roles
let output formats share the interpretation without embedding DOCX/PDF presentation choices in the
parser.

**Consequence.** Bare `=...` formulas are accepted in `Enter` and `Replace` payloads; code spans and
fences remain supported, and formula text is preserved. JSON-quoted `=...` is literal in Workbook
and action scalar contexts. Narrative prose and ordinary Tutorial tables retain narrative semantics,
so a quoted formula example keeps its formula role. Formula classification is limited to clear
spreadsheet contexts and does not introduce a new authoring language. Keep the standard GFM `\|`
escape for a literal table pipe. The XLSX student starting content remains unchanged.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md), [compiler.py](../tutorial_lib/compiler.py), and
[docx_styles.py](../tutorial_lib/docx_styles.py).

### ASCII menu separators

**Decision.** Continue accepting `>` and the Unicode right arrow as `Choose` path delimiters. Render
bold Roboto Mono segments with ASCII ` > ` separators.

**Why.** The selected three-font palette does not include a separate arrow font, and the ASCII menu
separator is already used in authored lessons.

**Consequence.** Normalize either accepted source delimiter to ASCII ` > ` in DOCX; do not require a
fourth font or arrow-glyph fallback.

**Owner.** [TUTORIAL_SPEC.md](TUTORIAL_SPEC.md) and
[docx_inline.py](../tutorial_lib/docx_inline.py).

### Original lesson voice and final-output evidence

**Decision.** Use the original lesson as the authority for sound wording, headings, humor, and
numbered grouping. Adapt content only for verified technical or scientific corrections, current
workbook destinations/data, or missing Caffeine instruction. Treat source review, generated-page
review, workbook walkthroughs, calculation checks, and integration fingerprints as distinct
evidence.

**Why.** Passing tests and successful builds did not catch a student-visible shift from explanatory
prose to repeated action labels. A source correction is useful only when the current generated
materials preserve it, and expert review does not establish student outcomes or Google behavior.

**Consequence.** Keep dated intermediate reports as historical records; the consolidated ledger
must link to the evidence and list remaining checks. Do not mark the active restoration complete
until a fresh integration review accepts the exact current sources and artifacts. State Google
Docs/Sheets validation and student-study limits explicitly.

**Owner.** [instructional voice restoration plan](active_plans/instructional_voice_restoration.md)
and its [review ledger](active_plans/reports/voice_restoration_summary.md).

### Student publishing edit contract

**Decision.** Use native Excel A1 references and the existing action formats. Keep the starting
workbook separate from the ordered learner activities. Worksheet edits make explicit structural
changes through preview and write modes while preserving authored words; the compiler does not
write tutorial prose.

**Why.** Authors need to revise workbook structure and data size without losing lesson text or
repairing dependent references by hand. A distinct starting workbook and activity sequence clarifies
what readers receive and what they do.

**Consequence.** Preview structural worksheet edits before writing them, and maintain references
automatically after columns, ranges, or data size change. Keep native A1 notation and existing
actions as the source contract.

**Owner.** [student publishing implementation ledger](active_plans/student_publishing_implementation.md)
and the existing tutorial source and compiler contracts.

### Native DOCX alignment and indentation

**Decision.** Use native DOCX paragraph styles for heading indentation and paragraph alignment,
including step headings with zero left indent and a 0.2-inch body indent. Estimate natural wrapped line counts from
font metrics and usable paragraph width; justify prose estimated to exceed two lines. Keep headings,
formula displays, hard-break paragraphs, and table entries left aligned, except the corrected formula
introduction, which remains justified.

**Why.** Native paragraph formatting survives Google Docs import and supports both relative heading
placement and full justification without relying on fixed spaces or direct-run alignment.

**Consequence.** Step headings sit left of body paragraphs, with varied heading indentation. Exact
wrapping can change after import, so the estimate is not a claim of live Google Docs verification.

**Owner.** [DOCX styles](../tutorial_lib/docx_styles.py), [DOCX renderer](../tutorial_lib/docx_renderer.py),
and the [student publishing implementation ledger](active_plans/student_publishing_implementation.md).



### Show three instructional views

**Decision.** Present the generated lesson document, supplied starter workbook, and completed
calculation output as distinct views.

**Why.** Readers need to distinguish what the author writes, what a student receives, and what a
completed calculation looks like.

**Consequence.** Label the starter and completed examples clearly; do not present the completed
calculation copy as the student starter.

**Owner.** [Student guide](AUTHORING_GUIDE.md), [course screenshot receipt](screenshots/README.md),
and the published course examples.

### Refresh captures with one command

**Decision.** Use one repository command to refresh the documentation capture sets after style changes.

**Why.** Style changes should be visible in the examples without manual, coordinate-based recropping.

**Consequence.** Use semantic document headings and workbook ranges as capture anchors, preserve
capture provenance in receipts, and run the rendering workflow outside the macOS sandbox because it
invokes LibreOffice. Keep capture helpers in the existing shared implementation rather than adding
a separate support namespace.

**Owner.** [Documentation refresh command](../devel/refresh_documentation.py),
[shared capture helpers](../devel/capture_readme_artifacts.py), and [usage guide](USAGE.md).

### Keep guide examples as literal Markdown

**Decision.** Write the guides as ordinary GitHub Markdown. Display snippets in fences and keep
placeholders explicitly labeled as non-runnable instructional notation. Export the three Parts
with the workbook from [authoring_features.md](examples/authoring_features.md).

**Why.** Authors need exact, copyable syntax alongside actual output. The guide's fences must stay
literal even when the guide itself is compiled for native review.

**Consequence.** The refresh command supplies the export workbook separately. The source guides are
not direct compiler inputs. Inspect GitHub rendering separately from native PDF output.

**Owner.** [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) and
[refresh_documentation.py](../devel/refresh_documentation.py).

### Size blank response panels by role

**Decision.** Give authored interpretation response rows a shared minimum total height of eight lines
or 123 points, while leaving taller authored regions unchanged.

**Why.** Learners need room for a complete written interpretation without losing intentionally larger
response areas.

**Consequence.** Apply the minimum across the authored rows that make up the response panel; keep the
response cells blank.

**Owner.** [Workbook renderer](../tutorial_lib/workbook.py) and
[response panel guidance](TUTORIAL_SPEC.md).

### Repair worksheet edits at their owner

**Decision.** Repair compiled table ownership and source-coordinate updates once in the worksheet
editor, including table movement, `At` blank-line parsing, and legacy fenced formulas.

**Why.** These failures affect the editor's own workbook/source synchronization boundary.

**Consequence.** Keep a few focused behavior checks at that boundary; do not add downstream correction
paths.

**Owner.** [Worksheet editor](../tutorial_lib/worksheet_edit.py) and
[worksheet maintenance instructions](USAGE.md#maintain-a-worksheet-after-a-layout-decision).


### Keep DOCX table headers with their first body row

**Decision.** Set `keep_with_next` on header-cell paragraphs so a table header cannot be stranded
at the bottom of a page without its first body row.

**Why.** Native PDF review found the Part 1 instructional table's header on page 5 while all five
data rows were pushed off the page, making the table content disappear from the rendered document.

**Consequence.** Apply this at the DOCX table renderer and verify the built PDF. The final native
review confirms all five rows together and all 106 cells across six tables are present.

**Owner.** [DOCX renderer](../tutorial_lib/docx_renderer.py); see the
[native visual report](active_plans/reports/pipeline_quality_followup_visual.md).

### Visual reference for original student tutorials

**Decision.** Make the authoring guide the entry point for BIOL 318 students who have completed
several tutorials. Teach document formatting, workbook construction, and build/refine through
copyable source and native output crops. Retain the six topic references and keep worksheet-edit
utilities optional.

**Why.** Students need tools to express their own scenarios and instructional approaches. The prior
Roots checkpoint progression taught a predetermined lesson and basic spreadsheet/statistics work.

**Consequence.** Roots demonstrates formatting only. One feature source supplies reusable captures.
Instructor excerpts retain their wording. Compiler checks remain technical; scientific and teaching
quality are author/instructor judgments. The student hub is consolidated into the authoring guide.
Earlier checkpoints remain examples rather than a required path.

**Owner.** [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md),
[FORMATTING_GUIDE.md](FORMATTING_GUIDE.md), and
[authoring_features.md](examples/authoring_features.md).

### Preserve prose during worksheet edits

**Decision.** Recognize standalone prose column references by uppercase spreadsheet notation, and
pair a Fill link's displayed range with its original semantic target before changing either.

**Why.** The independent guide walkthrough exposed ordinary `column is` becoming `column IS`
and a resized fill target diverging from its visible range. These are source-integrity defects,
not acceptable limitations of optional tooling.

**Consequence.** Preserve ordinary wording, keep coordinated references consistent, and retain the
existing compile-before-write and unchanged-source checks. This applies ASVS 2.2.1 functional
validation and 2.2.3 consistency of related values without introducing a new workflow.

**Owner.** [worksheet_edit.py](../tutorial_lib/worksheet_edit.py).
