"""Markdown adapter retaining physical rows before GFM table normalization."""

import pathlib
import markdown_it
import mdit_py_plugins.dollarmath
import tutorial_lib.model
import tutorial_lib.formulas
import tutorial_lib.semantic_bindings


def markdown_parser() -> markdown_it.MarkdownIt:
	parser = markdown_it.MarkdownIt("commonmark", {"html": True})
	parser.enable("table")
	mdit_py_plugins.dollarmath.dollarmath_plugin(parser, allow_space=False, allow_digits=False)
	parser.inline.ruler.before("link", "semantic_binding", tutorial_lib.semantic_bindings.inline_binding)
	parser.inline.add_terminator_char("=")
	parser.inline.ruler.before("text", "spreadsheet_formula", tutorial_lib.formulas.inline_formula)
	parser.core.ruler.before("inline", "terminal_hardbreak", restore_terminal_hardbreak)
	parser.core.ruler.after("inline", "formula_roles", tutorial_lib.formulas.annotate_formulas)
	return parser


def restore_terminal_hardbreak(state: object) -> None:
	"""Retain authored line breaks that block parsing trims at paragraph boundaries."""
	lines = state.src.splitlines(keepends=True)
	for token in state.tokens:
		if token.type != "inline" or token.map is None or not token.content.endswith("\\"):
			continue
		backslashes = len(token.content) - len(token.content.rstrip("\\"))
		if backslashes % 2 and lines[token.map[1] - 1].endswith("\n"):
			# Fences/code spans retain their own parsing; never rewrite source bytes.
			token.content += "\n"


def parse_source(source: str, path: str | pathlib.Path) -> tutorial_lib.model.Document:
	document = tutorial_lib.model.Document(pathlib.Path(path), source)
	document.tokens = markdown_parser().parse(source)
	return document


def split_table_row(line: str) -> list[str]:
	"""Split GFM geometry: an escaped pipe is literal even inside code spans."""
	line = line.strip()
	if line.startswith("|"):
		line = line[1:]
	if line.endswith("|"):
		backslashes = len(line[:-1]) - len(line[:-1].rstrip("\\"))
		if backslashes % 2 == 0:
			line = line[:-1]
	parts = [""]
	for character in line:
		backslashes = len(parts[-1]) - len(parts[-1].rstrip("\\"))
		if character == "|" and backslashes % 2 == 0:
			parts.append("")
		elif character == "|":
			parts[-1] = parts[-1][:-1] + "|"
		else:
			parts[-1] += character
	return [part.strip() for part in parts]
