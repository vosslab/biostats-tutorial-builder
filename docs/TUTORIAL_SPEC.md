# Tutorial specification

Status: active implementation and readiness review, 2026-10-22. Earlier implementation and
migration evidence applies to its recorded snapshots; current readiness work and closeout are tracked
in [tutorial_readiness_plan.md](active_plans/archive/tutorial_readiness_plan.md).

## Product contract

This repository supports open pedagogy and Student-Generated Content. Its authors write original
biology tutorials for classmates in one plain-text file, designing both the lesson and the workbook. The compiler maintains formatting and supported technical standards; authors and instructors
judge the scientific content and instructional quality. Start with [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md)
for visual examples; this specification defines the technical contract.

One authored Markdown file contains list-authored instructions and table-authored workbook data.
A single-source build produces a DOCX tutorial, an XLSX student workbook, and a PDF exported from
that DOCX through LibreOffice. A multi-source build produces one DOCX and PDF for each source plus
one compatible shared XLSX workbook. The editable files target Word, Excel, and Google Docs/Sheets
presentation. Uploading or importing files to Google services is always outside this workflow.
HTML output is outside the initial scope.

The Markdown file is the source of truth after migration. DOCX, XLSX, and PDF are generated outputs.
Local image companions are allowed; single-source means one content specification, not that every
image must be embedded in its text. Editing generated documents does not update the Markdown.

The first release supports simple teaching workbooks: rectangular data, labels, blank entry cells,
and scalar formulas. It does not promise arbitrary Excel workbook fidelity or live Google sync.

## Authoring and source-text contract

Authors make the spreadsheet design decisions: where data and calculation tables go, what labels
and formulas mean, and what learners must construct. The Workbook section is the student starting
state; Tutorial actions describe work students perform and remain blank in generated workbooks.
The renderer may add a shared professional presentation system, including color, typography,
borders, shading, spacing, and formula emphasis, without changing those learning activities.

Active lesson files use ASCII source text. Straight keyboard punctuation is the default. Readable
named entities such as `&alpha;` and ordinary HTML `sub` and `sup` tags are allowed. Unicode source
characters and numeric character references are source errors when linting a file; this rule keeps
student editing simple while allowing the renderer to produce styled output. In-memory compiler
calls retain Unicode support for parser and renderer tests.

Semantic action links keep an instruction and its executable target together. In explicit action
clauses of the form `In cell C2, enter ...`, the visible destination must agree with the link
target. The check is intentionally narrow: it does not treat every prose cell mention or a formula
input reference as a destination.

## Complete minimal example

This example uses two illustrative observations, not the original full teaching dataset.
The statistics cells are initially empty. Their assignments are instructions for students.

````markdown
# Comparing two hospitals

## Workbook

### Sheet: Hospital comparison

| Infant | Fried foods | Green veggies |
| --- | --- | --- |
| 1 | 9.56 | 9.16 |
| 2 | 8.88 | 8.85 |

#### At: F1

| Statistic | Fried foods | Green veggies |
| --- | --- | --- |

## Tutorial

### Part 3: Compare birth weights

- **Worksheet:** Hospital comparison

Compare birth weights at the two hospitals.

#### Step: Calculate sample means

- **Label F2:** Sample Mean
- **Enter G2:** `=AVERAGE(B2:B3)`
- **Enter H2:** `=AVERAGE(C2:C3)`
- **Compare:** Examine the values in `G2` and `H2`.

#### Step: Create a chart

##### Substep: Select the data

- **Select:** `B1:C3`

##### Substep: Insert the chart

- **Choose:** Insert > Chart
````

The output contains Part 3, Step 1, Step 2, Substep 2.1, and Substep 2.2. The document renders
substep labels as `2.1: Select the data`, without the word Substep. The workbook contains the two
tables at A1 and F1; F2:H2 remain blank but are visibly identified as student entry cells.

## Document structure

- Require exactly one H1 title, one H2 `Workbook`, and one H2 `Tutorial`, in that order.
- Permit ordinary introductory prose after the title; include it before the tutorial in DOCX.
- Treat reserved headings as structural only when parsed as headings, never inside code fences.
- Require at least one worksheet and one tutorial part. Empty scaffold parts are lint errors until
  filled; creating a scaffold does not claim that it is buildable.
- Restrict the Workbook section to worksheet declarations, metadata, tables, and the required
  reflection-question list. Report other unrecognized content rather than silently dropping it.
- Require exactly one `### Reflection Questions` heading under Workbook, with at least one ordinary
  ordered-list question. The compiler normalizes source list numbering to begin at 1, regardless of
  the Markdown list's authored start value; add no heading parameters.
- Exclude Workbook declarations, tables, and the authoritative reflection list from the DOCX/PDF.
  Repeat each full reflection question in its relevant Tutorial prose; do not append a generated
  reflection section to the DOCX. A table
  intentionally included in Tutorial is an ordinary document table and does not populate cells.
