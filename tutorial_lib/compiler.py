"""Compile parsed Markdown into one source-located tutorial/workbook model."""

import re
import json
import math
import pathlib
import urllib.parse
import tutorial_lib.model as model
import tutorial_lib.parser
import tutorial_lib.references as references
import tutorial_lib.semantic_bindings as bindings
import tutorial_lib.source_text
import tutorial_lib.reflections
import markdown_it.token

NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
STRUCTURE = re.compile(r"(Part|Step|Substep)(?: ([0-9]+(?:\.[0-9]+)?))?:\s*(.+)\Z", re.IGNORECASE)
ASSIGNMENT = re.compile(r"(Label|Enter|Replace|Fill)\s+(.+):\Z")


def span(document: model.Document, token: object) -> model.SourceSpan:
	location = token.map if token.map is not None else [0, 1]
	return model.SourceSpan(str(document.path), location[0] + 1, location[1])


def diagnostic(document: model.Document, category: str, location: model.SourceSpan,
	message: str, correction: str, severity: str = "error", **details) -> None:
	document.diagnostics.append(model.Diagnostic(
		severity, category, location, message, correction, **details,
	))


def scalar_text(raw: str) -> str:
	children = tutorial_lib.parser.markdown_parser().parseInline(raw)[0].children
	if len(children) == 1 and children[0].type == "code_inline":
		return children[0].content
	if any(child.type not in ("text", "html_inline", "softbreak") for child in children):
		raise ValueError("Only plain text or one complete code span is allowed")
	pieces = []
	for child in children:
		if child.type == "html_inline":
			if re.fullmatch(r"<br\s*/?>", child.content, re.IGNORECASE) is None:
				raise ValueError("Only br markup is allowed in workbook scalars")
			pieces.append("\n")
		else:
			pieces.append(child.content)
	return "".join(pieces).strip()


def parse_scalar(raw: str) -> model.Scalar:
	# Table structural escapes are already removed; JSON escapes belong to JSON,
	# not Markdown. Code spans still follow the normal Markdown literal rules.
	text = raw.strip() if raw.strip().startswith(('"', "=")) else scalar_text(raw)
	return _scalar_value(text)


def _scalar_value(text: str) -> model.Scalar:
	if not text:
		return model.Scalar("blank", None)
	if text.startswith('"'):
		try:
			value = json.loads(text)
		except json.JSONDecodeError as error:
			raise ValueError("Malformed JSON quoted string") from error
		if not isinstance(value, str):
			raise ValueError("Quoted cell value must be a JSON string")
		return model.Scalar("text", value)
	if text.startswith("="):
		if "\n" in text or not text[1:].strip():
			raise ValueError("A formula must contain one logical nonempty line")
		return model.Scalar("formula", text)
	if text in ("TRUE", "FALSE"):
		return model.Scalar("boolean", text == "TRUE")
	if NUMBER.fullmatch(text):
		value = float(text)
		if not math.isfinite(value):
			raise ValueError("Numeric values must be finite")
		if not any(item in text.lower() for item in (".", "e")):
			value = int(text)
		return model.Scalar("number", value)
	return model.Scalar("text", text)


