"""Native Word list definitions, including independent starts and nesting."""

import docx.oxml
import docx.oxml.ns
import docx.shared

import tutorial_lib.docx_styles


#============================================
def element(tag: str, value: str) -> object:
	node = docx.oxml.OxmlElement(f"w:{tag}")
	node.set(docx.oxml.ns.qn("w:val"), value)
	return node


#============================================
def create_list(document: object, ordered: bool, start: int, depth: int) -> int:
	"""Give each authored list its own numbering instance."""
	root = document.part.numbering_part.element
	abstract_ids = [int(item.get(docx.oxml.ns.qn("w:abstractNumId")))
		for item in root.findall(docx.oxml.ns.qn("w:abstractNum"))]
	abstract_id = max(abstract_ids, default=-1) + 1
	abstract = docx.oxml.OxmlElement("w:abstractNum")
	abstract.set(docx.oxml.ns.qn("w:abstractNumId"), str(abstract_id))
	abstract.append(element("multiLevelType", "singleLevel"))
	level = docx.oxml.OxmlElement("w:lvl")
	level.set(docx.oxml.ns.qn("w:ilvl"), "0")
	level.append(element("start", str(start)))
	level.append(element("numFmt", "decimal" if ordered else "bullet"))
	level.append(element("lvlText", "%1." if ordered else "\u2022"))
	level.append(element("suff", "tab"))
	properties = docx.oxml.OxmlElement("w:pPr")
	indent = docx.oxml.OxmlElement("w:ind")
	indent.set(docx.oxml.ns.qn("w:left"),
		str(tutorial_lib.docx_styles.list_text_indent_twips(depth)))
	indent.set(docx.oxml.ns.qn("w:hanging"),
		str(tutorial_lib.docx_styles.LIST_HANGING_TWIPS))
	properties.append(indent)
	tabs = docx.oxml.OxmlElement("w:tabs")
	tab = docx.oxml.OxmlElement("w:tab")
	tab.set(docx.oxml.ns.qn("w:val"), "num")
	tab.set(docx.oxml.ns.qn("w:pos"),
		str(tutorial_lib.docx_styles.list_text_indent_twips(depth)))
	tabs.append(tab)
	properties.append(tabs)
	level.append(properties)
	abstract.append(level)
	root.append(abstract)
	number = root.add_num(abstract_id)
	return number.numId


#============================================
def apply_list(paragraph: object, number_id: int) -> None:
	properties = paragraph._p.get_or_add_pPr().get_or_add_numPr()
	properties.get_or_add_ilvl().val = 0
	properties.get_or_add_numId().val = number_id
