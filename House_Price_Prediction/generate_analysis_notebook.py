"""
Script to generate notebooks/02_Statistical_Analysis.ipynb
Using nbformat for programmatic generation of valid JSON notebook structure.
"""

import nbformat as nbf
import os

nb = nbf.v4.new_notebook()
cells = []

# Title & Metadata
cells.append(nbf.v4.new_markdown_cell("""# House Area, Age and Property Price Prediction
## Notebook 2 — Statistical Analysis and Predictive Modelling

**Course:** Probability and Statistics  
**Dataset:** Real Estate Valuation Data Set — UCI Machine Learning Repository (ID 477)  
**Citation:** Yeh, I. (2018). Real Estate Valuation [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5J30W  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)"""))

# SECTION 1 — Introduction
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 1 — Introduction

### Objective
The objective of this notebook is to conduct a complete statistical analysis and predictive modeling workflow on the Real Estate Valuation dataset. We investigate how property characteristics relate to property valuation, test statistical hypotheses regarding location proximity and house age, and evaluate linear regression models on unseen test data.

### Dataset Source & Background
The dataset originates from the **UCI Machine Learning Repository** (ID 477), compiled by I-Cheng Yeh (2018). It comprises **414 historical property transactions** collected from **Sindian District, New Taipei City, Taiwan** between 2012 and 2013.

### Variables in Study
- **Target Variable ($Y$):** `Y house price of unit area` — measured in **10,000 New Taiwan Dollars (NTD) per Ping** ($1\\text{ Ping} \\approx 3.3\\text{ m}^2$).
- **Main Predictors ($X$):**
  - `X2 house age` (Years)
  - `X3 distance to the nearest MRT station` (Metres)
- **Additional Variables:**
  - `X1 transaction date` (Decimal year)
  - `X4 number of convenience stores` (Count)
  - `X5 latitude` & `X6 longitude` (Geographic coordinates)
  - `No` (Transaction identifier — excluded from all statistical and predictive models)

### Crucial Dataset Limitations
1. **Target Variable Definition:** The target variable is price *per unit area*, **not total property price**.
2. **Missing Total House Area:** The dataset does **not** contain total house floor area or total transaction price. We do not invent or fabricate either variable.
3. **Geographical & Temporal Specificity:** Observations are historical records from Sindian District, New Taipei City. Generalizing inferences beyond this district and period requires caution.

### Statistical Techniques Covered
1. **Descriptive Statistics:** Measures of central tendency, dispersion, and quartiles.
2. **Inferential Statistics:** One-sample $t$-based 95% Confidence Interval for the mean price.
3. **Two-Sample Welch's $t$-test & Mann-Whitney $U$ test:** Comparing prices across MRT proximity groups.
4. **One-Way ANOVA & Post-Hoc Tests:** Comparing prices across house-age tertiles.
5. **Correlation Analysis:** Pearson linear and Spearman rank correlations with heatmap.
6. **Simple Linear Regression (SLR):** Modeling price using house age via OLS.
7. **Multiple Linear Regression (MLR):** Modeling price using house age and MRT distance with full diagnostics and VIF.
8. **Train-Test Evaluation (80:20 Split):** Evaluating MAE, MSE, RMSE, and $R^2$ on held-out test data.
9. **Sample Predictions:** Practical valuation for realistic property profiles."""))

# SECTION 2 — Importing Libraries and Loading Data
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 2 — Importing Libraries and Loading Data

We import standard, well-documented Python scientific libraries. We set a global random seed of `42` to ensure complete reproducibility."""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

# Set visual style and reproducibility seed
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(42)

# Ensure figures output directory exists
figures_dir = os.path.join('..', 'outputs', 'figures')
os.makedirs(figures_dir, exist_ok=True)

print("Libraries imported successfully. Figure directory verified.")"""))

cells.append(nbf.v4.new_code_cell("""# Load the raw dataset from data/raw/
data_path = os.path.join('..', 'data', 'raw', 'real_estate_valuation.csv')
df = pd.read_csv(data_path)

# Verify shape and display first 5 rows
print(f"Dataset Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
df.head()"""))

cells.append(nbf.v4.new_code_cell("""# Define analysis dataframe excluding the identifier 'No'
if 'No' in df.columns:
    df_model = df.drop(columns=['No'])
    print("Identifier column 'No' successfully excluded from analysis dataframe.")
else:
    df_model = df.copy()

# Convenient short variable names for plotting and modelling
target = 'Y house price of unit area'
age = 'X2 house age'
mrt = 'X3 distance to the nearest MRT station'
stores = 'X4 number of convenience stores'"""))

# SECTION 3 — Descriptive Statistical Analysis
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 3 — Descriptive Statistical Analysis

We calculate the complete suite of descriptive statistics for the four primary variables:
- `X2 house age`
- `X3 distance to the nearest MRT station`
- `X4 number of convenience stores`
- `Y house price of unit area`

For each variable, we calculate:
$$\\text{Mean, Median, Mode, Variance, Standard Deviation, Min, Max, Range, } Q_1, Q_3, \\text{ and } \\text{IQR}$$"""))

cells.append(nbf.v4.new_code_cell("""# Compute descriptive statistics table
selected_vars = [age, mrt, stores, target]
stats_dict = {}

for col in selected_vars:
    series = df_model[col]
    mode_res = stats.mode(series, keepdims=True).mode[0]
    q1 = np.percentile(series, 25)
    q3 = np.percentile(series, 75)
    iqr = q3 - q1
    rng = series.max() - series.min()
    
    stats_dict[col] = {
        'Mean': round(series.mean(), 3),
        'Median': round(series.median(), 3),
        'Mode': round(mode_res, 3),
        'Variance': round(series.var(), 3),
        'Std Dev': round(series.std(), 3),
        'Minimum': round(series.min(), 3),
        'Maximum': round(series.max(), 3),
        'Range': round(rng, 3),
        'Q1 (25%)': round(q1, 3),
        'Q3 (75%)': round(q3, 3),
        'IQR': round(iqr, 3)
    }

desc_table = pd.DataFrame(stats_dict).T
print("Comprehensive Descriptive Statistics Summary:")
desc_table"""))

cells.append(nbf.v4.new_markdown_cell("""### Visualizations: Distributions and Scatter Relationships
We now create and save the 6 individual diagnostic charts:
1. Histogram of house price per unit area
2. Boxplot of house price per unit area
3. Histogram of house age
4. Boxplot of house age
5. Scatter plot: House age vs. Property price
6. Scatter plot: MRT distance vs. Property price"""))

