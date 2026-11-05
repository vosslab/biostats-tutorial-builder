"""Central style definitions for native, editable tutorial documents."""

import docx.enum.text
import docx.oxml
import docx.oxml.ns
import docx.shared


BODY_FONT = "PT Sans"
NARROW_FONT = "PT Sans Narrow"
CODE_FONT = "Roboto Mono"
BODY_SIZE = 11
CODE_SIZE = 9
PAGE_MARGIN = 0.6
FIGURE_MAX_WIDTH_INCHES = 6.5
FIGURE_MAX_HEIGHT_INCHES = 3
BODY_INDENT_INCHES = 0.3
BODY_INDENT_TWIPS = round(BODY_INDENT_INCHES * 1440)
LIST_INCREMENT_TWIPS = 360
LIST_HANGING_TWIPS = 240
LIST_HANGING_INCHES = LIST_HANGING_TWIPS / 1440
QUOTE_INDENT_INCHES = 0.25
CAPTION_INSET_INCHES = 0.2
TABLE_HEADER_FILL = "0067CC"
TABLE_STRIPE_FILL = "EEF5FC"
FORMULA_COLOR = "007A00"
FORMULA_BORDER = "007A00"
REFLECTION_FILL = "F3F7FC"
REFLECTION_BORDER = "174F91"


#============================================
def _set_explicit_font(style: object, font_name: str) -> None:
	"""Set a font family and remove theme selectors that override it in exports."""
	style.font.name = font_name
	r_fonts = style._element.get_or_add_rPr().get_or_add_rFonts()
	for theme_attribute in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
		r_fonts.attrib.pop(docx.oxml.ns.qn(f"w:{theme_attribute}"), None)
	for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
		r_fonts.set(docx.oxml.ns.qn(f"w:{attribute}"), font_name)


#============================================
def format_run(run: object, role: str | None = None, linked: bool = False,
	font_name: str | None = None) -> None:
	"""Apply portable role formatting directly, without custom character styles."""
	if role in ("code", "cell", "menu", "formula"):
		font_name = CODE_FONT
		run.font.size = docx.shared.Pt(CODE_SIZE)
	# Ordinary text inherits its editable paragraph style; only roles override fonts.
	if font_name is not None:
		_set_explicit_font(run, font_name)
	if role in ("cell", "menu"):
		run.bold = True
	if role == "menu":
		run.font.color.rgb = docx.shared.RGBColor.from_string("202124")
		shade(run._r.get_or_add_rPr(), "EEEEEE")
	if linked:
		run.font.underline = True
		run.font.color.rgb = docx.shared.RGBColor.from_string("174F91")
	if role == "formula":
		run.font.color.rgb = docx.shared.RGBColor.from_string(FORMULA_COLOR)


#============================================
def format_list(paragraph: object) -> None:
	"""Compact every paragraph within a list, including continuation paragraphs."""
	paragraph.paragraph_format.space_before = docx.shared.Pt(0)
	paragraph.paragraph_format.space_after = docx.shared.Pt(2)
	paragraph.paragraph_format.line_spacing = 1.0


#============================================
def content_indent(list_depth: int = 0, quote_depth: int = 0) -> float:
	"""Return the hierarchical text edge for body, lists, and quotations."""
	list_increment = (LIST_INCREMENT_TWIPS / 1440) * max(0, list_depth - 1)
	return BODY_INDENT_INCHES + list_increment + QUOTE_INDENT_INCHES * quote_depth


#============================================
def list_text_indent_twips(depth: int) -> int:
	"""Return a native list text edge for zero-based numbering depth."""
	return BODY_INDENT_TWIPS + LIST_INCREMENT_TWIPS * depth


#============================================
def format_content(paragraph: object, list_depth: int = 0, quote_depth: int = 0,
	list_item: bool = False) -> None:
	"""Align each narrative branch to its structural teaching edge."""
	paragraph.paragraph_format.left_indent = docx.shared.Inches(
		content_indent(list_depth, quote_depth))
	paragraph.paragraph_format.right_indent = docx.shared.Inches(0)
	paragraph.paragraph_format.first_line_indent = docx.shared.Inches(
		-LIST_HANGING_INCHES if list_item else 0)