def _table(document: model.Document, index: int, sheet: model.Worksheet,
	anchor: str) -> None:
	token = document.tokens[index]
	location = span(document, token)
	address = references.parse_reference(anchor, sheet.name)
	if address is None or ":" in anchor or "!" in anchor:
		diagnostic(document, "table-anchor", location, f"Invalid table anchor {anchor}",
			"Use one unqualified A1 cell")
		return
	lines = document.source.splitlines()[token.map[0]:token.map[1]]
	rows = [tutorial_lib.parser.split_table_row(line) for offset, line in enumerate(lines)
		if offset != 1]
	width = len(rows[0])
	if any(len(row) != width for row in rows):
		diagnostic(document, "ragged-table", location, "Table rows have different cell counts",
			"Give every authored row the same number of cells")
		return
	end_row = address.start_row + len(rows) - 1
	end_column = address.start_column + width - 1
	if end_row > 1048576 or end_column > 16384:
		diagnostic(document, "table-bounds", location, "Table exceeds XLSX coordinates",
			"Move or shorten the table")
		return
	region = model.TableRegion(address.start_row, address.start_column, end_row, end_column,
		location)
	for previous in sheet.regions:
		row = max(previous.start_row, region.start_row)
		column = max(previous.start_column, region.start_column)
		if row <= min(previous.end_row, end_row) and column <= min(previous.end_column, end_column):
			diagnostic(document, "table-overlap", location, "Workbook table rectangles overlap",
				"Move the anchored table", worksheet=sheet.name,
				address=f"{references.column_letters(column)}{row}", related=previous.span)
			return
	sheet.regions.append(region)
	for row_offset, row in enumerate(rows):
		physical = token.map[0] + row_offset + (1 if row_offset == 0 else 2)
		cell_span = model.SourceSpan(str(document.path), physical, physical)
		for column_offset, raw in enumerate(row):
			try:
				scalar = parse_scalar(raw)
			except ValueError as error:
				diagnostic(document, "cell-scalar", cell_span, str(error),
					"Use a supported plain scalar or JSON quoted string")
				continue
			row_number = address.start_row + row_offset
			column_number = address.start_column + column_offset
			sheet.cells[(row_number, column_number)] = model.CellSeed(
				row_number, column_number, scalar, cell_span,
			)


def _mapping(document: model.Document, sheet: model.Worksheet, payload: str,
	location: model.SourceSpan) -> None:
	url = urllib.parse.urlparse(payload)
	match = re.fullmatch(r"/spreadsheets/d/([A-Za-z0-9_-]+)/(?:edit)?", url.path)
	parameters = urllib.parse.parse_qs(url.fragment)
	if url.scheme != "https" or url.netloc != "docs.google.com" or match is None:
		diagnostic(document, "google-mapping", location, "Malformed Google Sheets URL",
			"Supply an https docs.google.com spreadsheet edit URL")
		return
	gids = parameters.get("gid", [])
	if gids and (len(gids) != 1 or not gids[0].isdigit()):
		diagnostic(document, "google-mapping", location, "Google tab gid must be numeric",
			"Copy the worksheet URL with its numeric gid")
		return
	if sheet.google is not None:
		diagnostic(document, "google-mapping", location, "Duplicate worksheet mapping",
			"Keep one Google URL per worksheet")
		return
	sheet.google = model.GoogleMapping(payload, match[1], gids[0] if gids else None)
	if not gids:
		diagnostic(document, "google-tab-missing", location, "URL has no tab gid",
			"Include the worksheet gid to enable cell links", "warning")


def _opening(inline: object) -> tuple[str | None, str]:
	children = inline.children
	# markdown-it emits an empty text token before an opening emphasis delimiter.
	start = 0
	while start < len(children) and children[start].type == "text" and not children[start].content:
		start += 1
	if start >= len(children) or children[start].type != "strong_open":
		return None, inline.content
	end = start + 1
	while end < len(children) and children[end].type != "strong_close":
		end += 1
	if end == len(children):
		return None, inline.content
	opening = "".join(child.content for child in children[start + 1:end])
	# Source extraction preserves code span delimiters needed by scalar validation.
	match = re.match(r"\s*(?:\*\*|__).*?(?:\*\*|__)\s*", inline.content)
	payload = inline.content[match.end():] if match is not None else ""
	return opening, payload


def compile_document(path: str | pathlib.Path) -> model.Document:
	path = pathlib.Path(path).resolve()
	document = compile_source(path.read_text(encoding="utf-8"), path)
	document.diagnostics.extend(tutorial_lib.source_text.source_diagnostics(document))
	return document


def compile_source(source: str, path: str | pathlib.Path = "tutorial.md") -> model.Document:
	document = tutorial_lib.parser.parse_source(source, path)
	_compile_structure(document)
	_validate_incomplete_instructions(document)
	import tutorial_lib.validation as validation
	validation.validate_document(document)
	if document.reflection_questions:
		name = "Reflection Questions"
		if any(sheet.name.casefold() == name.casefold() for sheet in document.worksheets):
			diagnostic(document, "reflection-questions", document.reflection_questions[0].span,
				"Generated reflection worksheet name collision", "Rename the authored worksheet")
		else:
			document.worksheets.append(tutorial_lib.reflections.worksheet(document))
	return document


