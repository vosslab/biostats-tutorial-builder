"""Static reference, availability, content, and instruction-history checks."""

import io
import re
import base64
import urllib.parse
import PIL.Image
import openpyxl.formula.translate
import openpyxl.formula.tokenizer
import tutorial_lib.model as model
import tutorial_lib.compiler as compiler
import tutorial_lib.references as references


IMAGE_DIMENSION = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?in\Z")


#============================================
def is_managed_screenshot_comment(token: object) -> bool:
	"""Identify complete nonvisible screenshot metadata without accepting adjacent HTML."""
	# ASVS 2.2.1: allow only complete, nonvisible managed metadata tokens.
	accepted = token.type == "html_block" and token.content.strip() in (
		"<!-- screenshots:begin (managed by screenshot-docs) -->",
		"<!-- screenshots:end -->",
	)
	return accepted


def _canonical_sheet(document: model.Document, name: str) -> model.Worksheet | None:
	for sheet in document.worksheets:
		if sheet.name.casefold() == name.casefold():
			return sheet
	return None


def _resolve(document: model.Document, reference: model.CellReference,
	location: model.SourceSpan) -> model.CellReference | None:
	sheet = _canonical_sheet(document, reference.sheet)
	if sheet is None:
		compiler.diagnostic(document, "unknown-sheet", location,
			f"Unknown worksheet {reference.sheet}", "Use a declared worksheet name",
			worksheet=reference.sheet, address=reference.address)
		return None
	return model.CellReference(sheet.name, reference.start_row, reference.start_column,
		reference.end_row, reference.end_column, reference.address)


def _initial_states(document: model.Document) -> dict:
	state = {}
	for sheet in document.worksheets:
		for coordinate, cell in sheet.cells.items():
			if cell.scalar.kind != "blank":
				state[(sheet.name, *coordinate)] = (cell.scalar, cell.span)
	return state


def _check_reference(document: model.Document, reference: model.CellReference,
	location: model.SourceSpan, states: list[dict], dataset: bool = False) -> None:
	reference = _resolve(document, reference, location)
	if reference is None:
		return
	# Source regions describe input capacity, not a requirement to fill every cell.
	sheet = _canonical_sheet(document, reference.sheet)
	if any(region.role == "source"
		and region.reference.start_row <= reference.start_row <= reference.end_row <= region.reference.end_row
		and region.reference.start_column <= reference.start_column <= reference.end_column <= region.reference.end_column
		for region in sheet.role_regions):
		return
	available = []
	for state in states:
		count = sum(1 for key in state if key[0] == reference.sheet
			and reference.start_row <= key[1] <= reference.end_row
			and reference.start_column <= key[2] <= reference.end_column)
		available.append(count)
	area = ((reference.end_row - reference.start_row + 1)
		* (reference.end_column - reference.start_column + 1))
	if any(count != area for count in available):
		category = "conditional-input" if any(count == area for count in available) else "unavailable-input"
		compiler.diagnostic(document, category, location,
			f"Reference {reference.address} includes inputs not supplied before use",
			"Check the input range and instruction order", "warning",
			worksheet=reference.sheet, address=reference.address)
	if dataset and reference.end_row > reference.start_row:
		sheet = _canonical_sheet(document, reference.sheet)
		rows = [row for (row, column), cell in sheet.cells.items()
			if reference.start_column <= column <= reference.end_column
			and cell.scalar.kind != "blank"]
		if rows and reference.end_row > max(rows):
			compiler.diagnostic(document, "range-overshoot", location,
				f"Range ends at row {reference.end_row}; populated source data ends at {max(rows)}",
				"Confirm intentional spare rows or correct the endpoint", "warning",
				worksheet=reference.sheet, address=reference.address)


