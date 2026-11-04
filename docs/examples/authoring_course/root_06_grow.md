# Exploring root lengths

Describe center and spread using invented root lengths of separate seedlings measured once in mm.
These practice data teach spreadsheet skills and provide no evidence about real plants.

## Workbook

### Sheet: Roots

| Root length (mm) | Deviation from mean (mm) |
| --- | --- |
| 12 | |
| 15 | |
| 18 | |
| 20 | |
| 25 | |
| 30 | |

#### At: D1

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
- **Select:** `A2:A7`
- **Compare:** Find the shortest and longest root lengths. Both describe individual roots.
- **Explain:** Tell a classmate what one row represents and what the unit means.
- **Read:** Summary headings are in `D1:E1`; the three Value cells start empty.

### Part: Summarize root lengths

- **Worksheet:** Roots

#### Step: Count the observations

- **Read:** Sample size is the number of numerical observations, not their sum.
- **Calculate:** In cell E2, enter [`=COUNT(A2:A7)`](enter:E2).
- **Check:** Compare the result with the number of supplied root lengths.

#### Step: Calculate the mean

- **Read:** The arithmetic mean adds the root lengths and divides by the sample size.
- **Calculate:** In cell E3, enter [`=AVERAGE(A2:A7)`](enter:E3).
- **Explain:** The mean describes the center of these observations in millimeters.

#### Step: Describe the spread

- **Read:** Sample standard deviation describes spread around the mean in millimeters.
  Use `STDEV.S`; its calculation uses the number of observations minus one.
- **Calculate:** In cell E4, enter [`=STDEV.S(A2:A7)`](enter:E4).
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
- **Calculate:** In cell B2, enter [`=A2-$E$3`](enter:B2).
- **Read:** The dollar signs keep the reference to the mean fixed when you fill down.
- **Extend:** [Fill down through B7](fill:B2:B7).
- **Check:** The root equal to the mean has a deviation of zero.
- **Explain:** Ordinary deviations can cancel when added. Standard deviation avoids
  cancellation by using squared deviations in its calculation.
