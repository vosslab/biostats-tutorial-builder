"""Translate recognized future-function names at the XLSX storage boundary only."""

import openpyxl.formula.tokenizer


# These modern statistical names are in the compiler's checked function vocabulary.
# OOXML stores them with _xlfn.; unknown functions remain explicitly unchecked.
# https://openpyxl.readthedocs.io/en/3.1/simple_formulae.html
FUTURE_FUNCTIONS = frozenset({
	"FILTER", "STDEV.S", "STDEV.P", "VAR.S", "VAR.P", "T.TEST", "F.TEST", "Z.TEST",
	"T.DIST", "T.DIST.2T", "T.DIST.RT", "T.INV", "T.INV.2T",
	"NORM.DIST", "NORM.S.DIST", "NORM.INV", "NORM.S.INV",
	"F.DIST", "F.DIST.RT", "F.INV", "F.INV.RT", "CHISQ.TEST",
	"CHISQ.DIST", "CHISQ.DIST.RT", "CHISQ.INV", "CHISQ.INV.RT",
})


#============================================
def _translate(formula: str, serialize: bool) -> str:
	"""Replace function tokens while preserving original spacing and string literals."""
	if not formula.startswith("="):
		raise ValueError("An XLSX formula must start with '='")
	tokens = openpyxl.formula.tokenizer.Tokenizer(formula).items
	pieces = ["="]
	position = 1
	for token in tokens:
		start = position
		if token.type == "WHITE-SPACE":
			# Tokenizer collapses consecutive whitespace; retain the original slice.
			while position < len(formula) and formula[position].isspace():
				position += 1
		else:
			if not formula.startswith(token.value, position):
				raise ValueError("Formula tokens do not match the original formula")
			position += len(token.value)
		value = formula[start:position]
		if token.type == "FUNC" and token.subtype == "OPEN":
			name = token.value[:-1]
			if serialize and name.upper() in FUTURE_FUNCTIONS:
				value = ("_xlfn._xlws." if name.upper() == "FILTER" else "_xlfn.") + value
			elif (not serialize and name.lower().startswith("_xlfn.")
				and name[6:].removeprefix("_xlws.").upper() in FUTURE_FUNCTIONS):
				value = value[6:].removeprefix("_xlws.")
		pieces.append(value)
	if position != len(formula):
		raise ValueError("Formula tokens do not cover the original formula")
	result = "".join(pieces)
	return result


#============================================
def serialize_formula(formula: str) -> str:
	"""Add required OOXML prefixes without changing authored formula semantics."""
	result = _translate(formula, serialize=True)
	return result


#============================================
def logical_formula(formula: str) -> str:
	"""Normalize recognized OOXML function prefixes when reading logical formulas."""
	result = _translate(formula, serialize=False)
	return result