cells.append(nbf.v4.new_code_cell("""# Figure 06: Histogram of House Price per Unit Area
plt.figure(figsize=(8, 5))
plt.hist(df_model[target], bins=25, color='darkorange', edgecolor='white', alpha=0.85)
plt.axvline(df_model[target].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_model[target].mean():.2f}")
plt.axvline(df_model[target].median(), color='navy', linestyle='-', linewidth=2, label=f"Median: {df_model[target].median():.2f}")
plt.title('Histogram of House Price per Unit Area', fontsize=14, pad=12)
plt.xlabel('House Price of Unit Area (10,000 NTD / Ping)', fontsize=12)
plt.ylabel('Frequency (Count)', fontsize=12)
plt.legend(fontsize=11)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '06_hist_price_unit_area.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 07: Boxplot of House Price per Unit Area
plt.figure(figsize=(6, 6))
plt.boxplot(df_model[target], patch_artist=True,
            boxprops=dict(facecolor='moccasin', color='darkorange'),
            medianprops=dict(color='red', linewidth=2.5),
            whiskerprops=dict(color='darkorange', linewidth=1.5),
            capprops=dict(color='darkorange', linewidth=1.5),
            flierprops=dict(marker='o', markerfacecolor='red', markeredgecolor='none', alpha=0.6, markersize=7))
plt.title('Boxplot of House Price per Unit Area', fontsize=14, pad=12)
plt.ylabel('House Price of Unit Area (10,000 NTD / Ping)', fontsize=12)
plt.xticks([1], ['All Observations (n=414)'])
plt.tight_layout()
fig_path = os.path.join(figures_dir, '07_boxplot_price_unit_area.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 08: Histogram of House Age
plt.figure(figsize=(8, 5))
plt.hist(df_model[age], bins=20, color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(df_model[age].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_model[age].mean():.2f} yrs")
plt.axvline(df_model[age].median(), color='navy', linestyle='-', linewidth=2, label=f"Median: {df_model[age].median():.2f} yrs")
plt.title('Histogram of House Age', fontsize=14, pad=12)
plt.xlabel('House Age (Years)', fontsize=12)
plt.ylabel('Frequency (Count)', fontsize=12)
plt.legend(fontsize=11)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '08_hist_house_age.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 09: Boxplot of House Age
plt.figure(figsize=(6, 6))
plt.boxplot(df_model[age], patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='steelblue'),
            medianprops=dict(color='navy', linewidth=2.5),
            whiskerprops=dict(color='steelblue', linewidth=1.5),
            capprops=dict(color='steelblue', linewidth=1.5),
            flierprops=dict(marker='o', markerfacecolor='navy', alpha=0.6))
plt.title('Boxplot of House Age', fontsize=14, pad=12)
plt.ylabel('House Age (Years)', fontsize=12)
plt.xticks([1], ['All Observations (n=414)'])
plt.tight_layout()
fig_path = os.path.join(figures_dir, '09_boxplot_house_age.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 10: Scatter plot of House Age vs House Price per Unit Area
plt.figure(figsize=(8, 5))
plt.scatter(df_model[age], df_model[target], color='teal', alpha=0.6, edgecolors='none', s=45)
plt.title('House Age vs. House Price per Unit Area', fontsize=14, pad=12)
plt.xlabel('House Age (Years)', fontsize=12)
plt.ylabel('Price of Unit Area (10,000 NTD / Ping)', fontsize=12)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '10_scatter_age_vs_price.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 11: Scatter plot of MRT Distance vs House Price per Unit Area
plt.figure(figsize=(8, 5))
plt.scatter(df_model[mrt], df_model[target], color='crimson', alpha=0.55, edgecolors='none', s=45)
plt.title('Distance to Nearest MRT Station vs. House Price per Unit Area', fontsize=14, pad=12)
plt.xlabel('Distance to Nearest MRT Station (Metres)', fontsize=12)
plt.ylabel('Price of Unit Area (10,000 NTD / Ping)', fontsize=12)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '11_scatter_mrt_vs_price.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Descriptive Statistics
1. **Variability:** `X3 distance to the nearest MRT station` exhibits the largest absolute variance ($s^2 = 1,592,920.631\\text{ m}^2$, $s = 1,262.110\\text{ m}$), reflecting properties situated immediately beside an MRT station ($23.38\\text{ m}$) alongside outlying properties over $6.4\\text{ km}$ away.
2. **Target Distribution ($Y$):** The price per unit area has a mean of $37.980$ and a median of $38.450$. The central body is fairly symmetric ($IQR = 18.900$), but the distribution possesses a long right tail with a maximum of $117.500$.
3. **Outliers:** The boxplot confirms an extreme upper outlier ($117.500\\text{ units}$), representing a property transacted at nearly triple the sample median.
4. **Graphical Relationships:**
   - **House Age:** Demonstrates a non-linear, slightly U-shaped or bimodal pattern. Very new properties (<10 yrs) and select mature properties command premium prices.
   - **MRT Distance:** Displays a distinct negative, non-linear decaying curve. Properties closest to MRT stations (< 500 m) consistently command higher prices per unit area."""))

# SECTION 4 — 95% Confidence Interval
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 4 — 95% Confidence Interval for Mean Property Price

Because the true population standard deviation $\\sigma$ is unknown, we construct a 95% confidence interval for the population mean $\\mu$ using Student's $t$-distribution:

$$\\bar{x} \\pm t_{\\alpha/2, \\, n-1} \\times \\frac{s}{\\sqrt{n}}$$

where:
- $\\bar{x}$ = sample mean
- $s$ = sample standard deviation
- $n$ = sample size ($414$)
- $df = n - 1 = 413$
- $t_{0.025, \\, 413}$ = critical two-tailed $t$-value"""))

cells.append(nbf.v4.new_code_cell("""# 95% Confidence Interval Calculation
y_series = df_model[target]
n = len(y_series)
x_bar = y_series.mean()
s = y_series.std(ddof=1)
df_deg = n - 1

# Critical t-value for 95% two-sided confidence
t_crit = stats.t.ppf(1 - 0.05/2, df=df_deg)

# Standard error and margin of error
std_error = s / np.sqrt(n)
margin_of_error = t_crit * std_error

# Confidence limits
ci_lower = x_bar - margin_of_error
ci_upper = x_bar + margin_of_error