#============================================
def usable_width(paragraph: object) -> float:
	"""Measure the current paragraph width from its real section and indents."""
	section = paragraph.part.document.sections[-1]
	left = paragraph.paragraph_format.left_indent or 0
	right = paragraph.paragraph_format.right_indent or 0
	width = section.page_width - section.left_margin - section.right_margin - left - right
	return max(1, width / docx.shared.Inches(1))


#============================================
def format_figure(paragraph: object) -> None:
	"""Center a standalone figure independently of the Normal body indent."""
	paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
	paragraph.paragraph_format.left_indent = docx.shared.Inches(0)
	paragraph.paragraph_format.right_indent = docx.shared.Inches(0)
	paragraph.paragraph_format.first_line_indent = docx.shared.Inches(0)
	paragraph.paragraph_format.space_after = docx.shared.Pt(0)


#============================================
def format_figure_caption(paragraph: object, list_depth: int = 0, quote_depth: int = 0) -> None:
	"""Align figure captions to the main body edge below centered figures."""
	paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.LEFT
	paragraph.paragraph_format.left_indent = docx.shared.Inches(
		content_indent(0, quote_depth) + CAPTION_INSET_INCHES)
	paragraph.paragraph_format.right_indent = docx.shared.Inches(CAPTION_INSET_INCHES)
	paragraph.paragraph_format.first_line_indent = docx.shared.Inches(0)
	paragraph.paragraph_format.space_after = docx.shared.Pt(8)


#============================================
def format_figure_caption_runs(paragraph: object) -> None:
	"""Use a compact caption size without replacing the native Normal style."""
	for run in paragraph.runs:
		run.font.size = docx.shared.Pt(BODY_SIZE - 1)


#============================================
def format_reflection_prompt(paragraph: object) -> None:
	"""Give a contextual reflection prompt a quiet, native paragraph callout."""
	paragraph.paragraph_format.space_before = docx.shared.Pt(4)
	paragraph.paragraph_format.space_after = docx.shared.Pt(6)
	properties = paragraph._p.get_or_add_pPr()
	shade(properties, REFLECTION_FILL)
	borders = docx.oxml.OxmlElement("w:pBdr")
	for edge in ("top", "left", "bottom", "right"):
		border = docx.oxml.OxmlElement(f"w:{edge}")
		for key, value in {"val": "single", "sz": "4", "space": "4", "color": REFLECTION_BORDER}.items():
			border.set(docx.oxml.ns.qn(f"w:{key}"), value)
		borders.append(border)
	properties.append(borders)


#============================================
def format_table_header(cell: object) -> None:
	"""Give authored tables a compact, readable teaching-material header."""
	shade(cell._tc.get_or_add_tcPr(), TABLE_HEADER_FILL)
	for paragraph in cell.paragraphs:
		paragraph.paragraph_format.space_after = docx.shared.Pt(2)
		for run in paragraph.runs:
			run.bold = True
			run.font.color.rgb = docx.shared.RGBColor.from_string("FFFFFF")


#============================================
def format_table_stripe(row: object) -> None:
	"""Use a quiet alternating tint so dense scientific tables remain scannable."""
	for cell in row.cells:
		shade(cell._tc.get_or_add_tcPr(), TABLE_STRIPE_FILL)


#============================================
def justify_narrative(paragraph: object) -> None:
	"""Justify every ordinary prose paragraph, never authored display lines.

	Word and Google Docs determine final wrapping themselves. Alignment must not depend
	on a local font-metric guess. Callers exclude lists, formulas, figures, quotes, and
	paragraphs with intentional hard breaks.
	"""
	if "\n" not in paragraph.text:
		paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY


#============================================
def shade(element: object, color: str) -> None:
	"""Apply an OOXML background without replacing the native content."""
	fill = docx.oxml.OxmlElement("w:shd")
	fill.set(docx.oxml.ns.qn("w:fill"), color)
	element.append(fill)