- Keep reflection questions in one ordered Workbook list. Authors use ordinary Tutorial prose to
  indicate when students should answer each question. A matching identifier, exact question, and
  answer-tab destination render as an inline shaded callout. Do not add a new reflection directive
  or associate questions with headings automatically.
- Use Markdown syntax parsing, not whole-document regular-expression replacement. Preserve source
  locations, list nesting, inline formatting, and formula text across semantic classification.

Supported tutorial prose includes paragraphs, emphasis, strong text, inline code, fenced code,
ordered and unordered lists, block quotes, links, local PNG/JPEG/WebP images, and ordinary GFM tables.
Reference-style links and images used by the existing exports are included. HTML character entities
and inline `sub`, `sup`, and `br` are supported; other raw HTML gets a source-located diagnostic.
The exact standalone comments `<!-- screenshots:begin (managed by screenshot-docs) -->` and
`<!-- screenshots:end -->` are nonvisible screenshot metadata. Surrounding whitespace is allowed;
each complete HTML block token must contain only one marker. They remain in source and produce no
DOCX/PDF text. Other HTML comments and adjacent raw HTML remain unsupported. Markers inside inline
code or fenced code remain literal examples.
Task lists, footnotes, executable content, and full mathematical typesetting are not initial features.
Unsupported visible constructs must be reported, not silently discarded. Plain Unicode scientific
text remains text; formulas receive no smart-quote or typography substitutions.

## Workbook authoring

### Worksheet declarations

`### Sheet: <name>` creates one worksheet, in declaration order. Names must be unique ignoring case
and valid XLSX worksheet names: nonempty, at most 31 characters, no `: \\ / ? * [ ]`, and no leading
or trailing apostrophe. Preserve the declared spelling. Do not silently truncate names.

One table directly beneath a sheet heading starts at A1. Additional tables require a preceding
`#### At: <cell>` heading, such as `#### At: F1`. That heading applies to exactly the following
table. Targets are single, unqualified A1 addresses. Each table is a rectangular block; its header
row is real spreadsheet content at the starting row. The Markdown separator row is not content.
Alignment markers affect neither cell values nor types. A header-only table is valid.

All authored rows count, including explicitly blank rows. Reject ragged tables before a Markdown
parser pads or truncates their cells. Reject overlapping table rectangles, even if their overlapping
values are blank or equal. Diagnose the two source locations and the first overlapping address.
Reject tables extending beyond XLSX row/column limits. Do not reserve whole sheets in memory.

### Cell values and types

Parse cell content after Markdown table escaping, using this ordered convention:

| Source content | Stored value |
| --- | --- |
| Empty cell | Blank cell |
| JSON double-quoted string, optionally in one code span | Literal text, including numeric-looking text |
| Formula beginning with `=`, optionally in one code span | Formula string |
| `TRUE` or `FALSE` | Boolean |
| Signed decimal or scientific-notation number | Numeric cell |
| Other plain text, optionally in one code span | Text |

Thus `0` is not blank; `"001"` preserves leading zeroes; and in a Workbook cell,
`"=not a formula"` is text, not a formula. This JSON scalar rule also applies to `Enter` and
`Replace` payloads. Tutorial prose and ordinary Tutorial tables use narrative semantics: quoting a
spreadsheet formula as an example does not make it a JSON literal scalar.
Implement strict finite numeric parsing, using decimal/scientific notation rather than locale
commas, currency, percentages, or date guessing. JSON strings use ordinary JSON escaping.
Reject malformed quoted strings. An explicit empty JSON string is distinct from a blank.

Workbook tables support plain text, one surrounding code span, entities, and `br` line breaks.
Other rich markup is an error in workbook cells; it is supported separately in tutorial prose.
Use `\|` for a literal pipe in a GFM cell, including formula text, and restore the literal pipe
before writing the cell. Handle backticks through normal Markdown code-span rules. Escape JSON
string contents only after removing the table's structural escaping.

Formula text means the semantic characters after Markdown decoding. Preserve function names,
spaces, quoted strings, `$` anchors, and sheet references. Never evaluate formulas in Python.
At the XLSX boundary, prefix only recognized modern function-name tokens with `_xlfn.` when
required by OOXML storage. Preserve the authored formula's mathematical meaning and all other
characters; this is a serialization rule, not formula rewriting. On readback, remove that prefix
only from recognized function tokens so validation and DOCX rendering see the logical authored
formula. Unknown functions remain unchanged and outside the checked function vocabulary.
Only leading `=` declares a formula; text beginning with `+`, `-`, or `@` remains text unless it
matches the numeric rule. XLSX serialization must explicitly preserve literal text cell types.

