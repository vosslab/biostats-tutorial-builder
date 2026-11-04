# Descriptive statistics: exam scores

Describe the center and spread of the exam scores supplied in the original descriptive-statistics
workbook. Compare your summary before and after excluding scores below 60.

## Workbook

### Sheet: Exam scores

| Exam score | Scores 60 and above |
| --- | --- |
| 99 | |
| 98 | |
| 94 | |
| 94 | |
| 92 | |
| 92 | |
| 92 | |
| 90 | |
| 89 | |
| 88 | |
| 88 | |
| 86 | |
| 85 | |
| 84 | |
| 84 | |
| 82 | |
| 82 | |
| 81 | |
| 79 | |
| 76 | |
| 71 | |
| 68 | |
| 67 | |
| 62 | |
| 61 | |
| 58 | |
| 57 | |
| 55 | |
| 49 | |
| 32 | |

#### At: D1

| Statistic | Original scores | Scores 60 and above |
| --- | --- | --- |
| Count | | |
| Mean | | |
| Median | | |
| Mode | | |
| Population standard deviation | | |

- **Region A1:A31:** source
- **Region B1:B31:** calculation
- **Region D1:F6:** results

### Reflection Questions

1. Which measure do you think best represents the center of the data: the mean, median, or mode? Justify your choice based on the data.
2. Observe the histogram and describe the overall shape of the data distribution. Would you describe the histogram as symmetric or skewed? What does this tell you about the exam scores?
3. If a few very high or very low exam scores were added to the data set, how would you expect the mean and median to change? Which measure is more sensitive to these changes and why?
4. What customization did you make to the Histogram figure, and why did you choose it?
5. How did removing these low scores affect each of these measures? What does this tell you about the sensitivity of these statistics to changes in the data set, and which measure(s) are more robust to such changes?

## Tutorial

### Part: Summarize exam scores

- **Worksheet:** Exam scores

#### Step: Calculate the original summaries

1. In cell E2, enter [`=COUNT(A2:A31)`](enter:E2).
2. In cell E3, enter [`=AVERAGE(A2:A31)`](enter:E3).
3. In cell E4, enter [`=MEDIAN(A2:A31)`](enter:E4).
4. In cell E5, enter [`=MODE.SNGL(A2:A31)`](enter:E5).
5. In cell E6, enter [`=STDEV.P(A2:A31)`](enter:E6).

Use population standard deviation here to describe this supplied set of scores.

#### Step: Examine the distribution

1. [Select A1:A31](select:A1:A31).
2. Insert a histogram in your spreadsheet application and label the exam-score axis.
3. Choose a bin width that helps you see the shape, then record and explain your customization.

#### Step: Compare after excluding low scores

1. In cell B2, enter [`=IF(A2>=60,A2,"")`](enter:B2).
2. [Fill B2:B31](fill:B2:B31) down. Blank results exclude scores below 60 while retaining the original data.
3. In cell F2, enter [`=COUNT(B2:B31)`](enter:F2).
4. In cell F3, enter [`=AVERAGE(B2:B31)`](enter:F3).
5. In cell F4, enter [`=MEDIAN(B2:B31)`](enter:F4).
6. In cell F5, enter [`=MODE.SNGL(B2:B31)`](enter:F5).
7. In cell F6, enter [`=STDEV.P(B2:B31)`](enter:F6).

Compare columns E and F, then answer all five reflection questions.
