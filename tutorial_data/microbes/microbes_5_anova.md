# **Microbial Diversity ANOVA Tutorial** **for BIOL 318/418**

For BIOL 318/418. Continue the Busse Woods teaching scenario using the original workbook observations.

## Workbook

### Sheet: 30 Year ANOVA Test

- **Region A1:G25:** source
- **Region H1:K11:** calculation
- **Region L1:M1:** calculation
- **Region L3:M11:** calculation
- **Region L2:M2:** results
- **Region H13:I13:** calculation
- **Region H14:I14:** results
- **Region H16:I16:** interpretation

| `"Sample\nID"` | `"1994\nShannon\nIndices"` | `"2004\nShannon\nIndices "` | `"2009\nShannon\nIndices "` | `"2014\nShannon\nIndices "` | `"2024\nShannon\nIndices "` |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 3.66 | 4.96 | 5.43 | 1.754 | 2.413 |  |  |  |  |  |  |  |
| 2.0 | 3.98 | 5.12 | 5.43 | 3.173 | 3.853 |  |  |  |  |  |  |  |
| 3.0 | 5.0 | 3.78 | 3.82 | 2.226 | 2.645 |  |  |  |  |  |  |  |
| 4.0 | 5.0 | 3.73 | 4.026 | 5.345 | 4.871 |  |  |  |  |  |  |  |
| 5.0 | 3.56 | 5.0 | 6.099 | 2.598 | 2.357 |  |  |  |  |  |  |  |
| 6.0 | 5.0 | 5.54 | 6.461 | 5.588 | 4.281 |  |  |  |  |  |  |  |
| 7.0 | 5.0 | 4.91 | 2.551 | 4.504 | 3.433 |  |  |  |  |  |  |  |
| 8.0 | 6.21 | 4.26 | 2.713 | 1.927 | 2.876 |  |  |  |  |  |  |  |
| 9.0 | 3.22 | 3.85 | 3.786 | 4.552 | 4.415 |  |  |  |  |  |  |  |
| 10.0 | 3.62 | 5.0 | 3.104 | 2.623 | 3.46 |  |  |  |  |  |  |  |
| 11.0 |  | 2.99 | 3.707 | 3.768 | 2.64 |  |  |  |  |  |  |  |
| 12.0 |  | 2.67 | 5.818 | 4.97 | 5.009 |  |  |  |  |  |  |  |
| 13.0 |  | 5.0 | 3.428 | 5.657 | 4.885 |  |  |  |  |  |  |  |
| 14.0 |  | 5.0 | 5.484 | 3.059 | 2.805 |  |  |  |  |  |  |  |
| 15.0 |  | 3.32 | 3.365 | 4.08 | 4.733 |  |  |  |  |  |  |  |
| 16.0 |  |  | 1.493 | 5.585 | 4.452 |  |  |  |  |  |  |  |
| 17.0 |  |  | 4.233 | 4.245 | 2.749 |  |  |  |  |  |  |  |
| 18.0 |  |  | 3.166 | 3.959 | 3.635 |  |  |  |  |  |  |  |
| 19.0 |  |  | 4.987 | 3.84 | 4.371 |  |  |  |  |  |  |  |
| 20.0 |  |  | 6.796 | 6.341 | 4.906 |  |  |  |  |  |  |  |
| 21.0 |  |  |  | 4.254 | 3.985 |  |  |  |  |  |  |  |
| 22.0 |  |  |  | 3.668 | 3.849 |  |  |  |  |  |  |  |
| 23.0 |  |  |  | 4.623 | 3.521 |  |  |  |  |  |  |  |
| 24.0 |  |  |  | 6.505 | 4.982 |  |  |  |  |  |  |  |

### Reflection Questions

1. Describe how the **sample means**, **F-statistic**, and **p-value** change when you modify some of the Shannon Index values.
2. Discuss how sample size influences the **ANOVA** test and compare this to earlier F-test results.

## Tutorial

### Part: Scenario

- **Worksheet:** 30 Year ANOVA Test

![ANOVA.](assets/microbes_5_anova_image1.png)

