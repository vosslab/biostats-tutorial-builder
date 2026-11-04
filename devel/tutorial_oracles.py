"""Independent statistical models for the migrated teaching datasets.

Cell locations are explicit teaching contracts, never inferred from formula text.
Only seed numbers and numeric parameter assignments enter the calculations.
"""

import math
import dataclasses
import pathlib

import numpy
import scipy.stats

import tutorial_lib.model
import tutorial_lib.references


#============================================
def analysis_sheet(document: tutorial_lib.model.Document) -> tutorial_lib.model.Worksheet:
	"""Select the last analysis worksheet, excluding generated response sheets."""
	sheet = next(sheet for sheet in reversed(document.worksheets) if not sheet.is_reflection)
	return sheet


#============================================
def observations(sheet: tutorial_lib.model.Worksheet, column: int,
	start: int = 2, end: int = 101) -> numpy.ndarray:
	"""Read numeric observations, ignoring the workbook's deliberately empty rows."""
	values = [seed.scalar.value for (row, col), seed in sorted(sheet.cells.items())
		if col == column and start <= row <= end and seed.scalar.kind == "number"]
	result = numpy.array(values, dtype=float)
	if len(result) < 2 or not numpy.isfinite(result).all():
		raise ValueError(f"Invalid observations in {sheet.name}, column {column}")
	return result


#============================================
def parameter(document: tutorial_lib.model.Document, address: str) -> float:
	values = [a.scalar.value for a in document.actions if a.target is not None
		and a.target.address == address and a.scalar is not None and a.scalar.kind == "number"]
	if len(values) != 1:
		raise ValueError(f"Expected one numeric parameter at {address}")
	return float(values[0])


#============================================
def decision(p_value: float, alpha: float) -> str:
	result = "Reject the Null Hypothesis" if p_value <= alpha else "Fail to Reject the Null Hypothesis"
	return result


#============================================
def tails(statistic: float, degrees: float | None = None) -> tuple[float, float, float]:
	distribution = scipy.stats.norm if degrees is None else scipy.stats.t(degrees)
	lower = float(distribution.cdf(statistic))
	higher = float(distribution.sf(statistic))
	two = float(2 * distribution.sf(abs(statistic)))
	return two, lower, higher


#============================================
def one_sample(document: tutorial_lib.model.Document) -> dict:
	is_baby = document.path.name.startswith("babies")
	is_z = "z_test" in document.path.name
	alpha_cell = ("E14" if is_z else "E15") if is_baby else "D14"
	alpha = parameter(document, alpha_cell)
	sheet = analysis_sheet(document)
	x = observations(sheet, 2, end=40 if is_baby and is_z else 101)
	n, mean, sd = len(x), float(numpy.mean(x)), float(numpy.std(x, ddof=1))
	mu = parameter(document, "E2" if is_baby else "D2")
	if is_z:
		sigma = parameter(document, "E3" if is_baby else "D3")
		statistic = (mean - mu) / (sigma / math.sqrt(n))
	else:
		statistic = float(scipy.stats.ttest_1samp(x, mu).statistic)
	two, lower, higher = tails(statistic, None if is_z else n - 1)
	if is_baby:
		result = {"E5": n, "E6": mean, "E7": sd, "E9": statistic}
		if is_z:
			result.update(E11=two, E12=higher, E16=decision(two, alpha), E17=decision(higher, alpha))
		else:
			result.update(E10=n - 1, E12=two, E13=higher,
				E17=decision(two, alpha), E18=decision(higher, alpha))
	else:
		result = {"D6": n, "D8": statistic, "D10": two, "D11": lower, "D12": higher,
			"D15": decision(two, alpha), "D16": decision(lower, alpha),
			"D17": decision(higher, alpha)}
		if is_z:
			result["D5"] = mean
		else:
			result.update(D4=mean, D5=sd, D9=n - 1, E10=two, E12=higher)
	return result


#============================================
def two_sample(document: tutorial_lib.model.Document) -> tuple[dict, dict]:
	sheet = analysis_sheet(document)
	x, y = observations(sheet, 2), observations(sheet, 3)
	if document.path.name.startswith("babies"):
		alpha = parameter(document, "G6")
		test = scipy.stats.ttest_ind(x, y, equal_var=False)
		two, _, higher = tails(float(test.statistic), float(test.df))
		common = {"G2": float(x.mean()), "H2": float(y.mean()),
			"G3": float(x.std(ddof=1)), "H3": float(y.std(ddof=1)),
			"G4": len(x), "H4": len(y)}
		scenarios = {"baseline": {"G5": two, "G7": decision(two, alpha)},
			"group-1-branch-2": {"G5": higher, "G7": decision(higher, alpha)}}
	else:
		alpha = parameter(document, "E21")
		# The course defines 2024 minus 2014: y is the first argument.
		test = scipy.stats.ttest_ind(y, x, equal_var=False)
		two, lower, higher = tails(float(test.statistic), float(test.df))
		common = {"E2": float(x.mean()), "E3": float(y.mean()),
			"E5": float(x.std(ddof=1)), "E6": float(y.std(ddof=1)),
			"E8": len(x), "E9": len(y), "E11": float(test.statistic), "E13": float(test.df),
			"E16": two, "F16": two, "G16": two, "E17": lower, "G17": lower,
			"E18": higher, "F18": higher, "G18": higher,
			"E22": decision(two, alpha), "E23": decision(lower, alpha),
			"E24": decision(higher, alpha)}
		scenarios = {}
	return common, scenarios