Workbook table formulas are prefilled in the student workbook. Formula instructions under Tutorial
are not prefilled. This distinction gives the author one visible way to choose starting content.
For each label, choose one owner: seed it in the Workbook table for students to inspect, or leave
the target blank and ask students to enter it with `Label`. Do not seed a label and ask students to
re-enter it. `Label` and `Enter` still reject a nonempty seeded target; identical repeated
assignments remain a redundancy warning.

### Optional Google link metadata

A worksheet can include this ordinary Markdown list item before its first table:

```markdown
- **Google Sheets:** https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=TAB_ID
```

Parse the spreadsheet ID and numeric `gid`; preserve the supplied URL as provenance. A URL missing
`gid` can identify the workbook but cannot establish a cell link for that tab. Report that limitation
as a warning. Reject malformed URLs and conflicting metadata; allow at most one URL per worksheet.
For a single generated workbook, mapped worksheets must share one spreadsheet ID. Repeated tab IDs
for different worksheets are errors. Do not infer `gid` from XLSX sheet IDs or worksheet positions.

Mapping is author-supplied, not verified against Google by an offline build. Uploaded XLSX files and
personal copies may receive different URLs. Updating the mapping and rebuilding updates links.
No API credentials, automatic upload, permissions changes, or document writes are required.

## Tutorial structure and numbering

Use H3 for `Part: <title>`, H4 for `Step: <title>`, and H5 for `Substep: <title>`.
Generate part numbers from 1, step numbers from 1 within each part, and substep numbers from 1
within each step. Substeps display their parent step number, for example `6.1` and `6.2`.

For migration or standalone parts, accept `Part 3:`, `Step 6:`, and `Substep 6.1:`. An explicit
number on the first sibling establishes the start of that sequence; subsequent explicit numbers
must equal the generated sequence. A first `Step 0:` is allowed for existing introductory steps;
parts start at 1 or greater, substep suffixes at 1. New authoring examples use unnumbered headings.
In shared builds, a source containing one Part uses its resolved reflection Part identity for that
heading and its title-area subtitle as well. Explicit Part numbers preserve identity in standalone builds.
An explicit substep parent must match its containing step. Invalid hierarchy, numbering gaps, and
contradictory labels are errors with suggested replacement headings. Do not rewrite sources on build.

Nonreserved headings inside Tutorial are informational and do not increment counters. They may not
skip heading levels or introduce structural parts/steps at incorrect levels. A Part requires at
least one Step; each Step requires content or substeps. Recognize reserved keywords case-sensitively
and flag near-miss structural headings rather than interpreting them as ordinary prose.

Ordinary list numbering is independent of step numbering. Keep nested lists and numbering starts.
Use explicit text for generated heading numbers in DOCX to avoid relying on imported Word field
updates. Internal Markdown heading links resolve through the same heading map used by rendering;
duplicate referenced slugs are errors. Literal prose such as "see Step 6" is not automatically
rewritten; warn on numeric step mentions and recommend an internal heading link where appropriate.

Contents includes all Steps and Substeps, with indented Substep links. A single Part is shown in a
standard Subtitle beneath the title and retained in the body, rather than repeated in Contents.
Multi-Part documents include Part entries to group their Steps. The native TOC field selects
Heading 2-3 for single-Part documents and Heading 1-3 otherwise; its cached entries are immediately
readable and linked. The Contents label is not an outline heading.

### Worksheet scope

Each part in a multi-sheet document begins with `- **Worksheet:** <name>` before its first Step.
In a single-sheet document, omission selects that sheet. Render this declaration as a short visible
worksheet instruction. Scope lasts for the entire part; use a new part to switch the default sheet.
An explicit declaration is allowed even with only one sheet. Missing or unknown scope is an error.

Cross-sheet references use familiar spreadsheet syntax: `'Other sheet'!B2` or
`'Other sheet'!B2:B25`. Apostrophes inside names are doubled. Assignment targets are single cells;
references, Select, and Fill actions may be ranges. Cross-sheet targets must name a declared worksheet.

### Workbook region roles

Workbook-only declarations use `- **Region A1:B26:** source` (or another supported role) to describe
the meaning of cells. The closed role set is `source`, `calculation`, `results`, and
`interpretation`. Seeded table cells default to `source`; calculation, results, and interpretation
regions are declared in the hidden Workbook section when needed. Roles describe meaning and do not
grant permissions. Explicit regions may not overlap.

## List-authored instructions

