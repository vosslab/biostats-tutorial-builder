"""Compile the authored question list and derive matching workbook/DOCX identities."""

import re
import dataclasses
import urllib.parse

import tutorial_lib.model as model
import tutorial_lib.semantic_bindings


#============================================
def _error(document: model.Document, location: model.SourceSpan, message: str) -> None:
	document.diagnostics.append(model.Diagnostic("error", "reflection-questions", location,
		message, "Use one ### Reflection Questions in Workbook with a nonempty flat numbered list"))


#============================================
def compile_questions(document: model.Document) -> set[int]:
	"""Consume question blocks without changing token positions or source spans."""
	ignored = set()
	section = None
	found = 0
	explicit_parts = set()
	for index, token in enumerate(document.tokens):
		if token.type != "heading_open":
			continue
		inline = document.tokens[index + 1]
		text = "".join(child.content for child in inline.children
			if child.type in ("text", "code_inline", "html_inline"))
		if token.tag == "h2":
			section = text
		if section == "Tutorial" and token.tag == "h3":
			match = re.fullmatch(r"Part ([1-9][0-9]*):\s*.+", text, re.IGNORECASE)
			if match:
				explicit_parts.add(int(match[1]))
		if not re.match(r"Reflection Questions\b", text, re.IGNORECASE):
			continue
		found += 1
		location = model.SourceSpan(str(document.path), token.map[0] + 1, token.map[1])
		if text != "Reflection Questions" or token.tag != "h3" or section != "Workbook":
			_error(document, location, "Reflection Questions must be an exact H3 in Workbook")
		if found > 1:
			_error(document, location, "Duplicate Reflection Questions section")
		end = index + 3
		while end < len(document.tokens) and document.tokens[end].type != "heading_open":
			end += 1
		ignored.update(range(index, end))
		body = document.tokens[index + 3:end]
		allowed = {"ordered_list_open": 0, "ordered_list_close": 0,
			"list_item_open": 1, "list_item_close": 1, "paragraph_open": 2,
			"paragraph_close": 2, "inline": 3}
		item_types = ["list_item_open", "paragraph_open", "inline", "paragraph_close",
			"list_item_close"]
		item_count = sum(item.type == "list_item_open" for item in body)
		if (not body or body[0].type != "ordered_list_open"
			or body[-1].type != "ordered_list_close"
			or any(item.type not in allowed or item.level != allowed[item.type] for item in body)
			or item_count == 0
			or [item.type for item in body[1:-1]] != item_types * item_count):
			_error(document, location, "Reflection Questions requires a flat numbered question list")
			continue
		for item in body:
			if item.type != "inline":
				continue
			question_span = model.SourceSpan(str(document.path), item.map[0] + 1, item.map[1])
			if any(child.type == "image" or child.type == "link_open"
				and tutorial_lib.semantic_bindings.binding_kind(
					urllib.parse.unquote(child.attrGet("href"))) is not None
				for child in item.children):
				_error(document, question_span,
					"Reflection questions cannot contain images or spreadsheet action bindings")
				continue
			pieces = []
			for child in item.children:
				if child.type == "html_inline":
					if re.fullmatch(r"<br\s*/?>", child.content, re.IGNORECASE):
						pieces.append("\n")
					elif child.content.lower() not in ("<sub>", "</sub>", "<sup>", "</sup>"):
						_error(document, question_span, f"Unsupported inline HTML {child.content}")
				elif child.type in ("softbreak", "hardbreak"):
					pieces.append(" " if child.type == "softbreak" else "\n")
				else:
					pieces.append(child.content)
			text = "".join(pieces).strip()
			if not text:
				_error(document, question_span, "Reflection question is empty")
			else:
				document.reflection_questions.append(model.ReflectionQuestion(
					text, question_span, item.children))
	if found == 0:
		_error(document, model.SourceSpan(str(document.path), 1, 1),
			"Required Reflection Questions section is missing")
	if len(explicit_parts) == 1:
		document.reflection_part_number = explicit_parts.pop()
	return ignored


#============================================
def question_identifier(document: model.Document, number: int) -> str:
	identifier = str(number)
	if document.reflection_part_number is not None:
		identifier = f"{document.reflection_part_number}.{number}"
	return identifier


#============================================
def worksheet(document: model.Document, name: str = "Reflection Questions") -> model.Worksheet:
	"""Create literal text seeds; answer placeholders remain editable ordinary cells."""
	location = document.reflection_questions[0].span
	sheet = model.Worksheet(name, location, is_reflection=True)
	sheet.cells[(1, 1)] = model.CellSeed(1, 1, model.Scalar("text", "Reflection Questions"), location)
	for number, question in enumerate(document.reflection_questions, 1):
		row = number * 2
		text = f"{question_identifier(document, number)}. {question.text}"
		sheet.cells[(row, 1)] = model.CellSeed(row, 1, model.Scalar("text", text), question.span)
		sheet.cells[(row + 1, 1)] = model.CellSeed(row + 1, 1,
			model.Scalar("text", "answer here"), question.span)
		sheet.entry_cells.add((row + 1, 1))
	return sheet


#============================================
def resolve_documents(documents: list[model.Document]) -> list[model.Document]:
	"""Copy source models and assign the same identity to DOCX and workbook output."""
	if len(documents) < 2:
		return list(documents)
	resolved = []
	used_numbers = {}
	for index, document in enumerate(documents, 1):
		number = document.reflection_part_number
		if number is None:
			number = index
		if number in used_numbers:
			raise ValueError(f"Reflection part identity collision: Part {number} in "
				f"{used_numbers[number]} and {document.path}; change the explicit Part number "
				"or source order")
		used_numbers[number] = document.path
		copy = dataclasses.replace(document, reflection_part_number=number,
			worksheets=[sheet for sheet in document.worksheets if not sheet.is_reflection])
		if copy.reflection_questions:
			name = f"Part {number} Reflection"
			if any(sheet.name.casefold() == name.casefold() for sheet in copy.worksheets):
				raise ValueError(f"Generated reflection worksheet name collision: {name}")
			copy.worksheets.append(worksheet(copy, name))
		resolved.append(copy)
	return resolved
