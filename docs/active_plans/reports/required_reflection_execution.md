# Required reflection questions: execution ledger

The accepted contract is in [required_reflection_questions.md](../active/required_reflection_questions.md).
This ledger records implementation evidence and root acceptance.

| Workstream | Status | Evidence or next evidence |
| --- | --- | --- |
| Core | Complete | Accepted implementation supplies the required Workbook list, matching generated output, automatic Part IDs, and no step mapping. |
| Corpus | Complete | All 12 corpus sources and 30 questions, templates, and examples compile; 13 single-source plus shared outputs match 46 source/output hashes. |
| Tests and consumers | Complete | 19 focused reflection tests pass. Final `source source_me.sh && python3 -m pytest tests -q` reports 2,146 passed, 1 failed; only the existing Podman connection failure remains (`/tmp/reflection_release_suite.log`). |
| Authoring docs | Complete | Updated student-facing contract and added a brief actual-preview capture guide; `docs/screenshots/authoring_reflection.webp` is natively inspected. |
| Specification and decisions | Complete | Fresh SPEC review `reflection_spec_rereview_v2` accepted the Workbook-list contract. |
| Review | Complete | Fresh QUALITY `reflection_quality_review_v2` and INTEGRATION `reflection_integration_review_v2` accepted. Calc: 103 expectations pass, zero errors; see [visual report](reflection_build_visual.md). |
| Root acceptance | Complete | Root accepted the integrated feature and evidence. |

Model assignment: Luna for bounded documentation work; Sol for core-coupled implementation. This is
an execution note, not a product or authoring requirement.

## Settled contract clarifications

- **D2 — tab names:** In shared builds use the literal spaced form `Part 2 Reflection`, following
  the examples. Resolve the identity from a unique explicit Part number or the source's one-based
  build position. Keep the native Word tab name `Reflection Questions` for a single-source build.
- **D3 — editable identifiers:** Render generated question identifiers as literal editable Normal
  text in both DOCX and workbook. Keep existing native Heading styles for headings. Avoid Word
  automatic list numbering, which can renumber imported documents (for example, `3.1`). Production
  code does not need numbered fields for these identifiers.
- **D4 — source list start:** Starting the Markdown ordered list at 1 is author guidance, not a
  compiler gate. Normalize its parsed ordered-list sequence to start at 1 as planned, regardless of
  the authored start value.

## Current evidence

- 19 focused reflection feature tests pass.
- All 12 corpus sources and 30 questions, templates, and examples compile. Thirteen single-source
  builds plus the shared build match all 46 output/source hashes.
- Calc passes 103 checks with zero errors. See [the build and visual report](reflection_build_visual.md).
- Native inspection covered 41 documentation images, including `docs/screenshots/authoring_reflection.webp`;
  the latest receipt contains 14 source and 22 image hashes. The actual-preview capture guide is in
  the authoring documentation.
- **Capture the actual preview:** run `source source_me.sh && python3 devel/refresh_documentation.py`
  outside the sandbox, then open `docs/screenshots/authoring_reflection.webp` in `view_image` and
  inspect the question text, numbering, and answer area. The refresh updates the screenshot receipt.
- Final command `source source_me.sh && python3 -m pytest tests -q` reports 2,146 passed and one
  existing Podman connection failure; full log: `/tmp/reflection_release_suite.log`. The earlier
  2,120-passed Caffeine evidence is a separate historical checkpoint.
- Google Docs/Sheets import remains unverified.

## Documentation checks

- Read `AGENTS.md`, `docs/MARKDOWN_STYLE.md`, `docs/REPO_STYLE.md`, `docs/PYTHON_STYLE.md`, and the
  latest dated `docs/CHANGELOG.md` entry.
- Searched the owned guides and contract documents for the old reflection proposal before editing.
- Confirmed the linked target filenames exist for the new links.
- `git diff --check` passed for tracked documentation edits; a trailing-whitespace search passed
  across all edited documentation, including the new plan and ledger.

The feature is implemented, reviewed, and accepted. No Google import verification is claimed.