Semantic action links bind an operation to the linked source text without changing the paragraph's
visible wording or list structure. Use ordinary Markdown links with one of these destinations:
`label:<cell>`, `enter:<cell>`, `replace:<cell>`, `fill:<range>`, or `select:<cell-or-range>`.
For example, `[**Sample Mean**](label:D5)`, `[=AVERAGE(B2:B26)](enter:E5)`,
`[Select C2:C26](select:C2:C26)`, and `[drag down](fill:C2:C26)` preserve the authored words as
the student-facing text; the semantic destination is not rendered. Multiple actions may be linked
in one paragraph, in source order, with each value or formula written once. Ordinary GFM numbered
and nested list grouping is preserved. There is no requirement to start every list item with a bold
action label.
Name the destination cell or range in visible prose or its parent instruction whenever the linked
text does not already name it. Hidden semantic destinations do not provide a student-facing cue.

Legacy action openings are also supported. Interpret an action when it is the opening strong span
of a list item; the span contains the action and its colon, and subsequent text is the payload.
Preserve that span as bold in the rendered document. Ordinary strong openings remain ordinary
instructions.

| Opening | Meaning | Effect on initial XLSX |
| --- | --- | --- |
| `**Label F2:**` | Student types a literal text label | Do not fill the answer |
| `**Enter G2:**` | Student types a scalar value or formula | Do not fill the answer |
| `**Replace G2:**` | Student deliberately changes a previously populated cell | Preserve initial value |
| `**Fill E2:F26:** Down` | Student copies first-row formulas down each selected column | Do not fill the answers |
| `**Select:**` | Student selects the single cell or range in the payload | None |
| `[...](select:A1:B26)` | Student selects the referenced cell or range | None |
| `[...](label:A1)` | Student types the linked visible text as a label | Do not fill the answer |
| `[...](enter:A1)` | Student enters the linked visible scalar or formula | Do not fill the answer |
| `[...](replace:A1)` | Student replaces a previously populated cell with linked text | Preserve initial value |
| `[...](fill:A2:A26)` | Student fills the referenced range down from its first row | Do not fill the answers |
| `**Choose:**` | Student follows a menu path | None |
| `**Compare:**`, `**Explain:**`, other prose openings | Ordinary instruction | None |

Legacy `Label` takes plain text (or one code span for literal text). Semantic `label:` links also
decode Markdown emphasis and entities for the assigned label while preserving that formatting in
the visible instruction. Quotes in a label are visible prose rather than JSON delimiters; code and
formula-looking literal label text retain their bytes. `Enter` and `Replace` use the workbook
scalar rules, preserving raw JSON-quoted copy text until scalar decoding. A formula may be written
directly after the action, optionally in one code span, or
in a fenced `sheets` block. A fenced formula may follow an otherwise empty action item as its nested
block. Require one logical formula line; visual wrapping is a renderer concern. Reject an additional
competing value or formula. Explanations belong in a subsequent paragraph or nested ordinary list
item, outside the scalar. A JSON double-quoted value beginning with `=` remains literal text in these
scalar contexts; quotation marks in Tutorial prose and ordinary Tutorial tables do not invoke the
workbook scalar convention.

Recognize a standalone spreadsheet formula before Markdown interprets operators such as `*` as
formatting. Apply formula semantics only at clear boundaries: an `Enter` or `Replace` scalar, a
complete formula code span or fence, a workbook cell, or a bounded spreadsheet expression in
narrative text. Narrative recognition covers complete spreadsheet-style expressions such as
`=SUM(A1:A3)`, `=A1+B1`, and `=(A1-B1)/SQRT(C1)`; it does not consume following explanation. Do not
classify statistical equations such as `alpha = 0.05` or `H = -sum(p_i ln(p_i))`, comparison
operators such as `<=` and `>=`, or URLs as spreadsheet formulas. JSON-quoted values are literal only
where Workbook and action scalar rules apply; a quoted formula example in narrative text keeps its
formula role.
Preserve the semantic formula text exactly; do not add color or other author markup. GFM table pipes
still require standard escaping (`\|`) when they are formula content.

Actions are valid in ordered or unordered lists and may appear in nested lists. A malformed
recognized action is an error, not silently demoted to prose. Actions require a containing Step.
Reject a list item when its only content is one or more bold, colon-terminated labels and it has no
substantive continuation, nonempty fenced instruction, valid action, or substantive descendant.
An empty child item does not make its parent substantive. This check follows parsed Markdown
structure and source locations. Ordinary prose list items need no action label or opening strong
span. Lists inside literal examples are exempt from semantic action parsing.

`Label`/`Enter` targeting a nonempty seeded cell or a previously assigned cell with a different
value is an error; use `Replace` for an intentional change. Identical repeated assignments are
warnings about redundancy. `Replace` requires a known prior value, seeded or instructed. Neither
action changes the generated workbook beyond the initial table content and entry-cell styling.
Track authored instruction state in document order without computing formula results.

`Fill` accepts only the literal payload `Down` and an ordered A1 range containing at least two
rows. A single column (`**Fill C2:C26:** Down`) and a rectangle (`**Fill E2:F26:** Down`) use
the same rule: each cell of the first row must already contain a formula in every incoming
instruction state, and that column's source formula must be identical across those states.
Missing, nonformula, or conflicting source values are errors. An author can put Fill inside
each alternative when the alternatives need different source formulas.

