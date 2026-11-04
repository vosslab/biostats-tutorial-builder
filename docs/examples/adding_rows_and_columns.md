# Adding a column and an observation

Compare sleep hours with a reference value of 7 hours. Keep the original observations and calculate
both squared sleep hours and the difference from 7 hours.

## Workbook

### Sheet: Sleep and scores

| Hours of sleep | Exam score | Sleep hours squared | Hours minus 7 |
| --- | --- | --- | --- |
| 5 | 72 | | |
| 7 | 88 | | |
| 9 | 81 | | |
| 6 | 79 | | |

- **Region A1:B5:** source
- **Region C1:D5:** calculation

### Reflection Questions

1. Why is the difference from 7 negative for 6 hours of sleep, while squared sleep hours is positive?

## Tutorial

### Part: Calculate two predictors

- **Worksheet:** Sleep and scores

The worksheet supplies the headings and observations. You will calculate the two blank columns.

#### Step: Square the sleep hours

1. In cell C2, enter:
   [`=A2^2`](enter:C2)
2. [Fill C2:C5](fill:C2:C5) down to include all four observations.
3. Check that 6 hours gives 36 in C5.

#### Step: Compare with 7 hours

1. In cell D2, enter:
   [`=A2-7`](enter:D2)
2. [Fill D2:D5](fill:D2:D5) down to include all four observations.
3. Explain why the value in D5 is negative.
