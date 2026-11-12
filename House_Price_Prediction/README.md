# House Area, Age and Property Price Prediction

## Course Information
- **Course:** Probability and Statistics (Academic Year 2025–2026)
- **Project Title:** House Area, Age and Property Price Prediction
- **Target Audience:** College Faculty, Academic Examiners, and Engineering Students

---

## Project Overview

This project provides an end-to-end, rigorous statistical and predictive modeling study on residential property valuation. 
Using the benchmark **Real Estate Valuation Dataset** from the UCI Machine Learning Repository, we bridge classical 
statistical theory (descriptive metrics, Student's t-confidence intervals, Welch's two-sample t-testing, One-Way ANOVA, 
and Tukey HSD post-hoc analysis) with modern predictive learning (Ordinary Least Squares regression, multicollinearity 
diagnostics, and out-of-sample train-test validation).

> **CRUCIAL DATASET LIMITATION & CLARIFICATION:**  
> The project title refers to *"House Area, Age and Property Price Prediction."* However, the underlying UCI dataset **does NOT contain total house floor area or total property transaction price**.  
> The target variable is **price per unit area** ($10{,}000\text{ New Taiwan Dollars per Ping}$, where $1\text{ Ping} \approx 3.3\text{ m}^2$).  
> In accordance with strict academic integrity, we do **NOT** fabricate house area or total price. All statistical analyses, hypothesis tests, regression models, and predictions strictly evaluate **unit-area valuation**.

---

## Dataset Description & Provenance

| Attribute | Details |
|---|---|
| **Source** | UCI Machine Learning Repository (Dataset ID: 477) |
| **Dataset Author** | Prof. I-Cheng Yeh (Department of Civil Engineering, Tamkang University, Taiwan, 2018) |
| **Citation** | Yeh, I. (2018). *Real Estate Valuation [Dataset]*. UCI ML Repository. https://doi.org/10.24432/C5J30W |
| **Sample Size** | 414 historical property transactions |
| **Features** | 8 columns total (1 observation identifier, 6 numerical features, 1 numerical target) |
| **Data Quality** | Exactly 0 missing values across all columns; exactly 0 duplicate rows |
| **Location & Time** | Sindian District, New Taipei City, Taiwan (Transactions from 2012–2013) |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |

### Variables in the Dataset

1. `No` (`int64`): Transaction index (1 to 414). **Excluded from all models.**
2. `X1 transaction date` (`float64`): Transaction epoch in decimal years (2012.667 to 2013.583).
3. `X2 house age` (`float64`): Structural building age in years (0.0 to 43.8 years).
4. `X3 distance to the nearest MRT station` (`float64`): Walking distance in metres (23.38 to 6,488.02 m).
5. `X4 number of convenience stores` (`int64`): Nearby convenience retail count (0 to 10 stores).
6. `X5 latitude` (`float64`): Geographic coordinate (24.932° to 25.015° N).
7. `X6 longitude` (`float64`): Geographic coordinate (121.474° to 121.566° E).
8. `Y house price of unit area` (`float64`): **Target Variable** ($10{,}000\text{ NTD / Ping}$).

---

## Project Directory Structure

