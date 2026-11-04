"""Maintain authored worksheet coordinates after a deliberate layout edit.

This module edits Markdown only when an author asks for a familiar spreadsheet
operation.  It does not choose a layout, create formulas, or alter scientific
interpretation.  A candidate is compiled before it can replace the source.
"""

import dataclasses
import difflib
import os
import pathlib
import re
import tempfile

import openpyxl.formula.tokenizer
import tutorial_lib.compiler
import tutorial_lib.formulas
import tutorial_lib.model
import tutorial_lib.parser
import tutorial_lib.references


CELL_OR_RANGE = re.compile(
	r"(?:(?:'(?:(?:[^']|'')+)'|[A-Za-z0-9_ .-]+)!)?"
	r"\$?[A-Za-z]{1,3}\$?[1-9][0-9]*(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?"
)
CELL_PART = re.compile(r"(\$?)([A-Za-z]{1,3})(\$?)([1-9][0-9]*)\Z")
ROW_WORD = re.compile(r"\brow(s?)\s+([1-9][0-9]*)\b", re.IGNORECASE)
# Spreadsheet columns are conventionally written in uppercase.  Matching only
# uppercase coordinates prevents ordinary prose such as "column is" from being
# mistaken for the valid Excel column IS during a layout edit.
COLUMN_WORD = re.compile(r"\b(?i:column(s?))\s+([A-Z]{1,3})(?:-([A-Z]{1,3}))?\b")
PROSE_REFERENCE = re.compile(
	# A coordinate is prose only when an author has named a spreadsheet thing.
	# Generic prepositions ("in B12") are common in biology and statistics;
	# scanning them changes prose rather than maintaining a worksheet.
	r"\b(?P<introducer>cell|cells|range|ranges|table|label|enter|replace|select)\s+"
	r"(?P<opening>\*\*)?(?P<reference>\$?[A-Za-z]{1,3}\$?[1-9][0-9]*"
	r"(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?)(?P<closing>\*\*)?",
	re.IGNORECASE,
)
TECHNICAL_RANGE_REFERENCE = re.compile(
	r"\b(?P<introducer>use|using|compare|write|calculate)\s+"
	r"(?P<reference>\$?[A-Za-z]{1,3}\$?[1-9][0-9]*:\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)",
	re.IGNORECASE,
)
INSTRUCTION_CUE = re.compile(
	r"\b(?:use|using|compare|write|calculate|enter|label|select|fill|formula|worksheet|spreadsheet)\b",
	re.IGNORECASE,
)
BINDING_TARGET = re.compile(r"\((?:label|enter|replace|fill|select):([^)]*)\)", re.IGNORECASE)
REGION_TARGET = re.compile(r"(\*\*Region\s+)([^:*]+(?:\:[^:*]+)?)(:\*\*)", re.IGNORECASE)
ANCHOR_TARGET = re.compile(r"^(####\s+At:\s+)(\S+)(\s*)$")
LEGACY_TARGET = re.compile(
	r"(\*\*(?:Label|Enter|Replace|Fill|Select)\s+)(\$?[A-Za-z]{1,3}\$?[1-9][0-9]*"
	r"(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?)(:\*\*)",
	re.IGNORECASE,
)
ACTION_CELL = re.compile(
	r"(\*\*)(\$?[A-Za-z]{1,3}\$?[1-9][0-9]*(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?)(\*\*:\s*"
	r"(?:Type|Enter|Label|Use|Select)\b)", re.IGNORECASE,
)
SHEET_HEADING = re.compile(r"^###\s+Sheet:\s*(.+?)\s*$")
TUTORIAL_SHEET = re.compile(r"\*\*Worksheet:\*\*\s*([^\n]+)")


class WorksheetEditError(ValueError):
	"""Stop an unsafe edit before source bytes are changed."""


@dataclasses.dataclass(frozen=True)
class WorksheetEdit:
	"""One familiar spreadsheet maintenance operation."""

	kind: str
	sheet: str
	at: int | None = None
	count: int | None = None
	source_range: str | None = None
	destination: str | None = None
	data_range: str | None = None
	rows: int | None = None


@dataclasses.dataclass(frozen=True)
class WorksheetEditResult:
	"""Previewable source replacement and author review notices."""

	source: str
	updated_source: str
	diff: str
	notices: tuple[str, ...]


#============================================
def column_number(value: str) -> int:
	"""Accept a spreadsheet column name or positive column number."""
	if value.isdigit():
		column = int(value)
	else:
		column = tutorial_lib.references.column_number(value)
	if not 1 <= column <= 16384:
		raise WorksheetEditError("Column must be between A and XFD")
	return column