Translate each source formula to the remaining cells of its column using ordinary spreadsheet
relative, mixed, and absolute A1 reference rules. Preserve string literals and quoted worksheet
names. Validate generated entries in row order, left to right, with the same conflict, redundancy,
formula-reference, and availability checks as Enter. Their source location is the authored Fill
item. Later instructions can use the resulting cells. Keep the authored Fill as one visible
instruction in DOCX/PDF; generated Enter children belong to validation and execution only.
Both execution engines replay those same children. Student XLSX contains only Workbook seeds;
Fill marks destination entry cells without inserting answers.

### Alternative calculations

Existing tutorials teach one-tailed and two-tailed alternatives for the same destination cell.
Support explicit sibling list groups so these are not mistaken for conflicting assignments:

```markdown
- **Alternative: Two-tailed test**
  - **Enter G5:** `=T.TEST(B2:B25,C2:C25,2,3)`
- **Alternative: One-tailed test**
  - **Enter G5:** `=T.TEST(B2:B25,C2:C25,1,3)`
```

Two or more contiguous Alternative items under the same parent form a choice group. Evaluate their
assignment history independently from the incoming state, then retain possible states. A later
reference to a cell filled in every branch is available; one filled in only some branches receives
a warning. Later replacement requires a value in every branch. Branches are instructional choices,
not executable conditional logic. Nested alternatives are outside initial scope and produce errors.
Normal prose explains the statistical direction; these examples do not assert that a one-tailed
function call alone establishes the desired directional hypothesis.

### Cell references and menu paths

Backticked A1 cells and ranges in tutorial prose are explicit references. Support `$D$4`, `D$4`,
`$D4`, rectangular ranges, and qualified worksheets. A1-shaped ordinary prose may receive a lint
suggestion but is not automatically linked: scientific identifiers and paper sizes can look like
cell addresses. Action targets are explicit references without requiring additional backticks.

`Choose` splits a menu path on `>` or the Unicode right arrow, trims each segment, and rejects empty
segments. Render segments in bold Roboto Mono separated by the ASCII `>` character with spaces.
Optional backticks around the whole path are accepted. Do not interpret greater-than comparisons
elsewhere as menus. Bold ordinary openings and menu formatting remain separate operations.

## Validation and diagnostics

Every diagnostic includes severity, stable category, source path and physical line, explanatory
message, and correction. Include worksheet/address and the related source line when applicable.
Preserve source locations through parsing, numbering, assignment resolution, and serialization.

Validation has separate, honestly reported levels:

1. Structure: headings, tables, types, action payloads, worksheet scope, and address syntax.
2. References: existing worksheets, seeded cells, intended student destinations, instruction order,
   and static references in the supported formula subset.
3. Consistency: conflicting assignments, range endpoints, unavailable inputs, and conditional writes.
4. External behavior: Google import, link navigation, and actual formula calculation, checked manually
   on representative outputs. Offline lint never claims this level passed.

Recognize static A1 references, quoted sheet names, and bounded rectangular ranges inside common
formulas. A tokenizer must distinguish references from function names and quoted strings; raw regex
scanning is insufficient. Whole-column/row ranges, named ranges, dynamic references such as INDIRECT,
external workbooks, and array/spill constructs are preserved but reported as not fully validated.
They must not produce a false "all references verified" result. A fully unknown function does not
by itself invalidate recognized static references, but its evaluation/compatibility is unverified.
Do not ship a statistical formula evaluator or a promise of full Sheets/Excel equivalence.

| Finding | Severity and response |
| --- | --- |
| Invalid hierarchy, unknown sheet, impossible address, table overlap | Error; correct structure/location |
| Conflicting assignment or malformed scalar/formula instruction | Error; correct target or use explicit replacement/alternatives |
| Missing image or unsupported visible document construct | Error; supply asset or supported representation |
| Unknown static sheet reference in a formula | Error; correct the sheet name |
| Input cell blank and never supplied before use | Warning; check range or instruction order |
| Data range extends beyond declared source capacity | Warning; confirm the input region or correct endpoint |
| Related formulas use different endpoints | Warning; compare inputs, do not auto-repair |
| Formula has unsupported reference syntax or function compatibility | Warning; state exactly what was not checked |
| Missing bold list opening or hard-coded step mention | Warning; improve source manually |
| Missing Google tab mapping | Link-status note; keep labels and offline validation |

Blank cells are legal. Compute populated extents from actual values, not styled cells, and exclude
future student outputs when checking the size of a dataset. Do not treat a long valid range as an
error merely because a formula can legitimately ignore blanks. Avoid inferring that two same-sized
datasets are conceptually interchangeable. No automatic statistical or scientific corrections.