def _label_only(inline: object) -> bool:
	"""Return whether an inline paragraph contains only bold colon labels."""
	children = inline.children or []
	strong_depth = 0
	labels = []
	current_label = []
	outside_text = []
	for child in children:
		if child.type == "strong_open":
			if strong_depth == 0:
				current_label = []
			strong_depth += 1
		elif child.type == "strong_close":
			strong_depth = max(0, strong_depth - 1)
			if strong_depth == 0:
				labels.append("".join(current_label).strip())
		elif child.type == "text":
			if strong_depth:
				current_label.append(child.content)
			else:
				outside_text.append(child.content)
		elif child.type in ("softbreak", "hardbreak"):
			outside_text.append(" ")
		elif child.type not in ("em_open", "em_close"):
			# Images, code spans, links, and other inline objects carry content.
			return False
	return bool(labels) and all(label.endswith(":") for label in labels) and not "".join(outside_text).strip()


def _valid_action(action: object, document: model.Document) -> bool:
	if action.kind in ("label", "enter", "replace"):
		valid = action.scalar is not None and action.target is not None
	elif action.kind == "select":
		valid = action.target is not None
	elif action.kind == "fill":
		valid = action.target is not None and action.payload.strip() == "Down"
	elif action.kind == "choose":
		valid = bool(action.menu) and all(action.menu)
	else:
		valid = action.kind == "worksheet" and bool(action.worksheet)
	if not valid:
		return False
	return not any(item.severity == "error" and item.span == action.span
		and item.category in ("action-syntax", "action-scalar", "action-target", "menu-path")
		for item in document.diagnostics)


def _validate_incomplete_instructions(document: model.Document) -> None:
	"""Reject list items that contain labels but give no instruction or content."""
	items = []
	tutorial_start = next((index + 3 for index, token in enumerate(document.tokens)
		if token.type == "heading_open" and token.tag == "h2"
		and index + 1 < len(document.tokens)
		and document.tokens[index + 1].content == "Tutorial"), len(document.tokens))
	for token in document.tokens[tutorial_start:]:
		if token.type == "list_item_open":
			items.append({"token": token, "level": token.level, "substantive": False})
		elif token.type == "list_item_close" and items:
			item = items.pop()
			if not item["substantive"]:
				location = span(document, item["token"])
				diagnostic(document, "incomplete-instruction", location,
					"List item contains labels but no instruction or content",
					"Add a nonempty explanation, nested instruction, or valid action")
			if items and item["substantive"]:
				items[-1]["substantive"] = True
		elif items:
			item = items[-1]
			if token.type == "inline" and token.level == item["level"] + 2:
				action = token.meta.get("action")
				if action is not None and _valid_action(action, document):
					item["substantive"] = True
				elif not _label_only(token):
					item["substantive"] = True
			elif token.type in ("fence", "code_block") \
					and token.level == item["level"] + 1 and token.content.strip():
				item["substantive"] = True