#============================================
def prepare_edit(path: pathlib.Path, request: WorksheetEdit) -> WorksheetEditResult:
	"""Compile, transform, recompile, and return an unwritten source preview.

	Args:
		path: Existing authoritative Markdown source.
		request: Validated author-requested worksheet operation.
	"""
	original_source = path.read_text(encoding="utf-8")
	document = tutorial_lib.compiler.compile_source(original_source, path)
	if document.has_errors:
		raise WorksheetEditError("Source does not compile; correct it before editing coordinates")
	sheet = _worksheet(document, request.sheet)
	_validate_request(request, sheet)
	if request.kind == "move-range":
		transform = _move_transform(request, sheet)
	elif request.kind == "resize-observations":
		transform = _resize_transform(request, sheet)
	else:
		transform = _insert_transform(request)
	# Table anchoring changes the candidate only.  The preview guard must retain
	# the exact bytes that the author originally approved for editing.
	_scopes = _line_scopes(original_source, document)
	updated, notices = _transform_source(original_source, _scopes, request.sheet, transform,
		document)
	updated = _patch_workbook_tables(updated, request, sheet, transform)
	if request.kind == "resize-observations":
		updated = _extend_data_table(updated, request, sheet)
		notices.extend(_worked_example_notices(updated, request, transform))
	if updated == original_source:
		raise WorksheetEditError("The requested edit does not affect this worksheet source")
	candidate = tutorial_lib.compiler.compile_source(updated, path)
	if candidate.has_errors:
		errors = [item.message for item in candidate.diagnostics if item.severity == "error"]
		raise WorksheetEditError("Edited source does not compile: " + "; ".join(errors[:3]))
	diff = "".join(difflib.unified_diff(original_source.splitlines(keepends=True),
		updated.splitlines(keepends=True), fromfile=str(path), tofile=str(path)))
	return WorksheetEditResult(original_source, updated, diff, tuple(dict.fromkeys(notices)))


#============================================
def write_edit(path: pathlib.Path, result: WorksheetEditResult) -> None:
	"""Atomically replace an unchanged source with its already-compiled candidate."""
	if path.read_text(encoding="utf-8") != result.source:
		raise WorksheetEditError("Source changed after preview; run the edit again")
	with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
		prefix=path.name + ".", suffix=".tmp", delete=False) as handle:
		handle.write(result.updated_source)
		temporary = pathlib.Path(handle.name)
	os.replace(temporary, path)


#============================================
def _worksheet(document: object, name: str) -> object:
	"""Find one declared worksheet using the compiler's case-insensitive rule."""
	matches = [sheet for sheet in document.worksheets if sheet.name.casefold() == name.casefold()]
	if len(matches) != 1:
		raise WorksheetEditError(f"Unknown worksheet: {name}")
	if matches[0].is_reflection:
		raise WorksheetEditError("Reflection worksheet layout is generated; edit its authored questions")
	return matches[0]


#============================================
def _validate_request(request: WorksheetEdit, sheet: object) -> None:
	"""Reject unsupported geometry before source transformation (ASVS 2.2.1)."""
	if request.kind in ("insert-rows", "insert-columns"):
		if request.at is None or request.count is None or request.at < 1 or request.count < 1:
			raise WorksheetEditError("Insert needs positive --at and --count values")
		limit = 1048576 if request.kind == "insert-rows" else 16384
		if request.at + request.count - 1 > limit:
			raise WorksheetEditError("Insert exceeds XLSX worksheet bounds")
		return
	if request.kind == "move-range":
		source = tutorial_lib.references.parse_reference(request.source_range or "", sheet.name)
		destination = tutorial_lib.references.parse_reference(request.destination or "", sheet.name)
		if source is None or destination is None or ":" in (request.destination or ""):
			raise WorksheetEditError("Move needs --range A1:B2 and a one-cell --destination")
		if source.sheet.casefold() != sheet.name.casefold() or destination.sheet.casefold() != sheet.name.casefold():
			raise WorksheetEditError("Move coordinates must belong to the selected worksheet")
		end_row = destination.start_row + source.end_row - source.start_row
		end_column = destination.start_column + source.end_column - source.start_column
		if end_row > 1048576 or end_column > 16384:
			raise WorksheetEditError("Move destination exceeds XLSX worksheet bounds")
		_ensure_move_destination(sheet, source, destination)
		return
	if request.kind == "resize-observations":
		reference = tutorial_lib.references.parse_reference(request.data_range or "", sheet.name)
		if reference is None or reference.start_row != 1 or reference.sheet.casefold() != sheet.name.casefold():
			raise WorksheetEditError("Resize needs a declared data table range beginning in row 1")
		if request.rows is None or request.rows < 1 or request.rows + 1 > 1048576:
			raise WorksheetEditError("Resize needs a positive observation count within XLSX limits")
		if not any(region.start_row == reference.start_row and region.start_column == reference.start_column
			and region.end_row == reference.end_row and region.end_column == reference.end_column
			for region in sheet.regions):
			raise WorksheetEditError("Resize range must exactly match a declared Markdown data table")
		return
	raise WorksheetEditError(f"Unknown worksheet edit: {request.kind}")