print("=== 95% Confidence Interval for Population Mean Price per Unit Area ===")
print(f"Sample Size (n)            : {n}")
print(f"Sample Mean (x_bar)        : {x_bar:.3f} (10,000 NTD/Ping)")
print(f"Sample Std Dev (s)         : {s:.3f}")
print(f"Degrees of Freedom (df)    : {df_deg}")
print(f"Critical t-value (t*)      : {t_crit:.3f}")
print(f"Standard Error (SE)        : {std_error:.3f}")
print(f"Margin of Error (MoE)      : {margin_of_error:.3f}")
print(f"95% Confidence Interval    : [{ci_lower:.3f}, {ci_upper:.3f}] (10,000 NTD/Ping)")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Confidence Interval
- **Academic Meaning:** If we were to draw repeated independent random samples of size $n=414$ from the same population and compute a 95% confidence interval from each sample, approximately 95% of those calculated intervals would encompass the true population mean price per unit area.
- **Common Misconception:** This does **not** mean there is a 95% probability that the fixed interval $[36.666, 39.295]$ contains $\\mu$. The true parameter $\\mu$ is a fixed (unknown) constant, not a random variable.
- **Sampling Mechanism Caveat:** Because the exact sampling method used by the dataset collectors is not documented, inference to a broader population should be interpreted with reasonable caution."""))

# SECTION 5 — Two-Sample t-Test (MRT Proximity)
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 5 — Hypothesis Testing: Does MRT Distance Relate to Differences in Mean Property Prices?

We investigate whether properties located close to an MRT station have a different population mean price per unit area than properties located further away.

### Group Definition
We divide the dataset using the sample median MRT distance ($492.231\\text{ m}$):
- **Near MRT:** $\\text{Distance} \\le \\text{Median}$
- **Far from MRT:** $\\text{Distance} > \\text{Median}$

*(This median split provides an exploratory, balanced contrast rather than an official legal definition of proximity).*

### Hypotheses
$$H_0: \\mu_{\\text{Near}} - \\mu_{\\text{Far}} = 0 \\quad (\\text{No difference in mean property price per unit area})$$
$$H_1: \\mu_{\\text{Near}} - \\mu_{\\text{Far}} \\ne 0 \\quad (\\text{A difference exists in mean property price per unit area})$$

Significance level: $\\alpha = 0.05$. We utilize **Welch's independent two-sample $t$-test**, which relaxes the assumption of equal population variances."""))

cells.append(nbf.v4.new_code_cell("""# Median split
median_mrt = df_model[mrt].median()
near_mrt = df_model[df_model[mrt] <= median_mrt][target]
far_mrt = df_model[df_model[mrt] > median_mrt][target]

# Compute group statistics
n_near, mean_near, std_near = len(near_mrt), near_mrt.mean(), near_mrt.std(ddof=1)
n_far, mean_far, std_far = len(far_mrt), far_mrt.mean(), far_mrt.std(ddof=1)

# Perform Welch's t-test (equal_var=False)
t_stat, p_val = stats.ttest_ind(near_mrt, far_mrt, equal_var=False)

# Welch-Satterthwaite degrees of freedom
s1_sq, s2_sq = std_near**2 / n_near, std_far**2 / n_far
df_welch = (s1_sq + s2_sq)**2 / ((s1_sq**2 / (n_near - 1)) + (s2_sq**2 / (n_far - 1)))

print("=== Welch's Independent Two-Sample t-Test Results ===")
print(f"Median MRT Distance Threshold : {median_mrt:.3f} metres")
print(f"Near MRT Group (<= Median)    : n = {n_near}, Mean = {mean_near:.3f}, Std Dev = {std_near:.3f}")
print(f"Far from MRT Group (> Median) : n = {n_far}, Mean = {mean_far:.3f}, Std Dev = {std_far:.3f}")
print(f"Difference in Means (Near-Far): {mean_near - mean_far:.3f} (10,000 NTD/Ping)")
print(f"Welch t-statistic             : {t_stat:.3f}")
print(f"Degrees of Freedom (df)       : {df_welch:.2f}")
print(f"p-value (two-tailed)          : {p_val:.4e}")

if p_val < 0.05:
    print("Decision                      : Reject the Null Hypothesis (H0) at alpha = 0.05")
else:
    print("Decision                      : Fail to Reject the Null Hypothesis (H0) at alpha = 0.05")"""))

cells.append(nbf.v4.new_markdown_cell("""### Diagnostic Visualizations & Robustness Check
We examine the distribution shapes of both groups and conduct a non-parametric **Mann-Whitney $U$ test** as a supplementary check."""))

cells.append(nbf.v4.new_code_cell("""# Figure 12: Comparison Boxplot of MRT Groups
plt.figure(figsize=(7, 6))
plt.boxplot([near_mrt, far_mrt], patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='navy'),
            medianprops=dict(color='firebrick', linewidth=2.5),
            flierprops=dict(marker='o', markerfacecolor='firebrick', alpha=0.5))
plt.title('House Price per Unit Area by MRT Proximity Group', fontsize=14, pad=12)
plt.ylabel('Price of Unit Area (10,000 NTD / Ping)', fontsize=12)
plt.xticks([1, 2], [f'Near MRT (<= {median_mrt:.0f}m)\\n(n={n_near})', f'Far from MRT (> {median_mrt:.0f}m)\\n(n={n_far})'], fontsize=11)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '12_boxplot_mrt_proximity_comparison.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")

# Supplementary Non-parametric Mann-Whitney U test
u_stat, p_val_u = stats.mannwhitneyu(near_mrt, far_mrt, alternative='two-sided')
print(f"Supplementary Robustness Check — Mann-Whitney U Test:")
print(f"  U-statistic = {u_stat:.1f}, p-value = {p_val_u:.4e} (Reject H0)")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Two-Sample Test
- **Decision:** Because $p = 4.065 \\times 10^{-45} < 0.05$, we reject $H_0$. There is overwhelming statistical evidence that mean property price per unit area differs between properties near and far from MRT stations.
- **Practical Impact:** Properties within $492\\text{ m}$ of an MRT station average $46.265$ units, compared to $29.452$ units for properties beyond $492\\text{ m}$ — an observed difference of **$16.813\\text{ units}$ (~57% higher)**.
- **Robustness:** The non-parametric Mann-Whitney $U$ test confirms this conclusion ($p = 1.195 \\times 10^{-40}$), demonstrating that the finding is not driven by distributional skew or extreme outliers."""))

# SECTION 6 — One-Way ANOVA (House Age Groups)
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 6 — One-Way ANOVA: Comparison of Property Prices Across House-Age Groups

We test whether mean property prices per unit area differ across different property age categories.