def _compile_structure(document: model.Document) -> None:
	reflection_indices = tutorial_lib.reflections.compile_questions(document)
	section = "introduction"
	seen_sections = []
	sheet = None
	anchor = None
	part = None
	step = None
	part_number = 0
	step_number = 0
	substep_number = 0
	part_has_step = False
	part_span = None
	scope = None
	list_stack = []
	item_stack = []
	alternative_counter = 0
	previous_heading_level = 1
	skip_until = -1
	title_count = 0
	for index, token in enumerate(document.tokens):
		if index in reflection_indices:
			continue
		location = span(document, token)
		if section != "Workbook":
			document.content_token_indices.append(index)
		if index <= skip_until:
			continue
		if token.type == "heading_open":
			inline = document.tokens[index + 1]
			text = "".join(child.content for child in inline.children
				if child.type in ("text", "code_inline", "html_inline"))
			level = int(token.tag[1:])
			if level == 1:
				title_count += 1
				document.title = text
				if index != 0:
					diagnostic(document, "document-structure", location,
						"Document title must be first", "Place one H1 title first")
			elif level == 2:
				if section == "Workbook" and anchor is not None:
					diagnostic(document, "table-anchor", location, "At heading has no following table",
						"Place one table after each At heading")
				seen_sections.append(text)
				section = text
				previous_heading_level = 2
				if text not in ("Workbook", "Tutorial"):
					diagnostic(document, "document-structure", location,
						f"Unknown H2 section {text}", "Use Workbook then Tutorial")
				# Structural section headings are omitted from student content.
				for omitted in range(index, index + 3):
					if omitted in document.content_token_indices:
						document.content_token_indices.remove(omitted)
				skip_until = index + 2
				continue
			elif section == "Workbook":
				if level == 3 and text.startswith("Sheet:"):
					if anchor is not None:
						diagnostic(document, "table-anchor", location, "At heading has no following table",
							"Place a table before declaring another worksheet")
					name = text[6:].strip()
					if (not name or len(name) > 31 or re.search(r"[:\\/?*\[\]]", name)
						or name.startswith("'") or name.endswith("'")):
						diagnostic(document, "worksheet-name", location, "Invalid worksheet name",
							"Use a valid XLSX worksheet name of at most 31 characters")
					if any(existing.name.casefold() == name.casefold()
						for existing in document.worksheets):
						diagnostic(document, "worksheet-name", location, "Duplicate worksheet name",
							"Use names unique ignoring case")
					sheet = model.Worksheet(name, location)
					document.worksheets.append(sheet)
					anchor = None
				elif level == 4 and text.startswith("At:"):
					if anchor is not None:
						diagnostic(document, "table-anchor", location, "Unused preceding At heading",
							"Place a table after each At heading")
					anchor = text[3:].strip()
				else:
					diagnostic(document, "workbook-content", location, "Unexpected Workbook heading",
						"Use Sheet or At declarations")
				skip_until = index + 2
				continue
			elif section == "Tutorial":
				match = STRUCTURE.fullmatch(text)
				if match is None and re.match(r"(?i)(part|step|substep)(?=\s|:|[0-9]|$)", text):
					diagnostic(document, "heading-syntax", location, "Near-miss structural heading",
						"Use Part:, Step:, or Substep: followed by a title")
				if level > previous_heading_level + 1:
					diagnostic(document, "heading-hierarchy", location, "Heading skips a level",
						"Use the next heading level")
				previous_heading_level = level
				kind, number, title = "informational", None, text
				prefix_length = 0
				if match is not None:
					kind, explicit, title = match.groups()
					kind = kind.capitalize()
					prefix_length = match.start(3)
					if kind != "Substep" and explicit is not None and "." in explicit:
						diagnostic(document, "heading-number", location, "Part and Step numbers must be integers",
							f"Use {kind}: {title}")
						explicit = None
					if level != {"Part": 3, "Step": 4, "Substep": 5}[kind]:
						diagnostic(document, "heading-hierarchy", location, "Structural heading at wrong level",
							"Use H3 Part, H4 Step, and H5 Substep")
					if kind == "Part":
						if part is not None and not part_has_step:
							diagnostic(document, "empty-part", part_span, "Part has no Step",
								"Add at least one Step with instructions")
						expected = int(explicit) if part_number == 0 and explicit else part_number + 1
						part_number = expected
						part, step, scope = title, None, None
						part_span, part_has_step, step_number = location, False, 0
						number = str(expected)
					elif kind == "Step":
						if part is None:
							diagnostic(document, "heading-hierarchy", location, "Step outside Part",
								"Add a Part heading before this Step")
						if scope is None:
							if len(document.worksheets) == 1:
								scope = document.worksheets[0].name
							else:
								diagnostic(document, "worksheet-scope", location, "Part has no worksheet scope",
									"Add a Worksheet declaration before its first Step")
						expected = int(explicit) if not part_has_step and explicit else step_number + 1
						step_number, substep_number = expected, 0
						part_has_step, step = True, title
						number = str(expected)
					else:
						if step is None:
							diagnostic(document, "heading-hierarchy", location, "Substep outside Step",
								"Add a containing Step")
						suffix = explicit.split(".")[-1] if explicit else None
						substep_number = int(suffix) if substep_number == 0 and suffix else substep_number + 1
						number = f"{step_number}.{substep_number}"
					if explicit is not None and explicit != number:
						diagnostic(document, "heading-number", location, "Contradictory explicit heading number",
							f"Use {kind} {number}: {title}")
					if kind == "Part" and part_number < 1 or kind == "Substep" and substep_number < 1:
						diagnostic(document, "heading-number", location, "Number must start at 1 or greater",
							"Use a positive part or substep number")
				display = f"{kind} {number}: {title}" if number else title
				if kind == "Substep":
					display = f"{number}: {title}"
				slug = re.sub(r"[^\w\s-]", "", text.lower())
				slug = re.sub(r"\s+", "-", slug.strip())
				heading = model.Heading(level, title, display, slug, location, index,
					kind.lower(), number, prefix_length)
				document.headings.append(heading)
				token.meta["heading"] = heading
			continue
		if section == "Workbook":
			if token.type == "table_open":
				if sheet is None:
					diagnostic(document, "worksheet-missing", location, "Table has no worksheet",
						"Declare a Sheet before the table")
				elif sheet.regions and anchor is None:
					diagnostic(document, "table-anchor", location, "Additional table has no At heading",
						"Add an At cell heading")
				else:
					_table(document, index, sheet, anchor if anchor is not None else "A1")
				anchor = None
				end = index + 1
				while document.tokens[end].type != "table_close":
					end += 1
				skip_until = end
			elif token.type == "inline":
				opening, payload = _opening(token)
				if opening is not None and opening.startswith("Region ") and sheet is not None:
					_role_region(document, sheet, opening, payload, location)
				elif (opening == "Google Sheets:" and sheet is not None
					and index >= 2 and document.tokens[index - 2].type == "list_item_open"
					and token.level == 3):
					if sheet.regions:
						diagnostic(document, "google-mapping", location, "Mapping occurs after first table",
							"Move metadata before the first table")
					_mapping(document, sheet, payload, location)
				else:
					diagnostic(document, "workbook-content", location, "Unrecognized Workbook content",
						"Move prose into Tutorial or use supported metadata")
			elif token.type in ("fence", "code_block", "html_block", "hr"):
				diagnostic(document, "workbook-content", location, "Unrecognized Workbook block",
					"Use worksheet declarations and rectangular tables")
			continue
		if section != "Tutorial":
			continue
		if token.type == "inline":
			_compile_bindings(document, token, index, scope, step, item_stack)
		if token.type in ("bullet_list_open", "ordered_list_open"):
			list_stack.append({"group": None, "branches": 0})
		elif token.type in ("bullet_list_close", "ordered_list_close"):
			list_stack.pop()
		elif token.type == "list_item_open":
			item_stack.append({"opening": False, "alternative": None, "end": token.map[1]})
		elif token.type == "list_item_close":
			item_stack.pop()
		elif token.type == "inline" and item_stack and not item_stack[-1]["opening"]:
			item_stack[-1]["opening"] = True
			opening, payload = _opening(token)
			if opening is not None and opening.startswith("Alternative:"):
				if not opening[len("Alternative:"):].strip() or payload.strip():
					diagnostic(document, "alternative-syntax", location,
						"Alternative needs its title inside the opening strong span",
						"Use **Alternative: Description** followed by nested instructions")
				if any(item["alternative"] is not None for item in item_stack[:-1]):
					diagnostic(document, "nested-alternative", location, "Nested alternatives are unsupported",
						"Keep alternatives as sibling choice items")
				if list_stack[-1]["group"] is None:
					alternative_counter += 1
					list_stack[-1]["group"] = alternative_counter
				list_stack[-1]["branches"] += 1
				item_stack[-1]["alternative"] = (
					list_stack[-1]["group"], list_stack[-1]["branches"],
				)
				token.meta["alternative"] = item_stack[-1]["alternative"]
				token.meta["alternative_end"] = item_stack[-1]["end"]
				continue
			if list_stack:
				list_stack[-1]["group"] = None
				list_stack[-1]["branches"] = 0
			if opening == "Worksheet:":
				if part is None or step is not None or scope is not None:
					diagnostic(document, "worksheet-scope", location, "Worksheet declaration is out of place",
						"Place one declaration after Part and before its first Step")
				scope = payload.strip()
				if not any(item.name == scope for item in document.worksheets):
					diagnostic(document, "unknown-sheet", location, f"Unknown worksheet {scope}",
						"Name a declared worksheet")
				action = model.Action("worksheet", location, index, payload, worksheet=scope)
				document.actions.append(action)
				token.meta["action"] = action
				continue
			assignment = ASSIGNMENT.fullmatch(opening) if opening is not None else None
			kind = assignment[1].lower() if assignment else None
			if opening in ("Select:", "Choose:"):
				kind = opening[:-1].lower()
			if kind is None:
				if opening is not None and re.match(r"(Label|Enter|Replace|Fill|Select|Choose)\b", opening):
					diagnostic(document, "action-syntax", location, "Malformed recognized action",
						"Use a complete action opening including its colon")
				continue
			if step is None:
				diagnostic(document, "action-scope", location, "Action has no containing Step",
					"Move this action beneath a Step")
			action = model.Action(kind, location, index, payload, worksheet=scope)
			alternatives = [item["alternative"] for item in item_stack if item["alternative"] is not None]
			if alternatives:
				action.alternative_group, action.alternative_branch = alternatives[-1]
			if kind == "choose":
				try:
					path = scalar_text(payload)
				except ValueError as error:
					diagnostic(document, "menu-path", location, str(error),
						"Use a plain menu path or one complete code span")
					continue
				action.menu = [part.strip() for part in re.split(r">|\u2192", path)]
				if any(not segment for segment in action.menu):
					diagnostic(document, "menu-path", location, "Empty menu path segment",
						"Supply a name between each menu separator")
			else:
				try:
					target_text = assignment[2] if assignment else scalar_text(payload)
				except ValueError as error:
					diagnostic(document, "action-target", location, str(error),
						"Use a plain A1 reference or one complete code span")
					continue
				action.target = references.parse_reference(target_text, scope if scope else "")
				if action.target is None or kind not in ("select", "fill") and ":" in target_text:
					diagnostic(document, "action-target", location, "Invalid action target",
						"Use one A1 cell for assignments or a valid range for Select or Fill")
				if kind == "fill":
					if payload.strip() != "Down":
						diagnostic(document, "action-syntax", location, "Fill supports only Down",
							"Use **Fill C2:C26:** Down")
					if action.target is not None and action.target.start_row == action.target.end_row:
						diagnostic(document, "action-target", location, "Fill needs more than one row",
							"Include the formula source row and at least one destination row")
				elif kind != "select":
					_scalar_action(document, action, index, item_stack[-1]["end"])
			document.actions.append(action)
			token.meta["action"] = action
	if title_count != 1 or seen_sections != ["Workbook", "Tutorial"]:
		diagnostic(document, "document-structure", model.SourceSpan(str(document.path), 1, 1),
			"Require one title followed by Workbook and Tutorial", "Use the required H1/H2 structure")
	if not document.worksheets:
		diagnostic(document, "worksheet-missing", model.SourceSpan(str(document.path), 1, 1),
			"Workbook has no worksheets", "Declare at least one Sheet")
	if part is None or not part_has_step:
		diagnostic(document, "empty-part", part_span if part_span else model.SourceSpan(str(document.path), 1, 1),
			"Tutorial needs a Part containing a Step", "Add authored tutorial instructions")
	section_indices = {document.tokens[index + 1].content: index
		for index, token in enumerate(document.tokens) if token.type == "heading_open"
		and token.tag == "h2"}
	if "Workbook" in section_indices and "Tutorial" in section_indices:
		document.content_token_indices = list(range(section_indices["Workbook"]))
		document.content_token_indices.extend(range(section_indices["Tutorial"] + 3,
			len(document.tokens)))
	document.content_token_indices = [index for index in document.content_token_indices
		if index not in reflection_indices]