#============================================
def _ensure_move_destination(sheet: object, source: object, destination: object) -> None:
	"""Reject a cut that would overwrite authored content outside its old rectangle."""
	for row, column in list(sheet.cells) + list(sheet.entry_cells):
		cell = sheet.cells.get((row, column))
		if cell is not None and cell.scalar.kind == "blank":
			continue
		if source.start_row <= row <= source.end_row and source.start_column <= column <= source.end_column:
			continue
		end_row = destination.start_row + source.end_row - source.start_row
		end_column = destination.start_column + source.end_column - source.start_column
		if (destination.start_row <= row <= end_row
			and destination.start_column <= column <= end_column):
			raise WorksheetEditError("Move destination contains authored content outside the moved range")


#============================================
def _insert_transform(request: WorksheetEdit) -> object:
	"""Create an A1 transformation for an inserted row or column."""
	def transform(reference: object) -> object:
		if request.kind == "insert-rows":
			return _reference_with(reference, _insert_index(reference.start_row, request.at, request.count),
				_insert_index(reference.end_row, request.at, request.count), reference.start_column,
				reference.end_column)
		return _reference_with(reference, reference.start_row, reference.end_row,
			_insert_index(reference.start_column, request.at, request.count),
			_insert_index(reference.end_column, request.at, request.count))
	return transform


#============================================
def _insert_index(value: int, at: int, count: int) -> int:
	"""Apply Excel-style insertion to one axis value."""
	return value + count if value >= at else value


#============================================
def _move_transform(request: WorksheetEdit, sheet: object) -> object:
	"""Move references wholly inside the selected cut rectangle."""
	source = tutorial_lib.references.parse_reference(request.source_range, sheet.name)
	destination = tutorial_lib.references.parse_reference(request.destination, sheet.name)
	row_delta = destination.start_row - source.start_row
	column_delta = destination.start_column - source.start_column
	def transform(reference: object) -> object:
		inside = (source.start_row <= reference.start_row <= reference.end_row <= source.end_row
			and source.start_column <= reference.start_column <= reference.end_column <= source.end_column)
		overlap = not (reference.end_row < source.start_row or reference.start_row > source.end_row
			or reference.end_column < source.start_column or reference.start_column > source.end_column)
		if overlap and not inside:
			raise WorksheetEditError(
				f"Reference {reference.address} partially intersects moved range {request.source_range}")
		if not inside:
			return reference
		return _reference_with(reference, reference.start_row + row_delta,
			reference.end_row + row_delta, reference.start_column + column_delta,
			reference.end_column + column_delta)
	return transform


#============================================
def _resize_transform(request: WorksheetEdit, sheet: object) -> object:
	"""Extend exact data-bottom references but retain intentional spare rows."""
	data = tutorial_lib.references.parse_reference(request.data_range, sheet.name)
	old_end = data.end_row
	new_end = request.rows + 1
	def transform(reference: object) -> object:
		# A lone C26 can be a historical observation or worked example.  Only
		# ranges express a data-dependent extent without rewriting science prose.
		if reference.start_row == reference.end_row:
			return reference
		end = new_end if reference.end_row == old_end else reference.end_row
		start = reference.start_row
		return _reference_with(reference, start, end, reference.start_column, reference.end_column)
	return transform


#============================================
def _reference_with(reference: object, start_row: int, end_row: int,
	start_column: int, end_column: int) -> object:
	"""Create a reference retaining its worksheet identity."""
	address = _address(start_row, end_row, start_column, end_column)
	return tutorial_lib.model.CellReference(reference.sheet, start_row, start_column,
		end_row, end_column, address)


#============================================
def _address(start_row: int, end_row: int, start_column: int, end_column: int) -> str:
	"""Render one bounded A1 address without presentation punctuation."""
	first = tutorial_lib.references.column_letters(start_column) + str(start_row)
	last = tutorial_lib.references.column_letters(end_column) + str(end_row)
	return first if first == last else first + ":" + last


