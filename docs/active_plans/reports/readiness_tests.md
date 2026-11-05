# Readiness test report

Historical snapshot: the Google runner was removed on 2026-11-05. Use
[LOCAL_VALIDATION.md](../../LOCAL_VALIDATION.md) for the current local-only workflow.

## New Python source checks

The tracked-only repository discovery gates did not include the untracked
`tutorial_lib/formula_io.py`. I enumerated new Python files with
`git ls-files --others --exclude-standard '*.py'`; it returned only that path.
I invoked the gates' single-file APIs directly using
`source source_me.sh && PYTHONPATH=tests python3`:

| Check | Result |
| --- | --- |
| `test_pyflakes_code_lint.collect_violations([path])` | Pass, no violations |
| `test_bandit_security.collect_violations([path])` | Pass, no violations |
| `file_utils.collect_python_violations([path], test_function_typing.check_file)` | Pass, no violations |
| `file_utils.collect_python_violations([path], test_import_star.check_file)` | Pass, no violations |
| `file_utils.collect_python_violations([path], test_import_dot.check_file)` | Pass, no violations |
| ASCII byte compliance and `test_shebangs.check_file(rel)` | Pass |

## CLI smoke checks

`make_tutorial.py --help` returned 0 and listed `lint`, `build`, and
`import-xlsx`. Both validator help commands returned 0 and showed their
current interfaces: `devel/validate_libreoffice.py` accepts tutorial paths,
required expectations, and optional output; `devel/validate_google_sheets.py`
accepts tutorial paths, optional output/expectations, and dry-run/live modes.

The renamed `make_tutorial.py import-xlsx` command returned 0 on the generated
`babies_1_z_test.xlsx` bundle. It wrote an authoring draft to the ignored
verification directory. The draft preserved both worksheet names and all
102 nonempty workbook cell values (including escaped embedded newlines). It
contains the expected instruction that tutorial prose remains to be authored;
that is the importer's draft contract, not a missing final lesson.

## Earlier full test suite

Command: `source source_me.sh && python3 -m pytest tests/ -q`, run outside the
sandbox as required by `AGENTS.md`. After the README opening was shortened to
plain prose, that run passed **1309 tests in 2.93 seconds**. The earlier run had
1307 passes and two failures in the README opening checks; the full suite passed
after that correction. A post-archive rerun, including documentation links,
passed 1309 tests in 3.04 seconds; its log is
`tutorial_output/verification/readiness/pytest_final_closeout.log`.