After successfully rejecting the **null hypothesis** using the **F-test**, you found evidence that Shannon Index values in Busse Woods had lower **variance** in 2024 than in 2014 under the test assumptions. The earlier t-test addressed the mean; neither result establishes more uniform species composition. However, this raised new questions: Has this pattern of declining diversity and reduced variability been happening for even longer? To investigate, you now have microbial diversity data spanning **30 years**, from **1994 to 2024**.

To analyze how microbial diversity has shifted over time, you decide to use **ANOVA** (Analysis of Variance). This statistical test will allow you to compare microbial diversity across **five different time points**: **1994**, **2004**, **2009**, **2014**, and **2024**. By comparing these years, you can ask whether at least one population mean differs; identifying a longer-term decline or periods of **stability** would require further analysis.

#### Why Use ANOVA Now?

**ANOVA** is ideal for comparing more than two groups, making it the perfect tool for analyzing microbial diversity across multiple years. This test will help determine whether the **diversity values** have changed significantly over time by comparing the **variance** within each year to the **variance** between the years. By doing so, you can assess evidence for differences among year means. ANOVA alone does not establish a **decline**, **homogenization**, or a long-term trend.

Choose the hypothesis and **alpha = 0.05** before inspecting results. This one-way ANOVA tests
**null hypothesis, H<sub>0</sub>: all five population mean Shannon indices are equal**, against **alternative hypothesis, H<sub>a</sub>: at least one differs**.
It uses a **right-tailed F test**; it is not a lower-tail or two-tail variance comparison.

The model assumes independent observations, approximately normal residuals within groups, and
common population variances. For this method exercise, assume independent samples within and
across years; repeated measurements at the same locations would require a model accounting for
dependence. In the scenario, the older theses used culture-based methods while later datasets
used sequencing. Their different detection and taxonomic limits confound year with measurement
method, so this calculation alone cannot establish a historical ecological trend.

#### Step: Copy the Data

1. Open the generated XLSX workbook in Google Sheets.
2. Select the worksheet named above. It already contains the original observations, so you do not
   need to copy the data into a new sheet.
3. Keep the original observations intact while you calculate the results.

