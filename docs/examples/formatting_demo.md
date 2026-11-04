# Formatting demo: squared sleep hours

This short lesson shows how ordinary ASCII Markdown becomes a polished tutorial and a labeled
student workbook. Students calculate the blank values; the worksheet already names each column.

## Workbook

### Sheet: Sleep and scores

| Hours of sleep | Exam score | Sleep hours squared |
| --- | --- | --- |
| 5 | 72 | |
| 7 | 88 | |
| 9 | 81 | |

- **Region A1:B4:** source
- **Region C1:C4:** calculation

#### At: E1

| Model feature | Why it matters |
| --- | --- |
| Linear term | Describes a steady change. |
| Squared term | Allows a curved relationship. |

### Reflection Questions

1. Why can a squared sleep-hours term describe a pattern that a straight-line model misses?

## Tutorial

### Part: Explore a curved relationship

- **Worksheet:** Sleep and scores

The data suggest that exam performance may rise and then fall as sleep changes. A squared predictor
lets a regression model describe that curve without changing the original observations.

#### Step: Inspect the observations

1. Read the supplied headings before changing the worksheet.
   - The first two columns contain the observations.
   - The third column is blank because you will construct its calculation.
2. Notice that the predictor is called **hours of sleep**, not *sleep quality*.

##### Explanation: Why square a value?

If a student sleeps 6 hours, squaring the value gives 36. The `^2` tells a spreadsheet to multiply
the value by itself. In a regression equation, the squared term can have coefficient &alpha; while
the ordinary sleep-hours term has its own coefficient.

#### Step: Calculate squared sleep hours

1. In cell C2, enter:
   [`=A2^2`](enter:C2)
2. [Fill C2:C4](fill:C2:C4) down to calculate the remaining rows.
3. Check that the value beside 9 hours of sleep is 81.

##### Explanation: Read a formula before copying it

The formula uses A2 because it refers to the sleep-hours value in the same row. Filling down changes
the row reference for each observation, so C3 uses A3 and C4 uses A4.

#### Step: Compare the model features

Use this table to record the purpose of each term after you have discussed the regression model.

| Model feature | What to record |
| --- | --- |
| Linear term | How the response changes in a straight-line model. |
| Squared term | How the curve bends as sleep changes. |

