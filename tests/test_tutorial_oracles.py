"""Protect direction and polynomial coefficient inference in independent oracles."""

import math

import numpy
import pytest

import tutorial_oracles


#============================================
def test_signed_tails_preserve_research_direction() -> None:
	"""A negative statistic must give a large right tail, including for student t."""
	for degrees in (None, 12):
		negative = tutorial_oracles.tails(-2., degrees)
		positive = tutorial_oracles.tails(2., degrees)
		assert negative[2] > .95
		assert negative == pytest.approx((positive[0], positive[2], positive[1]))
		assert negative[0] == pytest.approx(2 * negative[1])


#============================================
def test_quadratic_coefficient_order_and_standard_error() -> None:
	"""Prevent reversing LINEST predictor coefficients or using the wrong covariance."""
	x = numpy.array([-2., -1., 0., 1., 2.])
	# The residual is orthogonal to the intercept, x and x squared.
	y = numpy.array([9.1, 1.6, 1.6, 5.6, 17.1])
	result = tutorial_oracles.regression(x, y, 2)
	assert result["beta"] == pytest.approx([1., 2., 3.])
	assert result["df"] == 2
	assert result["se"][2] == pytest.approx(math.sqrt(.025))


def test_observations_follow_capacity_and_preserve_pair_alignment() -> None:
	"""A gap or incomplete pair must not shift one regression variable against another."""
	import tutorial_lib.compiler
	source = "# Example\n\n## Workbook\n\n### Sheet: Data\n\n"
	source += "| x | y |\n| --- | --- |\n| 1 | 2 |\n| | |\n| 3 | 4 |\n"
	source += "| 5 | |\n| 7 | 8 |\n| 9 | 10 |\n\n- **Region A1:B100:** source\n"
	source += "\n### Reflection Questions\n\n1. What changed?\n\n## Tutorial\n"
	source += "\n### Part: Analysis\n\n#### Step: Calculate\n\n- **Enter D2:** =COUNT(A2:A100)\n"
	document = tutorial_lib.compiler.compile_source(source)
	x, y = tutorial_oracles.paired_observations(document.worksheets[0])
	assert x.tolist() == [1, 3, 7, 9]
	assert y.tolist() == [2, 4, 8, 10]
	assert len(tutorial_oracles.observations(document.worksheets[0], 1)) == 5
