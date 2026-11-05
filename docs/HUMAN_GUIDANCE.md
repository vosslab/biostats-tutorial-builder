# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

- Make durable changes in starter-repo-template; consumer copies are vendored.
- A temporary, easily removable wrapper is acceptable for the Graphify crash.
  Make the edited node count match the expected normalized count.
- Semantic links should attach spreadsheet actions to the original natural prose; ordinary numbered
  and nested list grouping should remain intact. Do not require every list item to begin with a bold
  action label.

- Use readme-docs and screenshot-docs to showcase the repository's finished tutorial and workbook
  outputs.

## Tutorial converter

- Deliver working tutorials. Correct discovered calculation failures instead of accepting them as
  documented limitations.

- Delete the Google runner to avoid future confusion. Keep calculation validation local.

- Introduce the project as: "Create a biology tutorial for classmates in one plain-text file. Write
  the lesson and design the spreadsheet; the compiler formats your work as editable Word, PDF, and
  Excel files." Keep guides and screenshots current with the refined syntax.

- Use `y = ax^2 + bx + c` throughout Part 3 and its workbook. Keep beta notation in one brief
  note about later statistics study, rather than using it throughout the lesson.

- Pair hypothesis symbols with their names: "null hypothesis, H0" and "alternative hypothesis,
  Ha", using proper subscripts. Follow the hypothesis-testing terminology examples in my
  biology-problems matching set; do not use H0 as an unexplained standalone label.

- Make data-figure axis labels readable at their displayed document size. Draw gridlines behind
  points, so the grid does not obscure observations.

- Keep the code that generates data figures in a Git-tracked repository location so it can be
  reused when the figures need updating.

- Explain `!` when showing cross-sheet formulas. Prefer copying numbers between sheets when that
  is easier for general biology students to understand.

- Contents should include every Step and Substep, with Substeps indented beneath their parent
  Steps. Omit the usually single Part from Contents while preserving its body heading.

- Put the supplied workbook filename on its own line, as shown in the Caffeine introductions.
  Use the exact filename `Dr_Caffeines_All_Nighter_Academy_Student_Workbook.xlsx`.

- Label the Caffeine lessons Part 1, Part 2, and Part 3, including standalone builds, title-area
  subtitles, body headings, reflection identifiers, and workbook tabs.

- Keep figures within default maximum bounds of 6.5 inches wide and 3 inches tall, preserving
  proportions. Discourage size overrides; use them only when readability requires one.

- Format figure captions one point smaller than body text, with a larger inset like a journal.
  Figures have numbered captions and no titles; tables have titles.

- Integrate reflection prompts beside the relevant instruction in shaded aside boxes, rather than
  collecting them at the end of a Part. Keep their identifiers and answer tabs clear.

- Remove student section-assignment names from published tutorial text and headings.

- Keep heading weight consistent across equivalent Steps, Parts, and Substeps regardless of
  whether their source text has explicit bold markup.

- Visually distinguish spreadsheet menu paths such as File > Make a copy from ordinary prose.

- Use 0.6-inch margins on all four sides to maximize usable page space on my printers.

- Order workbook tabs by Part: work, reflection, then the next Part's work and reflection.

- Inspect the images and write specific, useful figure captions instead of generic illustration labels.

- Use consistent semantic headings and numbered substeps for distinct tasks throughout each lesson.
  Keep peer concepts at the same list depth; bold paragraphs are not a substitute for headings.

- Use more numbered Steps, Substeps, and action lists to make the instructional flow clear; avoid
  long stretches of unnumbered calculation paragraphs.

- Put each formula students must Enter or Replace on its own readable display line, with the
  destination cell immediately above it. Prefer one entry formula per numbered action.

- Formula displays should use green text and a compact green border around the formula itself,
  without a background fill or a full-width paragraph box. Keep reflection callouts shaded.

- Fully justify ordinary body prose. Keep headings, lists, equations, captions, and reflection
  callouts purposefully left aligned; center figures. Reflection callouts contain only the exact prompt
  and answer destination; explanation belongs outside the box.

- Use a visible hierarchy: Part at 0 inches, Step at 0.1, Substep at 0.2, and body/task text at
  0.3. Body paragraphs and first-level tasks share the 0.3-inch edge regardless of heading context.

- Advance each deeper list by 0.25 inches. Continuations, formulas, prompts, captions, and quotes
  derive from their real context.

- Tutorials are primarily for Google Docs, not print pagination. Review clipping, overlap,
  readability, and logical grouping; leave naturally sparse page tails alone.

- Google Drive uploading is always out of scope for this repository. Deliver and validate local
  files; do not upload them to Google Drive or import them into Google Docs or Google Sheets.