### Tertile Grouping
We segment the sample into three balanced age groups using empirical tertiles ($33.33\\%$ and $66.67\\%$ quantiles):
- **Younger Properties:** Age $\\le 13.0$ years
- **Middle-Aged Properties:** $13.0 < \\text{Age} \\le 26.6$ years
- **Older Properties:** Age $> 26.6$ years

### Hypotheses
$$H_0: \\mu_{\\text{Younger}} = \\mu_{\\text{Middle}} = \\mu_{\\text{Older}}$$
$$H_1: \\text{At least one population group mean is different}$$
Significance level: $\\alpha = 0.05$."""))

cells.append(nbf.v4.new_code_cell("""# Define age tertiles
df_model['Age_Group'] = pd.qcut(df_model[age], q=3, labels=['Younger', 'Middle-aged', 'Older'])

# Summary table by age group
anova_summary = df_model.groupby('Age_Group', observed=False)[target].agg(
    Sample_Size='count',
    Mean='mean',
    Variance='var',
    Std_Dev='std'
).round(3)
print("Summary Statistics across Age Groups:")
anova_summary"""))

cells.append(nbf.v4.new_code_cell("""# Compute ANOVA components manually and verify with scipy
groups = [group[target].values for name, group in df_model.groupby('Age_Group', observed=False)]
grand_mean = df_model[target].mean()
k = len(groups)
N = len(df_model[target])

# Sum of Squares
ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
ss_within = sum(sum((val - g.mean())**2 for val in g) for g in groups)
ss_total = ss_between + ss_within

# Degrees of Freedom
df_between = k - 1
df_within = N - k
df_total = N - 1

# Mean Squares
ms_between = ss_between / df_between
ms_within = ss_within / df_within

# F-statistic and p-value
f_stat = ms_between / ms_within
p_val_f = 1 - stats.f.cdf(f_stat, df_between, df_within)

anova_table = pd.DataFrame({
    'Source of Variation': ['Between Groups (Age)', 'Within Groups (Error)', 'Total'],
    'Sum of Squares (SS)': [round(ss_between, 3), round(ss_within, 3), round(ss_total, 3)],
    'df': [df_between, df_within, df_total],
    'Mean Square (MS)': [round(ms_between, 3), round(ms_within, 3), np.nan],
    'F-statistic': [round(f_stat, 3), np.nan, np.nan],
    'p-value': [f"{p_val_f:.4e}", np.nan, np.nan]
})
print("One-Way ANOVA Table:")
anova_table"""))

cells.append(nbf.v4.new_markdown_cell("""### ANOVA Assumption Checks & Post-Hoc Analysis
We test:
1. **Normality of Residuals:** Q-Q plot and Shapiro-Wilk test.
2. **Homogeneity of Variance:** Levene's test.
3. **Post-Hoc Pairwise Comparisons:** Tukey's Honestly Significant Difference (HSD) test."""))

cells.append(nbf.v4.new_code_cell("""# Model fit for residuals
anova_model = ols(f"Q('{target}') ~ C(Age_Group)", data=df_model).fit()
residuals_anova = anova_model.resid

# Figure 13: Residual diagnostics for ANOVA
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Q-Q plot
sm.qqplot(residuals_anova, line='45', fit=True, ax=axes[0])
axes[0].set_title('Normal Q-Q Plot of ANOVA Residuals', fontsize=13)

# Distribution plot
sns.histplot(residuals_anova, kde=True, ax=axes[1], color='darkslategray')
axes[1].set_title('Histogram of ANOVA Residuals', fontsize=13)
axes[1].set_xlabel('Residual Value')

plt.tight_layout()
fig_path = os.path.join(figures_dir, '13_anova_residual_diagnostics.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")

# Shapiro-Wilk and Levene Tests
shapiro_stat, shapiro_p = stats.shapiro(residuals_anova)
levene_stat, levene_p = stats.levene(*groups)

print("=== ANOVA Assumption Diagnostics ===")
print(f"Shapiro-Wilk Normality Test : W = {shapiro_stat:.4f}, p = {shapiro_p:.4e}")
print(f"Levene Homogeneity of Var   : Stat = {levene_stat:.4f}, p = {levene_p:.4f}")

# Tukey HSD Post-hoc comparison
print('\\n=== Tukey HSD Post-Hoc Pairwise Comparison ===')
tukey = pairwise_tukeyhsd(endog=df_model[target], groups=df_model['Age_Group'], alpha=0.05)
print(tukey)"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of ANOVA & Post-Hoc Results
- **Overall ANOVA:** $F = 32.062$, $p = 1.150 \\times 10^{-13} < 0.05$. We reject $H_0$. At least one age group has a statistically different population mean price per unit area.
- **Pairwise Tukey HSD Differences:**
  - **Younger vs. Middle-aged:** Statistically significant ($p < 0.001$), with younger properties commanding an average of $11.568\\text{ units}$ more.
  - **Younger vs. Older:** Statistically significant ($p < 0.001$), with younger properties commanding $9.220\\text{ units}$ more.
  - **Middle-aged vs. Older:** Not statistically significant ($p = 0.286$, mean difference of $2.349\\text{ units}$).
- **Causation Distinction:** These differences show a genuine statistical association between house age tertile and valuation, but do not prove that property aging directly causes lower prices; confounding factors like building redevelopment or location advantages also play a role."""))

# SECTION 7 — Correlation Analysis
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 7 — Correlation Between Property Characteristics and Price

We analyze the bivariate relationship between the target variable `Y house price of unit area` and the three primary characteristics:
1. `X2 house age`
2. `X3 distance to the nearest MRT station`
3. `X4 number of convenience stores`

We report both:
- **Pearson Linear Correlation ($r$):** Measures linear association.
- **Spearman Rank Correlation ($\\rho$):** Measures monotonic association (robust to non-normality and non-linearities)."""))

cells.append(nbf.v4.new_code_cell("""# Compute Pearson and Spearman correlations
corr_results = []
for var_name, label in [(age, 'House Age (X2)'), (mrt, 'MRT Distance (X3)'), (stores, 'Convenience Stores (X4)')]:
    r_val, r_p = stats.pearsonr(df_model[var_name], df_model[target])
    rho_val, rho_p = stats.spearmanr(df_model[var_name], df_model[target])
    
    corr_results.append({
        'Feature': label,
        'Pearson r': round(r_val, 3),
        'Pearson p-value': f"{r_p:.4e}",
        'Spearman rho': round(rho_val, 3),
        'Spearman p-value': f"{rho_p:.4e}",
        'Interpretation': 'Strong Negative' if r_val < -0.6 else ('Moderate Positive' if r_val > 0.5 else 'Weak Negative')
    })