```text
House_Price_Prediction/
│
├── data/
│   ├── raw/
│   │   └── real_estate_valuation.csv          # Official raw UCI dataset (414 rows)
│   └── processed/                             # Processed data directory
│
├── notebooks/
│   ├── 01_Dataset_Exploration.ipynb           # Stage 1: Data ingestion & exploration (Executed)
│   └── 02_Statistical_Analysis.ipynb          # Stage 2: Inference, ANOVA & Modeling (Executed)
│
├── outputs/
│   ├── figures/                               # 18 Publication-quality diagnostic figures
│   │   ├── 01_histogram_house_age.png
│   │   ├── ...
│   │   └── 18_test_actual_vs_predicted.png
│   ├── Final_Project_Report.pdf               # Deliverable 1: 21-Page Comprehensive Report
│   ├── Final_Project_Presentation.pptx        # Deliverable 2: 12 Widescreen Presentation Slides
│   ├── Viva_Questions_and_Answers.pdf         # Deliverable 3: 48 Viva Questions & Answers
│   └── Presentation_Script_and_Demo_Guide.pdf # Deliverable 4: 5-7 Min Script, Demo Guide & Cheat Sheet
│
├── download_dataset.py                        # Script to download UCI dataset via ucimlrepo
├── generate_notebook.py                       # Generator for 01_Dataset_Exploration.ipynb
├── generate_analysis_notebook.py              # Generator for 02_Statistical_Analysis.ipynb
├── generate_pdf_report.py                     # Generator for Final_Project_Report.pdf
├── generate_presentation.py                   # Generator for Final_Project_Presentation.pptx
├── generate_viva_pdf.py                       # Generator for Viva_Questions_and_Answers.pdf
├── generate_script_guide_pdf.py               # Generator for Presentation_Script_and_Demo_Guide.pdf
├── requirements.txt                           # Complete project package dependencies
└── README.md                                  # This documentation
```

---

## Setup & Execution Guide

### 1. Prerequisites
- Python 3.8+ (tested on Python 3.13)
- Windows PowerShell / Linux Bash

### 2. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Package Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Jupyter Notebooks
```bash
jupyter notebook notebooks/
```
Open and run:
1. `notebooks/01_Dataset_Exploration.ipynb`
2. `notebooks/02_Statistical_Analysis.ipynb`

---

## Summary of Core Statistical & Predictive Findings

### 1. Descriptive Statistics ($n = 414$)
- **Price per Unit Area ($Y$):** Mean = $37.980$, Median = $38.450$, Std Dev = $13.606$, $\text{IQR} = 18.900$, Outlier = $117.500\text{ units}$.
- **Distance to MRT ($X_3$):** Mean = $1,083.886\text{ m}$, Median = $492.231\text{ m}$, Std Dev = $1,262.110\text{ m}$ (Severe positive skew).
- **House Age ($X_2$):** Mean = $17.713\text{ yrs}$, Median = $16.100\text{ yrs}$, Mode = $0.000\text{ yrs}$ (Bimodal structure).

### 2. 95% Confidence Interval for Mean Price
- **Formula:** $\bar{x} \pm t_{\alpha/2, n-1} \times \frac{s}{\sqrt{n}}$ ($df = 413, t^* = 1.9657, \text{SE} = 0.669, \text{MoE} = 1.315$)
- **95% Confidence Interval:** **$[36.666, 39.295]\text{ (10,000 NTD/Ping)}$**

### 3. Hypothesis Testing I: MRT Proximity (Welch's Two-Sample $t$-Test)
- **Groups:** Split at sample median MRT distance ($492.231\text{ m}$).
  - Near MRT ($\le 492.2\text{ m}$, $n=210$): Mean = $46.265\text{ units}$
  - Far MRT ($> 492.2\text{ m}$, $n=204$): Mean = $29.452\text{ units}$
- **Outcome:** **$t = 15.995, df = 399.78, p = 4.065 \times 10^{-45}$**. **Reject $H_0$**.
- **Practical Takeaway:** Properties near MRT command an average **$+57.1\%$ valuation premium** ($+168,130\text{ NTD / Ping}$). Corroborated by Mann-Whitney $U$ test ($p = 1.195 \times 10^{-40}$).

### 4. Hypothesis Testing II: House-Age Tertiles (One-Way ANOVA & Tukey HSD)
- **Cohorts:** Younger ($\le 13\text{y}$, Mean = $44.91$), Middle-aged ($13\text{--}26.6\text{y}$, Mean = $33.34$), Older ($> 26.6\text{y}$, Mean = $35.69$).
- **Outcome:** **$F = 32.062, p = 1.150 \times 10^{-13}$**. **Reject $H_0$**.
- **Tukey HSD Post-Hoc:** Younger properties significantly outperform Middle-aged ($p < 0.001$) and Older ($p < 0.001$). The difference between Middle-aged and Older is **not significant** ($p = 0.286$), proving building depreciation plateaus after the first decade.