def _formula(document: model.Document, scalar: model.Scalar, sheet: str,
	location: model.SourceSpan, states: list[dict]) -> None:
	formula = str(scalar.value)
	static, limitations, invalid_addresses = references.formula_references(formula, sheet)
	resolved = []
	for reference in static:
		value = _resolve(document, reference, location)
		if value is not None:
			resolved.append(value)
			_check_reference(document, value, location, states, True)
	status = "partial" if limitations and static else "unchecked" if limitations else "verified"
	if len(resolved) != len(static):
		status = "partial"
	if invalid_addresses:
		status = "partial" if resolved else "unchecked"
	document.formula_checks.append(model.FormulaCheck(
		formula, location, status, tuple(resolved), tuple(limitations),
	))
	for limitation in limitations:
		if limitation == "Formula syntax could not be tokenized":
			compiler.diagnostic(document, "formula-syntax", location, limitation,
				"Correct the formula syntax before relying on reference validation")
		else:
			compiler.diagnostic(document, "formula-coverage", location, limitation,
				"Review this formula manually in the target spreadsheet application", "warning")
	for address in invalid_addresses:
		compiler.diagnostic(document, "invalid-address", location,
			f"Impossible static A1 address: {address}",
			"Use ordered cells within A1:XFD1048576", worksheet=sheet, address=address)


def _apply_action(document: model.Document, action: model.Action, states: list[dict]) -> None:
	if action.target is None:
		return
	target = _resolve(document, action.target, action.span)
	if target is None:
		return
	action.target = target
	if action.kind == "fill":
		_fill_down(document, action, states)
		return
	if action.kind == "select":
		_check_reference(document, target, action.span, states)
		return
	if action.scalar is None:
		return
	key = (target.sheet, target.start_row, target.start_column)
	sheet = _canonical_sheet(document, target.sheet)
	sheet.entry_cells.add((target.start_row, target.start_column))
	prior = [state.get(key) for state in states]
	if action.kind == "replace":
		if any(value is None for value in prior):
			compiler.diagnostic(document, "replacement-unavailable", action.span,
				"Replace requires a prior value in every possible branch",
				"Assign the cell in every alternative before replacing it",
				worksheet=target.sheet, address=target.address)
	else:
		conflicts = [value for value in prior if value is not None and value[0] != action.scalar]
		if conflicts:
			compiler.diagnostic(document, "assignment-conflict", action.span,
				"Destination already has a different value", "Use Replace or explicit alternatives",
				worksheet=target.sheet, address=target.address, related=conflicts[0][1])
		elif any(value is not None for value in prior):
			compiler.diagnostic(document, "assignment-redundant", action.span,
				"Identical assignment repeats a prior value", "Remove the redundant instruction",
				"warning", worksheet=target.sheet, address=target.address)
	if action.scalar.kind == "formula":
		_formula(document, action.scalar, target.sheet, action.span, states)
	for state in states:
		state[key] = (action.scalar, action.span)


def _fill_down(document: model.Document, action: model.Action, states: list[dict]) -> None:
	"""Translate each top-row formula, then reuse ordinary Enter validation."""
	target = action.target
	action.generated_actions.clear()
	if action.payload.strip() != "Down" or target.start_row == target.end_row:
		return
	sources = {}
	for column in range(target.start_column, target.end_column + 1):
		key = (target.sheet, target.start_row, column)
		prior = [state.get(key) for state in states]
		if any(value is None or value[0].kind != "formula" for value in prior):
			compiler.diagnostic(document, "fill-source", action.span,
				"Fill requires a first-row formula in every possible branch",
				"Enter a formula in each source cell before Fill", worksheet=target.sheet,
				address=f"{references.column_letters(column)}{target.start_row}")
			return
		if any(value[0] != prior[0][0] for value in prior):
			compiler.diagnostic(document, "fill-source", action.span,
				"Fill source formulas differ between possible branches",
				"Use identical source formulas or put Fill inside each alternative",
				worksheet=target.sheet, address=target.address)
			return
		sources[column] = str(prior[0][0].value)
	# Row order makes same-row references to earlier filled columns available.
	for row in range(target.start_row + 1, target.end_row + 1):
		for column, formula in sources.items():
			origin = f"{references.column_letters(column)}{target.start_row}"
			address = f"{references.column_letters(column)}{row}"
			try:
				translator = openpyxl.formula.translate.Translator(formula, origin=origin)
				translated = translator.translate_formula(address)
			except (openpyxl.formula.tokenizer.TokenizerError, IndexError,
				openpyxl.formula.translate.TranslatorError) as error:
				compiler.diagnostic(document, "fill-formula", action.span, str(error),
					"Correct the source formula before filling down")
				return
			child = model.Action("enter", action.span, action.token_index, translated,
				target=model.CellReference(target.sheet, row, column, row, column, address),
				scalar=model.Scalar("formula", translated), worksheet=target.sheet,
				alternative_group=action.alternative_group,
				alternative_branch=action.alternative_branch)
			action.generated_actions.append(child)
	for child in action.generated_actions:
		_apply_action(document, child, states)