Report errors together where independent checks can continue. Any semantic error prevents final
artifact publication; warnings permit it and remain in the validation report. There is no global
warnings-as-errors switch in the initial interface. The report distinguishes verified, partially
checked, and unchecked formulas rather than using a single misleading accuracy score.

## Output behavior

### DOCX

Use native paragraphs, list numbering, tables, hyperlinks, and editable formula text. Add a native
Word `PAGE` field in the footer and format the footer with Normal text. Use only these Google Docs
paragraph styles in the generated DOCX: Normal text, Title, Subtitle, Heading 1, Heading 2, and
Heading 3. Map Title to the document title, Subtitle to optional metadata, and Heading 1-3 to parts,
steps, and substeps. Use Normal text for body, lists, formulas, quotes, and tables. Apply instructional
emphasis and roles for formulas, cells, menus, and links directly to runs; do not depend on custom
tutorial paragraph or character styles. Unused stock styles may remain in the DOCX template, but
generated paragraphs reference only the six styles. Keep the style and direct-format values in one
renderer-owned definition.

Use 0.6-inch page margins. Part, Step, and Substep headings start at 0, 0.1, and 0.2 inches
relative to that margin. Ordinary body text and first-level task text share the 0.3-inch edge,
regardless of heading depth. Lists use hanging indents so wrapped lines align with task text;
true nested lists add 0.25 inches per level. Continuations follow their containing item.
Fully justify ordinary explanatory paragraphs. Left align lists, equations, captions, and prompt
callouts; center figures. Review for readability and clipping rather than optimizing print pages.

Use PT Sans for body text and headings, PT Sans Narrow for compact table text, and Roboto Mono for
formulas, cell references, and menu entries. Apply PT Sans Narrow only where rendered table content
needs the narrower face. These fonts are available in Google Docs and must also be installed in the
local PDF build environment. The builder does not download or install fonts. This DOCX/PDF font
contract does not change XLSX font styling. Formula-role text uses Roboto Mono and dark green
(`007A00`); ordinary inline formulas, code spans, formula fences, and formula cells receive the same
formula treatment while preserving their text. Keep PT Sans, PT Sans Narrow, and Roboto Mono
available in regular, bold, and italic variants. These font variants are independent of the six
paragraph styles named above.

Formula blocks use a readable dark-green monospace face with a compact native border around the
formula characters and no background fill. Each Enter or Replace formula appears on its own display
line with its destination immediately above it. Preserve
copyable formula text; do not insert soft hyphens,
smart quotes, invisible separators, or manual line breaks into it. Wrap visually where possible;
report a formula that cannot fit readably. Use text weight/borders in addition to color distinctions.
Use comfortable page margins and heading spacing; keep headings with following content. Set list
paragraphs to 2 pt after, 0 pt before, and single line spacing. Body paragraphs use 6 pt after and
1.08 line spacing. Keep a short instruction and its formula together, but allow a long Step to span
pages.

Render valid cell references as visibly styled text and, where mapped, hyperlinks to the supplied
spreadsheet/tab/range. Encode query/fragment values correctly. Links navigate to the instructor
workbook specified in source, not automatically to a student's personal copy. A document's visible
worksheet label remains useful without links. Resolve internal heading links to DOCX bookmarks.

Preserve image order, proportions, and alternative text. Render standalone and
line-break-separated teaching figures centered in a 6.5-inch-wide by 3-inch-tall maximum box, with
proportional page-height scaling and a numbered native-Normal caption below. Captions are one
point smaller than body text, left aligned with an extra 0.2-inch inset beyond the body edge. Keep genuine sentence
and linked images inline at their natural size. Resolve local assets relative to the Markdown
source; decode existing PNG/JPEG data-URI references without treating them as prose.
Use the DOCX caption rather than a redundant standalone figure title; scientific multi-panel figures
may retain short panel labels needed to distinguish the compared views.
An exceptional standalone-image override may follow the image as `{width=5in height=2in}`. Both
values are required to be positive inch values and further cap the standard figure box; they never
stretch or crop source pixels. Prefer the standard box unless the image needs a smaller readable
presentation.
Local `.webp` assets must have a genuine RIFF/WEBP container and decodable image content. For DOCX,
embed their decoded pixels losslessly as an in-memory PNG, preserving transparency and proportions.
Keep source WebP paths and bytes unchanged; build asset fingerprints identify the original WebP.
Use `$...$` for inline TeX and `$$...$$` for display TeX. Pandoc creates editable Office Math;
spreadsheet formulas remain literal text and retain dollar-sign anchors. Prefer familiar teaching
notation such as `$y = ax^2 + bx + c$`; hypothesis symbols accompany their full names.
No network fetching occurs during build. SVG and mathematical image generation require explicit
future work; migrate such content to supported assets or report it rather than discarding it.

