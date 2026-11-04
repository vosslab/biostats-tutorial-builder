# **"Joe's Hospital of Fried Foods" vs. "Green Veggies Health Center"**

**Two Sample T-Test Tutorial for BIOL 318/418**

## Workbook

### Sheet: Fried Foods vs Green Veggies

| Infant<br>Number | Joe's Fried Foods<br>Birth Weight (pounds) | Green Veggies<br>Birth Weight (pounds) |
| --- | --- | --- |
| 1 | 9.56 | 9.16 |
| 2 | 8.88 | 7.86 |
| 3 | 7.22 | 7.38 |
| 4 | 8.02 | 6.41 |
| 5 | 9.43 | 8.64 |
| 6 | 9.91 | 8.04 |
| 7 | 6.84 | 7.15 |
| 8 | 9.95 | 7.75 |
| 9 | 9.53 | 5.96 |
| 10 | 8.25 | 7.61 |
| 11 | 6.14 | 7.18 |
| 12 | 6.43 | 8.01 |
| 13 | 9.27 | 7.77 |
| 14 | 6.46 | 7.43 |
| 15 | 5.83 | 7.45 |
| 16 | 5.62 | 7.77 |
| 17 | 7.01 | 9.08 |
| 18 | 9.29 | 6.87 |
| 19 | 9.36 | 7.06 |
| 20 | 7.35 | 8.01 |
| 21 | 9.54 | 8.68 |
| 22 | 6.61 | 7.25 |
| 23 | 9.72 | 7.36 |
| 24 | 7.17 | 7.88 |

#### At: F1

| Statistical Names | Fried Food Values | Green Veggie Values |
| --- | --- | --- |

- **Region A1:C25:** source
- **Region F1:H4:** calculation
- **Region F5:G7:** results
- **Region F8:G8:** interpretation

### Reflection Questions

1. For the right-tailed alternative, state whether the data provide sufficient evidence that Joe's population mean is greater.

## Tutorial

### Part: Two-Sample T-Test Scenario

- **Worksheet:** Fried Foods vs Green Veggies

#### Previous Scenario: One-Sample T-Test with National Average

In the previous situation, you used a **one-sample t-test** to compare the average baby weights at
**"Joe's Hospital of Fried Foods"** to the national average of **7.5 lbs**. Since the **population
standard deviation** was unknown, you used the **sample standard deviation** from Joe's Hospital to
perform the test.

#### New Scenario: Comparing Two Hospitals (Two-Sample T-Test)

Now, things are getting competitive. Joe, hoping to reinstate his eligibility for the **Baby Butter
Ball Award**, faces a direct challenge from **Alex**, CEO of **"Green Veggies Health Center."**
Alex's superfood-rich prenatal care has her convinced that her hospital's babies are just as hefty,
if not heavier, than Joe's fried-food babies.

#### Step: Why Use a T-Test Now?

1. **Unknown Population Standard Deviation**: Like before, we do not know the population standard
   deviation for either hospital, so we will use each hospital's **sample standard deviation**.
2. **Comparison of Two Independent Groups**: A **two-sample t-test** is the correct tool to compare
   the average baby weights at **Joe's Hospital** and **Green Veggies Health Center**, which are
   independent groups. Matching infant numbers are identifiers, not evidence of paired observations.
3. **Small Sample Size**: There are 24 observations per hospital. For small samples, check
   independence, approximate normality, and influential outliers. We use Welch's version without
   assuming equal population variances.

#### Step: Set Up Your Google Sheet

1. Open the generated student XLSX in Google Sheets. This is a standalone workbook containing both
   hospitals' data.