def _content(document: model.Document, states_before: dict[int, list[dict]]) -> None:
	scope = document.worksheets[0].name if len(document.worksheets) == 1 else ""
	write_targets = {}
	for action in document.actions:
		if action.kind == "select" or action.target is None:
			continue
		write_targets.setdefault(action.token_index, set()).add((
			action.target.sheet.casefold(), action.target.start_row,
			action.target.start_column, action.target.end_row, action.target.end_column))
	heading_slugs = {}
	for heading in document.headings:
		heading_slugs.setdefault(heading.slug, []).append(heading)
	known_headings = {heading.token_index for heading in document.headings}
	for index in document.content_token_indices:
		token = document.tokens[index]
		if token.type == "heading_open" and index not in known_headings:
			text = document.tokens[index + 1].content
			slug = re.sub(r"[^\w\s-]", "", text.lower())
			slug = re.sub(r"\s+", "-", slug.strip())
			heading = model.Heading(int(token.tag[1:]), text, text, slug,
				compiler.span(document, token), index)
			token.meta["heading"] = heading
			heading_slugs.setdefault(slug, []).append(heading)
	for index in document.content_token_indices:
		token = document.tokens[index]
		location = compiler.span(document, token)
		if token.type == "heading_open" and token.meta.get("heading") is not None:
			if token.meta["heading"].kind == "part":
				scope = document.worksheets[0].name if len(document.worksheets) == 1 else ""
		if token.type == "html_block" and not is_managed_screenshot_comment(token):
			compiler.diagnostic(document, "unsupported-content", location,
				"Raw HTML block is unsupported", "Use supported Markdown blocks")
		if token.type != "inline":
			continue
		action = token.meta.get("action")
		if action is not None and action.worksheet is not None:
			scope = action.worksheet
		if re.search(r"\bStep\s+[0-9]+(?:\.[0-9]+)?", token.content) and not (
			index > 0 and document.tokens[index - 1].type == "heading_open"):
			compiler.diagnostic(document, "literal-step-number", location,
				"Literal step number may drift after editing", "Use an internal heading link", "warning")
		if re.search(r"^\[[ xX]\]\s", token.content):
			compiler.diagnostic(document, "unsupported-content", location, "Task lists are unsupported",
				"Use an ordinary instruction list")
		semantic_text = "".join(child.content if child.type == "text" else "\n"
			for child in token.children)
		if re.search(r"\[\^[^]]+\]", semantic_text):
			compiler.diagnostic(document, "unsupported-content", location, "Footnotes are unsupported",
				"Use an ordinary paragraph or link")
		for child_index, child in enumerate(token.children):
			if child.type == "html_inline" and not re.fullmatch(
				r"</?(?:sub|sup)>|<br\s*/?>", child.content, re.IGNORECASE):
				compiler.diagnostic(document, "unsupported-content", location,
					f"Unsupported inline HTML {child.content}", "Use sub, sup, br, or Markdown")
			if child.type == "image":
				_asset(document, child, location)
				if child_index + 1 < len(token.children):
					suffix = token.children[child_index + 1]
					if suffix.type == "text" and re.match(r"^\{[^}]*\}", suffix.content):
						compiler.diagnostic(document, "image-size", location,
							"Malformed image size attributes", "Use width=5in or height=2in")
			if child.type == "link_open":
				if "binding_action" in child.meta:
					continue
				href = child.attrGet("href")
				if href.startswith("#"):
					slug = urllib.parse.unquote(href[1:])
					matches = heading_slugs.get(slug, [])
					if len(matches) != 1:
						compiler.diagnostic(document, "heading-link", location,
							f"Heading link {href} resolves to {len(matches)} headings",
							"Use a unique existing heading slug")
					else:
						child.meta["heading"] = matches[0]
			if child.type == "code_inline":
				if "binding_action" in child.meta:
					continue
				# A literal scalar payload may look exactly like a sheet reference.
				# It is already parsed as the action value, so prose-reference
				# classification here would incorrectly treat e.g. `Absent!A1` as
				# a workbook link. Formula payloads and Select targets remain checked.
				if (action is not None and action.kind in ("label", "enter", "replace")
					and action.scalar is not None and action.scalar.kind == "text"
					and action.scalar.value == child.content):
					continue
				reference = references.parse_reference(child.content, scope)
				if reference is not None:
					resolved = _resolve(document, reference, location)
					if resolved is not None:
						child.meta["reference"] = resolved
						# Select payload is already checked once as an action.
						# A prose reference to a destination in this same paragraph names
						# what the paragraph is assigning. It is not a read of a prior
						# workbook value; formula inputs still use _formula's ordered check.
						destination = (resolved.sheet.casefold(), resolved.start_row,
							resolved.start_column, resolved.end_row, resolved.end_column)
						if (action is None and destination not in write_targets.get(index, set())):
							_check_reference(document, resolved, location, states_before[index])