#============================================
def variance_test(document: tutorial_lib.model.Document) -> dict:
	alpha = parameter(document, "E20")
	x, y = [observations(analysis_sheet(document), col) for col in (2, 3)]
	ratio = float(y.var(ddof=1) / x.var(ddof=1))
	distribution = scipy.stats.f(len(y) - 1, len(x) - 1)
	lower, higher = float(distribution.cdf(ratio)), float(distribution.sf(ratio))
	two = min(1., 2 * min(lower, higher))
	result = {"E5": float(x.std(ddof=1)), "E6": float(y.std(ddof=1)),
		"E8": len(x), "E9": len(y), "E11": ratio, "E13": len(x) - 1,
		"E14": len(y) - 1, "E16": two, "G16": two, "E17": lower, "G17": lower,
		"E18": higher, "F18": higher, "G18": higher, "E22": decision(two, alpha),
		"E23": decision(lower, alpha), "E24": decision(higher, alpha)}
	return result


#============================================
def anova(document: tutorial_lib.model.Document) -> dict:
	alpha = parameter(document, "I13")
	groups = [observations(analysis_sheet(document), col) for col in range(2, 7)]
	all_values = numpy.concatenate(groups)
	grand = float(all_values.mean())
	# Center raw observations, independently of the sheet's summary-table SUMPRODUCT.
	within = sum(float(numpy.dot(g - g.mean(), g - g.mean())) for g in groups)
	total = float(numpy.dot(all_values - grand, all_values - grand))
	between = total - within
	dfb, dfw = len(groups) - 1, len(all_values) - len(groups)
	test = scipy.stats.f_oneway(*groups)
	result = {"I11": grand, "I2": dfb, "I3": dfw, "I4": len(all_values) - 1,
		"J2": between, "J3": within, "J4": total, "K2": between / dfb,
		"K3": within / dfw, "L2": float(test.statistic), "M2": float(test.pvalue),
		"I14": decision(float(test.pvalue), alpha)}
	for index, group in enumerate(groups):
		column = tutorial_lib.references.column_letters(9 + index)
		result.update({column + "7": float(group.mean()),
			column + "8": float(group.var(ddof=1)), column + "9": len(group)})
	return result


#============================================
def regression(x: numpy.ndarray, y: numpy.ndarray, degree: int) -> dict:
	"""Fit the design with SVD least squares; covariance follows the QR factor."""
	design = numpy.vander(x, degree + 1, increasing=True)
	beta = numpy.linalg.lstsq(design, y, rcond=None)[0]
	residual = y - design @ beta
	df = len(y) - design.shape[1]
	sse = float(residual @ residual)
	_, upper = numpy.linalg.qr(design)
	inverse = numpy.linalg.solve(upper, numpy.eye(len(beta)))
	se = numpy.sqrt(numpy.diag(inverse @ inverse.T) * sse / df)
	r_squared = 1 - sse / float((y - y.mean()) @ (y - y.mean()))
	result = {"beta": beta, "se": se, "df": df, "r_squared": r_squared}
	return result


