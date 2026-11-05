# Build and refine your tutorial

**Learning goal:** Build your Markdown source, inspect the generated files, and correct a real
authoring problem before sharing a tutorial.

The Markdown file is the source of truth. The compiler creates editable DOCX and XLSX files and a
PDF review copy. Edit the Markdown, then build again; editing generated files does not update the
source.

[AUTHORING_GUIDE.md](../AUTHORING_GUIDE.md) | Previous: [PART_2_STATISTICS.md](PART_2_STATISTICS.md)

### Part 3: Build and refine

#### Step: Start an original source

Copy a small pattern or start from a suitable template, then write your own tutorial in a plain-text
file ending in `.md`. You can reuse the example's syntax and file structure while supplying your
own content.

When copying a complete file from GitHub, choose **Raw** and copy the plain text. Save it with a
`.md` extension in a plain-text editor; copying the rendered page can lose action-link syntax.

Keep your Workbook tables and Tutorial text in one source file. Use
[PART_1_CREATE.md](PART_1_CREATE.md) for document structure and content placeholders, and
[PART_2_STATISTICS.md](PART_2_STATISTICS.md) for the workbook syntax. Replace placeholders with your
own content before linting.

For complete runnable source that demonstrates the feature set, read
[authoring_features.md](../examples/authoring_features.md). For lessons that show the quality of a
finished tutorial, browse [TUTORIAL_CATALOG.md](../TUTORIAL_CATALOG.md). Those instructor-authored
tutorials are examples, not required models for your topic or teaching method.

#### Step: Lint before building

Follow [INSTALL.md](../INSTALL.md) once to set up the local tools. Open Terminal in the project
folder and start Bash. Run subsequent commands in that same shell:

```bash
bash
source source_me.sh
python3 make_tutorial.py lint my_tutorial.md
```

Replace `my_tutorial.md` with your filename. Lint checks source structure, worksheet names, table
shapes, supported actions, and known cell-reference conflicts. Read the reported line and correction
before changing the source.

#### Step: Build the document and workbook

When lint passes, build all three local outputs:

```bash
source source_me.sh
python3 make_tutorial.py build my_tutorial.md
```

To build just the Word document and Excel workbook first, use
`python3 make_tutorial.py build my_tutorial.md --format docx,xlsx`. This subset does not require
LibreOffice; use the default build above when you are ready to inspect the PDF too.

The default output folder is `tutorial_output/my_tutorial/`. It contains:

| File | Use it to inspect |
| --- | --- |
| `my_tutorial.docx` | The editable document students can import into Word or Google Docs. |
| `my_tutorial.pdf` | Document page layout, tables, images, and page breaks. |
| `my_tutorial.xlsx` | The starter workbook students can open in Excel or import into Google Sheets. |

A successful build establishes that the source meets compiler rules. It does not establish that a
scientific claim is accurate, a scenario is engaging, or a student will understand every step.

#### Step: Inspect what a reader receives

Use this short review after every meaningful revision:

1. Open the PDF and DOCX. Read the headings in order, check that Contents lists every Step and
   Substep, formulas and images are readable, and no material is clipped or overlaps.
2. Open the XLSX. Check that supplied data and labels are present, calculation cells are blank when
   students should work them out, and result or response areas have clear headings.
3. Work through the instructions in a disposable copy of the XLSX. Check the first and last formula
   destinations and every filled range.
4. Revise the Markdown source, then lint and build again.

This is a local review. The project delivers local files; Google Drive uploading and importing are
out of scope. Local output does not prove Google formatting or calculations.

#### Step: Correct a common mismatch

The visible destination and the semantic target must name the same cell:

```markdown
1. In cell E2, enter:
   [`=AVERAGE(A2:A6)`](enter:E2)
```

This source has a mismatch:

```markdown
1. In cell E2, enter:
   [`=AVERAGE(A2:A6)`](enter:E3)
```

For this mismatch, lint reports:

```text
error [action-visible-target] Visible cell E2 disagrees with enter target E3
  Correction: Use cell E3 in the instruction or change the binding target
```

Correct the written cell or the action target so both mean the same thing, then lint again.
Read all diagnostics: one incorrect destination can also cause a later Fill action to report
`fill-source` because its starting cell has no formula. Fix the destination first and rerun lint;
then address any remaining errors.
See [MISTAKES.md](../reference/MISTAKES.md) for table, formula, range, and blank-work errors.

#### Step: Apply quality judgment

The compiler enforces technical rules. You and the instructor judge the lesson itself. Before
sharing, check that your tutorial has:

- A biological question or clearly identified teaching scenario that you can explain and support.
- A reader goal that fits the data and requested calculation or spreadsheet work.
- Labels, instructions, and response spaces a classmate can recognize.
- Explanations and interpretation written in your own words.
- Sources for data, figures, and claims where they are needed.

This is an author review list, not a compiler gate. A file can build successfully and still need a
clearer explanation or a better question.

#### Step: Find advanced help when needed

The normal workflow is write, lint, build, inspect, and revise. If you deliberately move a table or
change a data range in an existing source, use the optional preview workflow in
[CHANGES.md](../reference/CHANGES.md). It can update marked worksheet references, but you still
review your scientific prose and rebuilt outputs.

Use the practical index in [FORMATTING_GUIDE.md](../FORMATTING_GUIDE.md) to find a feature while you
author. Return to [AUTHORING_GUIDE.md](../AUTHORING_GUIDE.md) when you need the three-part path or
the complete specification.
