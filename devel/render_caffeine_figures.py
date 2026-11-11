#!/usr/bin/env python3
"""Regenerate the Caffeine data figures from the canonical paired observations."""

# Standard Library
import pathlib
import subprocess

# PIP3 modules
import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot

# Local modules
import tutorial_lib.compiler
import tutorial_oracles


#============================================
def main() -> None:
	"""Fit both models to the same data and save legible, proportionally sized figures."""
	repository = pathlib.Path(subprocess.check_output(
		["git", "rev-parse", "--show-toplevel"], text=True).strip())
	root = repository / "tutorial_data" / "caffeine"
	document = tutorial_lib.compiler.compile_document(root / "caffeine_3_quadratic_regression.md")
	if document.has_errors:
		raise ValueError(f"Cannot plot invalid tutorial: {document.diagnostics}")
	sheet = next(sheet for sheet in document.worksheets if sheet.name == "Quadratic Regression")
	x, y = tutorial_oracles.paired_observations(sheet)
	if not (numpy.isfinite(x).all() and numpy.isfinite(y).all()):
		raise ValueError("Caffeine observations must be finite numbers")
	curve_x = numpy.linspace(x.min(), x.max(), 300)
	matplotlib.pyplot.rcParams.update({"font.size": 15, "axes.labelsize": 17,
		"xtick.labelsize": 14, "ytick.labelsize": 14})
	for comparison in (False, True):
		figure, axes = matplotlib.pyplot.subplots(1, 2 if comparison else 1,
			figsize=(8.5, 3.8) if comparison else (6.5, 3.8), layout="constrained",
			sharex=True, sharey=True, squeeze=False)
		for index, axis in enumerate(axes.flat):
			axis.set_axisbelow(True)
			axis.grid(color="#d9dee5", linewidth=0.6, zorder=0)
			axis.scatter(x, y, s=38, color="#0067cc", edgecolor="white",
				linewidth=0.6, zorder=3)
			axis.set_xlabel("Sleep (hours)")
			axis.set_xticks([3, 5, 7, 9, 11])
			axis.set_yticks([60, 70, 80, 90, 100])
			if index == 0:
				axis.set_ylabel("Exam score (%)")
			if comparison:
				coefficients = numpy.polyfit(x, y, index + 1)
				predicted = numpy.polyval(coefficients, x)
				r_squared = 1 - numpy.sum((y - predicted) ** 2) / numpy.sum((y - y.mean()) ** 2)
				if not 0 <= r_squared <= 1:
					raise ValueError(f"Fitted R-squared is outside 0 to 1: {r_squared}")
				axis.plot(curve_x, numpy.polyval(coefficients, curve_x),
					color="#b74300", linewidth=2.2, zorder=2)
				label = "Linear fit" if index == 0 else "Quadratic fit"
				axis.text(0.04, 0.96, f"{label}\n$R^2 = {r_squared:.3f}$",
					transform=axis.transAxes, va="top", fontsize=15,
					bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9})
		name = "model_comparison" if comparison else "scatter"
		figure.savefig(root / "assets" / f"caffeine_sleep_score_{name}.png", dpi=250)
		matplotlib.pyplot.close(figure)


if __name__ == "__main__":
	main()
