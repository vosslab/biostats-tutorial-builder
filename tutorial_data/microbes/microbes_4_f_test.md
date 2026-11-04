# **Microbial Diversity Two Sample F-Test Tutorial** **for BIOL 318/418**

For BIOL 318/418. Continue the Busse Woods teaching scenario using the original workbook observations.

## Workbook

### Sheet: Two Sample F-Test

- **Region A1:C25:** source
- **Region D1:G14:** calculation
- **Region D16:G18:** results
- **Region D20:E20:** calculation
- **Region D22:E24:** results
- **Region D26:E26:** interpretation

| "Sample Location" | `"2014\nShannon\nIndex "` | `"2024\nShannon\nIndex "` | "Statistical Names" | "Values" |
| --- | --- | --- | --- | --- |
| "Andrews Park" | 4.417 | 2.413 |  |  |
| "Beisner Road Entrance" | 5.359 | 3.853 |  |  |
| "Boat Launch Area" | 1.984 | 2.645 |  |  |
| "Busse Lake" | 6.923 | 4.871 |  |  |
| "Debra Park" | 1.412 | 2.357 |  |  |
| "Elk Pasture" | 4.677 | 4.281 |  |  |
| "Forest Central Grove" | 4.26 | 3.433 |  |  |
| "Forest North Grove" | 2.633 | 2.876 |  |  |
| "Forest South Grove" | 3.429 | 4.415 |  |  |
| "Forest West Grove" | 2.965 | 3.46 |  |  |
| "Lake Boating Center" | 4.728 | 2.64 |  |  |
| "Large Event Area" | 6.944 | 5.009 |  |  |
| "Main Dam" | 5.404 | 4.885 |  |  |
| "Main Pool" | 4.612 | 2.805 |  |  |
| "Marshall Park" | 5.028 | 4.733 |  |  |
| "Model Airplane Field" | 5.949 | 4.452 |  |  |
| "Nature Preserve" | 3.907 | 2.749 |  |  |
| "Ned Brown Meadow" | 4.305 | 3.635 |  |  |
| "North Pool" | 4.665 | 4.371 |  |  |
| "Osborn  Park" | 4.241 | 4.906 |  |  |
| "Salt Creek Trail" | 4.351 | 3.985 |  |  |
| "South Pool" | 3.791 | 3.849 |  |  |
| "Wildlife Refuge" | 4.079 | 3.521 |  |  |
| "Woodland Meadow" | 6.565 | 4.982 |  |  |

### Reflection Questions

1. Discuss how **sample size** affects the **F-test** results and compare this to earlier **T-test** results. Focus on how a larger sample size can reduce **uncertainty** under the model and change the **F-distribution**, without guaranteeing a smaller **p-value**.

## Tutorial

### Part: Scenario

- **Worksheet:** Two Sample F-Test

![T-test versus F-test.](assets/microbes_4_f_test_image1.png)

After comparing the microbial diversity in **Busse Woods** between **2014** and **2024** using a **Two Sample T-test**, you found evidence that the mean Shannon Index **decreased** over the past decade under the t-test model. However, while analyzing the data further, you observe something unexpected: the **2024 Shannon Index values** appear more **similar** to one another compared to those from **2014**. This raises new questions about whether the **variability** in microbial diversity has changed alongside the mean. Could environmental pressures like **urbanization** and **climate change** also be associated with changes in the spread of these diversity values?

Excited by this idea, you present your findings to your advisor, who praises your observation and suggests conducting an **F-test** to compare the **variances** between the two years. By comparing the **spread** of diversity values in **2014** and **2024**, the **F-test** will help determine whether the population variances of Shannon Index values differ in **Busse Woods**. This could prompt further questions about **ecological resilience** and whether some of the forest's unique **microenvironments** are being lost; the variance test alone cannot answer those questions.

#### Why Use an F-Test Now?

While the **Two Sample T-test** compared the **means** of microbial diversity between **2014** and **2024**, the **F-test** allows you to assess the **variances**. This test is ideal when you need to determine whether the **spread** of data has changed significantly between two groups or time periods. In this case, it will help you explore whether Shannon Index values in **Busse Woods** have become more **uniform** across observations. Similar index values do not imply similar species composition, and this test cannot identify the effects of **environmental pressures**.

Choose the hypothesis and **alpha = 0.05** before inspecting results. Calculating all three tails
below is a comparison exercise, not permission to select the smallest p-value. The main alternative
is **2024 population variance < 2014 population variance**; its null is >=. The two-tailed null is
equality (alternative: inequality); the higher-tail null is <= (alternative: >).