#============================================
def add_page_number(paragraph: object) -> None:
	"""Add a native Word PAGE field to a footer paragraph."""
	paragraph.style = "Normal"
	paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.RIGHT
	run = paragraph.add_run()
	field = docx.oxml.OxmlElement("w:fldSimple")
	field.set(docx.oxml.ns.qn("w:instr"), "PAGE")
	result = docx.oxml.OxmlElement("w:r")
	text = docx.oxml.OxmlElement("w:t")
	text.text = "1"
	result.append(text)
	field.append(result)
	run._r.addnext(field)


#============================================
def configure(document: object) -> None:
	"""Configure the six standard paragraph styles used by tutorial content."""
	for section in document.sections:
		section.top_margin = docx.shared.Inches(PAGE_MARGIN)
		section.bottom_margin = docx.shared.Inches(PAGE_MARGIN)
		section.left_margin = docx.shared.Inches(PAGE_MARGIN)
		section.right_margin = docx.shared.Inches(PAGE_MARGIN)
		add_page_number(section.footer.paragraphs[0])
	styles = document.styles
	normal = styles["Normal"]
	_set_explicit_font(normal, BODY_FONT)
	normal.font.size = docx.shared.Pt(BODY_SIZE)
	normal.paragraph_format.space_after = docx.shared.Pt(6)
	normal.paragraph_format.line_spacing = 1.08
	normal.paragraph_format.left_indent = docx.shared.Inches(0)
	for name in ("Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3"):
		style = styles[name]
		_set_explicit_font(style, BODY_FONT)
		if name.startswith("Heading"):
			level = int(name[-1])
			size = {1: 18, 2: 15, 3: 12}[level]
			style.font.size = docx.shared.Pt(size)
			style.font.bold = True
			style.paragraph_format.keep_with_next = True
			style.paragraph_format.space_before = docx.shared.Pt(14)
			style.paragraph_format.space_after = docx.shared.Pt(6)
			style.paragraph_format.left_indent = docx.shared.Inches(
				{"Heading 1": 0, "Heading 2": 0.1, "Heading 3": 0.2}[name])
			style.font.color.rgb = docx.shared.RGBColor.from_string(
				{"Heading 1": "003FFF", "Heading 2": "007576", "Heading 3": "B74300"}[name])
	title = styles["Title"]
	title.font.size = docx.shared.Pt(25)
	title.font.bold = True
	title.font.color.rgb = docx.shared.RGBColor.from_string("0067CC")
	title.paragraph_format.space_after = docx.shared.Pt(14)
	title.paragraph_format.left_indent = docx.shared.Inches(0)


#============================================
def format_formula(paragraph: object, list_depth: int = 0, quote_depth: int = 0) -> None:
	"""Reserve compact display space for an editable formula."""
	format_content(paragraph, list_depth, quote_depth)
	paragraph.paragraph_format.space_before = docx.shared.Pt(5)
	paragraph.paragraph_format.space_after = docx.shared.Pt(8)
	paragraph.paragraph_format.keep_with_next = None


#============================================
def format_formula_display_runs(paragraph: object) -> None:
	"""Box only formula-display characters, keeping surrounding page space unfilled."""
	for run in paragraph._p.findall(".//w:r", {"w": docx.oxml.ns.nsmap["w"]}):
		properties = run.get_or_add_rPr()
		for previous in properties.findall("w:color", {"w": docx.oxml.ns.nsmap["w"]}):
			properties.remove(previous)
		color = docx.oxml.OxmlElement("w:color")
		color.set(docx.oxml.ns.qn("w:val"), FORMULA_COLOR)
		properties.append(color)
		for previous in properties.findall("w:bdr", {"w": docx.oxml.ns.nsmap["w"]}):
			properties.remove(previous)
		border = docx.oxml.OxmlElement("w:bdr")
		for key, value in {"val": "single", "sz": "5", "space": "2", "color": FORMULA_BORDER}.items():
			border.set(docx.oxml.ns.qn(f"w:{key}"), value)
		properties.append(border)
