# **"Joe's Hospital of Fried Foods" vs. National Average**

**T-Test Tutorial for BIOL 318/418**

![][image1]

A **T-test** is a statistical test used when you want to know if the average of your sample is
meaningfully different from a known value, but you cannot assume the population standard deviation
is known. Instead, it uses the sample's own standard deviation and adjusts for smaller sample sizes
through the t-distribution. The result is a t test statistic, which tells you how far the sample
mean is from the hypothesized population mean in units of estimated standard error. Because it
accounts for added uncertainty, the t-test is appropriate when population variability is estimated
from the sample. Small samples also require attention to independence, approximate normality, and
outliers.

## Workbook

### Sheet: Datas for Part 1 and 2

| Infant<br>Number | Birth Weight<br>(pounds) |
| --- | --- |
| 1 | 9.56 |
| 2 | 7.88 |
| 3 | 7.22 |
| 4 | 8.02 |
| 5 | 7.43 |
| 6 | 9.91 |
| 7 | 6.84 |
| 8 | 9.95 |
| 9 | 9.53 |
| 10 | 8.25 |
| 11 | 6.14 |
| 12 | 6.43 |
| 13 | 9.27 |
| 14 | 6.46 |
| 15 | 5.83 |
| 16 | 5.62 |
| 17 | 7.01 |
| 18 | 6.29 |
| 19 | 9.36 |
| 20 | 7.35 |
| 21 | 9.54 |
| 22 | 6.61 |
| 23 | 9.72 |
| 24 | 7.17 |

- **Region A1:B25:** source

### Sheet: Part 2 National T-Test

| Infant<br>Number | Birth Weight<br>(pounds) |
| --- | --- |
| 1 | 9.56 |
| 2 | 7.88 |
| 3 | 7.22 |
| 4 | 8.02 |
| 5 | 7.43 |
| 6 | 9.91 |
| 7 | 6.84 |
| 8 | 9.95 |
| 9 | 9.53 |
| 10 | 8.25 |
| 11 | 6.14 |
| 12 | 6.43 |
| 13 | 9.27 |
| 14 | 6.46 |
| 15 | 5.83 |
| 16 | 5.62 |
| 17 | 7.01 |
| 18 | 6.29 |
| 19 | 9.36 |
| 20 | 7.35 |
| 21 | 9.54 |
| 22 | 6.61 |
| 23 | 9.72 |
| 24 | 7.17 |

#### At: D1

| Statistical Names | Statistical Values |
| --- | --- |

- **Region A1:B25:** source
- **Region D1:E10:** calculation
- **Region D12:E18:** results
- **Region D20:E20:** interpretation

#### At: E3

| not used |
| --- |

### Reflection Questions

1. Discuss when the t-test results start to resemble the z-test.
2. Discuss how the flexibility in sample size affects the results of the t-test and compare this to their earlier z-test results.

## Tutorial

### Part: Scenario

- **Worksheet:** Part 2 National T-Test

There are 24 supplied weights in rows 2-25. The formulas deliberately allow additions through
row 101, ignoring blank cells. Use independent observations from an approximately normal population
for this small-sample model; neither a t-test nor a z-test fixes biased sampling.

#### The New Challenge: Prove It with a One-Sample T-Test

The awards committee has pointed out that Joe's approach wasn't entirely sound. They raised two key issues:

1. Assumed Population Standard Deviation - Joe can no longer assume the national standard deviation
   applies, given the variation in practices across hospitals.
2. Small Sample Size - Joe has only 24 observations. For a small sample, check approximate normality
   and influential outliers; sample size alone does not invalidate a z-test.

#### The New Scenario: Enter the T-Test

Joe now faces a more realistic challenge. Without knowing the population standard deviation, Joe
must rely on his sample's standard deviation to redo the analysis. This is where the T-test comes
into play. The T-test is designed to account for the smaller sample size and the added uncertainty
from estimating the population standard deviation.

Feeling the pressure but determined to stay in the running for the Baby Butter Ball Award, Joe opens
his spreadsheet once again. This time, he must:

- Calculate the sample mean and the sample standard deviation from his hospital's baby weight data.
- Perform a one-sample T-test to determine if his babies' weights are significantly larger than
   the national average of 7.5 lbs.

For the one-tailed right-tail claim, null hypothesis, H<sub>0</sub>: the hospital mean is at most 7.5 lbs and alternative hypothesis, H<sub>a</sub>: it is
greater than 7.5 lbs. For the two-tailed comparison, null hypothesis, H<sub>0</sub>: it equals 7.5 lbs and alternative hypothesis, H<sub>a</sub>: it differs.
Choose the alternative before examining results. The national value is a fictional teaching
benchmark, not a verified current public-health estimate.

Joe's stated claim makes the right-tailed test the assigned test. Record that choice before
calculating either p-value. The two-tailed result is included for comparison, not as a second chance
to find a significant result.

#### Step: Why Use a T-Test Now?