#============================================
def _line_scopes(source: str, document: object) -> list[str | None]:
	"""Assign conservative worksheet scopes to physical source lines."""
	lines = source.splitlines()
	analysis_sheets = [sheet for sheet in document.worksheets if not sheet.is_reflection]
	single = analysis_sheets[0].name if len(analysis_sheets) == 1 else None
	scopes = []
	workbook_sheet = None
	tutorial_sheet = single
	in_tutorial = False
	for line in lines:
		if line.strip() == "## Tutorial":
			in_tutorial = True
		if not in_tutorial:
			match = SHEET_HEADING.match(line)
			if match is not None:
				workbook_sheet = match[1]
			scopes.append(workbook_sheet)
			continue
		match = TUTORIAL_SHEET.search(line)
		if match is not None:
			tutorial_sheet = match[1].strip()
		scopes.append(tutorial_sheet)
	return scopes


#============================================
def _transform_source(source: str, scopes: list[str | None], sheet: str, transform: object,
	document: object) -> tuple[str, list[str]]:
	"""Transform recognized visible and executable references in their worksheet scope."""
	lines = source.splitlines(keepends=True)
	notices = []
	updated = []
	# The compiler owns which fenced payloads are executable assignments.
	code_lines = set()
	formula_lines = set()
	for token in document.tokens:
		if token.type not in ("fence", "code_block") or token.map is None:
			continue
		code_lines.update(range(token.map[0], token.map[1]))
		if token.type != "fence" or token.info.strip() != "sheets":
			continue
		for action in document.actions:
			if action.kind not in ("enter", "replace") or action.scalar is None:
				continue
			if action.scalar.kind != "formula":
				continue
			# An action's enclosing list item includes its nested formula fence.
			opening = document.tokens[action.token_index - 2]
			if (opening.type == "list_item_open" and opening.map is not None
				and opening.map[0] <= token.map[0] < opening.map[1]):
				formula_lines.add(token.map[0] + 1)
	for index, line in enumerate(lines):
		scope = scopes[index]
		try:
			if index in formula_lines:
				formula = line.strip()
				updated.append(line.replace(formula,
					_transform_formula(formula, scope, sheet, transform), 1))
			elif index in code_lines:
				updated.append(line)
			else:
				updated.append(_transform_line(line, scope, sheet, transform))
		except WorksheetEditError as error:
			raise WorksheetEditError(f"{index + 1}: {error}") from error
		if scope is None and _line_has_unqualified_reference(line):
			notices.append(f"Line {index + 1}: multi-sheet reference left unchanged; add a Worksheet declaration or review it")
		elif _has_ambiguous_instruction_reference(line, updated[-1]):
			notices.append(
				f"Line {index + 1}: coordinate-looking text in an instruction was left unchanged; review it after the layout edit")
	return "".join(updated), notices