2. Make a personal copy of the workbook by going under **File** and "**Make a Copy**".
3. Change the name of the spreadsheet by adding your name and perhaps the date.
4. The original instructor template is available here: [Original instructor Google
  Sheet](https://docs.google.com/spreadsheets/d/13gzEAw_zGJyWcNErpK2m_N8bBzrRKbyZpBHAbtytVsI/edit).
   This link has no verified tab mapping. The generated workbook contains the complete original
   data in `A1:C25`, with 24 babies in each group. Ranges through row 101 intentionally leave room
   for practice additions; blank cells do not increase the sample sizes.

#### Before calculating summaries: choose the test

Before calculating or comparing the group means, standard deviations, or sample sizes, use the
research question to choose and record your alternative in your notes. Use a two-tailed test when
the question asks whether the means differ in either direction. Use a right-tailed test only for a
clear, justified prediction that Joe's mean is greater. For any difference, record H0: the hospital
population means are equal; H1: they differ. For Joe-greater, record H0: Joe's mean is less than or
equal to Green Veggies' mean; H1: Joe's mean is greater. Keep this choice for the final
interpretation, regardless of which result the summaries or p-values suggest.

#### Step: Set Up the Statistical Calculations

1. **Column F:** Type "Statistical Names."
2. **Column G:** Type "Fried Food Values."
3. **Column H:** Type "Green Veggie Values."
   These column headings are already supplied in the workbook.

#### Step: Calculate the Sample Means

1. In cell **F2**, type ["Sample Mean."](label:F2).
2. In cell **G2**, calculate the mean for Joe's Hospital using:
   - [=AVERAGE(B2:B101)](enter:G2)
3. In cell **H2**, calculate the mean for Green Veggies using:
   - [=AVERAGE(C2:C101)](enter:H2)

#### Step: Calculate the Sample Standard Deviations

1. In cell **F3**, type ["Sample Standard Deviation."](label:F3).
2. In cell **G3**, calculate the sample standard deviation for Joe's Hospital using:
   - [=STDEV.S(B2:B101)](enter:G3)
3. In cell **H3**, calculate the sample standard deviation for Green Veggies using:
   - [=STDEV.S(C2:C101)](enter:H3)

#### Step: Calculate the Sample Sizes

1. In cell **F4**, type ["Sample Size."](label:F4).
2. In cell **G4**, calculate the sample size for Joe's Hospital using:
   - [=COUNT(B2:B101)](enter:G4)
3. In cell **H4**, calculate the sample size for Green Veggies using:
   - [=COUNT(C2:C101)](enter:H4)

#### Step: Perform the Two-Sample T-Test in Google Sheets

##### Substep: Determine the Type of Test

When comparing two groups, like **"Joe's Hospital of Fried Foods"** and **"Green Vegetables Health
Center,"** you need to decide on the direction of your hypothesis:

* **Two-Tailed Test:** This is used when you want to test if there is **any significant difference**
  in the average weights between the two hospitals, regardless of direction. This means you're
  checking if the weights at one hospital are **either higher or lower** than the other.
  * **Example Hypothesis:**
    * **Null Hypothesis (H0):** The average weights at Joe's Hospital are equal to those at Green
      Veggies.
    * **Alternative Hypothesis (H1):** The average weights at Joe's Hospital are **different** from
      those at Green Veggies (either higher or lower).
  * Use a **two-tailed test** if you **do not have a specific expectation** about which hospital's
    average weight is higher.
* **One-Tailed Test:** This is used when you have a **specific direction** in mind. For example, if
  you specifically want to test if the babies at **Joe's Hospital** are **heavier** than those at
  **Green Veggies**, you would use a **one-tailed test**.
  * **Example Hypothesis:**
    * **Null Hypothesis (H0):** The average weights at Joe's Hospital are **less than or equal to**
      those at Green Veggies.
    * **Alternative Hypothesis (H1):** The average weights at Joe's Hospital are **greater** than
      those at Green Veggies.
  * Use a **one-tailed test** if you have a **specific hypothesis** about which hospital has heavier
    babies.

##### Substep: Calculate the P-Value Based on the Chosen Test

1. In cell **F5**, type [**"P-Value (Two-Sample T-Test)."**](label:F5).
2. In cell **G5**, use the `T.TEST` function to perform the two-sample t-test. The syntax of the
   `T.TEST` function is:
   - `=T.TEST(range1, range2, tails, type)`
   - Here's how you'll set up the formula:
     - **Range1 (Joe's Hospital):** B2:B101
     - **Range2 (Green Veggies):** C2:C101
     - **Tails:** This specifies if the test is **one-tailed** or **two-tailed**.
       - Enter **1** for a **one-tailed test**.
       - Enter **2** for a **two-tailed test**.
     - **Type:** This specifies the type of t-test. Use **3** to indicate that you are performing a
       **two-sample t-test with unequal variances** (Welch's t-test).
3. **Alternative: Two-tailed difference**
   1. **Two-Tailed Test:** If you want to check for any significant difference, enter:
      - [=T.TEST(B2:B101, C2:C101, 2, 3)](enter:G5)
      - Explanation:
        - **B2:B101** and **C2:C101** are the ranges for the weights of Joe's Hospital and Green
          Veggies, respectively.
        - The **first "2"** indicates a **two-tailed test**.
        - The **final "3"** indicates you are using the **two-sample t-test with unequal variances**
          (Welch's t-test).
4. **Alternative: One-tailed, Joe's mean greater**
   1. **One-Tailed Test:** If you want to check if babies at Joe's Hospital are **specifically heavier**,
      enter:
      - [=IF(G2>=H2,T.TEST(B2:B101,C2:C101,1,3),1-T.TEST(B2:B101,C2:C101,1,3))](enter:G5)
      - Explanation:
        - The **"1"** specifies that this is a **one-tailed test**. Google Sheets' one-tailed
          `T.TEST` uses the magnitude of the statistic. It does not select a directional alternative
          from the order of the ranges.
        - The `IF` checks the mean difference so this formula returns the right-tailed p-value for
          Joe greater than Green Veggies, including a p-value above 0.5 when the observed difference
          points the other way.

The supplied group means and standard deviations are calculated from their own columns, not copied
from the national-comparison tutorial.

##### Important Notes:

- **Two-Tailed Test:** Is more conservative since it tests for any difference in either direction.
  It splits the significance level (e.g., 0.05) between both tails of the distribution, requiring
  stronger evidence to reject the null hypothesis.
- **One-Tailed Test:** Is more powerful if you have a specific hypothesis about the direction of the
  difference (e.g., Joe's babies are heavier). However, it does **not** account for the possibility
  of a difference in the opposite direction, so it should only be used if you have a clear,
  justified expectation.

Before entering the decision, compare the p-value in G5 from your chosen alternative with a
significance level of 0.05. Enter the significance level and decision formula once.

#### Step: Make a Decision Using the P-Value

1. In **cell F6**, type [**"Significance Level (&alpha;)"**](label:F6). In **cell G6**, enter
   [0.05](enter:G6).
2. In **cell F7**, type [**"Decision"**](label:F7).
3. In **cell G7**, use an **IF** statement to compare the p-value to the significance level:
   - Enter: [=IF(G5 <= G6, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")](enter:G7)

#### Step: Interpret the Results

1. In cell **F8**, type [**"Interpretation."**](label:F8).
2. In cell **G8**, write a brief interpretation of the test results based on the p-value and your
   decision.

##### Example Interpretation:

* "With a p-value of \[calculated value\], we \[reject/fail to reject\] the null hypothesis, for
  the two-tailed test, indicating that the average weight of newborns at 'Joe's Hospital of Fried
  Foods' \[is/is not\] significantly different from that of 'Green Vegetables Health Center.'"

Answer reflection question 1 in the reflection tab. Failing to reject does not establish equal means. These observational
data do not establish a causal effect of either hospital's diet.

##### Statistical references

The [Google Sheets T.TEST documentation](https://support.google.com/docs/answer/6055837?hl=en)
explains the tails and type arguments and the absolute-statistic behavior.