corr_df = pd.DataFrame(corr_results)
print("Correlation with House Price per Unit Area (Y):")
corr_df"""))

cells.append(nbf.v4.new_code_cell("""# Figure 14: Correlation Heatmap
plt.figure(figsize=(8, 6))
corr_matrix = df_model[[target, age, mrt, stores]].corr(method='pearson')
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".3f", vmin=-1, vmax=1,
            cbar_kws={'label': 'Pearson Correlation Coefficient (r)'})
plt.title('Correlation Matrix of Primary Variables', fontsize=14, pad=12)
plt.tight_layout()
fig_path = os.path.join(figures_dir, '14_correlation_heatmap.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 15: Scatter plots with Trend Lines
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Age vs Price
sns.regplot(data=df_model, x=age, y=target, ax=axes[0],
            scatter_kws={'alpha': 0.45, 'color': 'steelblue'}, line_kws={'color': 'darkred', 'linewidth': 2})
axes[0].set_title(f'House Age vs. Price (r = -0.211)', fontsize=13)
axes[0].set_xlabel('House Age (Years)')
axes[0].set_ylabel('Price of Unit Area (10,000 NTD/Ping)')

# Plot 2: MRT Distance vs Price
sns.regplot(data=df_model, x=mrt, y=target, ax=axes[1],
            scatter_kws={'alpha': 0.45, 'color': 'forestgreen'}, line_kws={'color': 'darkred', 'linewidth': 2})
axes[1].set_title(f'MRT Distance vs. Price (r = -0.674)', fontsize=13)
axes[1].set_xlabel('Distance to MRT (Metres)')
axes[1].set_ylabel('Price of Unit Area (10,000 NTD/Ping)')

# Plot 3: Stores vs Price
sns.regplot(data=df_model, x=stores, y=target, ax=axes[2],
            scatter_kws={'alpha': 0.45, 'color': 'darkorange'}, line_kws={'color': 'darkred', 'linewidth': 2})
axes[2].set_title(f'Convenience Stores vs. Price (r = 0.571)', fontsize=13)
axes[2].set_xlabel('Nearby Convenience Stores (Count)')
axes[2].set_ylabel('Price of Unit Area (10,000 NTD/Ping)')

plt.tight_layout()
fig_path = os.path.join(figures_dir, '15_scatter_trendlines.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Correlation Analysis
1. **Distance to MRT (`X3`):** Exhibits the strongest association with price. Pearson $r = -0.674$ and Spearman $\\rho = -0.776$ (both $p < 10^{-50}$). The fact that Spearman is noticeably more negative than Pearson reflects the non-linear curvature: prices drop precipitously in the first 1,000 metres and then taper off.
2. **Nearby Convenience Stores (`X4`):** Displays a moderate positive relationship ($r = 0.571, \\rho = 0.617, p < 10^{-35}$). Properties surrounded by more convenience retail tend to have higher valuations per unit area.
3. **House Age (`X2`):** Exhibits a statistically significant but weak negative linear correlation ($r = -0.211, p = 1.560 \\times 10^{-5}$) and $\\rho = -0.282$.
4. **Correlation $\\ne$ Causation:** These associations reflect spatial patterns in Sindian District (e.g., convenience stores and MRT stations co-locate in commercial hubs). They do not imply that opening another store mechanically inflates house prices."""))

# SECTION 8 — Simple Linear Regression
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 8 — Simple Linear Regression: Predicting Property Price Using House Age

We fit a Simple Linear Regression (SLR) model via Ordinary Least Squares (OLS):

$$Y = \\beta_0 + \\beta_1 X + \\varepsilon$$

where $Y$ is `Y house price of unit area` and $X$ is `X2 house age`."""))

cells.append(nbf.v4.new_code_cell("""# Prepare features and fit OLS using statsmodels
X_slr = sm.add_constant(df_model[age])
y_target = df_model[target]

ols_slr = sm.OLS(y_target, X_slr).fit()
print(ols_slr.summary())"""))

cells.append(nbf.v4.new_code_cell("""# Extract key SLR statistics
beta0_slr = ols_slr.params.iloc[0]
beta1_slr = ols_slr.params.iloc[1]
p_val_slope_slr = ols_slr.pvalues.iloc[1]
r2_slr_full = ols_slr.rsquared
r2_adj_slr_full = ols_slr.rsquared_adj
f_stat_slr = ols_slr.fvalue
ci_slope = ols_slr.conf_int().iloc[1]

print("=== Simple Linear Regression Equation & Metrics ===")
print(f"Regression Equation : Y = {beta0_slr:.4f} + ({beta1_slr:.4f}) * X2")
print(f"Intercept (beta_0)   : {beta0_slr:.4f}")
print(f"Slope (beta_1)       : {beta1_slr:.4f} (10,000 NTD/Ping per year of age)")
print(f"Slope 95% CI         : [{ci_slope[0]:.4f}, {ci_slope[1]:.4f}]")
print(f"Slope p-value        : {p_val_slope_slr:.4e} (Significant)")
print(f"R-squared            : {r2_slr_full:.4f}")
print(f"Adjusted R-squared   : {r2_adj_slr_full:.4f}")
print(f"F-statistic          : {f_stat_slr:.3f} (p = {ols_slr.f_pvalue:.4e})")"""))

cells.append(nbf.v4.new_code_cell("""# Figure 16: SLR Regression Line & Residual Diagnostics
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Fitted line
axes[0].scatter(df_model[age], df_model[target], color='teal', alpha=0.5, label='Observations')
axes[0].plot(df_model[age], ols_slr.fittedvalues, color='red', linewidth=2.5, label='Fitted OLS Line')
axes[0].set_title(f'SLR: Fitted Line (R² = {r2_slr_full:.3f})', fontsize=13)
axes[0].set_xlabel('House Age (Years)')
axes[0].set_ylabel('Price of Unit Area (10,000 NTD/Ping)')
axes[0].legend()

# 2. Residuals vs Fitted
axes[1].scatter(ols_slr.fittedvalues, ols_slr.resid, color='darkslategray', alpha=0.5)
axes[1].axhline(0, color='red', linestyle='--')
axes[1].set_title('Residuals vs. Fitted Values', fontsize=13)
axes[1].set_xlabel('Fitted Values')
axes[1].set_ylabel('Residuals')

# 3. Normal Q-Q Plot of Residuals
sm.qqplot(ols_slr.resid, line='45', fit=True, ax=axes[2])
axes[2].set_title('Normal Q-Q Plot of Residuals', fontsize=13)

plt.tight_layout()
fig_path = os.path.join(figures_dir, '16_slr_diagnostics.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Simple Linear Regression
- **Intercept ($\\beta_0 = 42.435$):** The theoretical expected price per unit area for a brand-new house (age = 0) is approximately $42.435\\text{ units}$ ($424,350\\text{ NTD/Ping}$).
- **Slope ($\\beta_1 = -0.252$):** For each additional year of house age, the expected price per unit area decreases by $0.252\\text{ units}$ ($2,520\\text{ NTD/Ping}$).
- **Statistical Significance:** The slope is statistically significant ($t = -4.37$, $p = 1.560 \\times 10^{-5} < 0.05$).
- **$R^2 = 0.044$ (4.4%):** House age alone explains only $4.4\\%$ of the total variance in property price per unit area. More than $95\\%$ of the variance remains unexplained by age alone."""))