The classical F-test assumes **independent observations from normal populations** and is especially
sensitive to nonnormality. The same 24 named locations occur in both years, so this method exercise
makes a hypothetical independence assumption within and across years. If these are repeated site
measurements, use a variance comparison that accounts for dependence before drawing field conclusions.

#### Step: Copy the Data

1. Open the generated XLSX workbook in Google Sheets.
2. Select the worksheet named above. It already contains the original observations, so you do not
   need to copy the data into a new sheet.
3. Keep the original observations intact while you calculate the results.

The original course workbook remains a [source reference](https://docs.google.com/spreadsheets/d/1cAlU997q8IazW6wJhBwYRrrO2l6ls0yCAo3Rx9BlUY0/edit).
Formula ranges end at row 101 to leave room for practice. The summary functions ignore empty
cells; blank observations are not zeroes. Add hypothetical numeric data only within these ranges.

#### Step: Organize Your Sheet

1. The data will look like this:
   * **Column A**: Sample Location ID
   * **Column B**: **2014 Shannon Index** (microbial diversity from the 2014 dataset)
   * **Column C**: **2024 Shannon Index** (current microbial diversity data)
   * **Column D**: Statistical Names
   * **Columns E through G**: Calculated Values
2. Here's how to set it up:
   * In cell **D1**, type "**Statistical Names**".
   * In cell **E1**, type "**Values**".
   * In cell **F1**, type "[**Alternate Values 1**](label:F1)".
   * In cell **G1**, type "[**Alternate Values 2**](label:G1)".

#### Step: Calculate the Sample Statistics

Now, let us calculate the statistics needed for both datasets.

1. **Sample Means**:
   * Sample means are not needed for the F-test, so you can skip this step.
2. **Sample Standard Deviations**:
   * In cell D5, type [**2014 Sample Standard Deviation**](label:D5).
   * In **E5**, use the formula [`=STDEV(B2:B101)`](enter:E5) to calculate the sample standard deviation for **2014**.
   * In cell D6, type [**2024 Sample Standard Deviation**](label:D6).
   * In **E6**, use the formula [`=STDEV(C2:C101)`](enter:E6) to calculate the sample standard deviation for **2024**.
3. **Sample Sizes**:
   * In cell D8, type [**2014 Sample Size**](label:D8).
   * In **E8**, use the formula [`=COUNT(B2:B101)`](enter:E8) to count the number of samples for **2014**.
   * In cell D9, type [**2024 Sample Size**](label:D9).
   * In **E9**, use the formula [`=COUNT(C2:C101)`](enter:E9) to count the number of samples for **2024**.

#### Step: Calculate the F-Statistic

Now, we will calculate the **F-statistic** to compare the **variances** of the two datasets.

* In **cell D11**, type [**F-Statistic**](label:D11).
* In **E11**, calculate the **F-statistic** using this formula:
  [`=E6^2 / E5^2`](enter:E11)

#### Explanation: F-Statistic

The **F-statistic** is used to compare the **variances** of two samples. It is the ratio of the variances of the two datasets (2014 and 2024). If the **F-statistic** is close to **1**, it indicates that the **variances** of the two datasets are similar. Here, the 2024 variance is the numerator: an **F-statistic** greater than **1** means that 2024 has more observed **spread**, while a value below **1** means it has less. Statistical significance also depends on the degrees of freedom and chosen tail.

It is important to note that **sample means are not relevant** for the **F-test**. The test focuses entirely on the **spread** of the data (**variance**), regardless of where the data is centered (**mean**). This means that even if the two groups have the same or different means, the **F-test** only cares about how **spread out** the values are in each group.

This calculation will help determine whether the **spread** (**variability**) in microbial diversity across sampling locations has changed over time. Lower variance would indicate more **uniformity** in the **2024 index values**, not necessarily **homogenization** of species composition or reduced **ecological resilience**.

#### Step: Calculate the Degrees of Freedom

In an **F-test**, degrees of freedom are used differently than in a **T-test**. In this case, the degrees of freedom correspond to the **sample sizes** of each group, minus one for each. The **F-test** compares the **variances** of two samples, and the degrees of freedom help us interpret how reliable these variance estimates are.

**Step-by-Step Tutorial**:

* In **cell D13**, type [**Degrees of Freedom for 2014**](label:D13).
* In **E13**, type [`=E8 - 1`](enter:E13) to calculate the degrees of freedom for the **2014 dataset**.
* In **cell D14**, type [**Degrees of Freedom for 2024**](label:D14).
* In **E14**, type [`=E9 - 1`](enter:E14) to calculate the degrees of freedom for the **2024 dataset**.

#### Explanation

In the **F-test**, the **degrees of freedom (DF)** represent the number of independent deviations available after estimating each sample mean. For each sample, the **DF** is calculated as **sample size - 1**. This reflects the fact that one degree of freedom is used up in estimating the mean, so only the remaining data points are "free to vary."

Because the variance ratio is **2024 / 2014**, use the 2024 degrees of freedom (**E14**) first and the 2014 degrees of freedom (**E13**) second in F-distribution formulas, even when practice changes sample sizes.

These degrees of freedom are used to interpret the **F-statistic**, which compares the **variances** of the two samples. Larger degrees of freedom generally reduce uncertainty in estimates of population variance under the model assumptions.

In **biological studies**, where **sample sizes** are often small, the **F-distribution** becomes wider, meaning that it takes a larger difference in variances to conclude that they are statistically different. As both degrees of freedom increase (i.e., as both sample sizes increase), the **F-distribution** becomes more concentrated near 1 under the equal-variance null model.

#### Step: Determine the Type of Test (One-Tailed or Two-Tailed)

In an **F-test**, you are testing whether the **variances** between two datasets (in this case, the Shannon Index values for 2014 and 2024) are significantly different. You need to decide whether you are testing for any significant difference in variance (a **two-tailed test**) or a specific hypothesis about which year has greater variance (a **one-tailed test**).

* **Two-Tailed Test**: This test is used to check whether the **variance** of microbial diversity in 2024 is **significantly different** (either higher or lower) from that in 2014. If you are unsure about the direction of change but suspect there is a difference in the variability of the data, the two-tailed test is appropriate.
* **One-Tailed Test**: This test is used when you have a specific hypothesis about the direction of the variance difference. For example:
  * **Lower One-Tailed Test**: This checks if the **variance** in 2024 is **lower** than in 2014, indicating that Shannon Index values in 2024 may be more **homogeneous** across observations than in 2014.
  * **Higher One-Tailed Test**: This checks if the **variance** in 2024 is **higher** than in 2014, which could indicate that the microbial diversity in 2024 has **greater variability**.

For an **F-test**, you are no longer testing the **mean** or **direction of change** in microbial diversity but rather whether the **spread of values (variance)** has changed significantly. In this case, because your preselected hypothesis is **reduced variability** in Shannon Index values in 2024, a **lower one-tailed F-test** would be appropriate.

#### Step: Calculate the P-Values

Now that you are working with two samples (2014 and 2024 Shannon Index values), you will calculate the **F-statistic** and the **p-values** to compare the **variances** of microbial diversity between these two datasets. The **F-statistic** is the ratio of the variances between the two groups, and the **p-value** will help you determine if the observed variance difference is statistically significant.

You will perform both **two-tailed** and **one-tailed** tests (lower and higher) to check if the **variance** of microbial diversity has either increased or decreased from 2014 to 2024. You will also use both **manual calculations** and the **F.TEST** function to automate the process.

#### Explanation of F.DIST Inputs:

The function **`F.DIST`** is used to calculate the cumulative distribution function (CDF) of the F-distribution, which gives the lower-tail probability at the observed F-statistic under the equal-variance null model. Here are the inputs:

* **F.DIST(x, degrees_freedom1, degrees_freedom2, cumulative)**
  * **x**: This is the **F-statistic**, calculated as the ratio of the variances of the two groups.
  * **degrees_freedom1**: This is the **degrees of freedom** for the numerator dataset (here, the 2024 dataset), calculated as the sample size minus one.
  * **degrees_freedom2**: This is the **degrees of freedom** for the denominator dataset (here, the 2014 dataset), calculated as the sample size minus one.
  * **cumulative**: This specifies whether you want the **cumulative distribution function** (TRUE) or the **probability density function** (FALSE). You will use TRUE for calculating the cumulative probability.

#### Explanation of F.TEST Inputs:

The function **`F.TEST`** simplifies the F-test process by directly comparing the variances of two datasets and calculating the p-value. Here are the inputs:

* **F.TEST(array1, array2)**
  * **array1**: This is the range of values for the first dataset (for example, the 2014 Shannon Index values in column B).
  * **array2**: This is the range of values for the second dataset (for example, the 2024 Shannon Index values in column C).

The **`F.TEST`** function returns the **p-value**, which tells you whether the variance between the two datasets is significantly different. A smaller **p-value** (less than 0.05) suggests that the difference in variance is statistically significant.

##### Substep: Two-Tailed Test:

This test checks if the **variance** in microbial diversity has changed in **either direction** between 2014 and 2024.

#### Step-by-Step Tutorial:

* In **cell D16**, type [**P-Value (Two-Tailed)**](label:D16).
* In **E16**, calculate the **two-tailed p-value** using the following formula:
  * [`=MIN(1, 2 * MIN(F.DIST(E11, E14, E13, TRUE), F.DIST.RT(E11, E14, E13)))`](enter:E16)
  * This doubles the smaller tail probability, capped at 1, using the **variance** ratio and its numerator and denominator degrees of freedom.
* In **G16**, calculate the **p-value**:
  * [`=F.TEST(C2:C101, B2:B101)`](enter:G16)
  * This calculates the **two-tailed p-value** directly, comparing the **variances** between the two datasets (2014 in column B and 2024 in column C).

#### Explanation for Two-Tailed Test:

In this two-tailed **F-test**, you are testing whether the **variance** in microbial diversity has **significantly changed** between 2014 and 2024. The **F.DIST** function compares the **variances** of the two datasets, and the **F.TEST** function simplifies the process by calculating the p-value automatically. A significant **p-value** suggests that the **spread** (variance) in microbial diversity has either **increased or decreased** between 2014 and 2024.

##### Substep: One-Tailed Test (for lower values):

This test evaluates whether the **variance** in microbial diversity is **lower** in 2024 than in 2014, indicating that the index values have less spread across observations.

#### Step-by-Step Tutorial:

* In **cell D17**, type [**P-Value (One-Tailed, Lower)**](label:D17).
* In **E17**, use the following formula: [`=F.DIST(E11, E14, E13, TRUE)`](enter:E17) This calculates the **p-value** for a **lower one-tailed test**, testing if the **variance** in 2024 is smaller than in 2014.
* In **G17**, calculate the **one-tailed p-value** using: [`=IF(F.DIST(E11, E14, E13, TRUE) <= 0.5, F.TEST(C2:C101, B2:B101)/2, 1 - F.TEST(C2:C101, B2:B101)/2)`](enter:G17) This recovers the lower-tail probability from F.TEST, using half its two-tailed result only when the lower tail is at most 0.5, and otherwise using one minus that half.

#### Explanation for One-Tailed Test (Lower):

In this **one-tailed F-test**, you are testing if the **variance** in microbial diversity has **decreased**, meaning the diversity values are becoming more **uniform** in 2024. If the **p-value** is significant, it suggests that the **variance** in 2024 is **lower**, indicating more uniform index values across observations under the independent normal-population model.
Since **F.TEST** gives a **two-tailed p-value**, dividing by 2 gives the smaller tail only. Use the conditional formula above to select the lower tail even if practice changes the direction of the observed difference. For the **one-tailed lower test**, this means you are checking whether the variance in 2024 is significantly **lower** than in 2014. The p-value needs to reflect this **one-directional** hypothesis.

##### Substep: One-Tailed Test (for higher values):

This test evaluates whether the **variance** in microbial diversity is **higher** in 2024 than in 2014, suggesting that diversity is becoming more **variable**.

#### Step-by-Step Tutorial:

1. **In cell D18,** type [**P-Value (One-Tailed, Higher)**](label:D18).
2. **In E18,** use the following formula: [`=F.DIST.RT(E11, E14, E13)`](enter:E18).
   * This formula calculates the p-value for a higher one-tailed test, checking if the variance in **2024** is greater than that of **2014**.
   * The **F.DIST.RT** function calculates the right-tailed probability, which tests whether the variance in 2024 is significantly greater than in 2014.
3. **In F18,** use the following formula: [`=F.DIST(E5^2 / E6^2, E13, E14, TRUE)`](enter:F18).
   * This formula performs the same test but with the variances and their degrees of freedom swapped. It evaluates if the variance in **2024** is greater than the variance in **2014** by reversing the order of the ratio.
   * This approach helps confirm the results and provides insight into how the variances compare.
4. **In G18,** calculate the one-tailed p-value using: [`=1 - G17`](enter:G18).
   * This function simplifies the calculation, directly testing if the variance in **2024** is greater than in **2014** by comparing the two datasets.

#### Explanation for One-Tailed Test (Higher):

In this **one-tailed F-test**, you are assessing whether the **variance in microbial diversity** has increased between 2014 and 2024. A higher variance in 2024 suggests that diversity values are becoming more spread out, indicating greater variability in microbial communities.

The formula **F.DIST.RT(E11, E14, E13)** specifically tests if **2024** has more variability than **2014** by calculating the ratio of their variances. If the **p-value** is significant (typically less than 0.05), this means the **variance in 2024 is statistically greater** than in 2014. This increased spread concerns Shannon Index values; identifying an effect of **environmental factors**-such as urbanization or climate changes-would require additional evidence.

By comparing the right-tail calculation with the reciprocal-ratio calculation (and swapped degrees of freedom), you can confirm that both calculations give the same higher-tail probability.

#### Step: Decision Using an IF Statement

In hypothesis testing, the decision to **reject** or **fail to reject** the **null hypothesis** is based on comparing the **p-value** to a predetermined **significance level (&alpha;)**, often set at **0.05**. If the p-value is less than or equal to **0.05**, the result is considered **statistically significant**, meaning a variance ratio at least as extreme in the specified tail or tails would be unlikely under the null model. To make this process easier, we will use the **IF statement** in Google Sheets, which evaluates a condition and returns one value if true and another if false. In this case, we will check whether the p-value is less than or equal to **&alpha; (0.05)**.

#### Step-by-Step Tutorial:

* **In cell D20,** type [**Significance Level (&alpha;)**](label:D20).
* **In cell E20,** enter [**0.05**](enter:E20).
* **In cell D22,** type [**Two-Tail Decision**](label:D22).
* **In cell E22,** use the formula
  * [`=IF(E16 <= E20, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:E22)
  * to determine whether to reject the null hypothesis using the two-tailed test p-value.
* **In cell D23,** type [**One-Tail Decision (Lower)**](label:D23).
* **In cell E23,** use the formula
  * [`=IF(E17 <= E20, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:E23)
  * to determine whether to reject the null hypothesis using the one-tailed (lower) test p-value.
* **In cell D24,** type [**One-Tail Decision (Higher)**](label:D24).
* **In cell E24,** use the formula
  * [`=IF(E18 <= E20, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:E24)
  * to determine whether to reject the null hypothesis using the one-tailed (higher) test p-value.

#### Explanation

The **IF statement** simplifies decision-making by evaluating whether the **p-value** is **less than or equal to 0.05** (our significance level). If it is, the test result is **statistically significant**, and you **reject the null hypothesis**, meaning the variance between the two years is significantly different. For instance, if the one-tailed (higher) test p-value is less than **0.05**, you would reject the null hypothesis, indicating that the variance in **2024** is significantly higher than in **2014**. Conversely, if the p-value is greater than **0.05**, you would **fail to reject the null hypothesis**, meaning there is insufficient evidence for the chosen variance alternative; it does not establish equal variances.

This automated process ensures that you can efficiently assess whether there has been a significant change in microbial diversity variance over time in Busse Woods, allowing for a clearer interpretation of the variance comparison.

#### Step: Interpret the Results

You have just conducted the **F-test** to compare the **variance** in microbial diversity between **2014** and **2024**. Your focus is on determining whether the **variability** in the **Shannon Index** has significantly changed. Specifically, you are testing if the **2024 Shannon Index** values are **more uniform** or **more spread out** compared to **2014**.

#### Step-by-Step Tutorial:

* In **cell D26**, type [**Interpretation.**](label:D26)
* **In cell E26**, write a brief interpretation of your findings based on the **F-test** results. Example for the lower-tail alternative:
  * *"With a lower-tail p-value of [calculated value] and alpha = 0.05, we [reject/fail to reject] the null hypothesis, providing [sufficient/insufficient] evidence that the 2024 population variance of Shannon Index values is lower than in 2014."*

#### Explanation:

The interpretation depends on comparing the **p-value** to the **significance level** (**&alpha; = 0.05**). If the p-value is less than or equal to **0.05**, the result is **statistically significant**, and you **reject** the null hypothesis. This provides evidence for the chosen variance alternative. A **one-tailed** test addresses its specified direction; a **two-tailed** test addresses either direction.

If the **p-value** is greater than **0.05**, you **fail to reject** the null hypothesis. This means there is insufficient evidence for the chosen **variance** alternative. It does not establish that microbial diversity in **2024** is **similarly variable**, **more uniform**, or unaffected by environmental factors like **urbanization** or **climate change**.

By interpreting the results of the **F-test**, you can assess evidence for changes in the **variability** of Shannon Index values over time. The test does not identify an environmental cause.

For the original data, **F = 0.42265** with numerator and denominator df **23, 23**. The lower-tail
p-value is about **0.02207**, the two-tail p-value about **0.04413**, and the higher-tail p-value
about **0.97793**. At alpha = 0.05, the lower-tail and two-tail tests reject their null hypotheses;
the higher-tail test fails to reject.

#### Practice Task:

Save a separate practice copy after recording the original result. Modified values are hypothetical examples.

* Change some of the **Shannon Index** values in **Column B** (2014 data) and **Column C** (2024 data). Observe how the **sample standard deviations**, **F-statistic**, and **p-value** adjust.
* Add more sample locations (e.g., increase sample size beyond 30) and see how this impacts the **F-statistic** and **p-value**.
* Answer reflection question 1 in the reflection tab.

#### Key Takeaways:

1. Use the **F-test** to compare the **variability** (variance) between two datasets. This is useful for assessing whether Shannon Index values show more **uniformity** or more **variability** across observations.
2. The **F-distribution** focuses on comparing **variance** rather than **mean** values, giving a clearer picture of changes in **data spread**.
3. Larger **sample sizes** can reduce uncertainty under the model, but do not repair dependence, biased sampling, or nonnormality in the **F-test**.
4. The **F-test** complements the **T-test** by focusing on the **spread** of data in microbial diversity, which can reveal different patterns in diversity summaries over time.

### Part: Part 5 Setup: Expanding the Investigation into More Years with ANOVA

After conducting the **F-test** comparing microbial diversity in **2014** and **2024**, you successfully **rejected the null hypothesis**. The F-test provided evidence that **2024 Shannon Index values** had significantly **less variance** than **2014** under its assumptions; the earlier t-test addressed the **mean**. This raises important questions: Has this trend been ongoing for years? Has the decline in diversity and **reduction in variability** been happening gradually?

As you think about this, an idea strikes. You recall older data in the lab that has not been analyzed for years. Early in your time here, you heard about old student theses where previous graduate students collected microbial diversity data before modern sequencing methods became available. These projects were massive, each representing an entire thesis, where students relied on traditional culture-based techniques to estimate diversity.

Without DNA sequencing, these students used **plate counts** and **staining techniques** to identify and quantify microbial species. They grew colonies on **selective media** and counted **colony-forming units (CFUs)** as a measure of microbial abundance. Colonies differed in **colors, shapes, or growth patterns**. Staining methods like **Gram staining** helped differentiate broad microbial groups, but these traits alone did not uniquely identify every species.

These methods, while labor-intensive, provided valuable **estimates of culturable microbial diversity**. Manual colony counting required days of careful incubation and observation. Despite the limitations of these methods, the meticulous documentation provided solid data that can now offer insights into **microbial ecosystems** before high-throughput technologies.

Culture-based and sequencing-based estimates may detect different organisms and use different taxonomic resolution, confounding year with measurement method. Treat their comparison here as a teaching exercise rather than a validated historical trend.

Inspired by this, you explore three theses from **1994**, **2004**, and **2009**, each containing **Shannon Index values** based on these traditional microbial techniques. Combining this older data with the **2014** and **2024** data gives you a **30-year timeline** of microbial diversity at **Busse Woods**. Now, you are ready to conduct an **ANOVA (Analysis of Variance)** to determine whether at least one population mean Shannon Index differs among years.

With all the data in hand, you can now analyze how microbial diversity has shifted over the decades. **ANOVA** will allow you to compare multiple time points at once, helping you assess whether the changes in diversity across the years are significant.

#### Step: Moving to ANOVA

**ANOVA** allows for the comparison of **multiple groups** simultaneously, unlike a **T-test**, which compares only two. Here, you will analyze microbial diversity across five time points: **1994**, **2004**, **2009**, **2014**, and **2024**. The goal is to determine whether **microbial diversity** has shifted significantly over the past 30 years. **ANOVA** works by comparing the **variance within each year** (how much diversity fluctuated within that year) against the **variance between years** (the overall change in diversity across time).

This analysis will test whether at least one year mean differs. Establishing when declines began, whether periods of stability existed, or whether species composition became more **homogeneous** requires additional analyses and evidence.

***...Ask the instructor for the next tutorial link.***

[https://docs.google.com/document/d/1xkWsWENaOLRHUk6MO50anhL4DEbjmK8_xBmj22k3tts/edit](https://docs.google.com/document/d/1xkWsWENaOLRHUk6MO50anhL4DEbjmK8_xBmj22k3tts/edit)
