# **Microbial Diversity Benchmark T-Test Tutorial** **for BIOL 318/418**

## Workbook

### Sheet: Microbial T-Test

- **Region A1:B101:** source
- **Region C1:E9:** calculation
- **Region C10:E12:** results
- **Region C14:D14:** calculation
- **Region C15:D17:** results
- **Region C19:D19:** interpretation

| "Sample Location" | `"2024\nShannon\nIndex "` | "Statistical Names" | "Values" |
| --- | --- | --- | --- |
| "Andrews Park" | 2.413 |  |  |
| "Beisner Road Entrance" | 3.853 |  |  |
| "Boat Launch Area" | 2.645 |  |  |
| "Busse Lake" | 4.871 |  |  |
| "Debra Park" | 2.357 |  |  |
| "Elk Pasture" | 4.281 |  |  |
| "Forest Central Grove" | 3.433 |  |  |
| "Forest North Grove" | 2.876 |  |  |
| "Forest South Grove" | 4.415 |  |  |
| "Forest West Grove" | 3.46 |  |  |
| "Lake Boating Center" | 2.64 |  |  |
| "Large Event Area" | 5.009 |  |  |
| "Main Dam" | 4.885 |  |  |
| "Main Pool" | 2.805 |  |  |
| "Marshall Park" | 4.733 |  |  |
| "Model Airplane Field" | 4.452 |  |  |
| "Nature Preserve" | 2.749 |  |  |
| "Ned Brown Meadow" | 3.635 |  |  |
| "North Pool" | 4.371 |  |  |
| "Osborn  Park" | 4.906 |  |  |
| "Salt Creek Trail" | 3.985 |  |  |
| "South Pool" | 3.849 |  |  |
| "Wildlife Refuge" | 3.521 |  |  |
| "Woodland Meadow" | 4.982 |  |  |

### Reflection Questions

1. Discuss how the t reference distribution approaches the normal distribution as degrees of freedom increase; this does not make the population SD known or guarantee a smaller p-value.
2. Discuss how the flexibility in **sample size** affects the results of the **one-sample T-test** and compare this to your earlier **z-test** results. Specifically, observe how a larger sample size reduces uncertainty, impacting the p-value and overall hypothesis test results.

## Tutorial

### Part: Scenario:

![Z-test versus t-test.](assets/microbes_2_t_test_image1.png)

For this teaching scenario, assume representative independent observations from normally distributed populations. Choose the hypothesis and alpha = 0.05 before inspecting results; calculating all three tails is a comparison exercise, not permission to select the smallest p-value. The benchmark mean is stipulated to be 4.0; the population standard deviation is unknown.

Now, you face a more realistic challenge. Without knowing the true **population standard deviation** for microbial diversity, you must rely on the **sample standard deviation** from your collected data. This is where the **T-test** comes in. The T-test accounts for the uncertainty that comes from estimating the population standard deviation; a small sample size alone does not determine which test to use.

Feeling the pressure but determined to reach a solid conclusion about the health of Busse Woods, you open your spreadsheet again. This time, you will:

* Calculate the **sample mean** and **sample standard deviation** from your microbial diversity data.
* Perform a **one-sample T-test** to determine if the microbial diversity in Busse Woods is significantly lower than the benchmark value of 4.0, without identifying the cause of any difference

#### Why Use a T-Test Now?

The defining reason and a related consideration:

* **Unknown Population Standard Deviation**
* **Small Sample Size** makes the uncertainty from estimating SD especially important; it is not a separate criterion for choosing a t-test.

In environmental data, like microbial diversity in a forest preserve, the **population standard deviation** is often unknown. Instead, you must estimate it using your **sample's standard deviation**. This uncertainty makes the **T-test** appropriate under the stated assumptions. The **sample size** in your study is small (24 samples), and the t-distribution accounts for the uncertainty from estimating the population standard deviation; it cannot repair biased or dependent observations.

#### Step: Set Up Your Google Sheet for the T-Test

1. Open the generated XLSX workbook in Google Sheets.
2. Select the **"Microbial T-Test"** worksheet; its source data are already supplied.
3. Inspect the source observations before entering calculations.

