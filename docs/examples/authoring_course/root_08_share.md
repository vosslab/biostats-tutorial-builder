# Exploring root lengths

Describe center and spread using invented root lengths of separate seedlings measured once in mm.
These practice data teach spreadsheet skills and provide no evidence about real plants.

## Workbook

### Sheet: Roots

#### At: B1

| Root length (mm) | Deviation from mean (mm) |
| --- | --- |
| 12 | |
| 15 | |
| 18 | |
| 20 | |
| 25 | |
| 30 | |

#### At: E1

| Statistic | Value |
| --- | --- |
| Sample size | |
| Mean (mm) | |
| Sample standard deviation (mm) | |

### Reflection Questions

1. What does one root-length observation represent, and what can these invented data tell you about real plants?

## Tutorial

### Part: Explore the observations

- **Worksheet:** Roots

#### Step: Inspect the supplied data

- **Read:** Each number is one invented root length in millimeters.
- **Select:** `B2:B7`
- **Compare:** Find the shortest and longest root lengths. Both describe individual roots.
- **Explain:** Tell a classmate what one row represents and what the unit means.
- **Read:** Summary headings are in `E1:F1`; the three Value cells start empty.

### Part: Summarize root lengths

- **Worksheet:** Roots

#### Step: Count the observations

- **Read:** Sample size is the number of numerical observations, not their sum.
- **Calculate:** In cell F2, enter [`=COUNT(B2:B7)`](enter:F2).
- **Check:** Compare the result with the number of supplied root lengths.

#### Step: Calculate the mean

- **Read:** The arithmetic mean adds the root lengths and divides by the sample size.
- **Calculate:** In cell F3, enter [`=AVERAGE(B2:B7)`](enter:F3).
- **Explain:** The mean describes the center of these observations in millimeters.

#### Step: Describe the spread

- **Read:** Sample standard deviation describes spread around the mean in millimeters.
  Use `STDEV.S`; its calculation uses the number of observations minus one.
- **Calculate:** In cell F4, enter [`=STDEV.S(B2:B7)`](enter:F4).
- **Check:** Display three decimal places; keep full stored precision.
- **Explain:** Describe mean and SD together: center and spread among root lengths.
  SD is neither sample size nor the accuracy of an individual measurement.

### Part: Examine individual deviations

- **Worksheet:** Roots

The practice dataset now includes one additional invented root length of 30 mm.
The summary formulas include all six observations. Calculate the mean before deviations.

#### Step: Subtract the mean

- **Read:** A deviation is an individual root length minus the mean. A negative value
  marks a root shorter than the mean; a positive value marks a root longer than the mean.
- **Calculate:** In cell C2, enter [`=B2-$F$3`](enter:C2).
- **Read:** The dollar signs keep the reference to the mean fixed when you fill down.
- **Extend:** [Fill down through C7](fill:C2:C7).
- **Check:** The root equal to the mean has a deviation of zero.
- **Explain:** Ordinary deviations can cancel when added. Standard deviation avoids
  cancellation by using squared deviations in its calculation.

### Part: Check with a classmate

- **Worksheet:** Roots

#### Step: Review a fresh workbook

- **Share:** Give a classmate the tutorial and a fresh copy of its starting workbook.
  Ask them to follow the instructions without advice while you note where they pause.
- **Check:** Confirm that the supplied headings and row labels are present before they begin,
  and that the summary and deviation work cells start blank.

#### Step: Compare results and meaning

- **Check:** After completing the instructions, your classmate should obtain sample size 6,
  mean 20.000 mm, and sample standard deviation 6.603 mm.
- **Check:** The first deviation should be -8.000 mm and the last should be 10.000 mm.
- **Explain:** Ask your classmate what a negative deviation means and whether the standard
  deviation measures spread among roots or the accuracy of the ruler.
- **Revise:** Improve any unclear wording in the Markdown source, then rebuild both files.
  Keep the measurements described as invented; this exercise supports no biological claim.
