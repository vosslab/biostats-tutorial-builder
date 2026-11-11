"""Durable author-facing semantic contracts independent of rendering internals."""

import json
import tutorial_lib.compiler
import tutorial_lib.parser


def compile_tutorial(instructions: str, workbook: str = "") -> object:
	if not workbook:
		workbook = "### Sheet: Data\n\n| A | B |\n| --- | --- |\n| 1 | 2 |"
	source = "# Example\n\n## Workbook\n\n" + workbook
	source += ("\n\n### Reflection Questions\n\n"
		"1. How do the results support your conclusion?\n\n"
		"## Tutorial\n\n### Part 3: Analysis\n\n#### Step: Calculate\n\n")
	source += instructions
	return tutorial_lib.compiler.compile_source(source)


def test_scalar_fidelity_and_student_destinations() -> None:
	workbook = '### Sheet: Data\n\n| "001" | `"=text"` | `=IF(A2="x\\|y",1,0)` |\n'
	workbook += '| --- | --- | --- |\n| 0 | FALSE | |'
	document = compile_tutorial('- **Enter D2:** `=SUM(A2:B2)`', workbook)
	assert not document.has_errors
	sheet = document.worksheets[0]
	assert sheet.cells[(1, 1)].scalar.value == "001"
	assert sheet.cells[(1, 2)].scalar.kind == "text"
	assert sheet.cells[(1, 3)].scalar.value == '=IF(A2="x|y",1,0)'
	assert (2, 4) in sheet.entry_cells and (2, 4) not in sheet.cells
	assert sheet.cells[(2, 1)].scalar.value == 0
	assert sheet.cells[(2, 2)].scalar.value is False
	# Ordinary JSON escaping survives table syntax and optional code spans.
	for value in ('a\\b', 'say "hi"', 'x|y', 'line\nnext', '*literal*'):
		encoded = json.dumps(value).replace("|", "\\|")
		workbook = f'### Sheet: Data\n\n| {encoded} | `{encoded}` |\n| --- | --- |'
		document = compile_tutorial('- **Enter C2:** ' + json.dumps(value), workbook)
		assert not document.has_errors
		assert [cell.scalar.value for cell in document.worksheets[0].cells.values()] == [value, value]
		assert document.actions[0].scalar.value == value
	literal = compile_tutorial('- **Label C2:** `a\\b`')
	assert literal.actions[0].scalar.value == 'a\\b'


def test_automatic_formula_scalars_preserve_copy_text_and_validation() -> None:
	"""Plain formulas must retain operators and take the same validation path as code."""
	formulas = ['=A2*B2*3', '=IF(A2 > 0, "A*B", SUM(A2:B2))', "='Data'!A2 + B2"]
	for formula in formulas:
		variants = [formula, '`' + formula + '`', '\n\n  ```sheets\n  ' + formula + '\n  ```']
		for value in variants:
			document = compile_tutorial('- **Enter C2:** ' + value)
			assert not document.has_errors
			assert document.actions[0].scalar.value == formula
			assert document.formula_checks[0].formula == formula
			assert document.formula_checks[0].references
			assert (2, 3) not in document.worksheets[0].cells
	literals = [
		('Enter', '"=A2*B2*3"', '=A2*B2*3'),
		('Enter', '`"=A2*B2*3"`', '=A2*B2*3'),
		('Enter', json.dumps('*literal* _text_ <br> a\\b'), '*literal* _text_ <br> a\\b'),
		('Label', '=A2*B2*3', '=A2*B2*3'),
		('Label', '`=A2*B2*3`', '=A2*B2*3'),
	]
	for action, encoded, value in literals:
		document = compile_tutorial(f'- **{action} C2:** ' + encoded)
		assert not document.has_errors
		assert document.actions[0].scalar.kind == "text"
		assert document.actions[0].scalar.value == value
		assert not document.formula_checks
	invalid = compile_tutorial('- **Enter C2:** =SUM(Absent!A2:B2)')
	assert any(item.category == "unknown-sheet" for item in invalid.diagnostics)


