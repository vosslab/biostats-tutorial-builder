"""Prepare local tutorial execution cases and compare calculated values."""

import math

import tutorial_lib.model
import tutorial_lib.references


#============================================
def extended_value(scalar: tutorial_lib.model.Scalar) -> dict:
	"""Preserve scalar types, including formula and literal equals-prefixed text."""
	keys = {"formula": "formulaValue", "text": "stringValue", "number": "numberValue",
		"boolean": "boolValue"}
	if scalar.kind == "blank":
		return {}
	result = {keys[scalar.kind]: scalar.value}
	return result


#============================================
def cell_write(sheet: str, row: int, column: int,
	scalar: tutorial_lib.model.Scalar, line: int) -> dict:
	address = f"{tutorial_lib.references.column_letters(column)}{row}"
	result = {"sheet": sheet, "row": row, "column": column, "address": address,
		"value": extended_value(scalar), "line": line}
	return result


#============================================
def prepare_cases(document: tutorial_lib.model.Document) -> list[dict]:
	"""Cover each alternative once, changing one group from the baseline at a time."""
	if document.has_errors:
		raise ValueError(f"Cannot execute invalid tutorial: {document.path}")
	groups = {}
	for action in document.actions:
		if action.alternative_group is not None:
			groups.setdefault(action.alternative_group, set()).add(action.alternative_branch)
	baseline = {group: min(branches) for group, branches in groups.items()}
	selections = [("baseline", baseline)]
	for group, branches in sorted(groups.items()):
		for branch in sorted(branches):
			if branch != baseline[group]:
				selections.append((f"group-{group}-branch-{branch}", baseline | {group: branch}))
	seeds = []
	for sheet in document.worksheets:
		for seed in sheet.cells.values():
			seeds.append(cell_write(sheet.name, seed.row, seed.column,
				seed.scalar, seed.span.start_line))
	cases = []
	for name, selected in selections:
		writes = []
		for action in document.actions:
			if action.alternative_group is not None:
				if selected[action.alternative_group] != action.alternative_branch:
					continue
			executable = action.generated_actions if action.kind == "fill" else [action]
			for entry in executable:
				if entry.scalar is None or entry.target is None:
					continue
				write = cell_write(entry.target.sheet, entry.target.start_row,
					entry.target.start_column, entry.scalar, action.span.start_line)
				write["action"] = entry.kind
				writes.append(write)
		cases.append({"tutorial": str(document.path), "scenario": name,
			"branches": selected, "sheets": [sheet.name for sheet in document.worksheets],
			"seeds": seeds, "writes": writes})
	return cases


#============================================
def compare_expectations(cells: dict, expectations: dict) -> list[dict]:
	results = []
	for address, expectation in expectations.items():
		expected = expectation["value"]
		cell = cells.get(address, {})
		effective = cell.get("effectiveValue", {})
		actual = None
		has_actual_value = False
		for key in ("numberValue", "stringValue", "boolValue"):
			if key in effective:
				actual = effective[key]
				has_actual_value = True
		matches = has_actual_value and type(actual) is type(expected) and actual == expected
		if type(expected) in (int, float) and type(actual) in (int, float):
			matches = math.isclose(actual, expected,
				rel_tol=expectation.get("relative_tolerance", 1e-7),
				abs_tol=expectation.get("absolute_tolerance", 1e-9))
		results.append({"address": address, "expected": expected, "actual": actual,
			"status": "passed" if matches and "errorValue" not in effective else "failed"})
	return results