# SECTION 9 — Multiple Linear Regression
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 9 — Multiple Linear Regression: Predicting Property Price Using Multiple Variables

We construct a Multiple Linear Regression (MLR) model incorporating both primary predictors:

$$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\varepsilon$$

where:
- $Y$ = `Y house price of unit area`
- $X_1$ = `X2 house age`
- $X_2$ = `X3 distance to the nearest MRT station`"""))

cells.append(nbf.v4.new_code_cell("""# Prepare features and fit Multiple OLS
X_mlr = sm.add_constant(df_model[[age, mrt]])
ols_mlr = sm.OLS(y_target, X_mlr).fit()
print(ols_mlr.summary())"""))

cells.append(nbf.v4.new_code_cell("""# Extract MLR coefficients and metrics
b0 = ols_mlr.params.iloc[0]
b1 = ols_mlr.params.iloc[1]
b2 = ols_mlr.params.iloc[2]
conf_ints = ols_mlr.conf_int()

print("=== Multiple Linear Regression Equation & Metrics ===")
print(f"Regression Equation : Y = {b0:.4f} + ({b1:.4f})*Age + ({b2:.4f})*MRT_Dist")
print(f"Intercept (beta_0)   : {b0:.4f}")
print(f"House Age Coeff (b1) : {b1:.4f} (p = {ols_mlr.pvalues.iloc[1]:.4e}, 95% CI: [{conf_ints.iloc[1,0]:.4f}, {conf_ints.iloc[1,1]:.4f}])")
print(f"MRT Dist Coeff (b2)  : {b2:.4f} (p = {ols_mlr.pvalues.iloc[2]:.4e}, 95% CI: [{conf_ints.iloc[2,0]:.4f}, {conf_ints.iloc[2,1]:.4f}])")
print(f"R-squared            : {ols_mlr.rsquared:.4f}")
print(f"Adjusted R-squared   : {ols_mlr.rsquared_adj:.4f}")
print(f"Overall F-statistic  : {ols_mlr.fvalue:.3f} (p = {ols_mlr.f_pvalue:.4e})")"""))

cells.append(nbf.v4.new_markdown_cell("""### Model Diagnostics & Multicollinearity (VIF)
We calculate the **Variance Inflation Factor (VIF)** for the predictors and assess residual normality and homoscedasticity."""))

cells.append(nbf.v4.new_code_cell("""# Calculate Variance Inflation Factor (VIF)
X_vif_df = df_model[[age, mrt]]
X_vif_design = sm.add_constant(X_vif_df)

vif_data = pd.DataFrame({
    'Predictor': ['X2 house age', 'X3 distance to the nearest MRT station'],
    'VIF': [
        variance_inflation_factor(X_vif_design.values, 1),
        variance_inflation_factor(X_vif_design.values, 2)
    ]
})
print("Variance Inflation Factor (VIF) Analysis:")
vif_data"""))

cells.append(nbf.v4.new_code_cell("""# Figure 17: MLR Diagnostic Plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Actual vs Predicted
axes[0].scatter(ols_mlr.fittedvalues, df_model[target], color='royalblue', alpha=0.55)
axes[0].plot([df_model[target].min(), df_model[target].max()],
             [df_model[target].min(), df_model[target].max()], 'r--', linewidth=2)
axes[0].set_title('Actual vs. Predicted Price (MLR)', fontsize=13)
axes[0].set_xlabel('Predicted Price of Unit Area')
axes[0].set_ylabel('Actual Price of Unit Area')

# 2. Residuals vs Fitted
axes[1].scatter(ols_mlr.fittedvalues, ols_mlr.resid, color='navy', alpha=0.5)
axes[1].axhline(0, color='red', linestyle='--')
axes[1].set_title('Residuals vs. Fitted Values', fontsize=13)
axes[1].set_xlabel('Fitted Values')
axes[1].set_ylabel('Residuals')

# 3. Normal Q-Q Plot
sm.qqplot(ols_mlr.resid, line='45', fit=True, ax=axes[2])
axes[2].set_title('Normal Q-Q Plot of Residuals', fontsize=13)

plt.tight_layout()
fig_path = os.path.join(figures_dir, '17_mlr_diagnostics.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Multiple Linear Regression & Diagnostics
- **Equation:** $\\hat{Y} = 49.8856 - 0.2310 \\times \\text{Age} - 0.0072 \\times \\text{MRT\\_Dist}$
- **Predictor Contributions:**
  - Holding MRT distance constant, each additional year of house age reduces unit price by $0.2310\\text{ units}$ ($p = 1.05 \\times 10^{-7}$).
  - Holding house age constant, each additional 100 metres of distance to the nearest MRT station reduces unit price by $0.72\\text{ units}$ ($p = 2.44 \\times 10^{-53}$).
- **Variance Explained:** Adding MRT distance dramatically increases $R^2$ from **$4.4\\%$ (SLR) to $49.1\\%$ (MLR)**.
- **Multicollinearity:** Both VIF values are $\\approx 1.001$, far below the common caution threshold of $5$ or $10$. House age and MRT distance are virtually uncorrelated ($r = 0.026$), confirming that multicollinearity is not an issue.
- **Diagnostic Limitations:** Residual plots reveal slight heteroscedasticity (greater variance at higher predicted prices) and positive skew due to the extreme upper outlier ($117.5$)."""))

# SECTION 10 — Train-Test Split and Model Evaluation
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 10 — Train-Test Split and Predictive Performance Evaluation

To assess generalizability on unseen data, we evaluate both models using an **80:20 train-test split** (`test_size=0.2, random_state=42`).

### Methodological Rigor
- The split is executed strictly before model fitting.
- Models are trained **only** on the 80% training set ($n=331$).
- Predictions and evaluation metrics are computed **strictly on the held-out 20% test set** ($n=83$).
- The exact same split is shared across both models for fair comparison.

We compute:
$$\\text{MAE} = \\frac{1}{n} \\sum |y_i - \\hat{y}_i|$$
$$\\text{MSE} = \\frac{1}{n} \\sum (y_i - \\hat{y}_i)^2$$
$$\\text{RMSE} = \\sqrt{\\text{MSE}}$$
$$R^2 = 1 - \\frac{\\sum (y_i - \\hat{y}_i)^2}{\\sum (y_i - \\bar{y})^2}$$"""))