- Require every tutorial to contain reflection questions, using the literal words "Reflection
  Questions" in the authoring syntax. Students like having their answers on a separate tab.
- Use the supplied descriptive-statistics workbook as the reflection-layout precedent. Show actual
  Markdown conversions of past content before implementation and preserve question wording.
- Use the local repository guidance and the existing markdown-to-tutorial workflow when adapting
  the frozen materials; that is the point of this work.
- Release the three Dr. Caffeine Parts together as separate Google Docs with one shared Google
  Sheets workbook. Use the same regression dataset throughout so the warm-up supports the analysis.

- Fix demonstrated data-integrity defects when discovered, including unintended prose changes and
  mismatched visible/action-target ranges. Keep the worksheet-editor repair narrow; a documentation
  limitation is not a substitute for correcting known source corruption.

- Assess the guides with a concise quality rubric and an independent subagent review, including
  an attempt to author a small tutorial using only the documentation. Use findings to improve
  student authoring, not as a rigid acceptance gate.

- Make the README student friendly and emphasize the importance of students' contributions to
  open pedagogy.

- Prioritize DOCX and XLSX for importing into Google Docs and Google Sheets.
- Use LibreOffice to convert DOCX to PDF for useful output review; HTML preview is not needed.
- On this macOS host, run every command that can invoke LibreOffice outside the sandbox through
  the repository scripts; ODP imports may launch it indirectly for metafile conversion.
- Keep authoring easy for humans: use lists for tutorial instructions and GFM tables for the
  simple spreadsheet data.
- Keep the list-authored instructions and table-authored workbook in one Markdown file that
  produces all three outputs.
- Format spreadsheet formulas, cell IDs, menu choices, and bold list openings consistently.
  Enforce part, step, and substep numbering, and connect or check spreadsheet references.
- Examine djot-slide-builder and exam-formatting-tools for relevant patterns; the slide
  project's syntax guide does not directly apply to tutorial authoring.
- Migrate all three Fried Foods/babies tutorials, all five Microbes tutorials, and the three-part
  Dr Caffeine set. Include PETase in the inventory and identify its incomplete source material.
- Keep the workflow KISS and avoid speculative gates. Agents should resolve scientific migration
  issues with authoritative sources and document corrections.
- Use local DOCX/XLSX behavior checks and agent PDF visual assessment to determine completion.
  Google Drive uploads and Google Docs/Sheets imports are always out of scope, even with access.
- Complete milestones without waiting for human milestone signoff.
- Repair PETase with a clearly labeled synthetic Bradford dataset when original measurements
  cannot be recovered.
- Keep calculation checks local; the Google runner is removed. Do not upload files to run checks.
- Use the final layout `make_tutorial.py`, `tutorial_lib/`, `tutorial_data/`, and
  `tutorial_output/`; this supersedes the earlier distinct-prefix naming request.
- Apply the selected names consistently without old-name aliases or legacy compatibility stubs.
- Group authored lessons and their topic assets beneath `tutorial_data/`, preserving filenames and
  every unused legacy asset with its own topic.
- Treat this as preproduction: fix the design, keep it KISS, and finish the work without legacy
  compatibility layers or stubs. Check the real student walkthrough and current artifacts before
  declaring completion.
- Compare every original lesson directly with its generated materials, walk through the actual
  generated XLSX as a student, and invite independent challenges. Preserve author voice; change the
  converter only for recurring design issues, and do not add validation infrastructure for this review.
- Preserve existing lesson prose unless a change has a clear, evidence-based reason; keep the author's
  voice.
- Babies and Microbes are established lessons; preserve their teaching experience and voice while
  correcting verified errors, typos, and format faults. Make as few wording changes as practical.
- Treat the Dr Caffeine materials as a draft foundation, not a quality benchmark. Complete all three
  parts as polished, independently usable classroom lessons, with efficient Enter once / Fill down work.
- Make the source-to-output workflow produce engaging, scientifically accurate, classroom-ready
  lessons while preserving author voice; do not claim learner outcomes without evidence.
- For the teaching-quality pass, use HCI cognitive-walkthrough methods and targeted humanizer edits;
  expert inspection does not count as student testing. Keep wording changes focused on actual learner
  needs and preserve the source voice.
- Keep numbering coherent across the three independently usable Caffeine lessons.
- Use clearly defined Part and Step headings, then add real Substeps for distinct instructional
  tasks below a Step. Keep related ordered actions together instead of making each action a heading.
- Introduce regression with familiar `y = mx + b` and `y = ax^2 + bx + c` equations, defining y
  as predicted exam score. Keep Part 3 workbook labels consistent with a, b, and c.