def _asset(document: model.Document, token: object, location: model.SourceSpan) -> None:
	if "insecure_attrs" in token.meta:
		compiler.diagnostic(document, "image-size", location,
			"Image attributes support only width and height", "Use width=5in or height=2in")
	for name in ("width", "height"):
		value = token.attrGet(name)
		if value is not None and (IMAGE_DIMENSION.fullmatch(value) is None
			or float(value[:-2]) <= 0):
			compiler.diagnostic(document, "image-size", location,
				f"Image {name} must be a positive inch value", "Use width=5in or height=2in")
	source = token.attrGet("src")
	match = re.fullmatch(r"data:image/(png|jpeg);base64,([A-Za-z0-9+/=\s]+)", source)
	if match is not None:
		encoded = re.sub(r"\s", "", match[2])
		try:
			data = base64.b64decode(encoded, validate=True)
		except ValueError:
			compiler.diagnostic(document, "image-invalid", location, "Malformed image data URI",
				"Supply a valid PNG/JPEG data URI")
			return
		token.meta["asset"] = data
		token.meta["asset_mime"] = "image/" + match[1]
		if not _image_signature(data):
			compiler.diagnostic(document, "image-invalid", location, "Image data is not PNG/JPEG",
				"Supply a valid supported image")
		return
	url = urllib.parse.urlparse(source)
	if url.scheme or url.netloc:
		compiler.diagnostic(document, "image-unsupported", location,
			"Only local PNG/JPEG/WebP and PNG/JPEG data URIs are supported",
			"Save the image beside the source")
		return
	asset = (document.path.parent / urllib.parse.unquote(url.path)).resolve()
	if not asset.is_file() or asset.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
		compiler.diagnostic(document, "image-missing", location,
			f"Missing or unsupported local image {source}", "Supply a local PNG/JPEG/WebP image")
		return
	token.meta["asset"] = asset
	data = asset.read_bytes()
	valid = _webp_image(data) if asset.suffix.lower() == ".webp" else _image_signature(data)
	if not valid:
		compiler.diagnostic(document, "image-invalid", location, "Local image is not valid PNG/JPEG/WebP",
			"Supply a valid supported image")
	if asset not in document.assets:
		document.assets.append(asset)


def _image_signature(data: bytes) -> bool:
	return data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff")