#============================================
def caffeine(document: tutorial_lib.model.Document) -> dict:
	shared_sheets = {sheet.name for sheet in document.worksheets}
	if {"Data", "Sample Mean", "Linear Regression", "Quadratic Regression"} <= shared_sheets:
		data = next(sheet for sheet in document.worksheets if sheet.name == "Data")
		x, y = [observations(data, col, end=26) for col in (1, 2)]
		linear = regression(x, y, 1)
		intercept, slope = map(float, linear["beta"])
		linear_se = float(linear["se"][1])
		linear_statistic = slope / linear_se
		quadratic = regression(x, y, 2)
		b0, b1, b2 = map(float, quadratic["beta"])
		quadratic_se = float(quadratic["se"][2])
		quadratic_statistic = b2 / quadratic_se
		if "descriptive" in document.path.name:
			return {
			"Sample Mean!E2": float(x.mean()), "Sample Mean!F2": float(y.mean()),
			"Sample Mean!E3": float(numpy.median(x)), "Sample Mean!F3": float(numpy.median(y)),
			"Sample Mean!E4": float(x.std(ddof=1)), "Sample Mean!F4": float(y.std(ddof=1)),
			}
		if "2_linear" in document.path.name:
			return {
			"Linear Regression!E2": slope, "Linear Regression!E6": intercept,
			"Linear Regression!E10": linear["r_squared"],
			"Linear Regression!E14": intercept + slope * 7,
			"Linear Regression!H2": slope, "Linear Regression!H3": linear_se,
			"Linear Regression!H5": linear["df"],
			"Linear Regression!K2": linear_statistic, "Linear Regression!K6": linear["df"],
			"Linear Regression!K10": tails(linear_statistic, linear["df"])[0],
			}
		result = {
			"Quadratic Regression!N2": slope, "Quadratic Regression!N3": intercept,
			"Quadratic Regression!N4": linear["r_squared"],
			"Quadratic Regression!I2": b2, "Quadratic Regression!I3": b1,
			"Quadratic Regression!I4": b0, "Quadratic Regression!I5": quadratic["r_squared"],
			"Quadratic Regression!I6": quadratic_se, "Quadratic Regression!I7": quadratic["df"],
			"Quadratic Regression!I8": b0 + b1 * 7 + b2 * 49,
			"Quadratic Regression!I10": quadratic_statistic,
			"Quadratic Regression!I11": tails(quadratic_statistic, quadratic["df"])[0],
		}
		for row, value in enumerate(x, 2):
			result.update({f"Quadratic Regression!C{row}": float(value ** 2),
				f"Quadratic Regression!E{row}": float(value),
				f"Quadratic Regression!F{row}": float(value ** 2)})
		return result
	x, y = [observations(analysis_sheet(document), col, end=26) for col in (1, 2)]
	if "descriptive" in document.path.name:
		result = {"E2": float(x.mean()), "F2": float(y.mean()),
			"E3": float(numpy.median(x)), "F3": float(numpy.median(y)),
			"E4": float(x.std(ddof=1)), "F4": float(y.std(ddof=1))}
		return result
	linear = regression(x, y, 1)
	intercept, slope = map(float, linear["beta"])
	if "2_linear" in document.path.name:
		se = float(linear["se"][1])
		statistic = slope / se
		result = {"E2": slope, "E6": intercept, "E10": linear["r_squared"],
			"E14": intercept + slope * 7, "H2": slope, "H3": se, "H5": linear["df"],
			"K2": statistic, "K6": linear["df"],
			"K10": tails(statistic, linear["df"])[0]}
	else:
		quadratic = regression(x, y, 2)
		b0, b1, b2 = map(float, quadratic["beta"])
		se = float(quadratic["se"][2])
		statistic = b2 / se
		result = {"M2": slope, "M3": intercept, "M4": linear["r_squared"],
			"I2": b2, "I3": b1, "I4": b0, "I5": quadratic["r_squared"], "I6": se,
			"I7": quadratic["df"], "I8": b0 + b1 * 7 + b2 * 49,
			"I10": statistic, "I11": tails(statistic, quadratic["df"])[0]}
		for row, value in enumerate(x, 2):
			result.update({f"C{row}": float(value ** 2), f"E{row}": float(value),
				f"F{row}": float(value ** 2)})
	return result


#============================================
def caffeine_release(document: tutorial_lib.model.Document) -> dict:
	"""Return every Caffeine Part oracle for one merged shared workbook."""
	result = {}
	for name in ("caffeine_1_descriptive_statistics.md", "caffeine_2_linear_regression.md",
		"caffeine_3_quadratic_regression.md"):
		part = dataclasses.replace(document, path=pathlib.Path(name))
		result.update(caffeine(part))
	return result


#============================================
def petase(document: tutorial_lib.model.Document) -> dict:
	sheet = analysis_sheet(document)
	x, raw = [observations(sheet, col, end=8) for col in (1, 2)]
	y = raw - raw[0]
	fit = regression(x, y, 1)
	intercept, slope = map(float, fit["beta"])
	result = {"G2": slope, "G3": intercept, "G4": fit["r_squared"]}
	for row, concentration, absorbance in zip(range(2, 9), x, y):
		fitted = intercept + slope * concentration
		result.update({f"C{row}": float(absorbance), f"I{row}": float(fitted),
			f"J{row}": float(absorbance - fitted)})
	for row in range(13, 16):
		absorbance, dilution, volume = [float(sheet.cells[row, col].scalar.value)
			for col in (2, 3, 4)]
		concentration = (absorbance - raw[0] - intercept) / slope
		result.update({f"E{row}": concentration, f"F{row}": concentration * dilution,
			f"G{row}": concentration * dilution * volume})
	return result


#============================================
def calculate(document: tutorial_lib.model.Document) -> tuple[dict, dict]:
	"""Dispatch explicit curriculum models; unknown lessons fail instead of being skipped."""
	name = document.path.name
	scenarios = {}
	if "two_sample_t_test" in name:
		common, scenarios = two_sample(document)
	elif name.startswith("caffeine_"):
		common = caffeine(document)
	elif name == "petase_1_linear_regression.md":
		common = petase(document)
	elif name == "microbes_4_f_test.md":
		common = variance_test(document)
	elif name == "microbes_5_anova.md":
		common = anova(document)
	elif name in ("babies_1_z_test.md", "babies_2_t_test.md",
		"microbes_1_z_test.md", "microbes_2_t_test.md"):
		common = one_sample(document)
	else:
		raise ValueError(f"No independent statistical model for {name}")
	return common, scenarios