#============================================
def _transform_line(line: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Update explicit worksheet syntax without treating scientific prose as Excel.

	The first prototype scanned every ``=`` expression.  That made biological
	and statistical notation such as ``b1`` look like Excel's ``B1``.  Formulas
	are deliberately transformed only where Markdown makes their spreadsheet
	role unambiguous: an Enter/Replace link, a code span, or a workbook-table
	cell.  Ordinary prose equations belong to the author.
	"""
	updated = _transform_visible_references(line, scope, sheet, transform)
	updated = _transform_link_formulas(updated, scope, sheet, transform)
	updated = _transform_code_formulas(updated, scope, sheet, transform)
	updated = _transform_code_expression_references(updated, scope, sheet, transform)
	updated = _transform_instruction_formulas(updated, scope, sheet, transform)
	updated = _transform_table_formulas(updated, scope, sheet, transform)
	return updated


#============================================
def _transform_link_formulas(line: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Update a formula visibly paired with an executable Enter/Replace link."""
	pattern = re.compile(r"\[(?P<formula>=[^\]\n]+)\]\((?:enter|replace):[^)]*\)", re.IGNORECASE)
	return pattern.sub(lambda match: "[" + _transform_formula(match["formula"], scope, sheet, transform)
		+ match[0][match[0].index("]("):], line)


#============================================
def _transform_code_formulas(line: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Update explicitly code-formatted formulas, never unmarked prose math."""
	return re.sub(r"`(=[^`\n]+)`", lambda match: "`"
		+ _transform_formula(match[1], scope, sheet, transform) + "`", line)


#============================================
def _transform_code_expression_references(line: str, scope: str | None, sheet: str,
	transform: object) -> str:
	"""Update cell operands in an explicitly code-formatted math expression.

	A code span with an operator or a range separator is a displayed worksheet
	expression.  A plain code span such as ``B12 TP53`` remains biological prose,
	not an accidental cell reference.
	"""
	def expression(match: re.Match) -> str:
		content = match[1]
		if content.startswith("=") or not re.search(r"[:+*/^()-]", content):
			return match[0]
		# _transform_visible_references already handles a code span containing
		# exactly one A1 reference.  Do not apply the move a second time merely
		# because a range has a colon.
		if tutorial_lib.references.parse_reference(content, sheet) is not None:
			return match[0]
		return "`" + CELL_OR_RANGE.sub(lambda reference: _transform_reference_text(
			reference[0], scope, sheet, transform), content) + "`"
	return re.sub(r"`([^`\n]+)`", expression, line)


#============================================
def _transform_instruction_formulas(line: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Recognize a bare copyable formula only after an instructional verb.

	This covers the established ``Use =AVERAGE(...)`` template while avoiding a
	general equation scanner that would rewrite scientific variables such as b1.
	"""
	pattern = re.compile(r"(?P<prefix>\b(?:enter|type|use|formula)\s+)(?P<formula>=[^\n`]+)", re.IGNORECASE)
	def instruction(match: re.Match) -> str:
		end = tutorial_lib.formulas.formula_end(match["formula"], 0, len(match["formula"]))
		if end <= 1:
			return match[0]
		formula = match["formula"][:end]
		rest = match["formula"][end:]
		return match["prefix"] + _transform_formula(formula, scope, sheet, transform) + rest
	return pattern.sub(instruction, line)


#============================================
def _transform_table_formulas(line: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Update raw formula cells in the Workbook's simple Markdown tables."""
	if not line.lstrip().startswith("|"):
		return line
	parts = line.rstrip("\n").split("|")
	for index, part in enumerate(parts):
		stripped = part.strip()
		if stripped.startswith("="):
			prefix = part[:len(part) - len(part.lstrip())]
			suffix = part[len(part.rstrip()):]
			parts[index] = prefix + _transform_formula(stripped, scope, sheet, transform) + suffix
	ending = "\n" if line.endswith("\n") else ""
	return "|".join(parts) + ending


#============================================
def _transform_formula(formula: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Rewrite only tokenizer-recognized A1 operands; quoted formula text is untouched."""
	if scope is None:
		return formula
	try:
		tokens = openpyxl.formula.tokenizer.Tokenizer(formula).items
	except (openpyxl.formula.tokenizer.TokenizerError, IndexError):
		return formula
	values = []
	for token in tokens:
		value = token.value
		if token.type == "OPERAND" and token.subtype == "RANGE":
			value = _transform_reference_text(value, scope, sheet, transform)
		values.append(value)
	return "=" + "".join(values)


#============================================
def _transform_visible_references(text: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Update only explicit technical reference contexts, never arbitrary prose."""
	text = REGION_TARGET.sub(lambda match: match[1]
		+ _transform_reference_text(match[2], scope, sheet, transform) + match[3], text)
	anchor = ANCHOR_TARGET.match(text.rstrip("\n"))
	if anchor is not None:
		newline = "\n" if text.endswith("\n") else ""
		return anchor[1] + _transform_reference_text(anchor[2], scope, sheet, transform) + anchor[3] + newline
	text = ACTION_CELL.sub(lambda match: match[1]
		+ _transform_reference_text(match[2], scope, sheet, transform) + match[3], text)
	def code_reference(match: re.Match) -> str:
		return "`" + _transform_reference_text(match[1], scope, sheet, transform) + "`"
	text = re.sub(r"`((?:(?:'(?:(?:[^']|'')+)'|[A-Za-z0-9_ .-]+)!)?\$?[A-Za-z]{1,3}"
		r"\$?[1-9][0-9]*(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?)`", code_reference, text)
	def technical_range(match: re.Match) -> str:
		return match["introducer"] + " " + _transform_reference_text(
			match["reference"], scope, sheet, transform)
	text = TECHNICAL_RANGE_REFERENCE.sub(technical_range, text)
	def prose_reference(match: re.Match) -> str:
		if match["reference"] is None:
			return match[1] + _transform_reference_text(match[2], scope, sheet, transform) + match[3]
		return match["introducer"] + " " + (match["opening"] or "") \
			+ _transform_reference_text(match["reference"], scope, sheet, transform) \
			+ (match["closing"] or "")
	# Both forms recognize "Enter E2". Match the original text once so a legacy
	# target cannot also be shifted by the prose rule.
	prose = re.compile(LEGACY_TARGET.pattern + "|" + PROSE_REFERENCE.pattern, re.IGNORECASE)
	text = prose.sub(prose_reference, text)
	# This established tutorial style names an output and gives its cell in bold
	# parentheses.  The phrase makes the coordinate a worksheet instruction;
	# unrelated bold scientific symbols, including H0/H1, are left alone.
	text = _transform_named_output_reference(text, scope, sheet, transform)
	# The displayed end of a fill and a terse "label H1 [text](label:H1)"
	# describe one executable action.  Pair them before changing link payloads so
	# observation resizing can update a displayed endpoint even though a lone
	# cell reference normally remains an authored worked-example value.
	text = _transform_action_display_references(text, scope, sheet, transform)
	def binding_target(match: re.Match) -> str:
		prefix = match.group()[:match.start(1) - match.start()]
		return prefix + _transform_reference_text(match[1], scope, sheet, transform) + ")"
	text = BINDING_TARGET.sub(binding_target, text)
	if scope is not None and scope.casefold() == sheet.casefold():
		text = ROW_WORD.sub(lambda match: _row_word(match, transform), text)
		text = COLUMN_WORD.sub(lambda match: _column_word(match, transform), text)
	return text


#============================================
def _transform_named_output_reference(text: str, scope: str | None, sheet: str,
	transform: object) -> str:
	"""Update a bold coordinate after a recognizable calculated-output name."""
	pattern = re.compile(r"(?P<prefix>\b(?:degrees\s+of\s+freedom|f-statistic|p-value|"
		r"grand\s+mean|sample\s+size)[^\n()]{0,90}\(\*\*)(?P<reference>"
		r"\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)(?P<suffix>\*\*\))", re.IGNORECASE)
	return pattern.sub(lambda match: match["prefix"] + _transform_reference_text(
		match["reference"], scope, sheet, transform) + match["suffix"], text)


#============================================
def _transform_action_display_references(text: str, scope: str | None, sheet: str,
	transform: object) -> str:
	"""Synchronize visible coordinates with an adjacent semantic action link."""
	address = r"\$?[A-Za-z]{1,3}\$?[1-9][0-9]*(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?"
	pair = re.compile(r"(?P<prefix>\b(?:label|enter|replace|select)\s+)"
		r"(?P<reference>" + address + r")(?P<middle>\s+\[[^\]\n]+\]"
		r"\((?P<kind>label|enter|replace|select):(?P<target>[^)]*)\))", re.IGNORECASE)
	def paired(match: re.Match) -> str:
		visible = tutorial_lib.references.parse_reference(match["reference"], sheet)
		target = tutorial_lib.references.parse_reference(match["target"], sheet)
		if visible is None or target is None or visible.address != target.address:
			return match[0]
		updated = _transform_reference_text(match["reference"], scope, sheet, transform)
		return match["prefix"] + updated + match["middle"]
	text = pair.sub(paired, text)
	# A compact setup often lists several labels as ``L1 [heading]``, then
	# supplies the action link.  Equality with that link target makes this a
	# technical coordinate rather than an arbitrary A1-looking word.
	bare_pair = re.compile(r"(?P<reference>" + address + r")(?P<middle>\s+\[[^\]\n]+\]"
		r"\((?:label|enter|replace|select):(?P<target>[^)]*)\))", re.IGNORECASE)
	def bare_paired(match: re.Match) -> str:
		visible = tutorial_lib.references.parse_reference(match["reference"], sheet)
		target = tutorial_lib.references.parse_reference(match["target"], sheet)
		if visible is None or target is None or visible.address != target.address:
			return match[0]
		updated = _transform_reference_text(match["reference"], scope, sheet, transform)
		return updated + match["middle"]
	text = bare_pair.sub(bare_paired, text)
	# This common authoring form displays the complete range inside the action
	# link itself. Keep its visible range synchronized with the semantic target
	# before the target is rewritten below.
	fill_range = re.compile(
		r"\[(?P<prefix>[^\]\n]*?\b)(?P<reference>" + address
		+ r")\]\(fill:(?P<target>[^)]*)\)", re.IGNORECASE)
	def fill_range_text(match: re.Match) -> str:
		visible = tutorial_lib.references.parse_reference(match["reference"], sheet)
		target = tutorial_lib.references.parse_reference(match["target"], sheet)
		if (visible is None or target is None or visible.address != target.address
			or visible.sheet.casefold() != sheet.casefold() or target.sheet.casefold() != sheet.casefold()):
			return match[0]
		updated = _transform_reference_text(match["reference"], scope, sheet, transform)
		return "[" + match["prefix"] + updated + "](fill:" + match["target"] + ")"
	text = fill_range.sub(fill_range_text, text)
	fill = re.compile(
		r"\[(?P<prefix>[^\]\n]*\bthrough\s+)(?P<reference>" + address
		+ r")\]\(fill:(?P<target>[^)]*)\)", re.IGNORECASE)
	def fill_end(match: re.Match) -> str:
		visible = tutorial_lib.references.parse_reference(match["reference"], sheet)
		target = tutorial_lib.references.parse_reference(match["target"], sheet)
		if (visible is None or target is None or visible.sheet.casefold() != sheet.casefold()
			or target.sheet.casefold() != sheet.casefold()):
			return match[0]
		if (visible.start_row, visible.start_column) != (target.end_row, target.end_column):
			return match[0]
		updated = transform(target)
		end = _address(updated.end_row, updated.end_row, updated.end_column, updated.end_column)
		return "[" + match["prefix"] + end + "](fill:" + match["target"] + ")"
	return fill.sub(fill_end, text)


#============================================
def _transform_reference_text(value: str, scope: str | None, sheet: str, transform: object) -> str:
	"""Transform one A1 expression only when it belongs to the selected worksheet."""
	match = re.fullmatch(r"(?:(?P<prefix>'(?P<quoted>(?:[^']|'')+)'|(?P<plain>[^'!]+))!)?(?P<address>.+)", value)
	if match is None:
		return value
	qualified = match.group("prefix") is not None
	name = match.group("quoted").replace("''", "'") if match.group("quoted") is not None else match.group("plain")
	if qualified and name.casefold() != sheet.casefold():
		return value
	if not qualified and (scope is None or scope.casefold() != sheet.casefold()):
		return value
	reference = tutorial_lib.references.parse_reference(match.group("address"), sheet)
	if reference is None:
		return value
	updated = transform(reference)
	prefix = match.group("prefix") + "!" if qualified else ""
	return prefix + _preserve_anchor_address(match.group("address"), updated)


#============================================
def _preserve_anchor_address(original: str, updated: object) -> str:
	"""Render transformed coordinates while retaining authored row/column anchors."""
	parts = original.split(":")
	coordinates = [(updated.start_row, updated.start_column), (updated.end_row, updated.end_column)]
	result = []
	for index, part in enumerate(parts):
		match = CELL_PART.fullmatch(part)
		if match is None:
			return updated.address
		column_anchor, unused_letters, row_anchor, unused_row = match.groups()
		row, column = coordinates[index if len(parts) > 1 else 0]
		result.append(column_anchor + tutorial_lib.references.column_letters(column)
			+ row_anchor + str(row))
	return ":".join(result)


#============================================
def _row_word(match: re.Match, transform: object) -> str:
	"""Transform a recognizable prose row number through a single-cell reference."""
	row = int(match[2])
	reference = tutorial_lib.model.CellReference("", row, 1, row, 1, f"A{row}")
	updated = transform(reference)
	prefix = match[0][:len("row") + len(match[1])]
	return prefix + " " + str(updated.start_row)


#============================================
def _column_word(match: re.Match, transform: object) -> str:
	"""Transform a recognizable prose column name through a single-cell reference."""
	column = tutorial_lib.references.column_number(match[2])
	end_column = tutorial_lib.references.column_number(match[3]) if match[3] else column
	reference = tutorial_lib.model.CellReference("", 1, column, 1, end_column,
		tutorial_lib.references.column_letters(column) + "1")
	updated = transform(reference)
	prefix = match[0][:len("column") + len(match[1])]
	value = tutorial_lib.references.column_letters(updated.start_column)
	if updated.end_column != updated.start_column:
		value += "-" + tutorial_lib.references.column_letters(updated.end_column)
	return prefix + " " + value


#============================================
def _line_has_unqualified_reference(line: str) -> bool:
	"""Identify a reviewable A1-looking expression in an ambiguous multi-sheet line."""
	return PROSE_REFERENCE.search(line) is not None or BINDING_TARGET.search(line) is not None


#============================================
def _has_ambiguous_instruction_reference(original: str, updated: str) -> bool:
	"""Flag a likely instruction coordinate that intentionally was not guessed.

	A1-shaped text is also normal scientific notation (for example, B12 and
	b1).  The edit command therefore leaves bare single cells alone.  When the
	line otherwise reads like a spreadsheet instruction, a notice keeps that
	conservative choice visible to the author instead of silently promising
	complete synchronization.
	"""
	if INSTRUCTION_CUE.search(original) is None:
		return False
	original_references = CELL_OR_RANGE.findall(original)
	updated_references = CELL_OR_RANGE.findall(updated)
	return any(before == after for before, after in zip(original_references, updated_references))


#============================================
def _patch_workbook_tables(source: str, request: WorksheetEdit, sheet: object,
	transform: object) -> str:
	"""Keep the supplied Markdown table at the same physical worksheet geometry.

	A primary table is implicitly at A1.  When an insertion pushes that table,
	make its position explicit rather than silently changing where its data land.
	"""
	if request.kind not in ("insert-rows", "insert-columns"):
		return source
	lines = source.splitlines(keepends=True)
	# Compiler regions retain every table's source span and physical geometry.
	# Work backwards so inserted lines cannot invalidate subsequent spans.
	for region in reversed(sheet.regions):
		start = region.span.start_line - 1
		end = region.span.end_line
		preceding = start - 1
		while preceding >= 0 and not lines[preceding].strip():
			preceding -= 1
		anchor_line = preceding if preceding >= 0 and ANCHOR_TARGET.match(
			lines[preceding].rstrip("\n")) else None
		width = region.end_column - region.start_column + 1
		position = region.start_column if request.kind == "insert-columns" else region.start_row
		last = region.end_column if request.kind == "insert-columns" else region.end_row
		if request.at <= position:
			if anchor_line is None:
				anchor = _address(region.start_row, region.start_row,
					region.start_column, region.start_column)
				reference = tutorial_lib.references.parse_reference(anchor, sheet.name)
				lines = _set_table_anchor(lines, start, None, transform(reference).address)
		elif request.at <= last:
			if request.kind == "insert-columns":
				index = request.at - region.start_column
				for row in range(start, end):
					cells = tutorial_lib.parser.split_table_row(lines[row])
					# Added delimiter cells must remain valid GFM table syntax.
					cells[index:index] = ["---" if row == start + 1 else ""] * request.count
					lines[row] = "| " + " | ".join(cell.replace("|", r"\|")
						for cell in cells) + " |\n"
			else:
				index = start + 2 + request.at - region.start_row - 1
				blank = "|" + " |" * width + "\n"
				lines[index:index] = [blank] * request.count
	return "".join(lines)


#============================================
def _set_table_anchor(lines: list[str], start: int, anchor_line: int | None,
	anchor: str) -> list[str]:
	"""Set or introduce an ASCII Workbook At heading for a shifted data table."""
	line = "#### At: " + anchor + "\n"
	if anchor_line is None:
		lines[start:start] = [line, "\n"]
	else:
		lines[anchor_line] = line
	return lines


#============================================
def _extend_data_table(source: str, request: WorksheetEdit, sheet: object) -> str:
	"""Add blank Markdown rows so a resized supplied-data table keeps its geometry."""
	data = tutorial_lib.references.parse_reference(request.data_range, sheet.name)
	old_rows = data.end_row - 1
	if request.rows == old_rows:
		return source
	lines = source.splitlines(keepends=True)
	start = _table_start_line(lines, sheet.name)
	if start is None:
		raise WorksheetEditError("Could not locate the declared data table for resize")
	end = start + 2
	while end < len(lines) and lines[end].lstrip().startswith("|"):
		end += 1
	blank = "|" + " |" * (data.end_column - data.start_column + 1) + "\n"
	if request.rows > old_rows:
		lines[end:end] = [blank] * (request.rows - old_rows)
	else:
		remove_start = end - (old_rows - request.rows)
		del lines[remove_start:end]
	return "".join(lines)


#============================================
def _table_start_line(lines: list[str], sheet_name: str) -> int | None:
	"""Find the first Markdown table following the selected workbook sheet heading."""
	in_sheet = False
	for index, line in enumerate(lines):
		match = SHEET_HEADING.match(line.rstrip("\n"))
		if match is not None:
			in_sheet = match[1].casefold() == sheet_name.casefold()
			continue
		if in_sheet and line.lstrip().startswith("|"):
			return index
	return None


#============================================
def _worked_example_notices(source: str, request: WorksheetEdit, transform: object) -> list[str]:
	"""Flag likely numeric examples near resized ranges without revising claims."""
	notices = []
	for number, line in enumerate(source.splitlines(), start=1):
		if not re.search(r"\d", line):
			continue
		if "=" in line or CELL_OR_RANGE.search(line) is not None:
			notices.append(
				f"Line {number}: review numerical explanation after changing observation count")
	return notices