def test_narrative_formulas_stop_before_prose_and_preserve_markdown() -> None:
	"""Protect prose boundaries without surrendering multiplication to Markdown."""
	source = 'Use =A2*B2*C2, then **compare** =SUM(A2:B2) with (=XXXX).\n\n'
	source += 'Keep alpha = 0.05, x=3, a<=b, a>=b and https://example.org/?x=3.\n\n'
	source += '[=IF(A2<3,"A B",0)](https://example.org) and **=A2*B2**.'
	source += '\n\nCompare =A1+B1. Use =T.TEST(A2:A3,B2:B3,2,3).'
	document = tutorial_lib.parser.parse_source(source, 'narrative.md')
	children = [child for token in document.tokens for child in token.children or []]
	formulas = [child.content for child in children if child.meta.get("role") == "formula"]
	assert formulas == [
		'=A2*B2*C2', '=SUM(A2:B2)', '=XXXX', '=IF(A2<3,"A B",0)', '=A2*B2',
		'=A1+B1', '=T.TEST(A2:A3,B2:B3,2,3)',
	]
	assert document.source == source
	assert any(child.type == "strong_open" for child in children)
	assert sum(child.type == "link_open" for child in children) == 1


def test_invalid_tables_report_physical_and_related_locations() -> None:
	workbook = '### Sheet: Data\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n'
	workbook += '\n#### At: B2\n\n| | |\n| --- | --- |'
	document = compile_tutorial('- **Explain:** Observe.', workbook)
	overlap = next(item for item in document.diagnostics if item.category == "table-overlap")
	assert overlap.address == "B2" and overlap.related.start_line == 7
	ragged = compile_tutorial('- **Explain:** Observe.', workbook.replace('| 1 | 2 |', '| 1 |'))
	assert any(item.category == "ragged-table" for item in ragged.diagnostics)


def test_alternatives_preserve_possible_states_and_numbering() -> None:
	instructions = '- **Alternative: First**\n  - **Enter D2:** `=SUM(A2:B2)`\n'
	instructions += '- **Alternative: Second**\n  - **Enter D2:** `=AVERAGE(A2:B2)`\n'
	instructions += '\n#### Step: Continue\n\n##### Substep: Review\n\n'
	instructions += '- **Replace D2:** `=MAX(A2:B2)`\n'
	document = compile_tutorial(instructions)
	assert not document.has_errors
	assert [heading.number for heading in document.headings] == ["3", "1", "2", "2.1"]
	conditional = compile_tutorial(instructions.replace(
		'  - **Enter D2:** `=AVERAGE(A2:B2)`', '  - **Explain:** No entry.'))
	assert any(item.category == "replacement-unavailable" for item in conditional.diagnostics)


def test_informational_hyphenated_headings_and_structural_typos() -> None:
	"""Step-by-Step is prose, while malformed numbered Step prefixes remain errors."""
	document = compile_tutorial('##### Step-by-Step Tutorial:\n\nRead the instructions.')
	assert not document.has_errors
	assert document.headings[-1].display == 'Step-by-Step Tutorial:'
	for heading in ('Step2: Calculate', 'Step 2 Calculate', 'Step:'):
		document = compile_tutorial('#### ' + heading + '\n\nRead the instructions.')
		assert any(item.category == 'heading-syntax' for item in document.diagnostics)


def test_static_formula_tokens_skip_strings_and_report_partial_coverage() -> None:
	instructions = '- **Enter D2:** `=IF(A2="Missing!Z99",SUM($A$2:B$2),0)`\n'
	instructions += '- **Enter D3:** `=SUM(A:A)+INDIRECT("Z99")`\n'
	document = compile_tutorial(instructions)
	assert not document.has_errors
	assert document.formula_checks[0].status == "verified"
	assert [ref.address for ref in document.formula_checks[0].references] == ["A2", "$A$2:B$2"]
	assert document.formula_checks[1].status == "unchecked"
	wrong_sheet = compile_tutorial('- **Enter D2:** `=SUM(Absent!A2:B2)`')
	assert any(item.category == "unknown-sheet" for item in wrong_sheet.diagnostics)
	for address in ('XFE1', 'A1048577', 'A0', 'B2:A1'):
		invalid = compile_tutorial(f'- **Enter D2:** `={address}+1`')
		assert any(item.category == "invalid-address" and item.severity == "error"
			for item in invalid.diagnostics)
		assert invalid.formula_checks[0].status != "verified"
	for formula in ('=SUM(A1))', '=A1)'):
		malformed = compile_tutorial(f'- **Enter D2:** `{formula}`')
		assert malformed.has_errors
		assert malformed.formula_checks[0].status != "verified"
		diagnostic = next(item for item in malformed.diagnostics if item.category == "formula-syntax")
		assert diagnostic.span.start_line > 1
		assert "Correct the formula syntax" in diagnostic.correction


def test_literal_scalar_reference_text_is_not_classified_as_workbook_reference() -> None:
	for action in ('Label', 'Enter'):
		document = compile_tutorial(f'- **{action} C2:** `Absent!A1`')
		assert not any(item.category == "unknown-sheet" for item in document.diagnostics)
	assert any(item.category == "unknown-sheet" for item in compile_tutorial(
		'- **Explain:** Refer to `Absent!A1`.').diagnostics)
	assert any(item.category == "unknown-sheet" for item in compile_tutorial(
		'- **Select:** `Absent!A1`').diagnostics)