### XLSX

Write worksheets, values, types, and formulas exactly as the Workbook model specifies. Freeze panes
at `A2`; use at least 12-character column widths, including for blank student-entry cells, while
keeping widths bounded. Use modest header emphasis, wrapped text, and a distinct style on blank
student entry cells. Do not populate Label/Enter answers, add hidden solutions, or overwrite seed
values. Use `0.000` as the default number format for numeric seeds, formulas, and blank authored
work cells, including fill destinations. Preserve stored precision; formatting does not round
values or evaluate formulas. Text and Boolean seeds retain their types. Lessons can teach an
explicit number-format menu task for other displays; do not infer statistical significance,
percentages, or scientific notation from values or promise full workbook fidelity.
Do not fabricate cached formula results. Request recalculation on opening when supported by the
chosen writer, and disclose that calculation was not performed by the converter.

Round-trip generated XLSX through the reader to check sheet order, addresses, values/types, and
formula strings. Compare logical contents, not ZIP bytes or application-generated metadata.
The representation supports teaching data, not preserved charts, macros, pivots, merged cells,
conditional formatting, or arbitrary styles. Initial generation does not create charts merely
because the tutorial instructs students to create them.

### PDF and publication

Convert the just-generated DOCX through LibreOffice Writer's PDF export, not Impress or a separate
layout renderer. Verify that the current run created a nonempty readable PDF. Use isolated staging
paths so an old PDF cannot masquerade as success. On this macOS host, commands invoking LibreOffice
must run outside the sandbox, through the project's conversion wrapper.

Each default build publishes `tutorial_output/<source-stem>/<source-stem>.docx`, `.xlsx`, and `.pdf`, plus
`validation.json`. The JSON is build evidence, not a fourth teaching deliverable. It includes source
and asset fingerprints, diagnostic locations, reference-check coverage, and output status. It makes
no claim about Google import unless separate recorded acceptance evidence exists.

Generate and verify all requested outputs in staging before replacing the previous successful
bundle. A failed PDF conversion is a failed complete build; keep previous published outputs intact
and report the failed stage. Do not expose mixed-generation bundles as successful. Refuse source/
input overwrite and publication to an existing directory not owned by this converter. Treat a prior
validation manifest as ownership evidence; compare recorded fingerprints to detect modified outputs
and report a conflict rather than overwriting user edits. Identical inputs need not produce identical
ZIP/PDF bytes, but must produce equivalent tutorial/workbook content.

## Command-line interface

The current CLI provides these commands:

```bash
source source_me.sh && python3 make_tutorial.py lint tutorial.md
source source_me.sh && python3 make_tutorial.py build tutorial.md
source source_me.sh && python3 make_tutorial.py build tutorial.md --format docx,xlsx
source source_me.sh && python3 make_tutorial.py build part_1.md part_2.md part_3.md \
  --output-dir tutorial_output/release
source source_me.sh && python3 make_tutorial.py import-xlsx template.xlsx --output draft.md
```

`lint` parses and validates without running LibreOffice or writing deliverables. `build` defaults
to all three teaching outputs. `--format` (`-f`) accepts `all`, `docx,xlsx`, `docx`, or `xlsx`;
requesting PDF always generates its DOCX prerequisite. `--output-dir` (`-o`) selects a bundle
directory. The default output directory is relative to the invocation directory; asset resolution
remains relative to the input file. A subset build publishes only the requested formats and its
manifest, so an old PDF is not carried into a new bundle as if it matched the new DOCX.
With more than one source, every source basename must be unique, compatible worksheet declarations
are merged into `workbook.xlsx`, and each source receives its own DOCX and PDF. Conflicting seeded
cell values or worksheet roles stop the build rather than choosing an arbitrary workbook state.
Shared data tabs come first; each source's action-target worksheets are followed immediately by
its distinct reflection tab, in source order. A single-source tab is
`Reflection Questions`; shared-build tabs use `Part {resolvedpart} Reflection`, such as
`Part 2 Reflection`. Use the single unique explicit Part identity within each source; use the
source's one-based build position only when it has no unique explicit Part identity.
Duplicate resolved identities across sources or conflicting tab names stop publication; they
do not trigger a fallback to source position. Workbook question identifiers are `1`, `2`, ...
without an explicit Part identity and `3.1`, `3.2`, ... for explicit Part 3; shared-build
questions use the resolved identity, such as `1.1`, `2.1` for implicit first and second sources.
Tutorial prose repeats the full corresponding prompt at its teaching point. Each reflection tab
stacks question text and editable answer space in one wide column, with wrapped text and rows at
least 47.25 points high.