### 5. Correlation Structure
- **MRT Distance ($X_3$):** Pearson $r = -0.674$, Spearman $\rho = -0.776$ (Dominant monotonic decay).
- **Convenience Stores ($X_4$):** Pearson $r = +0.571$, Spearman $\rho = +0.617$ (Commercial urban clustering).
- **House Age ($X_2$):** Pearson $r = -0.211$, Spearman $\rho = -0.282$ (Modest negative association).

### 6. Ordinary Least Squares Regression Models
- **Simple Linear Regression (Age):**  
  $\hat{Y} = 42.4347 - 0.2515 \times \text{Age} \quad (R^2 = 0.0443, p = 1.56 \times 10^{-5})$  
  *Limitation:* Explains only $4.4\%$ of valuation variance.
- **Multiple Linear Regression (Age + MRT):**  
  $\hat{Y} = 49.8856 - 0.2310 \times \text{Age} - 0.0072 \times \text{MRT} \quad (R^2 = 0.4911, \text{Adj } R^2 = 0.4887, F = 198.3, p = 2.65 \times 10^{-60})$  
  *Multicollinearity:* $\text{VIF}_{\text{Age}} = 1.001, \text{VIF}_{\text{MRT}} = 1.001$ (Zero collinearity concerns).

### 7. Predictive Performance on Held-Out Test Data (80:20 Split, $n = 83$)

| Metric | Simple Linear Regression (Age Only) | Multiple Linear Regression (Age + MRT) | Performance Comparison |
|---|---|---|---|
| **Mean Absolute Error (MAE)** | $10.621\text{ units}$ | **$6.248\text{ units}$** | **$41.2\%$ Error Reduction** |
| **Mean Squared Error (MSE)** | $165.205$ | **$71.206$** | **$56.9\%$ Error Reduction** |
| **Root Mean Squared Error (RMSE)** | $12.853\text{ units}$ | **$8.438\text{ units}$** | **$34.4\%$ Error Reduction** |
| **Test $R^2$** | $0.0152$ ($1.5\%$) | **$0.5756$ ($57.6\%$)** | **$+0.5604$ Increase (37× Higher)** |

---

## Final Submission Deliverables (In `outputs/`)

1. **[`outputs/Final_Project_Report.pdf`](file:///d:/PAS/eseprojtuso/House_Price_Prediction/outputs/Final_Project_Report.pdf)**
   - Complete 21-page formal academic report with cover page, abstract, table of contents, numbered tables, mathematical equations, figures, diagnostics, and references.
2. **[`outputs/Final_Project_Presentation.pptx`](file:///d:/PAS/eseprojtuso/House_Price_Prediction/outputs/Final_Project_Presentation.pptx)**
   - 12 professionally styled widescreen (16:9) slides featuring card layouts, KPI callouts, embedded figures, and concise bullet points.
3. **[`outputs/Viva_Questions_and_Answers.pdf`](file:///d:/PAS/eseprojtuso/House_Price_Prediction/outputs/Viva_Questions_and_Answers.pdf)**
   - 6-page viva booklet containing 48 rigorously answered oral defense questions across 8 categories (Project Scope, Python/Libraries, Descriptive, Inference, Testing, Correlation, Regression, Evaluation).
4. **[`outputs/Presentation_Script_and_Demo_Guide.pdf`](file:///d:/PAS/eseprojtuso/House_Price_Prediction/outputs/Presentation_Script_and_Demo_Guide.pdf)**
   - 6-page practical guide containing a 5–7 minute slide-by-slide natural speaking script, a 10-step live Jupyter demonstration sequence, faculty question defense tactics, and a 1-page revision cheat sheet.