#============================================
def _webp_image(data: bytes) -> bool:
	"""Require both WebP container identification and decodable image pixels."""
	# ASVS 5.2.2: validate WebP content rather than trusting the filename extension.
	if not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
		return False
	try:
		image = PIL.Image.open(io.BytesIO(data), formats=("WEBP",))
	except (OSError, ValueError):
		return False
	with image:
		try:
			image.load()
		except (OSError, ValueError):
			return False
	return True


def validate_document(document: model.Document) -> None:
	initial = _initial_states(document)
	states = [initial]
	for sheet in document.worksheets:
		if sheet.google is None:
			compiler.diagnostic(document, "google-unmapped", sheet.span,
				"Worksheet has no Google cell-link mapping", "Optionally add a Google Sheets URL", "note")
		for cell in sheet.cells.values():
			if cell.scalar.kind == "formula":
				_formula(document, cell.scalar, sheet.name, cell.span, [initial])
	mapped = [sheet for sheet in document.worksheets if sheet.google is not None]
	for offset, sheet in enumerate(mapped):
		for previous in mapped[:offset]:
			if sheet.google.spreadsheet_id != previous.google.spreadsheet_id:
				compiler.diagnostic(document, "google-mapping", sheet.span,
					"Mapped sheets refer to different Google workbooks", "Use one spreadsheet ID")
			if sheet.google.gid is not None and sheet.google.gid == previous.google.gid:
				compiler.diagnostic(document, "google-mapping", sheet.span,
					"Different worksheets share a Google tab gid", "Supply distinct tab IDs")
	by_token = {}
	for action in document.actions:
		by_token.setdefault(action.token_index, []).append(action)
	states_before = {}
	active_group = None
	incoming = None
	branches = {}
	group_ends = {}
	group_counts = {}
	for token in document.tokens:
		if "alternative" in token.meta:
			group, branch = token.meta["alternative"]
			group_ends[group] = max(group_ends.get(group, 0), token.meta["alternative_end"])
			group_counts[group] = branch
	for group, count in group_counts.items():
		if count < 2:
			token = next(item for item in document.tokens
				if item.meta.get("alternative", (None,))[0] == group)
			compiler.diagnostic(document, "alternative-group", compiler.span(document, token),
				"Alternative group needs at least two branches", "Add a contiguous sibling alternative")
	for index in range(len(document.tokens)):
		token = document.tokens[index]
		actions = by_token.get(index, [])
		if active_group is not None and token.map is not None and token.map[0] >= group_ends[active_group]:
			states = [state for branch_states in branches.values() for state in branch_states]
			active_group = None
		if "alternative" in token.meta:
			group, branch = token.meta["alternative"]
			if group != active_group:
				incoming = [state.copy() for state in states]
				branches = {}
			states = [state.copy() for state in incoming]
			branches[branch] = states
			active_group = group
		states_before[index] = [state.copy() for state in states]
		for action in actions:
			_apply_action(document, action, states)
	_content(document, states_before)
	_ranges(document)
	_empty_steps(document)


def _ranges(document: model.Document) -> None:
	seen = {}
	for check in document.formula_checks:
		for reference in check.references:
			if reference.start_row == reference.end_row:
				continue
			key = (reference.sheet, reference.start_row, reference.start_column, reference.end_column)
			if key in seen and seen[key][0] != reference.end_row:
				compiler.diagnostic(document, "range-endpoint", check.span,
					"Related formulas use different range endpoints", "Compare the authored input ranges",
					"warning", worksheet=reference.sheet, address=reference.address,
					related=seen[key][1])
			seen[key] = (reference.end_row, check.span)


def _empty_steps(document: model.Document) -> None:
	for heading in document.headings:
		if heading.kind != "step":
			continue
		start = heading.token_index + 3
		end = len(document.tokens)
		for following in document.headings:
			if following.token_index > heading.token_index and following.level <= heading.level:
				end = following.token_index
				break
		if not any(token.type in ("inline", "fence", "code_block", "image", "table_open")
			for token in document.tokens[start:end]):
			compiler.diagnostic(document, "empty-step", heading.span, "Step has no content or substeps",
				"Add instructions or a Substep")
