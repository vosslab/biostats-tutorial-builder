# **Microbial Diversity Z-Test Tutorial** **for BIOL 318/418**

## Workbook

### Sheet: Microbial Z-Test

- **Region A1:B101:** source
- **Region C1:D9:** calculation
- **Region C10:D12:** results
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

1. Discuss how both **changing the dataset size** and modifying individual Shannon Index values impacts the hypothesis test results.

## Tutorial

### Part: Scenario:

![Busse Woods, with wooded shorelines around the lake.](assets/microbes_1_z_test_image1.png)

For this teaching scenario, assume representative independent observations from normally distributed populations. Choose the hypothesis and alpha = 0.05 before inspecting results; calculating all three tails is a comparison exercise, not permission to select the smallest p-value. Treat the benchmark mean 4.0 and population standard deviation 0.6 as known stipulated values.

Urbanization around **Busse Woods** may have disrupted the ecosystem, leading to a possible decline in microbial diversity. By comparing the current microbial diversity in **Busse Woods** to the benchmark for similar ecosystems, we can ask whether microbial diversity is lower than the benchmark; this comparison cannot identify an environmental cause. You are analyzing microbial diversity in soil samples collected from different locations in **Busse Woods Forest Preserve** using **SSU rRNA sequencing**. Urbanization around **Busse Woods** is raising concerns that human activities and environmental pressures may be negatively affecting soil health and biodiversity.

The **Shannon Index** is a widely used measure of biodiversity that takes into account both the number of species present, known as **species richness**, and how evenly individuals are distributed among those species, known as **evenness**. The index is calculated by summing the proportion of individuals belonging to each species in a community and multiplying this by the natural logarithm of that proportion, then summing the results for all species and taking the negative of the total. A higher **Shannon Index** value indicates greater biodiversity, with no universal upper bound independent of community size and logarithm base.

The primary goal of this exercise is to determine whether microbial diversity (measured using the **Shannon Index**) in **Busse Woods** has decreased compared to the benchmark of 4.0, which is stipulated for similar ecosystems in this exercise. The population standard deviation for microbial diversity in similar ecosystems is stipulated to be known and equal to 0.6.

In this tutorial, you will use **Google Sheets** to conduct a **Z-test** using the sample data to investigate whether microbial diversity at **Busse Woods** is lower than the benchmark.

* **null hypothesis, H<sub>0</sub>**: The population mean microbial diversity in the forest preserve is at least the benchmark (Shannon Index >= 4.0).
* **alternative hypothesis, H<sub>a</sub>**: The population mean microbial diversity in the forest preserve is lower than the benchmark (Shannon Index < 4.0).

#### Step: Find Your Copy of the Spreadsheet

1. Open the generated XLSX workbook in Google Sheets.
2. Select the **"Microbial Z-Test"** worksheet; its source data are already supplied.
3. Inspect the source observations before entering calculations.