cells.append(nbf.v4.new_code_cell("""# 80:20 Train-Test Split with fixed random seed 42
X_features = df_model[[age, mrt]]
y_labels = df_model[target]

X_train, X_test, y_train, y_test = train_test_split(
    X_features, y_labels, test_size=0.2, random_state=42
)

print(f"Training set size: {X_train.shape[0]} samples")
print(f"Test set size    : {X_test.shape[0]} samples")"""))

cells.append(nbf.v4.new_code_cell("""# 1. Fit SLR on Training Data (House Age only)
model_slr_train = LinearRegression()
model_slr_train.fit(X_train[[age]], y_train)

# Predict on test data
y_pred_slr = model_slr_train.predict(X_test[[age]])

# Evaluate SLR metrics
mae_slr = mean_absolute_error(y_test, y_pred_slr)
mse_slr = mean_squared_error(y_test, y_pred_slr)
rmse_slr = np.sqrt(mse_slr)
r2_slr = r2_score(y_test, y_pred_slr)

# 2. Fit MLR on Training Data (House Age + MRT Distance)
model_mlr_train = LinearRegression()
model_mlr_train.fit(X_train, y_train)

# Predict on test data
y_pred_mlr = model_mlr_train.predict(X_test)

# Evaluate MLR metrics
mae_mlr = mean_absolute_error(y_test, y_pred_mlr)
mse_mlr = mean_squared_error(y_test, y_pred_mlr)
rmse_mlr = np.sqrt(mse_mlr)
r2_mlr = r2_score(y_test, y_pred_mlr)

# Summary Comparison Table
eval_comparison = pd.DataFrame({
    'Metric': ['MAE (Mean Absolute Error)', 'MSE (Mean Squared Error)', 'RMSE (Root Mean Squared Error)', 'R-squared (R²)'],
    'SLR (Age Only)': [round(mae_slr, 3), round(mse_slr, 3), round(rmse_slr, 3), round(r2_slr, 4)],
    'MLR (Age + MRT)': [round(mae_mlr, 3), round(mse_mlr, 3), round(rmse_mlr, 3), round(r2_mlr, 4)],
    'Improvement': [
        f"{((mae_slr - mae_mlr)/mae_slr)*100:.1f}% reduction",
        f"{((mse_slr - mse_mlr)/mse_slr)*100:.1f}% reduction",
        f"{((rmse_slr - rmse_mlr)/rmse_slr)*100:.1f}% reduction",
        f"+{r2_mlr - r2_slr:.4f}"
    ]
})
print("Test Set Performance Evaluation Comparison:")
eval_comparison"""))

cells.append(nbf.v4.new_code_cell("""# Figure 18 & 19: Actual vs Predicted Plots on Held-out Test Data
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# SLR Test Plot
axes[0].scatter(y_test, y_pred_slr, color='teal', alpha=0.7, edgecolors='white', s=60)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
axes[0].set_title(f'SLR Test Predictions (R² = {r2_slr:.3f}, MAE = {mae_slr:.2f})', fontsize=13)
axes[0].set_xlabel('Actual Price of Unit Area (10,000 NTD/Ping)', fontsize=11)
axes[0].set_ylabel('Predicted Price (10,000 NTD/Ping)', fontsize=11)

# MLR Test Plot
axes[1].scatter(y_test, y_pred_mlr, color='royalblue', alpha=0.7, edgecolors='white', s=60)
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
axes[1].set_title(f'MLR Test Predictions (R² = {r2_mlr:.3f}, MAE = {mae_mlr:.2f})', fontsize=13)
axes[1].set_xlabel('Actual Price of Unit Area (10,000 NTD/Ping)', fontsize=11)
axes[1].set_ylabel('Predicted Price (10,000 NTD/Ping)', fontsize=11)

plt.tight_layout()
fig_path = os.path.join(figures_dir, '18_test_actual_vs_predicted.png')
plt.savefig(fig_path, dpi=300)
plt.show()
print(f"Saved: {fig_path}")"""))

cells.append(nbf.v4.new_markdown_cell("""### Interpretation of Predictive Evaluation
1. **Model Superiority:** The Multiple Linear Regression model substantially outperforms the Simple Linear Regression model across all test metrics:
   - **MAE:** Drops from $10.621$ to $6.248$ (a **$41.2\\%$ error reduction**).
   - **RMSE:** Drops from $12.853$ to $8.438$ (a **$34.4\\%$ error reduction**).
   - **Test $R^2$:** Rises from $0.0152$ ($1.5\\%$) to **$0.5756$ ($57.6\\%$)**.
2. **Metric Definitions:**
   - **MAE ($6.248$):** On unseen transactions, MLR predictions miss the actual price per unit area by an average of $62,480\\text{ NTD per Ping}$.
   - **RMSE ($8.438$):** Penalizes larger prediction errors more heavily by squaring residuals before taking the root.
3. **Generalization:** Adding proximity to transit transforms a virtually non-predictive baseline ($R^2 \\approx 1.5\\%$) into a functional explanatory model ($R^2 = 57.6\\%$) on unseen data."""))

# SECTION 11 — Sample Predictions
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 11 — Predicting Property Price for Example Properties

We apply the trained Multiple Linear Regression model to three realistic property profiles within the empirical domain ($0 \\le \\text{Age} \\le 40$, $50 \\le \\text{MRT} \\le 3000\\text{ m}$).

> **Reminder:** These are expected model predictions for price *per unit area* (10,000 NTD / Ping). They do **not** represent total house prices, as total square footage is not part of this dataset."""))

cells.append(nbf.v4.new_code_cell("""# Define 3 realistic property scenarios
sample_profiles = pd.DataFrame({
    'Scenario': ['A: Brand-New & Transit-Adjacent', 'B: Mid-Age & Moderate Distance', 'C: Older & Far from Transit'],
    'X2 house age': [2.0, 15.0, 32.0],
    'X3 distance to the nearest MRT station': [150.0, 600.0, 2200.0]
})

