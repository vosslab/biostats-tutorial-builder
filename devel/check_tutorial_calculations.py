#!/usr/bin/env python3
"""Generate independent expected results and validate all tutorial cell mappings."""

import json
import math
import pathlib
import argparse

import numpy
import scipy.stats

import tutorial_lib.compiler
import tutorial_lib.build
import tutorial_lib.model
import tutorial_oracles
import sheets_validation_lib


#============================================
def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("-o", "--output", dest="output", type=pathlib.Path,
		default=pathlib.Path("tutorial_output/validation"))
	args = parser.parse_args()
	return args


#============================================
def expectations(values: dict, sheet: str) -> dict:
	result = {}
	for cell, value in values.items():
		address = cell if "!" in cell else sheet + "!" + cell
		if isinstance(value, (int, float)) and not math.isfinite(value):
			raise ValueError(f"Nonfinite oracle at {address}")
		result[address] = {"value": value,
			"relative_tolerance": 1e-7, "absolute_tolerance": 1e-10}
	return result


#============================================
def synthetic_direction_checks() -> list[dict]:
	"""Exercise intended models in both directions without changing teaching seeds."""
	checks = []
	for sign in (-1, 1):
		x = numpy.array([1., 2., 3., 4., 5.]) + 2 * sign
		one = scipy.stats.ttest_1samp(x, 3.)
		welch = scipy.stats.ttest_ind(x, numpy.array([1., 2., 3., 4., 5.]), equal_var=False)
		for label, test in (("one-sample-t", one), ("Welch-t", welch)):
			two, lower, higher = tutorial_oracles.tails(float(test.statistic), float(test.df))
			if not (math.isclose(two, float(test.pvalue), rel_tol=1e-12)
				and math.isclose(lower + higher, 1., abs_tol=1e-14)
				and (higher < .5 if sign > 0 else higher > .5)):
				raise ValueError(f"Synthetic directional model failed: {label}, sign={sign}")
			checks.append({"model": label, "sign": sign, "statistic": float(test.statistic),
				"two_tailed": two, "lower": lower, "higher": higher, "status": "passed"})
		two, lower, higher = tutorial_oracles.tails(2. * sign)
		if not (math.isclose(two, 2 * min(lower, higher), rel_tol=1e-12)
			and (higher < .5 if sign > 0 else higher > .5)):
			raise ValueError("Synthetic Z direction failed")
		checks.append({"model": "Z", "sign": sign, "two_tailed": two,
			"lower": lower, "higher": higher, "status": "passed"})
	for ratio in (.4, 2.5):
		lower = float(scipy.stats.f.cdf(ratio, 9, 14))
		higher = float(scipy.stats.f.sf(ratio, 9, 14))
		reciprocal = float(scipy.stats.f.cdf(1 / ratio, 14, 9))
		if not math.isclose(higher, reciprocal, rel_tol=1e-12):
			raise ValueError("F reciprocal orientation failed")
		checks.append({"model": "F", "ratio": ratio, "numerator_df": 9,
			"denominator_df": 14, "lower": lower, "higher": higher,
			"two_tailed": min(1., 2 * min(lower, higher)), "status": "passed"})
	return checks


#============================================
def check_mapping(document: tutorial_lib.model.Document, item: dict) -> dict:
	cases = sheets_validation_lib.prepare_cases(document)
	provenance = []
	for case in cases:
		values = item["common"] | item["scenarios"].get(case["scenario"], {})
		formulas = {write["sheet"] + "!" + write["address"]: write
			for write in case["seeds"] + case["writes"] if "formulaValue" in write["value"]}
		missing, extra = set(formulas) - set(values), set(values) - set(formulas)
		if missing or extra:
			raise ValueError(f"{document.path}: oracle mapping missing={missing}, extra={extra}")
		for address, expected in values.items():
			provenance.append({"scenario": case["scenario"], "address": address,
				"source_line": formulas[address]["line"], "expected": expected["value"]})
	result = {"tutorial": str(document.path), "scenario_count": len(cases),
		"formula_checks": len(provenance), "mapping_status": "passed", "outputs": provenance}
	return result


#============================================
def check_caffeine_release(documents: list[tutorial_lib.model.Document]) -> dict:
	"""Verify the three Caffeine Parts as one completed shared workbook."""
	workbook = tutorial_lib.build.merge_documents(documents)
	values = tutorial_oracles.caffeine_release(workbook)
	item = {"common": expectations(values, tutorial_oracles.analysis_sheet(workbook).name), "scenarios": {}}
	result = check_mapping(workbook, item)
	result["tutorial"] = "shared Caffeine release"
	return result


#============================================
def main() -> int:
	args = parse_args()
	paths = sorted(pathlib.Path("tutorial_data").glob("*.md"))
	if not paths:
		raise ValueError("No tutorial sources found")
	payload, details = {"tutorials": {}}, []
	documents = {}
	for path in paths:
		document = tutorial_lib.compiler.compile_document(path)
		if document.has_errors:
			raise ValueError(f"Cannot validate invalid tutorial {path}")
		documents[path.name] = document
		common, scenarios = tutorial_oracles.calculate(document)
		sheet = tutorial_oracles.analysis_sheet(document).name
		item = {"common": expectations(common, sheet), "scenarios": {
			name: expectations(values, sheet) for name, values in scenarios.items()}}
		payload["tutorials"][path.name] = item
		details.append(check_mapping(document, item))
	caffeine_names = ("caffeine_1_descriptive_statistics.md", "caffeine_2_linear_regression.md",
		"caffeine_3_quadratic_regression.md")
	shared_releases = []
	if all(name in documents for name in caffeine_names):
		shared_releases.append(check_caffeine_release([documents[name] for name in caffeine_names]))
	checks = synthetic_direction_checks()
	report = {"status": "independent_expectations_generated", "sheets_status": "not_executed",
		"tutorial_count": len(details), "scenario_count": sum(d["scenario_count"] for d in details),
		"formula_checks": sum(d["formula_checks"] for d in details),
		"shared_releases": shared_releases,
		"synthetic_direction_checks": checks, "tutorials": details,
		"method": "SciPy probability/test APIs and NumPy SVD/QR models from compiled numeric seeds; "
			"authored formula strings never enter numerical calculations"}
	args.output.mkdir(parents=True, exist_ok=True)
	for name, value in (("tutorial_expectations.json", payload), ("independent_oracles.json", report)):
		(args.output / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
	print(f"Generated {report['tutorial_count']} tutorials, {report['scenario_count']} scenarios, "
		f"{report['formula_checks']} formula expectations, {len(checks)} synthetic direction checks")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