The original course spreadsheet remains a [source reference](https://docs.google.com/spreadsheets/d/1cAlU997q8IazW6wJhBwYRrrO2l6ls0yCAo3Rx9BlUY0/edit).

4. The data in Column B represents the **Shannon Index** for microbial samples from Busse Woods.

Each year has 24 observations in rows 2:25. Formula ranges extend through row 101 for practice; empty observations are ignored, not treated as zeroes.

#### Step: Set Up the Known Population Values

1. **Column C** will be used for **Statistical Names**.
2. **Column D** will contain the **calculated values**.
3. In **cell C1**, the header already contains **"Statistical Names"**.
4. In **cell D1**, the header already contains **"Values"**.
5. In **cell C2**, type **"[Population Mean](label:C2)"**, and in **cell D2**, enter **[4.0](enter:D2)** (the stipulated benchmark for similar ecosystems).
6. In **cell C3**, type **"[Population Standard Deviation](label:C3)"**, and in **cell D3**, enter **[0.6](enter:D3)** (the stipulated known population standard deviation).

#### Step: Calculate the Sample Mean

1. In **cell C5**, type **"[Sample Mean](label:C5)"**.
2. In **cell D5**, use the **AVERAGE** function to calculate the sample mean for your microbial diversity values:
   * Enter: [`=AVERAGE(B2:B101)`](enter:D5)
   * This formula calculates the mean of Shannon Index values from cells B2 to B101, allowing for flexibility if you add more data. It will automatically ignore empty cells.
3. In **cell C6**, type **"[Sample Size](label:C6)"**, and in **cell D6**, use the **COUNT** function to count the number of samples:
   * Enter: [`=COUNT(B2:B101)`](enter:D6)

#### Step: Calculate the Z-Statistic

1. In **cell C8**, type **"[Z-Statistic](label:C8)"**.
2. In **cell D8**, calculate the Z-statistic using the formula:
   * Enter: [`=(D5 - D2) / (D3 / SQRT(D6))`](enter:D8)
   * This formula uses the sample mean (D5), population mean (D2), population standard deviation (D3), and sample size (D6). The Z-statistic helps you determine how far the sample mean is from the population mean, accounting for sample size.

#### Explanation:

The Z-statistic standardizes the difference between the **sample mean** and the **population mean** by converting it into units of standard error. This allows you to assess whether the observed microbial diversity at Busse Woods is significantly different from the expected diversity.

#### Step: Determine the Type of Test (One-Tailed or Two-Tailed)

Main lower-tail question: null hypothesis, H<sub>0</sub>: mean >= 4.0; alternative hypothesis, H<sub>a</sub>: mean < 4.0. The two-tailed comparison uses null hypothesis, H<sub>0</sub>: mean = 4.0 versus alternative hypothesis, H<sub>a</sub>: mean != 4.0; the higher-tail comparison uses null hypothesis, H<sub>0</sub>: mean <= 4.0 versus alternative hypothesis, H<sub>a</sub>: mean > 4.0.

When performing a Z-test on microbial diversity data from Busse Woods, you need to decide whether you are testing for **any significant difference** or a **specific directional difference** from the known benchmark (Shannon Index of 4.0).

#### **Two-Tailed Test:**

This is used when you want to test if there is any **significant difference** in the microbial diversity of your forest preserve, regardless of whether it's higher or lower than the known benchmark. You're checking for **any deviation** from the benchmark value.

* **Example Hypothesis**:

  * **null hypothesis, H<sub>0</sub>**: The average microbial diversity in the forest preserve is equal to the benchmark (Shannon Index \= 4.0).

  * **alternative hypothesis, H<sub>a</sub>**: The average microbial diversity in the forest preserve is different from the benchmark (either higher or lower).

Use a **two-tailed test** if you do not have a specific expectation about whether the microbial diversity is **higher or lower** than the benchmark. You're testing for any difference.

#### **One-Tailed Test:**

This is used when you have a **specific direction** in mind. For example, if you believe that the microbial diversity in your forest preserve is **higher** than the benchmark, you would use a **one-tailed test**.

* **Example Hypothesis**:

  * **null hypothesis, H<sub>0</sub>**: The microbial diversity in the forest preserve is less than or equal to the benchmark (Shannon Index <= 4.0).

  * **alternative hypothesis, H<sub>a</sub>**: The microbial diversity in the forest preserve is **greater** than the benchmark (Shannon Index \> 4.0).

Use a **one-tailed test** if you have a specific hypothesis about whether the microbial diversity is **higher** (or lower, if reversed) than the benchmark. This allows you to test for a **directional** difference.

#### Step: Calculate the P-Values

To help **you** better understand the different types of tests and how p-values are calculated, **we will guide you** through the steps for calculating all possible p-values (one-tailed and two-tailed).

##### Substep: Two-Tailed Test:

A two-tailed test is used when you want to check for any difference, whether microbial diversity in Busse Woods is higher or lower than the benchmark.

* **In cell C10**, type **"[P-Value (Two-Tailed)](label:C10)"**.
* **In cell D10**, enter the formula:
  [`=2 * (1 - NORM.DIST(ABS(D8), 0, 1, TRUE))`](enter:D10)

#### Explanation for Two-Tailed Test:

In a two-tailed test, **you're checking for deviations in both directions**-whether microbial diversity is higher or lower than the benchmark. The formula starts by calculating the **absolute value** of the Z-statistic using the **`ABS(D8)`** function, which ensures **we only focus on the magnitude** of the difference between the sample mean and the benchmark. This step is crucial since we're concerned with both positive and negative deviations.

The function **`NORM.DIST(ABS(D8), 0, 1, TRUE)`** gives the cumulative probability to the left of the absolute Z-statistic **you've calculated**. Since **we want to test both sides** (higher and lower), we subtract this value from 1 to find the **probability in the upper tail**, and then multiply by 2 to account for both tails. **This final formula ensures you include both extremes** in your analysis.

However, because we are performing a **two-tailed test**, we are interested in deviations in **both directions**-whether the microbial diversity in Busse Woods is **higher or lower** than the benchmark. To account for this, we first need to find the probability in the **upper tail** of the distribution. The function **`NORM.DIST(ABS(D8), 0, 1, TRUE)`** gives the cumulative probability for the area under the curve to the **left** of the absolute value of the Z-statistic (i.e., the probability that the Z-statistic is less than or equal to this value). To find the probability of observing a Z-statistic **greater than or equal to the absolute value** of D8 (the upper tail), we subtract this cumulative probability from **1**. This gives us the likelihood of observing a value in the **right tail** of the distribution, beyond the calculated Z-statistic.

Take a look at this image of the **normal distribution curve**, which will help visualize this process:
![A standard normal curve with the area left of Z = -1 shaded.](assets/microbes_1_z_test_image2.png)
The shaded area to the left of **Z \= -1** in the image represents **P(Z \< -1)**, or the cumulative probability to the left of -1. This area is given by **`NORM.DIST(-1, 0, 1, TRUE)`**. The complement of this illustrated cumulative probability is the area to the right of -1. For our two-tailed calculation, instead subtract the cumulative probability at **ABS(D8)** from **1** to obtain the upper tail beyond the positive magnitude. By the symmetry of the normal distribution, **`1 - NORM.DIST(ABS(D8), 0, 1, TRUE)`** is equivalent to **`NORM.DIST(-ABS(D8), 0, 1, TRUE)`**, since the normal curve is symmetric around zero. Both approaches give the probability of observing a value in the **upper tail**.

Since we are conducting a **two-tailed test**, we need to account for **extreme values in both tails**-those significantly **higher** and those significantly **lower** than the benchmark. To do this, we multiply the **upper tail probability** by **2**, which ensures that we include both the **left** and **right** tails of the distribution. The final formula, **`2 * (1 - NORM.DIST(ABS(D8), 0, 1, TRUE))`**, gives the total probability of observing a Z-statistic as extreme or more extreme than the one calculated, regardless of direction.

##### Substep: One-Tailed Test (for lower values):

A one-tailed test is used when you have a specific directional hypothesis. In this case, we are testing if microbial diversity in Busse Woods is **lower** than the benchmark.

* **In cell C11**, type **"[P-Value (One-Tailed, Lower)](label:C11)"**.
* **In cell D11**, enter the formula:
  [`=NORM.DIST(D8, 0, 1, TRUE)`](enter:D11)

#### Explanation for One-Tailed Test (Lower):

For a one-tailed test, we are only interested in whether microbial diversity is **lower** than the benchmark. The function **`NORM.DIST(D8, 0, 1, TRUE)`** calculates the cumulative probability of observing a Z-statistic less than or equal to the calculated Z-statistic. This directly gives us the p-value for the **lower tail**, which is the probability, under the null model, of a Z-statistic this low or lower.

##### Substep: One-Tailed Test (for higher values):

Even though the hypothesis is about **lower** microbial diversity, we can still calculate the p-value for the **opposite direction** (whether microbial diversity is **higher** than the benchmark) to see how such results would be interpreted.

* **In cell C12**, type **"[P-Value (One-Tailed, Higher)](label:C12)"**.
* **In cell D12**, enter the formula:
  [`=1 - NORM.DIST(D8, 0, 1, TRUE)`](enter:D12)

#### Explanation for One-Tailed Test (Higher):

For testing whether microbial diversity is **higher** than the benchmark, we calculate the complement of the cumulative probability. The function **`NORM.DIST(D8, 0, 1, TRUE)`** gives the cumulative probability for values **less than or equal** to D8. By subtracting this value from **1**, we obtain the probability of observing a value **greater than** the calculated Z-statistic, representing the probability, under the null model, of a Z-statistic this high or higher.

#### Step: Make a Decision Using an IF Statement

In hypothesis testing, the decision to reject or fail to reject the null hypothesis depends on the comparison between the p-value and the significance level (&alpha;). The significance level is typically set at 0.05, meaning that if the p-value is less than or equal to 0.05, we consider the result statistically significant and reject the null hypothesis.

To automate this decision-making process in Google Sheets, **we use the IF statement**, a logical function that **evaluates a condition** and returns one value if the condition is true, and another if it is false. In this case, the condition will check **whether the p-value is less than or equal to the significance level**.

1. In **cell C14**, type **"[Significance Level (&alpha;)](label:C14)."**
2. In **cell D14**, enter **[0.05](enter:D14)**.
3. In **cell C15**, type **"[Two-Tail Decision](label:C15)."**
4. In **cell D15**, use an **IF statement** to determine whether to reject the null hypothesis using the two-tailed p-value:
   * [`=IF(D10 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D15)
5. In **cell C16**, type **"[One-Tail Decision (Lower)](label:C16)"**
6. In **cell D16**, use the IF statement to make a decision based on the one-tailed lower p-value:
   * [`=IF(D11 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D16)
7. In **cell C17**, type **"[One-Tail Decision (Higher)](label:C17)"**
8. In **cell D17**, use the IF statement to make a decision based on the one-tailed higher p-value:
   * [`=IF(D12 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`](enter:D17)

#### Explanation

The **IF statement** is a fundamental programming concept that allows you to make decisions based on conditions. In this case, **we use it to compare** the p-value to the significance level (**&alpha;**) and **decide** whether to reject or fail to reject the null hypothesis.

In hypothesis testing, if the **p-value is less than or equal to the significance level** (0.05), we consider the result **statistically significant**. This means you have enough evidence to reject the null hypothesis. For example, if we are conducting a two-tailed test and the two-tailed p-value is less than or equal to 0.05, we reject the null hypothesis, which would indicate that microbial diversity in Busse Woods is significantly different from the benchmark. If the p-value is greater than 0.05, the evidence is insufficient to reject the null hypothesis, meaning there is insufficient evidence of a difference; this does not establish equality.

For one-tailed tests, we perform the same comparison but only focus on testing either higher or lower values. The formula **`IF(D11 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`** is used when testing whether microbial diversity is lower than the benchmark. If the p-value is less than or equal to 0.05, we reject the null hypothesis and conclude that microbial diversity is significantly lower. Conversely, for testing whether microbial diversity is higher than the benchmark, the formula **`IF(D12 <= D14, "Reject the Null Hypothesis", "Fail to Reject the Null Hypothesis")`** performs the same function, but focused on higher values. If the p-value in this case is less than or equal to 0.05, we reject the null hypothesis and conclude that the microbial diversity is significantly higher.

By using the IF statement in Google Sheets, you can automate the process of making these decisions based on your p-values, ensuring clarity and accuracy in interpreting the results of your hypothesis tests.

#### Step: Interpret the Results

At this point, you should have determined that we are only interested in the results of the **one-tailed (lower)** test. You are specifically testing whether the microbial diversity in Busse Woods is **lower than the benchmark**. This comparison does not identify whether urbanization or other environmental pressures caused a difference. The goal is to see if the data supports the hypothesis that microbial diversity has declined.

1. In **cell C19**, type **"[Interpretation](label:C19)"**.
2. In **cell D19**, write a brief interpretation of your findings based on the one-tailed (lower) test:
   **One-Tailed Test Example (Lower):**
   "With a p-value of \[calculated value\], we \[reject/fail to reject\] the null hypothesis, indicating that the data \[provide/do not provide\] sufficient evidence of a population mean lower than the benchmark."

#### Explanation:

In hypothesis testing, the interpretation relies on comparing the **p-value** to the significance level (**&alpha; \= 0.05**). If the p-value is less than or equal to 0.05, the result is considered **statistically significant**, and the null hypothesis is rejected. Rejecting the null hypothesis means that the data provides enough evidence to conclude that microbial diversity in Busse Woods is **significantly lower** than the benchmark. This does not establish that environmental factors, such as urbanization, caused the difference.

If the p-value is greater than 0.05, you fail to reject the null hypothesis. This means there is **not enough evidence** to claim that microbial diversity is lower than the benchmark. This does not establish equality with the benchmark or rule out an effect of external factors.

By completing this interpretation, you can clearly state whether the data provide evidence of lower microbial diversity in Busse Woods based on your hypothesis test results. This helps you draw a meaningful conclusion about the health of the ecosystem.

#### Practice Task:

Save a separate practice copy after recording the original result. Add hypothetical numeric observations only within rows 2:101; leave unobserved cells blank.

* **Add more diversity index values** to Column B. Observe how the **Z-statistic** and **p-value** adjust as you increase the sample size. Notice how adding more data points, especially extreme values, can affect the outcome of the hypothesis test. This will help you understand the sensitivity of the test to the number of samples.
* **Modify some existing values** in Column B by increasing or decreasing the Shannon Index values. Watch how the **Z-statistic** and **p-value** change as a result. This will show how changes to individual values can impact the test results. Try adding values that are either much higher or much lower than the current ones to see the extent of the changes.
* Answer reflection question 1 in the reflection tab. Think about how a larger representative independent sample can reduce the standard error, while extreme individual values might skew the results; more data do not guarantee a smaller p-value or repair biased sampling. This exercise will reinforce the importance of both sample size and data consistency in hypothesis testing.

#### Key Takeaways:

1. **Flexibility:** This setup allows you to vary the number of samples dynamically by entering values in **Column B**. By using a flexible range (B2:B101), you can observe how adding or removing data points influences the outcome of the test. This highlights how sample size plays a critical role in the reliability of statistical results, especially in ecological data where sample numbers can vary widely.
2. **Z-Statistics**: Z-statistics provide a standardized way to compare the **sample mean** to a known **population mean**. Even when the sample size changes, using the Z-statistic allows for a clear comparison. Understanding how to standardize values using Z-statistics is essential for comparing your sample to a benchmark, helping you determine whether the microbial diversity in Busse Woods deviates significantly from the expected value.
3. **Dynamic Calculations**: One of the advantages of using Google Sheets is that it automatically recalculates the **Z-statistic** and **p-value** when you modify the data. This allows you to perform real-time analysis and instantly see how changes in your data affect the results. Being able to experiment with different values and sample sizes will help you better grasp the relationship between your data and hypothesis testing, showing the effects of data changes without needing to manually recalculate each time.

#### Setup: Microbial Diversity at Busse Woods

After conducting the Z-test on microbial diversity at Busse Woods, you were confident that the diversity was significantly lower than the benchmark in the preselected lower-tail test. You were ready to present your findings and celebrate a successful environmental analysis.

However, just as you began preparing your report, your supervisor sent a critical email:

"*While you compared Busse Woods' microbial diversity to the benchmark using a Z-test, we noticed a major issue. You assumed that the population standard deviation was known, but for environmental data like this, making that assumption is risky. Ecosystems vary greatly depending on factors like soil type and vegetation cover, and these can differ even within the same location. The key question is whether the population standard deviation is truly known, not whether N is below 30. If it is unknown, you should be using a T-test, which accounts for the extra uncertainty when estimating the population standard deviation from your sample data. To validate your findings, you must redo the analysis using a T-test.*"

You realize that the Z-test may not have been appropriate because of these assumptions. To ensure the accuracy of your conclusions, you now need to switch to a **T-test** and recalculate your results. This new approach will take into account the uncertainty in estimating the population standard deviation. By using the T-test, you hope to avoid any doubts about the validity of your findings and deliver a solid environmental assessment.

#### Moving to the T-Test

In the next part of this tutorial, we will learn how to conduct a **T-test** when the population standard deviation is **unknown**, and the sample size is relatively small. The **T-test** adjusts for the extra uncertainty when estimating the population standard deviation from the sample, under the stated sampling assumptions.

***...Ask the instructor for the next tutorial link.***