- Keep standalone figures consistently sized and horizontally centered; preserve every image's
  proportions, and keep captions readable beneath the figure.
- Prefer the standard standalone-figure size. Use per-image maximum bounds only for exceptional
  readability needs, never as routine styling.
- When the work queue is busy, prioritize implementing queued fixes and defer slow rebuilds and
  validation checks until the queue is lower.
- In generated DOCX/PDF, use Regular PT Sans for body text, PT Sans Narrow for compact tables, and
  Roboto Mono for formulas/cells/menus. These are available in Google Docs. Keep Atkinson Hyperlegible
  Next out of this project because it is unavailable there.
- In generated DOCX, use Google Docs' Normal text, Title, Subtitle, and Heading 1-3 paragraph styles.
  Map Title to titles, Subtitle to optional metadata, Heading 1-3 to parts/steps/substeps, and Normal
  text to body/list/formula/quote/table text and the page footer. Use direct formatting for emphasis.
- Keep the GFM-to-DOCX/XLSX/PDF workflow easy to author: auto-style spreadsheet formulas from `=`
  in dark green without color markup, and make tutorial lists more compact. The older 4:55 samples
  feel less fun; preserve lesson voice and fonts, and keep student answer cells blank.
- Restore the original wording, descriptive headings, humor, and compact numbered groups across all
  tutorials. Change prose only for technical references, formulas, data, or genuine science errors;
  complete missing Caffeine content while preserving its good prose.
- I distrust LLM-written prose. Prefer existing authored content when it is available, and keep any
  humanizer edits restrained and grounded in the author's science and voice.
- Keep Roots in the course for now.
- Show the literal student source in fenced code blocks, and inspect rendered GFM documentation
  rather than assuming Markdown source will render correctly. I am concerned about the existing files.

## Student publishing

- This repo supports open pedagogy and Student-Generated Content. Authors create original biology
  tutorials for classmates; introduce the project without a specific course name or number.
- Teach Markdown and the compiler through copyable source beside tightly cropped actual Word and
  Excel output. Make the guides a practical, comprehensive visual reference.
- Keep Roots as a simple formatting example without a deeper meaning or prescribed scenario.
  Students supply their own scenarios, questions, explanations, and instructional approaches.
- Use clearly identified placeholders to invite student content. The manager writes explanatory
  documentation; preserve existing instructor educational content and student authorship.
- Focus the three Parts on document formatting, workbook construction, and building/refining files.
  Keep advanced maintenance optional and prioritize useful guides over documentation infrastructure.
- Separate compiler-enforced standards from advisory scientific and instructional quality review.

- Organize the student course as Parts, Steps, and Substeps. Use cropped visuals to emphasize the
  relevant part of a page, and refresh screenshots automatically after style changes.
- Let the course proceed without human milestone gates.

- Tutorial authors should learn spreadsheet formulas, layout, and design; readers should
  learn statistics and how to construct spreadsheets.
- Keep source characters ASCII. Straight quotes and named entities are acceptable; numeric character
  references are unwanted.
- Preserve authored prose. Following a template is acceptable.
- Update references automatically when authors move columns or ranges or change data size.
- Give the compiler considerable visual freedom, including color and flair. My favorite palette
  includes dark reds, oranges, lime, green, teal, cyan, blue, purple, magenta, and pink; select
  colors purposefully.
- Give Parts, Steps, Substeps, and task text the explicit stepped indentation hierarchy recorded
  above. Keep figures centered in the printable page and figure captions inset beyond body text.
- Never stretch figures. Use proportional image sizing, figure captions and numbers, table titles,
  native contents, and a clear left-to-right instructional hierarchy in released documents.
- Use one explicit workbook name in the file and every Make a copy instruction. Render explanatory
  equations as readable mathematics rather than plain-text variable names.
- Fully justify paragraphs that run longer than two lines.
- Use the README and current output screenshots to show off the pipeline's capabilities.
- Tutorial authors establish labels and worksheet structure first; they do not start with unlabeled
  colored areas. Tutorial users do not generally enter headings.
- I intentionally have no `.gitignore` rule for `__pycache__`, because it lets me know when agents
  are not following guidelines.
- I would consider adding a separate page showing how different syntax converts into formatting,
  using Markdown and cropped screenshots.
- Spreadsheet numerical formatting needs work; the default should be three decimal places.
- The formatting guide should explain how formulas and spreadsheet actions connect to workbook
  tables, with an example of adding a new row or column.
- Make the README landing page friendlier to non-coding students, with more about where to start
  and what to read.