def _role_region(document: model.Document, sheet: model.Worksheet, opening: str,
	payload: str, location: model.SourceSpan) -> None:
	match = re.fullmatch(r"Region (.+):", opening)
	reference = references.parse_reference(match[1], sheet.name) if match else None
	role = payload.strip()
	if reference is None or reference.sheet.casefold() != sheet.name.casefold():
		diagnostic(document, "role-region", location, "Invalid worksheet role region",
			"Use a bounded A1 range on this worksheet")
		return
	if role not in ("source", "calculation", "results", "interpretation"):
		diagnostic(document, "role-region", location, f"Unknown worksheet role {role}",
			"Use source, calculation, results, or interpretation")
		return
	for previous in sheet.role_regions:
		other = previous.reference
		if (max(reference.start_row, other.start_row) <= min(reference.end_row, other.end_row)
			and max(reference.start_column, other.start_column)
			<= min(reference.end_column, other.end_column)):
			diagnostic(document, "role-region-overlap", location, "Explicit role regions overlap",
				"Keep explicit role regions disjoint", related=previous.span)
			return
	sheet.role_regions.append(model.RoleRegion(role, reference, location))


def _compile_bindings(document: model.Document, inline: object, index: int,
	scope: str | None, step: str | None, item_stack: list) -> None:
	children = inline.children
	for position, child in enumerate(children):
		if child.type != "link_open":
			continue
		href = urllib.parse.unquote(child.attrGet("href"))
		kind = bindings.binding_kind(href)
		if kind is None:
			continue
		location = span(document, inline)
		binding_index = sum(1 for previous in children[:position]
			if previous.type == "link_open" and bindings.binding_kind(
				urllib.parse.unquote(previous.attrGet("href"))) is not None)
		raw = child.meta["binding_payload"]
		value = raw
		default_sheet = scope if scope else (
			document.worksheets[0].name if len(document.worksheets) == 1 else "")
		target_text = href.split(":", 1)[1]
		target = references.parse_reference(target_text, default_sheet)
		action = model.Action(kind, location, index, "Down" if kind == "fill" else raw,
			target=target, worksheet=default_sheet)
		_visible_destination(document, inline, action, location, binding_index)
		alternatives = [item["alternative"] for item in item_stack if item["alternative"] is not None]
		if alternatives:
			action.alternative_group, action.alternative_branch = alternatives[-1]
		if step is None:
			diagnostic(document, "action-scope", location, "Binding has no containing Step",
				"Move this instruction beneath a Step")
		if target is None or kind not in ("fill", "select") and ":" in target_text:
			diagnostic(document, "action-target", location, "Invalid binding target",
				"Use one bounded A1 cell for assignments or a range for Fill or Select")
		if kind == "fill" and target is not None and target.start_row == target.end_row:
			diagnostic(document, "action-target", location, "Fill needs more than one row",
				"Include the formula source row and at least one destination row")
		if kind in ("label", "enter", "replace"):
			try:
				value = bindings.scalar_payload(raw, tutorial_lib.parser.markdown_parser(), kind)
				if kind == "label":
					action.scalar = model.Scalar("text", value)
				else:
					action.scalar = _scalar_value(value)
				if not raw.strip() or action.scalar.kind == "blank":
					raise ValueError("Assignment payload is empty")
			except ValueError as error:
				diagnostic(document, "action-scalar", location, str(error),
					"Use one scalar value as the visible binding text")
		child.meta["binding_action"] = action
		end = position + 1
		while end < len(children) and children[end].type != "link_close":
			children[end].meta["binding_action"] = action
			if action.scalar is not None and action.scalar.kind == "text":
				children[end].meta.pop("role", None)
			end += 1
		if end < len(children):
			children[end].meta["binding_action"] = action
		# Raw JSON and formula-looking labels must never acquire inferred formula markup.
		if action.scalar is not None and action.scalar.kind == "text" and (
			value.startswith("=") or kind != "label" and value.startswith('"')):
			# Keep enclosing author emphasis; literal punctuation inside the payload
			# cannot introduce its own Markdown formatting or formula-role tokens.
			first, last = position + 1, end
			while first < last and (children[first].type in ("strong_open", "em_open")
				or children[first].type == "text" and not children[first].content):
				first += 1
			while last > first and (children[last - 1].type in ("strong_close", "em_close")
				or children[last - 1].type == "text" and not children[last - 1].content):
				last -= 1
			literal = markdown_it.token.Token("text", "", 0)
			if last - first == 1 and children[first].type == "code_inline":
				literal = children[first]
			literal.content = value
			literal.meta["binding_action"] = action
			children[first:last] = [literal]
		document.actions.append(action)