Question identifiers are literal, editable Normal text in the workbook. Keep native
Heading styles for section and question headings; do not rely on Word automatic list numbering or
numbering fields for generated question identifiers.
`import-xlsx` takes `--output` (`-o`) and refuses an existing destination. Do not add theme, parser,
diagnostic-threshold, or spreadsheet-engine switches.

Commands return zero on successful requested work, including advisory warnings, and nonzero on
validation, I/O, or conversion failure. Diagnostics are concise and source-located; do not silently
catch unexpected internal failures. CLI exceptions must retain their cause for debugging.

## Import and migration

`import-xlsx` creates a draft single-source Markdown file: title, Workbook section, and a Tutorial
scaffold awaiting authored instructions. It is a one-time import, not a second maintained source.
Import values and formulas, never cached results in place of formulas. Explicitly quote text whose
type would otherwise change. Preserve blank rows/columns needed to retain addresses.

For a sheet with only populated cells near A1, emit its populated bounding rectangle at A1. For
sparse sheets, emit contiguous occupied row runs as separate tables anchored at their original
top-left cell; include internal gaps so coordinates stay unchanged. Import row-run tables with their
first source row as the GFM header. A blank worksheet becomes a one-cell blank table at A1. Limit
allocation to populated cells and refuse pathological sparse extents with an actionable diagnostic.

Inventory unsupported features before writing the draft. Ordinary fonts, fills, widths, and number
formats may be discarded with a prominent import summary. Merges, charts, macros, rich text, dates,
error cells, or other content whose meaning would be lost block import until the user supplies a
simpler workbook or the format is explicitly extended. Imported dates must not silently become
serial numbers or strings. Do not silently drop a worksheet or truncate its name.

For the first teaching migration, combine imported data with a manually normalized copy of the
Fried Foods two-sample tutorial. Record source filenames and correction notes outside the student
document. Keep `2025_Artifacts/` unchanged. Images can be extracted to a sibling assets directory.
Do not implement a heuristic all-purpose Google Docs Markdown importer in the first release.

## Acceptance contract

- A writer can change one formula once and get the new document text and validation association.
- Inserting a Step renumbers later steps and substeps without editing numeric labels throughout.
- Multiple sheets and cross-sheet references resolve without repeating Google URLs per instruction.
- Workbook table addresses, blanks, literal text, numbers, and formulas survive XLSX generation.
- Student entry cells are blank unless explicitly seeded by a Workbook table.
- The known legacy range discrepancy produces an actionable warning, not a silent correction.
- Native DOCX formulas remain editable and copyable in the document; the paired XLSX preserves the
  intended initial layout and representative formulas as formula strings.
- The LibreOffice PDF has readable formulas, images, lists, and heading/page flow, without clipping.
- A failed build preserves the previous successful bundle and accurately reports partial checking.

## Completion evidence

Local completion uses automated behavior checks for DOCX/XLSX behavior and autonomous agent
assessment of generated PDF layout. No human milestone signoff is required. Scientific migration
questions are resolved against authoritative sources, with corrections and citations recorded in
the migration records. These checks do not establish Google Docs or Sheets import behavior.

Google Drive uploads and Google Docs/Sheets imports are always outside this workflow. Deliver and
validate local artifacts without making Google access a completion requirement.

The static validator checks formula syntax, references, and authored assignments; it never evaluates
formulas. For real local execution, `devel/validate_libreoffice.py` applies all authored
assignments for each scenario, opens and recalculates the final workbook state in LibreOffice Calc,
and compares saved results with independent SciPy/NumPy expectations. This verifies final states,
not intermediate steps. On the current snapshot Calc passed 254 expected values across 13
scenarios. This is local execution evidence only; the Google runner has been removed.
See [LOCAL_VALIDATION.md](LOCAL_VALIDATION.md)
and [local_calculation_readiness.md](active_plans/reports/local_calculation_readiness.md).


### Variable sample sizes

A source role region declares input capacity, independently of how many observations its table
supplies. For example, a source region through row 101 can initially contain 25 observations.
References inside that capacity may include empty cells without unavailable-input warnings.
Calculation cells outside source regions retain instruction-order checks.

Use COUNT to calculate N from numeric observations, not a constant or a last-row calculation.
Cover the source capacity in analysis formulas and fill blank-aware helpers across that capacity.
For regression, filter response and predictor ranges with the same complete-numeric-pair condition.
Keep independent samples separate and preserve intentional calibration/unknown boundaries.
Bounded capacity is a limit on supported input space, not an expected sample size.

Before publishing any tutorial, the LLM author must verify that adding a data point at the bottom and
deleting a data point from the middle both preserve correct final results without formula edits.
Apply these checks to that tutorial's input structure and scientific purpose. These are documented as LLM author review requirements. No human review or approval is needed.
This is verbal publication guidance, not a universal automated test or compiler gate. See
[AUTHORING_GUIDE.md](AUTHORING_GUIDE.md#required-llm-author-review-before-publishing).
