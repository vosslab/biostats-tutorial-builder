# Exploring root lengths

Describe the center and spread of root lengths in a small practice dataset.
These invented measurements represent separate seedlings measured once in millimeters.
They are for learning spreadsheet skills; they provide no evidence about real plants.

## Workbook

### Sheet: Roots

| Root length (mm) |
| --- |
| 12 |
| 15 |
| 18 |
| 20 |
| 25 |

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
- **Select:** `A2:A6`
- **Compare:** Find the shortest and longest root lengths. Both describe individual roots.
- **Explain:** Tell a classmate what one row represents and what the unit means.
- **Read:** Summary headings are in `D1:E1`; the three Value cells start empty.

### Part: Summarize root lengths

- **Worksheet:** Roots

#### Step: Count the observations

- **Read:** Sample size is the number of numerical observations, not their sum.
- **Calculate:** In cell E2, enter [`=COUNT(A2:A6)`](enter:E2).
- **Check:** Compare the result with the number of supplied root lengths.

#### Step: Calculate the mean

- **Read:** The arithmetic mean adds the root lengths and divides by the sample size.
- **Calculate:** In cell E3, enter [`=AVERAGE(A2:A6)`](enter:E3).
- **Explain:** The mean describes the center of these observations in millimeters.
