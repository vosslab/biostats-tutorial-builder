# Plan: Required reflection questions

## Goal

Require each tutorial source to author one `### Reflection Questions` section under `## Workbook`.
Keep the questions in the single Markdown source, show a generated reflection section in the DOCX,
and collect them on a generated workbook tab with editable answer space. The DOCX and workbook use
the same literal editable question identifiers. Authors write ordinary numbered list items; the
compiler normalizes their source numbering to begin at 1, regardless of the Markdown start value.
They do not supply tab names, parameters, citation IDs, or step associations.

## Authoring contract

The Workbook section contains worksheet declarations and tables plus exactly one reflection heading
and a nonempty ordinary ordered list. The reserved heading has no parameters. Questions are authored
as ordinary Markdown list items. The compiler normalizes source list numbering to `1.`, `2.`, etc.,
regardless of the authored Markdown start value; starting at 1 remains author guidance, not a lint
gate.

```markdown
## Workbook

### Sheet: Roots

| Root length | Squared length |
| --- | --- |
| 12 | |
| 15 | |

### Reflection Questions

1. Which measure best represents the center of these data, and why?
2. What does the distribution suggest about the observations?

## Tutorial

### Part: Describe the data

#### Step: Compare measures

After you calculate the mean and median, answer Reflection Question 1.
```

Reflection questions can be answered at different points in the tutorial. Authors place ordinary
timing references in Tutorial prose and keep their numbering accurate when the list changes. The
compiler does not link questions to activities, steps, or citations. The Workbook section remains
excluded from the generated DOCX except for the generated reflection section.

## Generated output

- Append one generated `Reflection Questions` section to the DOCX using native Heading styles.
  Direct students to the matching workbook tab. Use the same literal identifiers as editable Normal
  text in the document and tab. Do not use Word automatic list numbering or numbering fields for IDs.
- Add one generated reflection tab per source. A single-source tab is `Reflection Questions`.
  In a multi-source build, use `Part {resolvedpart} Reflection` (for example, `Part 2 Reflection`).
  Use the single unique explicit Part identity within each source; use that source's one-based
  position in build order only when it has no unique explicit Part identity. Duplicate resolved
  identities across sources and conflicting names fail before publishing; they do not trigger
  a fallback to source position.
- Sort multi-source tabs in source order. Each source retains its own question list and tab.
- Number a single source's questions `1`, `2`, ... when it has no explicit Part identity. With a
  unique explicit Part 3 identity, use `3.1`, `3.2`, ... . In a merged build, use the resolved Part
  identity, so an implicit first source uses `1.1`, `1.2`, and an implicit second source uses
  `2.1`, `2.2`. Keep identifiers identical in DOCX and XLSX.
- Use one wide worksheet column with each question stacked above its answer area. Wrap question
  text and set question/answer rows at least 47.25 points high. Follow the supplied descriptive-
  statistics workbook's layout precedent.
- Preserve authored question text. Add no configurable numbering, tab-name, or layout parameters.

## Work and evidence

| Workstream | Completion evidence |
| --- | --- |
| Core contract | Compiler enforces the Workbook heading/list rule and preserves source locations. |
| Generated output | DOCX section and workbook tabs use matching identifiers, names, ordering, and readable answer rows. |
| Source migration | Migrate the 12 current lessons, templates, and buildable examples separately; preserve question wording and author timing references. |
| Tests and consumers | Focused checks cover required syntax, number resolution, duplicate identities, generated outputs, and existing consumers of workbook sheet order. |
| Authoring docs | Guides and specification show the literal syntax, numbering rules, generated tab, and answer layout. |
| Review | Inspect generated DOCX and workbook output; record exact automated and visual checks in the execution report. |

## Boundaries

Do not add activity-local reflection blocks, author parameters, citation IDs, automatic activity
associations, question grading, answer checking, tab-name options, or a separate reflection-content
file. Questions are not calculation inputs. Keep the frozen descriptive-statistics workbook as a
visual precedent; do not migrate that archived course. Keep all LibreOffice-invoking commands outside
the sandbox through repository scripts.

## Status

Implementation is complete and accepted. All core, corpus, build, visual, and review evidence is
recorded in [the execution ledger](../reports/required_reflection_execution.md). Google import is
unverified.