The original course spreadsheet remains a [source reference](https://docs.google.com/spreadsheets/d/1cAlU997q8IazW6wJhBwYRrrO2l6ls0yCAo3Rx9BlUY0/edit).

4. The data in Column B represents the **Shannon Index** for microbial samples from Busse Woods.

Each year has 24 observations in rows 2:25. Formula ranges extend through row 101 for practice; empty observations are ignored, not treated as zeroes.

#### Step: Set Up the Known Population Values

1. Column C will be used for **Statistical Names**.
2. Column D will contain the calculated values.
3. In cell **C1**, the header already contains **"Statistical Names"**.
4. In cell **D1**, the header already contains **"Values"**.
5. In cell **C2**, type **"[Population Mean](label:C2),"** and in cell **D2**, enter **[4.0](enter:D2)** (the stipulated benchmark for similar ecosystems).

#### Step: Calculate the Sample Statistics

1. In cell **C4**, type **"[Sample Mean](label:C4)."**
2. In cell **D4**, use the **AVERAGE** function to calculate the sample mean for your microbial diversity values:
   * Enter: [`=AVERAGE(B2:B101)`](enter:D4)
3. In cell **C5**, type **"[Sample Standard Deviation](label:C5)."**
4. In cell **D5**, use the **STDEV** function to calculate the sample standard deviation:
   * Enter: [`=STDEV(B2:B101)`](enter:D5)
5. In cell **C6**, type **"[Sample Size](label:C6),"** and in cell **D6**, use the **COUNT** function to count the number of samples:
   * Enter: [`=COUNT(B2:B101)`](enter:D6)

#### Step: Calculate the T-Statistic

1. In cell **C8**, type **"[T-Statistic](label:C8)."**
2. In cell **D8**, use this formula to calculate the t-statistic:
   * Enter: [`=(D4 - D2) / (D5 / SQRT(D6))`](enter:D8)
   * This formula uses the sample mean (D4), the assumed population mean (D2), the sample standard deviation (D5), and the sample size (D6).

#### Explanation: T-Statistic

The **T-statistic** measures how far the **sample mean** is from the **population mean**, relative to the variability in the sample. It accounts for both the **sample standard deviation** and the **sample size**, providing a standardized way to compare the sample to the population. By dividing the difference between the **sample mean** and the **population mean** by the standard error (which is the **sample standard deviation** divided by the square root of the **sample size**), the **T-statistic** allows us to determine how extreme the observed sample is compared to what we would expect if the **null hypothesis** were true.

#### Step: Calculate the Degrees of Freedom

1. In cell **C9**, type **"[Degrees of Freedom](label:C9)."**
2. In cell **D9**, calculate the degrees of freedom using:
   * Enter: [`=D6 - 1`](enter:D9)
   * Here, `D6` is the sample size, so subtracting 1 gives us the degrees of freedom.

#### Explanation: Why Do We Use Degrees of Freedom?

In statistics, **degrees of freedom** represent the number of independent values in a dataset that can vary when estimating a statistical parameter. In the context of a **T-test**, degrees of freedom adjust for the uncertainty introduced when estimating the **population standard deviation** using the **sample standard deviation**.

When calculating the **sample standard deviation**, the deviations from the estimated sample mean must sum to zero, leaving only n - 1 independently varying deviations. This is why we subtract **1** from the **sample size** to get the **degrees of freedom**. Smaller degrees of freedom result in a more conservative test, meaning we need stronger evidence to reject the **null hypothesis**. Larger sample sizes, and therefore more degrees of freedom, lead to a **T-distribution** that more closely resembles a **normal (Z) distribution**.

#### Step: Determine the Type of Test (One-Tailed or Two-Tailed)

Main lower-tail question: H0: mean >= 4.0; H1: mean < 4.0. The two-tailed comparison uses H0: mean = 4.0 versus H1: mean != 4.0; the higher-tail comparison uses H0: mean <= 4.0 versus H1: mean > 4.0.

For the **T-test** on **microbial diversity** data from **Busse Woods**, you need to decide whether you are testing for any **significant difference** or a specific **directional difference** from the benchmark (**Shannon Index** of 4.0).

* **Two-Tailed Test:** Use this when you are checking if the **microbial diversity** is either **higher or lower** than the benchmark. This is for testing any significant deviation from the benchmark, regardless of direction.
* **One-Tailed Test:** Use this when you have a specific hypothesis about the direction of the difference, such as testing if **microbial diversity** is **lower** than the benchmark. A **one-tailed test** focuses on deviations in a single direction.

In this case, since you suspect that the diversity has **decreased** due to **urbanization**, you would likely choose a **one-tailed test (lower)** to check if the **microbial diversity** is significantly **lower** than the benchmark.

#### Step: Calculate the P-Values

In this step, we will calculate p-values: probabilities, under the null model and its assumptions, of results at least as extreme in the specified tail or tails. A p-value is not the probability that the null hypothesis is true or that chance caused the difference.

You will calculate the **p-values** using different approaches: **T.DIST.2T** for the two-tailed test, **T.DIST** for flexible cumulative probability. Each method provides a different way of assessing the statistical significance of your data. By comparing the results from each function, you will gain a clearer understanding of how the **T-test** works in Google Sheets.

##### Substep: Two-Tailed Test:

For the **two-tailed test**, you are testing whether the microbial diversity in **Busse Woods** is either **higher** or **lower** than the benchmark. Here are the function inputs you will use:

**T.DIST.2T(x, degrees\_freedom):** x is the absolute value of the **T-statistic** (calculated in **D8**), and **degrees\_freedom** is provided in **D9**. This function handles both tails of the distribution and calculates the p-value automatically.

**T.DIST(x, degrees\_freedom, cumulative):** x is the absolute value of the **T-statistic**, **degrees\_freedom** is in **D9**, and **cumulative** is set to **TRUE**. You will need to subtract from **1** and multiply by **2** to cover both sides of the distribution.

#### Step-by-Step Tutorial:

* In cell **C10**, type **"[P-Value (Two-Tailed)](label:C10)"**.
* In cell **D10**, enter the formula:
  [`=T.DIST.2T(ABS(D8), D9)`](enter:D10)
* In cell **E10**, enter the formula:
  [`=2 * (1 - T.DIST(ABS(D8), D9, TRUE))`](enter:E10)

#### Explanation for Two-Tailed Test:

In a **two-tailed test**, you are checking whether the **microbial diversity** in Busse Woods is **significantly higher or lower** than the **benchmark**. The formula starts by calculating the **absolute value** of the **T-statistic** using **ABS(D8)**. This captures the **magnitude of the difference** between the **sample mean** and the **benchmark**.

The **T.DIST.2T** function handles **both tails** of the **distribution**. This means the result automatically accounts for deviations in **both directions**.

The second formula, **T.DIST**, requires you to handle **both sides manually**. First, calculate the **cumulative probability** for **one tail** using **T.DIST**. Then, subtract it from 1 to capture the **upper tail**. Finally, multiply by 2 to account for both **upper and lower tails**.

##### Substep: One-Tailed Test (for lower values):

For the **one-tailed test**, you are interested in testing whether the microbial diversity in **Busse Woods** is **lower** than the benchmark. This test compares diversity with the benchmark without identifying an environmental cause. Here are the function inputs:

**T.DIST(x, degrees\_freedom, cumulative):** x is the **T-statistic** (calculated in **D8**), degrees\_freedom is in **D9**, and **cumulative** is set to **TRUE**. This function calculates the cumulative probability for values less than or equal to the **T-statistic**.

#### Step-by-Step Tutorial:

* In cell **C11**, type **"[P-Value (One-Tailed, Lower)](label:C11)"**.
* In cell **D11**, enter the formula:
  [`=T.DIST(D8, D9, TRUE)`](enter:D11)
* Leave cell **E11** blank

#### Explanation for One-Tailed Test (Lower):

In a **one-tailed test**, you are only interested in whether the microbial diversity is **lower** than the benchmark. The **T.DIST** function calculates the **cumulative probability** for values **less than or equal to** the **T-statistic**, meaning you are testing for values in the **lower tail** of the distribution. Use the signed T-statistic so that a positive statistic gives a large lower-tail probability. T.TEST requires two samples and is not used for this one-sample benchmark test.

##### Substep: One-Tailed Test (for higher values):

Although you are testing whether the microbial diversity is **lower** than the benchmark, it is also useful to calculate the **p-value** for the **opposite direction** to understand how much diversity might exceed expectations. Here are the function inputs for the **one-tailed test** for higher values:

**1 - T.DIST(x, degrees\_freedom, TRUE):** x is the signed **T-statistic**, and **degrees\_freedom** is in **D9**. Subtract the cumulative probability from one to test for an increase in diversity.

**T.DIST(x, degrees\_freedom, cumulative):** x is the **T-statistic** (calculated in **D8**), degrees\_freedom is in **D9**, and **cumulative** is set to **TRUE**. This function calculates the cumulative probability for values less than or equal to the **T-statistic**. In order to get values above, we subtract this result from one.

#### Step-by-Step Tutorial:

* In cell **C12**, type **"[P-Value (One-Tailed, Higher)](label:C12)"**.
* In cell **D12**, enter the formula:
  [`=1 - T.DIST(D8, D9, TRUE)`](enter:D12)
* In cell **E12**, enter the formula:
  [`=T.DIST(-D8, D9, TRUE)`](enter:E12)

#### Explanation for One-Tailed Test (Higher):

This test examines whether the microbial diversity in **Busse Woods** is **higher** than the benchmark, testing for potential **increases** in biodiversity. The complement of **T.DIST** calculates the probability of obtaining a **T-statistic** greater than or equal to the calculated value, which is ideal for testing whether the diversity exceeds the benchmark. This approach provides insight into the **upper tail** of the distribution and how microbial diversity might vary in the **opposite direction** of your primary hypothesis.

#### Step: Decision Using an IF Statement

In hypothesis testing, the decision to **reject** or **fail to reject** the null hypothesis depends on comparing the p-value to a predetermined significance level (&alpha;). Typically, &alpha; is set at 0.05, meaning if the p-value is less than or equal to 0.05, we consider the result **statistically significant** and reject the null hypothesis. To streamline this decision process in Google Sheets, we will use the **IF statement**, which evaluates a condition and returns one value if the condition is true and another if false. In this case, we will check whether the p-value is less than or equal to &alpha;.

#### Step-by-Step Tutorial:

* In **cell C14**, type "**[Significance Level (&alpha;)](label:C14)**." In **cell D14**, enter **[0.05](enter:D14)**.
* In **cell C15**, type "**[Two-Tail Decision](label:C15)**."
* In **cell D15**, use the **IF statement** to determine whether to reject the null hypothesis using the two-tailed test p-value:
  **Formula:** [`=IF(D10 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D15)
* In **cell C16**, type "**[One-Tail Decision (Lower)](label:C16).**"
* In **cell D16**, use the **IF statement** to determine whether to reject the null hypothesis using the one-tailed (lower) test p-value:
  **Formula:** [`=IF(D11 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D16)
* In **cell C17**, type "**[One-Tail Decision (Higher)](label:C17).**"
* In **cell D17**, use the **IF statement** to determine whether to reject the null hypothesis using the one-tailed (higher) test p-value:
  **Formula:** [`=IF(D12 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D17)

#### Explanation

The **IF statement** is a basic yet powerful programming concept that allows the program to evaluate a condition and make decisions. Here, we use it to compare the **p-value** to the **significance level (&alpha;)** and automate the decision-making process in hypothesis testing.

In statistical analysis, if the **p-value** is less than or equal to the **significance level (0.05)**, the result is considered **statistically significant**, meaning there is sufficient evidence to reject the null hypothesis. For instance, if the two-tailed test's p-value is <= 0.05, we reject the null hypothesis, indicating that microbial diversity in **Busse Woods** is **significantly different** from the benchmark. Conversely, if the p-value exceeds 0.05, we **fail to reject** the null hypothesis, meaning there is insufficient evidence of a difference; equality with the benchmark is not established.

This process helps determine whether the data support a difference in microbial diversity at Busse Woods relative to the benchmark; it does not establish an environmental cause.

#### Step: Interpret the Results

At this point, you should have conducted both the **two-tailed** and **one-tailed tests** (lower and higher) to compare the microbial diversity in **Busse Woods** against the benchmark value (Shannon Index \= 4.0). You should have determined that the focus is on the **One-Tailed Test (Lower)** to assess whether microbial diversity in **Busse Woods** is **significantly lower** than the benchmark. The goal is to determine if diversity is lower than the benchmark, without attributing a difference to an environmental cause. You are specifically testing if the microbial diversity in **Busse Woods** has decreased compared to the expected average for similar ecosystems.

#### Step-by-Step Tutorial:

1. In **cell C19**, type **[Interpretation](label:C19)**.
2. In **cell D19**, write a brief interpretation of your findings based on the one-tailed (lower) test. Example: "With a p-value of \[calculated value\], we \[reject/fail to reject\] the null hypothesis, indicating that the data \[provide/do not provide\] sufficient evidence of a population mean lower than the benchmark."

#### Explanation:

In hypothesis testing, the interpretation depends on comparing the **p-value** to the **significance level** (&alpha; \= 0.05). If the **p-value** is **less than or equal to 0.05**, the result is considered **statistically significant**, meaning the null hypothesis is **rejected**. Rejecting the null hypothesis in this case suggests that microbial diversity in **Busse Woods** is **significantly lower** than the benchmark value of **4.0** (representing the average diversity for similar ecosystems). This does not establish that **urbanization**, **pollution**, or **climate change** caused the difference.

If the **p-value is greater than 0.05**, you **fail to reject** the null hypothesis. This means there is **insufficient evidence** to conclude that microbial diversity is lower than the benchmark. This does not establish equality with the benchmark or rule out an environmental effect.

Completing this interpretation allows you to clearly state whether the data provide evidence that microbial diversity in **Busse Woods** is lower than the benchmark, based on the results of your hypothesis test. This helps you draw meaningful conclusions about the **health of the ecosystem** and whether the data supports the hypothesis that biodiversity in **Busse Woods** has declined.

#### Practice Task:

Save a separate practice copy after recording the original result. Add hypothetical numeric observations only within rows 2:101; leave unobserved cells blank.

* Change some of the **Shannon Index** values for microbial diversity in **Column B** (Busse Woods data). Observe how the **sample standard deviation**, **t-statistic**, and **p-value** adjust automatically.
* Add more sample locations (e.g., increasing the sample size beyond 30\) and note how the **p-value** changes. Answer reflection question 1 in the reflection tab.
* Answer reflection question 2 in the reflection tab.

#### Key Takeaways:

1. Use the **one-sample T-test** when comparing a dataset (e.g., **Shannon Index** values for microbial diversity in **Busse Woods**) to a known benchmark when the **population standard deviation is unknown** under the stated sampling assumptions.
2. The **t-distribution** accounts for additional uncertainty introduced by using the **sample standard deviation** instead of the population standard deviation.
3. As the **sample size increases**, the t reference distribution approaches the normal reference distribution. This occurs because the **t-distribution** approximates the **normal distribution** as the sample size becomes larger, making their reference probabilities more similar when the standardized statistics are comparable; the population SD remains unknown.
4. The **one-sample T-test** is particularly useful for assessing whether microbial diversity in **Busse Woods** has significantly declined in comparison to the benchmark, especially when the sample size is limited.

#### Setup: Microbial Diversity at Busse Woods

After conducting the **T-test** on microbial diversity at **Busse Woods**, your confidence in the significant difference from the benchmark began to waver. The results of the **T-test** did not confirm the earlier findings from the **Z-test**, and you now question whether the diversity at **Busse Woods** is truly different from the benchmark.

This project is important to you. For months, your team has monitored the effects of **urbanization** and **climate change** on biodiversity in urban forest preserves. **Busse Woods**, once considered a pristine environment, has shown signs of stress in recent years. Your goal was to provide hard data showing whether these changes were affecting **microbial ecosystems**, a key indicator of environmental health. While the **Z-test** initially suggested a significant shift, the new results call that conclusion into doubt.

Just as you were preparing to discard your report and start over, your advisor suggested a new approach. You both remembered that your team has access to a rich dataset from **2014**, a time when concerns about rising temperatures and pollution were increasing. Instead of only comparing the current data to a benchmark, your advisor proposed analyzing changes over time. This could provide a clearer picture of how **Busse Woods** has evolved in response to **environmental pressures**.

By comparing your current data from **2024** with diversity data collected in **2014**, you can determine whether there has been a significant decrease in microbial diversity over the last decade. This comparison over time will test for a difference in the mean Shannon Index; it cannot establish how environmental factors affected **Busse Woods' microbial communities**.

#### Moving to the Two Sample T-Test

In the next part of this tutorial, we will learn how to conduct a **Two Sample T-test**, which allows for a direct comparison between **two different datasets**. By comparing microbial diversity from **Busse Woods in 2014** with your current data from **2024**, you will gain insights into how the ecosystem has changed over the past decade. This analysis could reveal a difference in mean diversity, without identifying whether **urbanization** or **climate change** caused it. The findings from this comparison may provide stronger evidence to support conservation efforts and inform future environmental policies.

***...Ask the instructor for the next tutorial link.***
