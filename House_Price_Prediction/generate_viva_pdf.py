"""
Script to generate outputs/Viva_Questions_and_Answers.pdf
Target: 48 comprehensively answered academic Viva/Oral defense questions.
Categories A through H: Project, Python, Descriptive, Inference, Testing, Correlation, Regression, Evaluation.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

class VivaNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Running Header
        self.drawString(54, 800, "Comprehensive Viva Voce Question Bank & Evaluator Guide")
        self.drawRightString(541, 800, "Probability & Statistics Course Project")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Running Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.line(54, 48, 541, 48)
        self.drawString(54, 38, "House Area, Age and Property Price Prediction | Academic Viva Preparation")
        self.drawRightString(541, 38, page_text)
        self.restoreState()

def build_viva_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(base_dir, "outputs", "Viva_Questions_and_Answers.pdf")
    
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1A365D")    # Navy
    c_secondary = colors.HexColor("#2B6CB0")  # Blue
    c_dark = colors.HexColor("#2D3748")       # Charcoal
    c_cat_bg = colors.HexColor("#EDF2F7")     # Light gray
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=c_secondary,
        spaceAfter=15
    )
    
    cat_heading = ParagraphStyle(
        'CatHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    
    a_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=8
    )

    story = []
    
    story.append(Paragraph("Comprehensive Viva Voce Question Bank & Model Answers", title_style))
    story.append(Paragraph("House Area, Age and Property Price Prediction — Course: Probability & Statistics (48 Questions)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=12))

    intro_p = (
        "This question bank is designed to prepare students for academic viva voce examinations, project defense panels, "
        "and faculty Q&A sessions. It contains 48 rigorous, academically grounded questions spanning 8 categories. "
        "Answers begin with intuitive, beginner-friendly explanations, integrate exact computed numerical values from our analysis, "
        "and highlight common evaluator traps to ensure confident, articulate oral defense."
    )
    story.append(Paragraph(intro_p, a_style))
    story.append(Spacer(1, 8))

    # Viva Questions Catalog: 48 Questions across 8 Categories
    viva_categories = [
        ("Category A: Project Understanding & Scope", [
            ("Q1. What is the fundamental objective of this project?",
             "The objective is to conduct an empirical statistical investigation into how residential property characteristics—specifically structural building age and proximity to mass transit—relate to property valuation per unit area, and to evaluate the predictive accuracy of linear regression models on unseen test data."),
            ("Q2. Where does the dataset come from, and who collected it?",
             "The dataset is the official Real Estate Valuation Dataset from the UCI Machine Learning Repository (Dataset ID: 477), published by Prof. I-Cheng Yeh of Tamkang University, Taiwan (2018). It comprises 414 historical property transactions from Sindian District, New Taipei City (2012–2013)."),
            ("Q3. What does the target variable represent, and what are its exact measurement units?",
             "The target variable is 'Y house price of unit area', measured in units of 10,000 New Taiwan Dollars (NTD) per Ping. One Ping is a traditional Taiwanese unit of area equal to approximately 3.306 square metres (or ~35.58 square feet)."),
            ("Q4. Does the dataset contain total house floor area or total transaction price?",
             "No. The dataset does NOT contain total house floor area or total transaction price. The project title is assigned by the course curriculum, but our analysis strictly predicts price per unit area. In accordance with academic integrity, we do not fabricate total area or total price."),
            ("Q5. Can the findings of this project be directly generalized to today's housing market in any city?",
             "No. Inferences strictly apply to Sindian District, New Taipei City during the 2012–2013 timeframe. Spatial layout, transit connectivity, density, and inflation vary substantially across different cities and decades, preventing unconstrained generalization."),
            ("Q6. Why is observation 'No' excluded from all analysis and modeling?",
             "'No' is merely an administrative serial index (1 to 414) denoting transaction order. It carries no economic or physical meaning. Including an arbitrary identifier in a regression model would introduce spurious correlations and violate sound methodology.")
        ]),
        
        ("Category B: Python Programming & Data Handling", [
            ("Q7. What role does Pandas play in this project?",
             "Pandas provides the core tabular data structures (DataFrames and Series) enabling dataset ingestion (pd.read_csv), data type verification, missing-value audits (.isnull().sum()), aggregation (.groupby()), and descriptive summary generation (.describe())."),
            ("Q8. Why is NumPy utilized alongside Pandas?",
             "NumPy provides high-performance vectorized numerical operations, percentile and quartile calculations (np.percentile), mathematical functions (np.sqrt), and random number generation with fixed seed control (np.random.seed(42))."),
            ("Q9. How do Matplotlib and Seaborn differ in your visualization pipeline?",
             "Matplotlib serves as the low-level plotting engine providing explicit control over figure axes, layout geometry, labels, and file exports (plt.savefig). Seaborn is built on top of Matplotlib, providing polished statistical plotting routines such as correlation heatmaps and regression trendlines with confidence bands."),
            ("Q10. How did you verify dataset cleanliness before modeling?",
             "We programmatically audited the dataset: df.shape confirmed 414 rows and 8 columns; df.isnull().sum().sum() verified exactly 0 missing values; df.duplicated().sum() verified 0 duplicate rows; and df.dtypes verified that all 8 columns were valid numerical types (int64 and float64)."),
            ("Q11. Why did you set a random seed (np.random.seed(42)) in your scripts?",
             "A fixed random seed ensures complete scientific reproducibility. Operations involving pseudo-randomness—such as the 80:20 train-test split—generate the exact same partition every time the code executes, allowing evaluators to verify identical numerical metrics."),
            ("Q12. What library was used for statistical hypothesis testing and OLS regression?",
             "Scipy (scipy.stats) was used for Student's t, Welch's t, Mann-Whitney U, and ANOVA calculations. Statsmodels was used for detailed econometric Ordinary Least Squares (OLS) summaries and VIF calculations, while Scikit-Learn was used for the train-test split and predictive evaluation.")
        ]),

        ("Category C: Descriptive Statistics & Data Distributions", [
            ("Q13. What is the fundamental difference between the mean and the median?",
             "The mean is the arithmetic average, computed by summing all values and dividing by sample size; it is sensitive to extreme outliers. The median is the 50th percentile (middle value of sorted observations); it is resistant and robust to extreme skewness and outliers."),
            ("Q14. In your dataset, what are the mean and median of property price per unit area?",
             "The sample mean is 37.980 units (379,800 NTD/Ping), and the sample median is 38.450 units (384,500 NTD/Ping). Because mean and median are remarkably close, the central body of the distribution is largely symmetrical."),
            ("Q15. Did you detect any outliers in the target variable?",
             "Yes. The boxplot and five-number summary revealed an extreme upper outlier transacted at 117.500 units (1,175,000 NTD/Ping)—more than triple the median. We preserved this observation in the raw dataset to reflect genuine market volatility, verifying findings with non-parametric tests."),
            ("Q16. What is the Interquartile Range (IQR) and what was its value for property prices?",
             "IQR is the spread between the 75th percentile (Q3) and 25th percentile (Q1): IQR = Q3 - Q1. It captures the middle 50% of the data. For property price per unit area, Q1 = 27.700, Q3 = 46.600, yielding an IQR of 18.900 units."),
            ("Q17. Which variable in the dataset exhibited the highest dispersion/variability?",
             "Distance to the nearest MRT station (X3) exhibited the highest absolute variance (s² = 1,592,920.63 m², s = 1,262.11 m), spanning from 23.38 metres to 6,488.02 metres. Its mean (1,083.89 m) is more than double its median (492.23 m), demonstrating severe positive skewness."),
            ("Q18. What was the distribution shape of house age (X2)?",
             "House age exhibited a bimodal distribution with a mean of 17.71 years and median of 16.10 years. There is a prominent spike of brand-new properties (mode = 0.0 years) followed by a secondary cluster of mature properties aged 25 to 35 years.")
        ]),

        ("Category D: Probability & Statistical Inference", [
            ("Q19. What is the difference between a sample statistic and a population parameter?",
             "A parameter is a fixed, typically unobservable numerical characteristic of an entire population (e.g., population mean μ, population variance σ²). A statistic is a numerical measure calculated from observed sample data (e.g., sample mean x̄, sample variance s²) used to estimate the parameter."),
            ("Q20. What is Standard Error (SE) and how does it differ from Standard Deviation (s)?",
             "Standard deviation (s = 13.606) measures the dispersion of individual data points around the sample mean. Standard Error (SE = s / √n = 0.669) measures the variability or precision of the sample mean itself across hypothetical repeated random samples of size n."),
            ("Q21. What is the exact 95% confidence interval calculated for mean property price?",
             "The 95% Student's t-confidence interval is [36.666, 39.295] in 10,000 NTD per Ping. It was calculated using x̄ = 37.980, s = 13.606, n = 414, df = 413, and t* = 1.9657, yielding a Margin of Error of 1.315 units."),
            ("Q22. What is the correct academic interpretation of a 95% confidence interval?",
             "If we were to draw repeated independent random samples of size n = 414 from the population and compute a 95% confidence interval from each, approximately 95% of those intervals would encompass the true population mean μ."),
            ("Q23. Why is it technically incorrect to say 'there is a 95% probability that μ lies between 36.666 and 39.295'?",
             "In classical frequentist statistics, the population mean μ is a fixed unknown constant, not a random variable. The interval is fixed once calculated. Therefore, the parameter μ is either inside the interval (probability 1) or outside it (probability 0). The 95% probability refers to the long-run performance of the estimation procedure."),
            ("Q24. Define Type I error and Type II error in hypothesis testing.",
             "A Type I error (false positive) occurs when a researcher rejects a true null hypothesis H₀; its maximum probability is controlled by the significance level α (0.05). A Type II error (false negative, probability β) occurs when a researcher fails to reject a false null hypothesis.")
        ]),

        ("Category E: Hypothesis Testing (Welch's t-Test & ANOVA)", [
            ("Q25. Why did you use Welch's t-test instead of Student's standard independent two-sample t-test?",
             "Student's standard two-sample t-test assumes equal population variances (homoscedasticity). In real estate, pricing variances differ between prime urban transit zones and distant peripheral zones. Welch's t-test relaxes the equal variance assumption, providing robust Type I error control."),
            ("Q26. What were the hypotheses and findings for your MRT proximity test?",
             "H₀: μ_Near - μ_Far = 0 vs. H₁: μ_Near - μ_Far ≠ 0 (split at sample median MRT = 492.23 m). Near MRT (n=210) had x̄ = 46.265; Far MRT (n=204) had x̄ = 29.452. Welch t = 15.995 (df = 399.78), p = 4.065 × 10⁻⁴⁵. We decisively reject H₀, proving a significant +57.1% transit price premium."),
            ("Q27. Why did you perform a Mann-Whitney U test as a robustness check?",
             "Because property prices include an extreme upper outlier (117.50 units) and slight positive skew, we ran the non-parametric Mann-Whitney U test on ranked data. It yielded U = 37,669.0, p = 1.195 × 10⁻⁴⁰, proving that the transit premium is not an artifact of outliers or non-normality."),
            ("Q28. What is One-Way ANOVA and why was it used for house age?",
             "ANOVA (Analysis of Variance) tests whether the population means of three or more independent groups are equal by partitioning total sum of squares into between-group and within-group variance. We used it to test whether mean property prices differ across younger, middle-aged, and older tertiles."),
            ("Q29. What were the ANOVA results for house-age tertiles?",
             "The test yielded F = 32.062 (df = 2, 411) with p = 1.150 × 10⁻¹³. Because p < 0.05, we reject H₀, concluding that at least one house-age tertile has a significantly different population mean price."),
            ("Q30. What did Tukey's HSD post-hoc test reveal about house-age groups?",
             "Tukey's HSD showed that Younger properties (x̄ = 44.91) had significantly higher mean prices than Middle-aged (x̄ = 33.34, p < 0.001) and Older properties (x̄ = 35.69, p < 0.001). However, the difference between Middle-aged and Older properties (-2.35 units, p = 0.286) was NOT statistically significant."),
            ("Q31. How did you verify ANOVA assumptions?",
             "We checked normality of residuals using a Q-Q plot and the Shapiro-Wilk test (W = 0.9577, p = 8.16e-10), which showed slight tail departure. We tested homogeneity of variances using Levene's test (Stat = 2.060, p = 0.1287); because p > 0.05, equal variance was satisfied.")
        ]),

        ("Category F: Correlation Analysis", [
            ("Q32. What is the difference between Pearson correlation (r) and Spearman correlation (ρ)?",
             "Pearson r measures the strength and direction of linear relationships between continuous variables. Spearman ρ is a non-parametric rank correlation that measures monotonic relationships (whether variables increase/decrease together) and is robust to non-linearities and outliers."),
            ("Q33. What was the correlation between distance to nearest MRT and property price?",
             "MRT distance had a strong negative linear correlation of Pearson r = -0.674 (p = 4.64 × 10⁻⁵⁶) and an even stronger monotonic correlation of Spearman ρ = -0.776 (p = 1.81 × 10⁻⁸⁴)."),
            ("Q34. Why is Spearman's correlation (ρ = -0.776) stronger than Pearson's (r = -0.674) for MRT distance?",
             "The relationship is non-linear and decaying: property prices drop sharply within the first 1,000 metres of an MRT station and then flatten into a plateau. Spearman's rank ordering captures this monotonic curve better than a straight Pearson line."),
            ("Q35. Number of convenience stores had a positive correlation (r = +0.571). Does opening a new store cause house prices to rise?",
             "No. Correlation does not imply causation. In urban centers, convenience stores and rapid transit stations naturally cluster in densely populated, commercialized areas. The presence of stores is a proxy for urban amenities and commercial density, not a direct mechanical cause of higher property values.")
        ]),

        ("Category G: Regression Analysis & Diagnostics", [
            ("Q36. What is the Simple Linear Regression equation fitted for house age?",
             "The OLS equation is: Ŷ = 42.4347 - 0.2515 × (House Age). The intercept (42.435) is the expected price per Ping for a brand-new house (Age = 0), and the slope (-0.2515) indicates an expected decrease of 2,515 NTD per Ping per year of age."),
            ("Q37. What is R-squared (R²) and what was its value for the Simple Linear Regression model?",
             "R² (coefficient of determination) measures the proportion of variance in the dependent variable explained by the independent variables. For the SLR model, R² = 0.0443 (4.43%). Building age alone explains less than 5% of property price variance, leaving over 95.5% unexplained."),
            ("Q38. What is the Multiple Linear Regression equation fitted in your project?",
             "The fitted OLS equation is: Ŷ = 49.8856 - 0.2310 × (House Age) - 0.0072 × (MRT Distance). Overall model fit is R² = 0.4911 (49.11%), with an F-statistic of 198.3 (p = 2.65 × 10⁻⁶⁰)."),
            ("Q39. How do you interpret the coefficients in the Multiple Linear Regression model?",
             "Holding MRT distance constant, each additional year of house age reduces unit price by 0.2310 units (2,310 NTD/Ping, p = 1.05e-7). Holding house age constant, each additional 100 metres of distance from an MRT station reduces unit price by 0.72 units (7,200 NTD/Ping, p = 2.44e-53)."),
            ("Q40. What is multicollinearity and how did you test for it?",
             "Multicollinearity occurs when predictor variables are highly correlated with each other, destabilizing coefficient estimates and inflating standard errors. We tested it using the Variance Inflation Factor (VIF). Both VIF(Age) and VIF(MRT) were exactly 1.001 (far below the warning threshold of 5.0), confirming zero collinearity."),
            ("Q41. What did residual diagnostic plots reveal about the Multiple Regression model?",
             "Residuals vs. fitted plots showed general linearity and independence, but revealed slight fan-shaped heteroscedasticity (larger variance at higher predicted prices) and positive skewness in the Q-Q plot driven by the single high-value transaction at 117.50 units.")
        ]),

        ("Category H: Predictive Evaluation & Applied Decision Making", [
            ("Q42. Why did you use an 80:20 train-test split rather than evaluating on the whole dataset?",
             "Evaluating a model on training data introduces optimism bias because parameters are tuned to fit those specific points. An 80:20 split (331 train, 83 test) provides an unbiased assessment of how well the model generalizes to previously unseen property transactions."),
            ("Q43. Compare the test-set performance metrics between SLR and MLR.",
             "On the held-out test set: MLR reduced MAE by 41.2% (from 10.621 to 6.248 units), reduced RMSE by 34.4% (from 12.853 to 8.438 units), and increased test R² from 0.0152 (1.5%) to 0.5756 (57.6%). MLR is decisively superior."),
            ("Q44. What does a Mean Absolute Error (MAE) of 6.248 units mean in practical real estate terms?",
             "It means that on unseen transactions in this district, the multiple regression model's predictions differ from actual recorded market prices by an average of 6.248 units, which equals 62,480 New Taiwan Dollars per Ping (~$2,000 USD per 3.3 m²)."),
            ("Q45. Why is RMSE (8.438) higher than MAE (6.248)?",
             "RMSE squares individual errors before taking the square root, giving disproportionate penalty to large prediction errors. In real estate appraisal, where occasional luxury or renovated homes create large positive errors, RMSE will always exceed MAE."),
            ("Q46. Can a test R-squared ever be negative, and what would it mean?",
             "Yes, on held-out test data, R² = 1 - (SS_res / SS_tot) can be negative if the model's predictions perform worse than simply predicting the training mean for every test observation. Our MLR model achieved a positive test R² of 0.5756, indicating robust explanatory power."),
            ("Q47. If an appraiser inputs House Age = 2 years and MRT Distance = 150 metres, what is the predicted price?",
             "Applying Ŷ = 49.8856 - 0.2310(2) - 0.0072(150), the model predicts 48.51 units (485,100 NTD per Ping), accurately capturing the premium commanded by new transit-adjacent properties."),
            ("Q48. What are the two most critical takeaways from this entire statistical study?",
             "First, mass transit accessibility is the single dominant driver of residential unit-area property value in Sindian District, explaining nearly 50% of market variation, whereas building age has only a modest, non-linear impact. Second, multiple regression models generalize effectively to unseen data, cutting prediction errors by over 40% compared to single-variable baselines.")
        ])
    ]

    for cat_name, q_list in viva_categories:
        story.append(Paragraph(cat_name, cat_heading))
        story.append(HRFlowable(width="100%", thickness=0.5, color=c_secondary, spaceBefore=1, spaceAfter=6))
        for q_text, a_text in q_list:
            story.append(Paragraph(f"<b>{q_text}</b>", q_style))
            story.append(Paragraph(a_text, a_style))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=VivaNumberedCanvas)
    
    reader = pypdf.PdfReader(output_pdf)
    num_pages = len(reader.pages)
    print(f"Viva Questions & Answers PDF successfully created at: {output_pdf}")
    print(f"Total Page Count: {num_pages} pages | Questions Prepared: 48 questions")
    return output_pdf, num_pages

if __name__ == '__main__':
    build_viva_pdf()