1. **Unknown Population Standard Deviation:** In real-world situations, we often **do not have** the
   population standard deviation. Therefore, we estimate it using the **sample standard deviation**.
2. **Small Sample Size:** When population variability is estimated from the sample, the t-test
   accounts for the added uncertainty. For a small sample, check approximate normality and outliers;
   t is not a cure for non-normal or dependent data.

#### Step: Set Up Your Google Sheet for the T-Test

1. Open the generated student XLSX in Google Sheets. This standalone workbook contains the data
   needed for this tutorial.
2. ***Again***, copy the data from the first sheet, tab named "***Datas for Part 1 and 2***", and
   paste it into the sheet tab named **"Part 2 National T-Test"** if you want to reset practice
   edits. The working sheet already contains all 24 original observations.
3. Working in the tab **"Part 2 National T-Test"**
4. **Columns D and E:** Set aside these columns for statistical calculations.
5. In cell **D1**, it should say "**Statistical Names**".
6. In cell **E1**, it should say "**Statistical Values**".
7. In cell **D2**, it should say [Population Mean](label:D2).
8. In cell **E2**, enter [7.5](enter:E2).
   1. ^ this is our representative mean baby weight of the population
9. In cell **D3**, it should say [**Population St.Dev.**](label:D3).
10. In cell **E3**, leave as not used, since we will not be using it. The test estimates variability
    from the sample instead of using a known population standard deviation.
11. After completion your table should contain the entries above; the supplied headings are already
    present in the workbook.

#### Step: Calculate the Sample Size

1. In cell **D5**, it should say [**"Sample Size."**](label:D5)
2. In cell **E5**, use the `COUNT` function to dynamically count the number of weights:
   - Enter: [=COUNT(B2:B101)](enter:E5)

#### Step: Calculate the Sample Mean

1. In cell **D6**, it should say [**"Sample Mean."**](label:D6)
2. In cell **E6**, use the `AVERAGE` function to calculate the sample mean:
   - Enter: [=AVERAGE(B2:B101)](enter:E6)

#### Step: Calculate the Sample Standard Deviation

1. In cell **D7**, it should say [**"Sample St.Dev."**](label:D7)
2. In cell **E7**, use the `STDEV.S` function to calculate the sample standard deviation:
   - Enter: [=STDEV.S(B2:B101)](enter:E7)

#### Step: Calculate the T-Statistic

1. In cell **D9**, it should say [**"T-Statistic."**](label:D9)
2. In cell **E9**, use this formula to calculate the t-statistic:
   - Enter: [=(E6 - E2) / (E7 / SQRT(E5))](enter:E9)
   - This formula uses the sample mean (E6), the assumed population mean (E2 at 7.5 lbs), the sample
     standard deviation (E7), and the sample size (E5).

#### Step: Calculate the Degrees of Freedom

1. In cell **D10**, it should say [**"Degrees of Freedom."**](label:D10)
2. In cell **E10**, calculate the degrees of freedom using:
   - Enter: [=E5 - 1](enter:E10)
   - Here, `E5` is the sample size, so subtracting 1 gives us the degrees of freedom.

##### Explanation: Why Do We Use Degrees of Freedom?

- **What Are Degrees of Freedom?** In statistics, **degrees of freedom** represent the number of
  independent values in a dataset that can vary when estimating a statistical parameter. In the
  context of a t-test, degrees of freedom are used to account for the fact that we are estimating
  the population standard deviation using the **sample standard deviation**.
- **Why Subtract 1?** When calculating the **sample standard deviation**, estimating the mean
  constrains the deviations from that mean to sum to zero, leaving n-1 independent deviations.
  This is why we lose one degree of freedom, which
  adjusts for the uncertainty introduced when estimating the standard deviation from a limited
  sample.
- **Impact on the T-Distribution:** The t-distribution changes shape depending on the degrees of
  freedom. For smaller sample sizes (fewer degrees of freedom), the t-distribution has **heavier
  tails**, reflecting greater variability and uncertainty. As the sample size grows (increasing
  degrees of freedom), the t-distribution becomes more similar to the **normal (z) distribution**.
- **Why It Matters:** In the t-test, degrees of freedom help adjust the **critical values** and
  **p-values** to reflect the sample size's impact. Smaller degrees of freedom make the test more
  conservative, meaning we need stronger evidence to reject the null hypothesis.

#### Step: Calculate the P-Value for the T-Test

##### Substep: Understand the Research Question

- **One-Tailed Test:** Use this if you want to test whether the babies at "Joe's Hospital of Fried
  Foods" are **larger** than the national average. This type of test only looks for a difference in
  **one direction** (greater than).
- **Two-Tailed Test:** Use this if you want to check for **any significant difference** (either
  larger or smaller) in baby weights compared to the national average. This type of test considers
  differences in **both directions**.

##### Substep: Calculate the P-Value Based on the Chosen Test