# Generate model predictions using trained MLR
sample_profiles['Predicted Price per Unit Area (10,000 NTD/Ping)'] = model_mlr_train.predict(
    sample_profiles[[age, mrt]]
).round(2)

print("=== Sample Model Predictions for Illustrative Scenarios ===")
sample_profiles"""))

cells.append(nbf.v4.new_markdown_cell("""### Scenario Takeaways
- **Profile A (New & Near MRT):** Valuation is high at **$48.51\\text{ units}$**, driven by minimal age degradation and prime metro proximity ($150\\text{ m}$).
- **Profile B (Typical Suburban Profile):** Valuation is moderate at **$42.27\\text{ units}$**.
- **Profile C (Mature & Distant):** Valuation declines to **$27.05\\text{ units}$**, reflecting the cumulative penalty of property aging and substantial transit distance ($2.2\\text{ km}$)."""))

# SECTION 12 — Final Results & Comparison
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 12 — Overall Statistical Findings

Below is the consolidated synthesis of all statistical tests, inferential procedures, and predictive evaluations performed in this analysis."""))

cells.append(nbf.v4.new_code_cell("""final_summary_data = [
    {
        'Technique': 'Descriptive Statistics',
        'Main Result': f"Mean Price = {desc_table.loc[target, 'Mean']}, Median = {desc_table.loc[target, 'Median']}",
        'Statistical Interpretation': 'Distribution is moderately symmetric around 38 units with an extreme upper outlier (117.5).'
    },
    {
        'Technique': '95% Confidence Interval',
        'Main Result': f"[{ci_lower:.3f}, {ci_upper:.3f}] (10,000 NTD/Ping)",
        'Statistical Interpretation': f"We are 95% confident that the population mean price per unit area lies within this interval."
    },
    {
        'Technique': "Welch's Two-Sample t-test",
        'Main Result': f"t = {t_stat:.3f}, p = {p_val:.2e}",
        'Statistical Interpretation': 'Reject H0. Properties near MRT stations have significantly higher mean price than distant ones.'
    },
    {
        'Technique': 'One-Way ANOVA',
        'Main Result': f"F = {f_stat:.3f}, p = {p_val_f:.2e}",
        'Statistical Interpretation': 'Reject H0. Mean property price differs significantly across younger, middle-aged, and older tertiles.'
    },
    {
        'Technique': 'Correlation Analysis',
        'Main Result': f"MRT r = {corr_df.loc[1, 'Pearson r']}, Stores r = {corr_df.loc[2, 'Pearson r']}",
        'Statistical Interpretation': 'Strong negative correlation with MRT distance; moderate positive correlation with nearby stores.'
    },
    {
        'Technique': 'Simple Regression (SLR)',
        'Main Result': f"Y = {beta0_slr:.2f} + ({beta1_slr:.3f})*Age, R² = {r2_slr_full:.4f}",
        'Statistical Interpretation': 'Statistically significant slope, but age alone explains only 4.4% of price variance.'
    },
    {
        'Technique': 'Multiple Regression (MLR)',
        'Main Result': f"R² = {ols_mlr.rsquared:.4f}, Adj R² = {ols_mlr.rsquared_adj:.4f}",
        'Statistical Interpretation': 'Adding MRT distance increases explained variance to 49.1% with no multicollinearity (VIF ~ 1.0).'
    },
    {
        'Technique': 'Predictive Model Evaluation',
        'Main Result': f"Test MLR MAE = {mae_mlr:.2f}, Test MLR R² = {r2_mlr:.4f}",
        'Statistical Interpretation': 'MLR outperforms SLR on held-out test data, reducing test MAE by 41.2% and explaining 57.6% of test variance.'
    }
]

final_comparison_table = pd.DataFrame(final_summary_data)
final_comparison_table"""))

# SECTION 13 — Limitations
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 13 — Limitations

1. **Sample Size:** Limited to 414 historical property transactions.
2. **Geographical Specificity:** The records originate solely from Sindian District, New Taipei City, Taiwan. Real estate dynamics, density patterns, and transit accessibility vary greatly across other cities and countries.
3. **Temporal Bounds:** Collected between 2012 and 2013; findings reflect market conditions and interest rate environments from that specific timeframe.
4. **Sampling Methodology:** The official UCI documentation does not detail whether transactions were sampled randomly, consecutively, or filtered by specific brokerage firms.
5. **Absence of Total Property Area:** The target variable is price *per Ping*. Total transaction price and square footage are missing from the dataset.
6. **Omitted Confounders:** Important property determinants (e.g., architectural floor level, interior condition, property management fees, layout, and school district quality) are unobserved in this dataset.
7. **Association vs. Causation:** All statistical models establish mathematical association and predictive utility, not direct causal mechanisms."""))

# SECTION 14 — Conclusion
cells.append(nbf.v4.new_markdown_cell("""---
## SECTION 14 — Conclusion

Based strictly on our empirical statistical findings:
1. **House Age:** Demonstrates a modest, statistically significant negative association with property price per unit area ($-0.23\\text{ to } -0.25\\text{ units/year}$). However, age alone accounts for only $4.4\\%$ of valuation variability.
2. **MRT Proximity:** Proximity to transit is the single dominant predictor in this dataset. Properties within median walking distance ($492\\text{ m}$) command an average premium of $57\\%$ over more distant properties.
3. **Multiple Linear Regression Performance:** Combining house age with MRT distance produces an explanatory model explaining $49.1\\%$ of sample variance, and generalizing to explain $57.6\\%$ of variance on unseen test data ($MAE = 6.25\\text{ units}$).
4. **Summary for Academic Faculty:** Proximity to mass transit and building age jointly provide strong, statistically verified predictive power for residential unit-area valuation in this market, with transit accessibility exerting the most decisive influence."""))

cells.append(nbf.v4.new_code_cell("""# Verify all newly generated figures in outputs/figures/
print("All saved figures in outputs/figures/:")
for f in sorted(os.listdir(figures_dir)):
    print(f"  - {f}")"""))

nb['cells'] = cells
nb_path = os.path.join(os.path.dirname(__file__), 'notebooks', '02_Statistical_Analysis.ipynb')
with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook 02_Statistical_Analysis.ipynb generated successfully.")