def test_action_payload_contracts_produce_source_diagnostics() -> None:
	cases = [
		('- **Choose:** **Insert** > Chart', 'menu-path'),
		('- **Select:** **A1**', 'action-target'),
		('- **Label C2:**\n\n  ```sheets\n  =A2\n  ```', 'action-scalar'),
		('- **Enter C2:**\n\n  ```sheets\n  =\n  ```', 'action-scalar'),
		('- **Enter C2:** `=   `', 'action-scalar'),
	]
	for instructions, category in cases:
		document = compile_tutorial(instructions)
		assert document.has_errors
		assert any(item.category == category and item.span.start_line > 1
			for item in document.diagnostics)
	valid = compile_tutorial('- **Enter C2:**\n\n  ```sheets\n  =A2\n  ```')
	assert not valid.has_errors
	assert valid.actions[0].scalar.value == '=A2'


def test_label_only_list_items_need_substantive_content() -> None:
	empty_leaf = compile_tutorial('- **Guide:** **For Sample Means:**')
	diagnostics = [item for item in empty_leaf.diagnostics
		if item.category == "incomplete-instruction"]
	assert len(diagnostics) == 1
	assert diagnostics[0].severity == "error"
	assert diagnostics[0].span.start_line == 21

	valid = compile_tutorial('- **Guide:** **Setup Another Table:**\n'
		'  - **Enter C2:** `=A2`')
	assert not any(item.category == "incomplete-instruction" for item in valid.diagnostics)
	assert not valid.has_errors

	for instructions in (
		'- **Guide:**\n\n  Continue in prose.',
		'- **Guide:** **For Sample Means:**\n  Continue in the same paragraph.',
		'- **Enter C2:** `=A2`',
	):
		document = compile_tutorial(instructions)
		assert not any(item.category == "incomplete-instruction" for item in document.diagnostics)

	empty_child = compile_tutorial('- **Guide:**\n  - **Setup Another Table:**')
	assert any(item.category == "incomplete-instruction" and item.span.start_line == 22
		for item in empty_child.diagnostics)

	nonempty_fence = compile_tutorial('- **Guide:** **For Sample Means:**\n\n'
		'  ```text\n  Notes for this step.\n  ```')
	assert not any(item.category == "incomplete-instruction"
		for item in nonempty_fence.diagnostics)
	empty_fence = compile_tutorial('- **Guide:** **For Sample Means:**\n\n'
		'  ```text\n  ```')
	assert any(item.category == "incomplete-instruction" for item in empty_fence.diagnostics)

	outside_tutorial = ('# Example\n\n- **Introduction:** **Overview:**\n\n'
		'## Workbook\n\n- **Worksheet:** **Instructions:**\n\n'
		'### Sheet: Data\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n'
		'### Reflection Questions\n\n'
		'1. How do the results support your conclusion?\n\n'
		'## Tutorial\n\n### Part 3: Analysis\n\n#### Step: Calculate\n\n'
		'- **Enter C2:** `=A2`')
	document = tutorial_lib.compiler.compile_source(outside_tutorial)
	assert not any(item.category == "incomplete-instruction" for item in document.diagnostics)
	inside_tutorial = outside_tutorial.replace(
		'- **Enter C2:** `=A2`', '- **Guide:** **For Sample Means:**')
	# The same label-only shape is diagnosed when it appears in the Tutorial region.
	document = tutorial_lib.compiler.compile_source(inside_tutorial)
	assert any(item.category == "incomplete-instruction" for item in document.diagnostics)


def test_unsupported_footnotes_exempt_literal_code() -> None:
	literal = compile_tutorial('- **Explain:** Type `[^1]` literally.')
	assert not literal.has_errors
	footnote = compile_tutorial('- **Explain:** This needs a footnote[^1].')
	assert any(item.category == "unsupported-content" for item in footnote.diagnostics)


def test_source_capacity_allows_spare_rows_without_hiding_missing_results() -> None:
	"""Input capacity can be partly empty; unsupplied calculation cells still warn."""
	workbook = "### Sheet: Data\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n"
	workbook += "\n- **Region A1:B100:** source\n"
	document = compile_tutorial(
		"- **Enter D2:** =COUNT(A2:A100)\n- **Enter D3:** =E2+1", workbook)
	assert not document.has_errors
	warnings = [item for item in document.diagnostics if item.category == "unavailable-input"]
	assert [item.address for item in warnings] == ["E2"]