def _visible_destination(document: model.Document, inline: object, action: model.Action,
	location: model.SourceSpan, binding_index: int) -> None:
	"""Reject an explicit `cell C2` phrase that contradicts its binding target."""
	if action.kind not in ("label", "enter", "replace") or action.target is None:
		return
	if action.target.start_row != action.target.end_row or action.target.start_column != action.target.end_column:
		return
	binding_links = []
	for match in re.finditer(r"\[([^]]*)\]\(([^)]*)\)", inline.content):
		if bindings.binding_kind(urllib.parse.unquote(match[2])) is not None:
			binding_links.append(match)
	if binding_index >= len(binding_links):
		return
	# Look only at the clause before this action link. Earlier actions in the
	# same paragraph may name different destinations.
	visible = inline.content[:binding_links[binding_index].start()]
	visible = visible.replace("**", "").replace("`", "")
	matches = list(re.finditer(
		r"(?:^|[.;:*][\s\"']*|,\s*(?:and\s+)?|\b(?:and|then)\s+)In\s+"
		r"(?:cell\s+)?(\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)\s*,?\s+"
		r"(?:type|enter|calculate|use|replace|label)\b", visible, re.IGNORECASE))
	if not matches:
		return
	match = matches[-1]
	mentioned = references.parse_reference(match[1], action.worksheet or "")
	if mentioned is None or (mentioned.start_row == action.target.start_row
		and mentioned.start_column == action.target.start_column
		and mentioned.sheet.casefold() == action.target.sheet.casefold()):
		return
	diagnostic(document, "action-visible-target", location,
		f"Visible cell {match[1]} disagrees with {action.kind} target {action.target.address}",
		f"Use cell {action.target.address} in the instruction or change the binding target")