1. **Determine the Type of Test:** Decide if you are conducting a **two-tailed test** or a
  **one-tailed test** based on the research question:
   - **Two-Tailed Test:** Tests for any difference (either larger or smaller) in baby weights.
   - **One-Tailed Test:** Tests if the baby weights are **specifically larger** than the national
     average.
2. **Calculate the P-Value:**
   - **Two-Tailed Test:**
     1. In cell **D12**, it should say [**P-Value (Two-Tailed)**](label:D12).
     2. In cell **E12**, use the `T.DIST.2T` function:
        - Enter: [=T.DIST.2T(ABS(E9), E10)](enter:E12)
        - This formula calculates the p-value for a **two-tailed test** using the **absolute value** of
          the t-statistic (in cell E9) and the **degrees of freedom** (in cell E10).
        - **Explanation:** The `T.DIST.2T` function checks for differences in both directions
          (greater or smaller) between the sample mean and the population mean.
   - **One-Tailed Test:**
     1. In cell **D13**, it should say
        [**P-Value (One-Tailed, Right Tail)**](label:D13).
     2. In cell **E13**, use one minus the cumulative `T.DIST` function:
        - Enter: [=1 - T.DIST(E9, E10, TRUE)](enter:E13)
        - This formula calculates the p-value for a **one-tailed test** using the signed t-statistic
          (in cell E9) and the **degrees of freedom** (in cell E10). A negative t-statistic therefore
          gives a right-tail p-value greater than 0.5.
        - **Explanation:** One minus the cumulative `T.DIST` function tests the probability of
          observing a value as extreme or more extreme in **one direction** (greater than the
          population mean).

##### Substep: Important Notes:

* For a positive t-statistic and a right-tailed alternative, the **two-tailed
  p-value** is double the right-tailed p-value. With a negative statistic, the right-tailed p-value
  exceeds 0.5; do not blindly halve a two-tailed value.
* Make sure to use the correct function based on whether you are conducting a
  **one-tailed** or **two-tailed** test. This choice directly impacts the interpretation of your
  hypothesis test.

Both p-values and decisions are calculated so you can compare the two approaches. Report only the
result for the test you chose from the research question before calculating either p-value; do not
choose between the tests based on which p-value is smaller.

#### Step: Decision Using an IF Statement

1. In cell **D15**, it should say ["Significance Level (&alpha;)."](label:D15)
2. In cell **E15**, enter [0.05](enter:E15).
3. In cell **D17**, it should say ["*Two-Tail Decision*."](label:D17)
4. In cell **E17**, use the **IF** statement to automatically determine whether to reject the null
   hypothesis:
   - Using the **two-tailed test** p-value (in **E12**), enter the formula:
     [=IF(E12 <= E15, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")](enter:E17).
5. In cell **D18**, it should say ["*One-Tail Decision*."](label:D18)
6. In cell **E18**, use the **IF** statement to automatically determine whether to reject the null
   hypothesis:
   - Using the **one-tailed test** p-value (in **E13**), enter the formula:
     [=IF(E13 <= E15, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")](enter:E18).

#### Step: Interpret the Results

1. In cell **D20**, it should say [**"Interpretation."**](label:D20)
2. In cell **E20**, write a brief interpretation of your findings based on the p-value and test type.

#### Practice Task:

* Change some baby weights in Column B and observe how the sample standard
  deviation, t-statistic, and p-value adjust automatically.
* Add more baby weights (e.g., increasing the sample size beyond 30) and note how
  the p-value changes. Answer reflection question 1 in the reflection tab.
* Answer reflection question 2 in the reflection tab.

#### Key Takeaways:

1. Use the **t-test** when the **population standard deviation is unknown** and is
  estimated from the sample. A small sample alone does not decide between z and t; independence and
  approximate normality remain important.
2. The **t-distribution** accounts for the additional uncertainty introduced by using the sample
   standard deviation.
3. When the sample size is large, the t-test and z-test produce similar results,
  showing that the t-distribution approximates the normal distribution as the sample size increases.

#### Joe's Redemption - Reinstating the Award

After carefully following the steps, Joe anxiously awaits the results. Unfortunately, the t-test does
not show that his babies are significantly larger than the national average. With the supplied data
and a significance level of 0.05, the right-tailed p-value is about 0.154, so he must fail to reject
the null hypothesis. The committee does not reinstate his eligibility for the Baby Butter Ball
Award.

As Joe accepts the news, he feels a sense of relief but also humility. "I've learned a valuable
lesson," he admits, holding back his excitement. "From now on, I'll make sure I'm using the right
statistical tools."

But Joe can't resist a small smile. For now, the award remains out of his grasp, but he is more
determined than ever to prove that fried food really does make babies thrive... or at least win
awards. These data do not support either claim.

##### Statistical references

The [NIST guide to tests of a process
mean](https://www.itl.nist.gov/div898/handbook/prc/section2/prc.htm)
distinguishes the known-standard-deviation z-test from the estimated-standard-deviation t-test.

[image1]: assets/babies_2_image1.png