The original course workbook remains a [source reference](https://docs.google.com/spreadsheets/d/1cAlU997q8IazW6wJhBwYRrrO2l6ls0yCAo3Rx9BlUY0/edit).
Formula ranges end at row 101 to leave room for practice. The summary functions ignore empty
cells; blank observations are not zeroes. Add hypothetical numeric data only within these ranges.

#### Step: Organize Your Sheet into an ANOVA Table Layout

In this step, we will set up a traditional ANOVA table with **source of variation**, **sum of squares (SS)**, **degrees of freedom (DF)**, **mean square (MS)**, **F-statistic**, and **P-value**.

#### **ANOVA Table Setup:**

1. **Column A**: Sample ID. **Columns B-F**: Your raw data for each year (1994, 2004, 2009, 2014, and 2024).
2. **Column G**: we will leave this blank to separate the data from the calculations
3. **Column H**: This column will be used to label the **sources of variation** in the ANOVA.
4. **Columns I-M**: These columns will contain the calculated values for sums of squares, degrees of freedom, mean squares, F-statistic, and p-value.

#### Step-by-Step Tutorial:

1. In **Column H**, create the row headers for the **ANOVA table**:
   * **H1**: Type "[**Source of Variation**](label:H1)".
   * **H2**: Type "[**Between Groups**](label:H2)".
   * **H3**: Type "[**Within Groups**](label:H3)".
   * **H4**: Type "[**Total**](label:H4)".
2. In **Columns I-M**, add the following column headers:
   * **I1**: Type "[**Degrees of Freedom (DF)**](label:I1)".
   * **J1**: Type "[**Sum of Squares (SS)**](label:J1)".
   * **K1**: Type "[**Mean Square (MS)**](label:K1)".
   * **L1**: Type "[**F-Statistic**](label:L1)".
   * **M1**: Type "[**P-Value**](label:M1)".
3. The final table should look something like this

| Source of Variation | Degrees of Freedom (DF) | Sum of Squares (SS) | Mean Square (MS) | F-Statistic | P-Value |
| :---: | ----- | ----- | ----- | ----- | ----- |
| **Between Groups** |  |  |  |  |  |
| **Within Groups** |  |  |  |  |  |
| **Total** |  |  |  |  |  |

#### Step: Calculate the Group Statistics

The first step in an ANOVA test is to calculate the basic statistics for each group (in this case, each year). You need to calculate the **mean**, **variance**, and **sample size** for each group. These statistics will help us understand how each group differs individually before comparing them across time.

#### Step-by-Step Tutorial:

We will set up another table to organize the **group statistics** for each year.

1. **Setup Another Table:**
   * In **cell H6**, type [**Sample Name**](label:H6).
   * In **cell I6**, type [**1994 Sample**](label:I6).
   * In **cell J6**, type [**2004 Sample**](label:J6).
   * In **cell K6**, type [**2009 Sample**](label:K6).
   * In **cell L6**, type [**2014 Sample**](label:L6).
   * In **cell M6**, type [**2024 Sample**](label:M6).
2. **For Sample Means:**
   * In **cell H7**, type [**Sample Means**](label:H7).
   * In **cell I7**, use the formula [`=AVERAGE(B2:B101)`](enter:I7) to calculate the **sample mean** for 1994.
   * In **cell J7**, use the formula [`=AVERAGE(C2:C101)`](enter:J7) to calculate the **sample mean** for 2004.
   * In **cell K7**, use the formula [`=AVERAGE(D2:D101)`](enter:K7) to calculate the **sample mean** for 2009.
   * In **cell L7**, use the formula [`=AVERAGE(E2:E101)`](enter:L7) to calculate the **sample mean** for 2014.
   * In **cell M7**, use the formula [`=AVERAGE(F2:F101)`](enter:M7) to calculate the **sample mean** for 2024.
3. **For Sample Variances:**
   * In **cell H8**, type [**Sample Variances**](label:H8).
   * In **cell I8**, use the formula [`=VAR.S(B2:B101)`](enter:I8) to calculate the **sample variance** for 1994.
   * In **cell J8**, use the formula [`=VAR.S(C2:C101)`](enter:J8) to calculate the **sample variance** for 2004.
   * In **cell K8**, use the formula [`=VAR.S(D2:D101)`](enter:K8) to calculate the **sample variance** for 2009.
   * In **cell L8**, use the formula [`=VAR.S(E2:E101)`](enter:L8) to calculate the **sample variance** for 2014.
   * In **cell M8**, use the formula [`=VAR.S(F2:F101)`](enter:M8) to calculate the **sample variance** for 2024.
4. **For Sample Sizes:**
   * In **cell H9**, type [**Sample Sizes**](label:H9).
   * In **cell I9**, use the formula [`=COUNT(B2:B101)`](enter:I9) to calculate the **sample size** for 1994.
   * In **cell J9**, use the formula [`=COUNT(C2:C101)`](enter:J9) to calculate the **sample size** for 2004.
   * In **cell K9**, use the formula [`=COUNT(D2:D101)`](enter:K9) to calculate the **sample size** for 2009.
   * In **cell L9**, use the formula [`=COUNT(E2:E101)`](enter:L9) to calculate the **sample size** for 2014.
   * In **cell M9**, use the formula [`=COUNT(F2:F101)`](enter:M9) to calculate the **sample size** for 2024.

#### Explanation:

This step focuses on calculating the **group statistics**: the **means**, **variances**, and **sample sizes** for each year's data. These values will be crucial for the ANOVA test because they allow us to assess how each group behaves individually. The **means** show us the average microbial diversity in each year, while the **variances** tell us how much the data is spread out within each year. Finally, the **sample sizes** help evaluate the reliability of these statistics for each year.

These statistics will feed into the next step, where we calculate the **sums of squares** and start filling out the ANOVA table.

#### Step: Calculate the Grand Mean

In this step, you will calculate the **grand mean**, which is the overall average of all data points across the different groups. The grand mean helps you compare individual group means to the overall dataset. It serves as a reference point for future steps, such as calculating the total variability and assessing how much each group deviates from the overall dataset. You will calculate the grand mean using the **AVERAGE** function to capture the mean of all values in the dataset.

#### Step-by-Step Tutorial:

* In **cell H11**, type [**Grand Mean**](label:H11).
* In **cell I11**, use the formula [`=AVERAGE(B2:F101)`](enter:I11) to calculate the **overall mean** of all the Shannon Index values.

#### Step: Calculate the Degrees of Freedom (DF)

In this step, you will calculate the **Degrees of Freedom (DF)** for both the **between groups** (DF treatment) and **within groups** (DF error) components, as well as the **total DF**. The DF reflects the number of independent data points contributing to each variance estimate. In ANOVA, the DF for each component helps us understand the amount of information available for estimating the variability between and within groups.

#### Step-by-Step Tutorial:

* In **cell `I2`**, use the formula [`=COUNT(I7:M7) - 1`](enter:I2) to calculate the **DF Between** (DF treatment). This calculates the degrees of freedom for the variation between groups, which is the number of groups minus one.
* In **cell `I3`**, use the formula [`=COUNT(B2:F101) - COUNT(I7:M7)`](enter:I3) to calculate the **DF Within** (DF error). This calculates the degrees of freedom for the variation within groups by subtracting the number of groups from the total number of observations.
* In **cell `I4`**, use the formula [`=COUNT(B2:F101) - 1`](enter:I4) to calculate the **DF Total**. This is the degrees of freedom for the total variability, representing the total number of observations minus one.

#### Explanation:

The **Degrees of Freedom (DF)** reflect the number of independent values that contribute to the variance estimates in the ANOVA table. Here is how the different components of the DF are calculated:

* **DF Between (DF treatment)**: This is the degrees of freedom associated with the variability between groups (for example, between different years). It is calculated as the number of groups (**k**) minus one. The formula `=COUNT(I7:M7) - 1` counts the number of groups and subtracts one.
* **DF Within (DF error)**: This is the degrees of freedom associated with the variability within groups. It is calculated as the total number of observations (**n**) minus the number of groups (**k**). The formula `=COUNT(B2:F101) - COUNT(I7:M7)` calculates the total number of observations and subtracts the number of groups to give the DF within.
* **DF Total**: This is the total degrees of freedom, representing the total variability in the dataset. It is calculated as the total number of observations (**n**) minus one. The formula `=COUNT(B2:F101) - 1` calculates this directly.

The relationship between these degrees of freedom is: `DF Total = DF Between + DF Within`

#### Step: Calculate the Regression Sum of Squares (SSR)

In this step, you will calculate the **Regression Sum of Squares (SSR)**. This represents how much of the total variance is explained by the differences between the group means. The SSR helps quantify the portion of the total variation that can be attributed to the differences between the groups, such as the different years in your dataset.

#### Step-by-Step Tutorial:

* Go back up to our original table.
* In **cell `J2`**, type the formula [`=SUMPRODUCT((I7:M7 - I11)^2, I9:M9)`](enter:J2) to calculate the **SS Between**.

#### Explanation:

The **SSR** quantifies the variation between the group means and how much of the total variance can be explained by the differences between those means. By comparing the mean values of each group to the **grand mean** (the overall average), the **SSR** isolates the variance due to differences between the groups. This is calculated by summing the squared deviations of each group mean from the grand mean, weighted by the sample size of each group.

The **SUMPRODUCT** function multiplies corresponding elements from two arrays and sums the products. In this case, `(I7:M7 - I11)^2` calculates the squared differences between each group mean (from cells `I7:M7`) and the grand mean (in `I11`). The second array, `I9:M9`, contains the sample sizes for each group. **SUMPRODUCT** multiplies these squared differences by the respective sample sizes and sums them to yield the **SSR**, which tells us how much of the total variance is explained by the differences between the group means.

#### Step: Calculate the Error Sum of Squares (SSE)

In this step, you will calculate the **Error Sum of Squares (SSE)**. This measures the variation within each group that cannot be explained by differences between the group means. It captures how much of the total variability is due to random differences within the groups.

#### Step-by-Step Tutorial:

1. In **cell `J3`**, use the formula [`=SUMPRODUCT((I9:M9 - 1), I8:M8)`](enter:J3) to calculate the SSE. This formula calculates the squared deviations of each observation from its respective group mean.

#### Explanation:

The **SSE** quantifies the variability within the groups that is not explained by the differences between the group means. By calculating the squared deviations of each observation from the group mean, this step identifies the portion of variance due to random fluctuations within each group. Summing these squared deviations provides the **SSE**, which is essential for understanding how much of the total variation is due to within-group differences.

#### Step: Calculate the Total Sum of Squares (SST)

In this step, you will calculate the **Total Sum of Squares (SST)**, which measures the overall variability in the dataset. The SST accounts for both the variability between the group means (SSR) and the variability within each group (SSE). It compares each data point to the **grand mean** to capture the total variance in the dataset.

#### Step-by-Step Tutorial:

1. In **cell `J4`**, use the formula [`=J2 + J3`](enter:J4) to calculate the SST.

#### Explanation:

The **Total Sum of Squares (SST)** measures the overall variance in the dataset by comparing each individual data point to the grand mean. It captures all the variability present in the data. The **SST** is broken down into two components:

1. **SSR**: The portion of the total variance explained by the differences between the group means.
2. **SSE**: The portion of the total variance that is due to random variability within the groups, not explained by the group means.

The relationship between these terms is: `SST = SSR + SSE`

By calculating the **SST**, you quantify the total variability in your dataset, which you will later partition into the components explained by group differences (SSR) and the remaining unexplained variation (SSE).

#### Step: Calculate the Mean Square (MS)

The **mean square (MS)** is calculated by dividing the **sum of squares (SS)** by the **degrees of freedom (DF)**. This represents the average variability for each source of variance (between groups and within groups).

#### Step-by-Step Tutorial:

* In cell **`K2`**, type [`=J2/I2`](enter:K2) to calculate the **MS Between**.
* In cell **`K3`**, type [`=J3/I3`](enter:K3) to calculate the **MS Within**.

#### Explanation:

The **mean squares (MS)** are the average variability per **degree of freedom** for each source of variance. The **MS Between** tells us how much variability is due to the differences between years, while the **MS Within** captures the average variability within each year. These values are crucial for calculating the **F-statistic** in the next step.

#### Step: Calculate the F-Statistic

Now that you have calculated the **mean squares**, the next step is to calculate the **F-statistic** for the observed differences in microbial diversity between years. In an ANOVA, the F-statistic compares the **between groups** mean square with the **within groups** mean square. In the next step, you will use it and the **degrees of freedom** to calculate the **p-value**.

#### Step-by-Step Tutorial:

* In cell **`L2`**, type [`=K2/K3`](enter:L2) to calculate the **F-statistic**.

#### Explanation:

The **F-statistic** is the ratio of the **between groups variance** to the **within groups variance**. A larger F-statistic suggests that more of the variance is due to differences between years, and provides stronger evidence against equal population means under the ANOVA assumptions. We will use the F-statistic in the next step to determine statistical significance.

#### Step: Calculate the P-Value

Now that the F-statistic has been calculated, we can determine whether the differences in microbial diversity between the years are statistically significant by calculating the **P-value**. The P-value gives the probability, under the equal-means null model and its assumptions, of an F-statistic at least as large as the one observed. A smaller P-value (typically less than 0.05) indicates that the differences between the groups are statistically significant.

#### Step-by-Step Tutorial:

* In **cell `M2`**, use the formula [`=F.DIST.RT(L2, I2, I3)`](enter:M2) to calculate the P-value.

#### **Explanation:**

The **F.DIST.RT** function calculates the right-tailed probability of the F-distribution. This function takes the following inputs:

* The **F-statistic** (calculated in cell **L2**),
* **Degrees of freedom** between the groups (**I2**),
* **Degrees of freedom** within the groups (**I3**).

The result of this function gives us the **P-value**, which shows whether the differences in microbial diversity across the years (1994, 2004, 2009, 2014, and 2024) are statistically significant. If the P-value is less than or equal to 0.05, you can reject equal population means in favor of at least one differing mean. This does not identify which years differ or show that every year-to-year change is significant.

#### Step: Decision Using an IF Statement

In hypothesis testing, the decision to **reject** or **fail to reject** the **null hypothesis** is based on the **p-value** and the significance level (**&alpha;**) set before the test. In most cases, **&alpha;** is 0.05. If the **p-value** is less than or equal to 0.05, the result is considered **statistically significant**, meaning an F-statistic at least as large as observed would be unlikely under the equal-means null model. To simplify this decision-making process in **Google Sheets**, we will use the **IF** statement to evaluate whether the **p-value** is less than or equal to the significance level (0.05).

#### Step-by-Step Tutorial:

1. In cell **H13**, type [**Significance Level (&alpha;)**](label:H13).
2. In cell **I13**, enter [**0.05**](enter:I13).
3. In cell **H14**, type [**Decision**](label:H14).
4. In cell **I14**, use the formula [`=IF(M2 <= I13, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:I14) to decide whether to reject the null hypothesis based on the **ANOVA** p-value.

#### Explanation

The **IF** statement evaluates whether the **p-value** (in **M2**) is less than or equal to **0.05** (the significance level). If the **p-value** is smaller than or equal to 0.05, you will **reject the null hypothesis**, indicating that the variation in microbial diversity across the years is statistically significant. If the **p-value** is greater than 0.05, you will **fail to reject the null hypothesis**, meaning there is insufficient evidence that the population means differ. This does not establish equality.

This process simplifies the interpretation of your **ANOVA** results, ensuring that you can quickly assess whether there is a statistically significant difference in microbial diversity over the years.

#### Step: Interpret the Results

Now that you have calculated the **ANOVA** results, the next step is to **interpret** the findings. This involves assessing whether microbial diversity in Busse Woods has changed significantly over the decades (1994 to 2024). By comparing the **p-value** to **0.05**, you can assess evidence against equal population means. This comparison cannot determine whether environmental pressures like **urbanization** or **climate change** caused the differences.

#### Step-by-Step Tutorial:

* In **cell H16**, type [**Interpretation.**](label:H16)
* **In cell I16**, write a brief interpretation of your findings based on the **ANOVA** results. Example:
  * "With a **right-tail p-value** of [calculated value] and alpha = 0.05, we [reject/fail to reject] the equal-means null hypothesis, providing [sufficient/insufficient] evidence that at least one population mean Shannon Index differs among years."

#### Explanation:

The interpretation hinges on comparing the **p-value** to the **significance level** (&alpha; = 0.05). If the **p-value** is less than or equal to 0.05, the **null hypothesis** is **rejected**, which suggests that there are **statistically significant differences** in microbial diversity between the different years. The omnibus result does not identify which means differ, establish a declining trend, or identify an environmental cause.

If the **p-value** is greater than 0.05, you would **fail to reject the null hypothesis**, meaning there is insufficient evidence against equal population means. It does not establish unchanged diversity or equal variances, and cannot determine whether **environmental pressures** caused the observed pattern.

#### Practice Task:

Save a separate practice copy after recording the original result. Modified values are hypothetical examples.

* Modify some of the Shannon Index values for the **1994**, **2004**, **2009**, **2014**, and **2024** data columns. Answer reflection question 1 in the reflection tab.
* Add hypothetical numeric observations within rows 2:101 (increase the sample size) and note the impact on the **ANOVA** results.
* Answer reflection question 2 in the reflection tab.

#### Key Takeaways:

1. **ANOVA** allows for the comparison of **multiple groups** at once, making it useful for assessing whether microbial diversity has changed over multiple decades.
2. The **p-value** helps determine whether the differences in **microbial diversity** across years are **statistically significant**.
3. A larger sample size can reduce uncertainty under the model, but does not repair biased sampling, dependence, or measurement-method differences.
4. **ANOVA** is a powerful tool for testing differences among multiple population means. Identifying **trends over time** or the impact of **environmental factors** requires additional analyses and evidence.