def _scalar_action(document: model.Document, action: model.Action, index: int,
	item_end: int) -> None:
	raw = action.payload
	fences = []
	for following in document.tokens[index + 1:]:
		if following.map is not None and following.map[0] >= item_end:
			break
		if following.type == "fence" and following.level == document.tokens[index].level - 1:
			fences.append(following)
	if fences:
		if (action.kind == "label" or raw.strip() or len(fences) != 1
			or fences[0].info.strip() != "sheets"):
			diagnostic(document, "action-scalar", action.span, "Competing or unsupported formula block",
				"Use literal text for Label; use one sheets formula block for Enter or Replace")
			return
		formula = fences[0].content.rstrip("\n")
		if (not formula.startswith("=") or not formula[1:].strip()
			or "\n" in formula):
			diagnostic(document, "action-scalar", action.span, "Formula block must contain one formula line",
				"Use one logical line starting with equals")
			return
		action.scalar = _scalar_value(formula)
		return
	try:
		if action.kind == "label":
			action.scalar = model.Scalar("text", scalar_text(raw))
		else:
			action.scalar = parse_scalar(raw)
			if action.scalar.kind == "blank":
				raise ValueError("Assignment payload is empty")
	except ValueError as error:
		diagnostic(document, "action-scalar", action.span, str(error),
			"Use one scalar; put explanations in a separate paragraph")
