# markdown-to-tutorial

BIOL 318 students use Markdown to create original biostatistics tutorials for classmates and future
students. The compiler turns your writing into editable Word and Excel files, helping you contribute
to a shared collection of learning materials.

## Your contribution matters

You have completed several biostatistics tutorials. Now you can draw on that experience to help
someone else learn. The questions you found interesting, the explanations that helped you, and the
steps that needed more clarity can inform the tutorial you create.

This is **open pedagogy**: students help create the educational materials others learn from.
Your tutorial contributes to a growing collection of **Student-Generated Content (SGC)** for
classmates and future students. Your own biological scenario, research question, and explanations
bring another perspective to that collection.

You make the scientific and teaching decisions. Markdown is plain text with simple formatting
markers; the compiler is the tool that turns it into consistently formatted files. The shared
standards help readers navigate your work while keeping your ideas and voice your own. Review
your science, credit your sources, and check that another student can follow your instructions.

## Start authoring

Start with [docs/AUTHORING_GUIDE.md](docs/AUTHORING_GUIDE.md). You do not need to know Markdown
before you begin. The guide pairs copyable source with pictures of the resulting Word document or
Excel workbook: "If you type this, it looks like this."

Read the three Parts in order or look up a feature as you need it while developing your own tutorial.
The short examples demonstrate formatting; your project supplies the content.

| What you need | Where to go |
| --- | --- |
| A visual menu of compiler features | [docs/FORMATTING_GUIDE.md](docs/FORMATTING_GUIDE.md) |
| Part 1: Document formatting | [docs/learn/PART_1_CREATE.md](docs/learn/PART_1_CREATE.md) |
| Part 2: Excel workbook construction | [docs/learn/PART_2_STATISTICS.md](docs/learn/PART_2_STATISTICS.md) |
| Part 3: Building and refining files | [docs/learn/PART_3_IMPROVE.md](docs/learn/PART_3_IMPROVE.md) |

## Markdown becomes a tutorial

<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->

Write this inside a Tutorial Part and Step:

```markdown
#### Step: Enter a formula

1. In cell E2, enter [`=AVERAGE(A2:A6)`](enter:E2).
```

The Word document shows the numbered step and formatted formula:

![Word output showing the Enter a formula step and its E2 instruction](docs/screenshots/authoring_enter.webp)

The Excel starter supplies the labels and data while leaving the reader's calculations blank:

![Excel starter with source measurements, a blank calculation column, and labeled results with blank Value cells](docs/screenshots/authoring_workbook.webp)

The complete source is [docs/examples/authoring_features.md](docs/examples/authoring_features.md).
Roots is simply a small formatting example. Use your own content in your tutorial.

## See instructor examples

The existing z-test lessons show finished classroom materials and source structure:

- [tutorial_data/babies/babies_1_z_test.md](tutorial_data/babies/babies_1_z_test.md)
- [tutorial_data/microbes/microbes_1_z_test.md](tutorial_data/microbes/microbes_1_z_test.md)

This cropped F-test instruction shows a longer formula with the instructor's explanation:

![Microbes F-test instruction with a formatted formula and its explanation](docs/screenshots/microbes_4_formula_instruction.webp)

Browse [docs/TUTORIAL_CATALOG.md](docs/TUTORIAL_CATALOG.md) for the collection. These examples
demonstrate what the compiler can produce. Your tutorial can use a different scenario and structure.

## Build your files

Follow [docs/INSTALL.md](docs/INSTALL.md) once to download the project and install its requirements.
In a Bash shell opened in the project folder:

```bash
source source_me.sh
python3 make_tutorial.py lint docs/examples/authoring_features.md
python3 make_tutorial.py build docs/examples/authoring_features.md --format docx,xlsx
```

Open the Word and Excel files in `tutorial_output/authoring_features/`. For a PDF as well, run
the build with `--format all`; that uses LibreOffice. Use your own `.md` path when building your
tutorial. See Part 3 for the normal edit, build, inspect, and correct workflow.

Local rendering and spreadsheet checks are separate from Google Docs/Sheets import and classroom
use. Offline lint does not evaluate scientific accuracy or prove Google compatibility.

## Reference and maintenance

- [docs/TUTORIAL_SPEC.md](docs/TUTORIAL_SPEC.md): complete supported syntax and limits.
- [docs/USAGE.md](docs/USAGE.md): build commands and optional workbook maintenance tools.
- [docs/screenshots/README.md](docs/screenshots/README.md): actual-output screenshot provenance
  and the existing refresh command.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): project changes.
