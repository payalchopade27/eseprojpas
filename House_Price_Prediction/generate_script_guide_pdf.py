"""
Script to generate outputs/Presentation_Script_and_Demo_Guide.pdf
Four core parts:
Part A: 5-7 Minute Natural Slide-by-Slide Presentation Script
Part B: Step-by-Step Live Notebook Demonstration Guide
Part C: Faculty Difficult Question Handling & Survival Tactics
Part D: 1-Page Last-Minute Examination Revision Cheat Sheet
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

class DemoNumberedCanvas(canvas.Canvas):
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
        
        # Header
        self.drawString(54, 800, "Presentation Script, Live Demonstration Guide & Quick Revision Sheet")
        self.drawRightString(541, 800, "Probability & Statistics Course Project")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.line(54, 48, 541, 48)
        self.drawString(54, 38, "House Area, Age and Property Price Prediction | Academic Defense Package")
        self.drawRightString(541, 38, page_text)
        self.restoreState()

def build_demo_guide_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(base_dir, "outputs", "Presentation_Script_and_Demo_Guide.pdf")
    
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
    c_accent = colors.HexColor("#C53030")     # Red
    c_bg_light = colors.HexColor("#F7FAFC")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceAfter=12
    )
    
    part_heading = ParagraphStyle(
        'PartHeading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    script_spoken = ParagraphStyle(
        'ScriptSpoken',
        parent=body,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor("#1A202C"),
        leftIndent=12,
        spaceAfter=6
    )
    
    box_header = ParagraphStyle(
        'BoxHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#2C5282")
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )
    
    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("Presentation Speaking Script, Live Demo Sequence & Revision Guide", title_style))
    story.append(Paragraph("A Comprehensive Practical Handbook for Academic Defense & Faculty Viva Voce", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=10))

    # ====================================================
    # PART A: 5-7 MINUTE PRESENTATION SCRIPT
    # ====================================================
    story.append(Paragraph("Part A: 5–7 Minute Natural Presentation Speaking Script", part_heading))
    story.append(Paragraph(
        "This slide-by-slide script is written from the first-person perspective of an engineering student explaining her own project. "
        "It avoids robotic jargon, emphasizes practical intuition, clearly highlights genuine numbers, and transitions naturally across the 12 presentation slides. "
        "Estimated speaking pace: ~130–140 words per minute (~6 minutes total).",
        body
    ))
    story.append(Spacer(1, 4))

    slides_script = [
        ("Slide 1: Title Slide (0:00 – 0:30)",
         "Good morning, respected professors and evaluation committee members. Today, I am presenting my Probability and Statistics course project titled 'House Area, Age and Property Price Prediction.' "
         "In this study, we bridge theoretical statistical inference with practical predictive modeling using genuine historical real estate transactions from the UCI Machine Learning Repository. "
         "We investigate how structural building age and proximity to mass transit explain residential property valuations. Let us begin with the project motivation."),
         
        ("Slide 2: Introduction & Problem Statement (0:30 – 1:05)",
         "Real estate valuation is central to household wealth, commercial lending, and municipal development. Traditionally, property appraisers relied on subjective heuristics or small comparable sales. "
         "Our goal is to apply statistical science to answer four fundamental questions: First, what are the reliable population bounds for property valuation? "
         "Second, does proximity to mass transit deliver a measurable price premium? Third, does building age cause a linear decay in valuation? "
         "And fourth, can linear regression generalize accurately to predict prices on unseen test transactions?"),

        ("Slide 3: Dataset Provenance & Crucial Boundaries (1:05 – 1:45)",
         "Our study uses the official Real Estate Valuation Dataset collected by Prof. I-Cheng Yeh from Sindian District, New Taipei City, Taiwan, containing 414 historical transactions. "
         "Right at the outset, I want to clarify an essential dataset characteristic: While our course project title includes the words 'House Area,' the dataset itself does NOT record total floor area or total transaction price. "
         "The actual target variable is price per unit area, measured in 10,000 New Taiwan Dollars per Ping, where one Ping is roughly 3.3 square metres. "
         "Rather than fabricating artificial area figures, our analysis maintains complete academic integrity by modeling and predicting price per unit area directly."),

        ("Slide 4: Exploratory Data Analysis & Distributions (1:45 – 2:20)",
         "Before fitting any models, we verified dataset hygiene. There are zero missing values and zero duplicates across all 414 observations. "
         "Looking at the distributions on this slide, the target price per unit area has a sample mean of 37.98 and median of 38.45 units, showing a symmetric central body with an IQR of 18.9 units. "
         "We identified a single extreme upper outlier at 117.5 units, which we preserved and verified through non-parametric methods. "
         "Furthermore, house age exhibits a bimodal distribution with a large spike of brand-new properties alongside older homes built 30 years ago."),

        ("Slide 5: Comprehensive Descriptive Statistics (2:20 – 3:00)",
         "Turning to our numerical summary, the most striking finding is the dispersion of transit distance. Properties range from just 23 metres to nearly 6.5 kilometres from the nearest MRT station. "
         "Its standard deviation exceeds 1,260 metres, and its mean of 1,083 metres is more than double its median of 492 metres, confirming severe right-skewness. "
         "In contrast, convenience stores average about 4 per property. This spatial disparity establishes why transit proximity plays such a dominant role in our subsequent inferential tests."),

        ("Slide 6: Confidence Interval & Transit Hypothesis Test (3:00 – 3:45)",
         "In our inferential analysis, we first constructed a 95% Student's t-confidence interval for the population mean property price. With 413 degrees of freedom and a margin of error of 1.315 units, "
         "the true mean unit price lies within [36.666, 39.295] with 95% confidence. "
         "Next, we tested whether transit accessibility creates a significant valuation difference by splitting the data at the median distance of 492 metres. "
         "Conducting a two-sample Welch's t-test, properties near an MRT station averaged 46.27 units versus 29.45 units for distant properties. "
         "The test statistic was t = 15.995 with p = 4.065e-45, decisively rejecting the null hypothesis. Transit-proximate properties enjoy an average premium of 57.1%, "
         "a finding corroborated by a non-parametric Mann-Whitney U test with p = 1.195e-40."),

        ("Slide 7: One-Way ANOVA & Correlation Analysis (3:45 – 4:30)",
         "We also investigated property age across three balanced tertile cohorts using One-Way ANOVA. The test yielded F = 32.062 with p = 1.15e-13, rejecting the null hypothesis of equal cohort means. "
         "However, Tukey's HSD post-hoc test revealed a fascinating non-linear dynamic: Younger properties command a significant premium over middle-aged and older homes (p < 0.001), "
         "but the difference between middle-aged and older homes is statistically insignificant (p = 0.286). Building depreciation plateaus after the first decade. "
         "In our correlation analysis, MRT distance displayed the strongest relationship with r = -0.674 and Spearman rho = -0.776, while convenience stores showed a moderate positive association of r = 0.571."),

        ("Slide 8: Simple vs. Multiple Linear Regression (4:30 – 5:10)",
         "To test predictive capacity, we first formulated a Simple Linear Regression using house age. Although the slope of -0.2515 units per year is statistically significant (p = 1.56e-5), "
         "the model achieved an R² of only 0.0443—meaning age explains less than 5% of price variation. "
         "We then expanded to a Multiple Linear Regression incorporating both house age and MRT distance. The resulting equation is Y_hat = 49.8856 - 0.2310*Age - 0.0072*MRT_Dist. "
         "This increased R² eleven-fold to 0.4911. Both predictors are highly significant (p < 10⁻⁶), and VIF values of exactly 1.001 confirm complete absence of multicollinearity."),

        ("Slide 9: Out-of-Sample Predictive Evaluation (5:10 – 5:50)",
         "To rigorously evaluate generalization, we tested both models on a strictly held-out 20% test partition of 83 unseen transactions. "
         "The Multiple Regression model decisively outperformed the simple model: Mean Absolute Error dropped from 10.62 to 6.25 units—a 41.2% reduction in prediction error. "
         "RMSE dropped by 34.4%, and test R² surged from 0.0152 to 0.5756. "
         "On unseen data, combining age and transit proximity explains over 57.5% of market price variation, proving the practical value of multiple regression."),

        ("Slide 10: Practical Valuation Scenarios (5:50 – 6:20)",
         "To demonstrate real-world appraisal utility, we evaluated three representative profiles within our observed domain. "
         "A brand-new property 150 metres from an MRT station is predicted at 48.51 units (485,100 NTD/Ping). A mid-aged suburban apartment at 600 metres yields 42.27 units. "
         "Meanwhile, an older property 2.2 kilometres away drops to 27.05 units—a steep 44.2% discount reflecting the cumulative penalty of age and transit isolation."),

        ("Slide 11: Limitations & Future Scope (6:20 – 6:45)",
         "Every rigorous study must acknowledge its boundaries. First, total floor area is unobserved, meaning we cannot predict total house price. "
         "Second, the data represents 414 historical transactions from Sindian District in 2012–2013 and should not be blindly applied to modern cities without recalibration. "
         "Finally, unobserved factors like floor elevation and interior layout represent omitted variables. Future work could incorporate modern geospatial satellite layers and non-linear machine learning."),

        ("Slide 12: Conclusion & Q&A (6:45 – 7:05)",
         "In summary, mass transit proximity is the single dominant determinant of property price per unit area in Sindian District, explaining nearly 50% of market variance. "
         "Building age has a secondary, non-linear impact concentrated in early years. Most importantly, multiple regression cuts unseen prediction errors by over 40%. "
         "Thank you for your time and attention. I am now delighted to take your questions.")
    ]

    for s_title, s_text in slides_script:
        story.append(Paragraph(f"<b>{s_title}</b>", section_heading))
        story.append(Paragraph(f"<i>\"{s_text}\"</i>", script_spoken))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # ====================================================
    # PART B: LIVE NOTEBOOK DEMONSTRATION GUIDE
    # ====================================================
    story.append(Paragraph("Part B: Step-by-Step Live Notebook Demonstration Sequence", part_heading))
    story.append(Paragraph(
        "When presenting in front of faculty or defense examiners, follow this exact 10-step sequence across your two executed notebooks. "
        "Keep your browser or Jupyter interface open, zoomed to ~125% for legibility.",
        body
    ))
    story.append(Spacer(1, 4))

    demo_steps = [
        ("Step 1: Open Project Directory & Inspect Structure",
         "Directory Terminal / Explorer",
         "Show clean separation: data/raw, notebooks, outputs/figures, requirements.txt, README.md.",
         "Demonstrates organized, professional software engineering practices."),
        
        ("Step 2: Launch '01_Dataset_Exploration.ipynb'",
         "Notebook 1, Sections 1 & 3",
         "Point to dataset citation (UCI ID: 477) and emphasize that Y is price per unit area (10,000 NTD/Ping).",
         "Proves you understand dataset boundaries and aren't claiming total price prediction."),
        
        ("Step 3: Show Data Quality & Hygiene Cells",
         "Notebook 1, Section 5",
         "Scroll to missing value audit (df.isnull().sum() = 0), duplicate check (= 0), and 'No' identifier exclusion.",
         "Shows faculty that the data was programmatically verified before any modeling."),
        
        ("Step 4: Display Initial Distribution Visualizations",
         "Notebook 1, Section 7",
         "Highlight Histogram and Boxplot of Y (Figures 01 & 04) showing median 38.45 and outlier 117.5.",
         "Demonstrates mastery of univariate exploratory data analysis."),
         
        ("Step 5: Launch '02_Statistical_Analysis.ipynb'",
         "Notebook 2, Section 3",
         "Display Table of Comprehensive Descriptive Statistics (Mean, Median, Std, IQR for X2, X3, X4, Y).",
         "Show that MRT distance has extreme variance (s = 1,262 m) and heavy right-skewness."),
         
        ("Step 6: Demonstrate 95% Confidence Interval Calculation",
         "Notebook 2, Section 4",
         "Walk through x̄ = 37.980, s = 13.606, df = 413, t* = 1.9657, MoE = 1.315 -> CI: [36.666, 39.295].",
         "Explain the frequentist definition of confidence intervals and avoid the 'probability fallacy'."),
         
        ("Step 7: Demonstrate Welch's Two-Sample t-Test & Robustness",
         "Notebook 2, Section 5",
         "Show median split (492.2 m), group means (46.26 vs 29.45), t = 15.995, p = 4.06e-45, and Mann-Whitney U.",
         "Proves transit proximity is statistically overwhelming (+57% premium) and robust to outliers."),
         
        ("Step 8: Demonstrate One-Way ANOVA & Post-Hoc Tukey HSD",
         "Notebook 2, Section 6",
         "Show tertiles summary, ANOVA F = 32.062 (p = 1.15e-13), and Tukey pairwise differences.",
         "Highlight that Younger homes are significantly higher, but Middle vs Older is NOT significant (p = 0.286)."),
         
        ("Step 9: Demonstrate Multiple Regression & Multicollinearity (VIF)",
         "Notebook 2, Sections 8 & 9",
         "Contrast SLR (R² = 0.044) with MLR (R² = 0.491). Point to VIF table where both values equal 1.001.",
         "Shows that age alone is weak, transit adds massive power, and multicollinearity is absent."),
         
        ("Step 10: Demonstrate Out-of-Sample Predictive Evaluation (80:20)",
         "Notebook 2, Section 10",
         "Show evaluation table: MLR cuts MAE by 41.2% (6.25 vs 10.62) and achieves test R² = 0.5756 on held-out test data.",
         "Concludes the demo on modern machine learning rigor—model validated on unseen test data.")
    ]

    t_demo_data = [
        [Paragraph("<b>Step & Action</b>", table_header), Paragraph("<b>Target Section</b>", table_header), Paragraph("<b>What to Show & Explain</b>", table_header), Paragraph("<b>What Evaluator Notices</b>", table_header)]
    ]
    for st, sec, exp, notc in demo_steps:
        t_demo_data.append([
            Paragraph(f"<b>{st}</b>", table_cell),
            Paragraph(sec, table_cell_center),
            Paragraph(exp, table_cell),
            Paragraph(notc, table_cell)
        ])
        
    t_demo = Table(t_demo_data, colWidths=[110, 85, 170, 115])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_demo)
    story.append(PageBreak())

    # ====================================================
    # PART C: FACULTY DIFFICULT QUESTION HANDLING
    # ====================================================
    story.append(Paragraph("Part C: Faculty Difficult Question Handling & Defense Tactics", part_heading))
    story.append(Paragraph(
        "Evaluation committees often probe conceptual edges, edge cases, and methodological limitations to assess true understanding. "
        "Below are model handling strategies for the 4 most challenging questions.",
        body
    ))
    story.append(Spacer(1, 4))

    tough_questions = [
        ("Tough Question 1: 'Your SLR has p < 0.0001 for house age, yet you claim house age barely explains property prices. Isn't that contradictory?'",
         "Handling Strategy: Distinguish statistical significance from practical explanatory power.",
         "Answer: 'Not at all, professor. Statistical significance simply means we can reject the null hypothesis that the slope is exactly zero—with n = 414, even tiny slope effects produce small p-values. However, practical explanatory power is measured by R-squared, which is only 0.0443. This means house age alone leaves over 95.5% of market price variation completely unexplained. A statistically real relationship is not necessarily an economically powerful one.'"),

        ("Tough Question 2: 'Convenience stores have r = +0.571. If a developer builds 5 convenience stores, will unit price increase by 10 units?'",
         "Handling Strategy: Reject causal interpretation and explain urban spatial co-location.",
         "Answer: 'No, professor. Correlation does not imply causation. In New Taipei City, commercial convenience stores co-locate around rapid transit hubs and high-density population nodes. The store count is a spatial proxy for commercial vibrancy and urban density, not an isolated mechanical cause of price appreciation.'"),

        ("Tough Question 3: 'Why did you use Welch's t-test instead of standard Student's t-test?'",
         "Handling Strategy: Reference unequal population variances in spatial sub-markets.",
         "Answer: 'Student's t-test assumes homoscedasticity—equal variances between groups. In real estate, properties in prime transit cores show higher price dispersion (variance = 138.2) than peripheral suburban properties (variance = 88.1). Welch's t-test does not assume equal variances, providing robust protection against inflated Type I errors.'"),

        ("Tough Question 4: 'If you do not know the answer to a question during viva...'",
         "Handling Strategy: Intellectual honesty, foundational reasoning, and research poise.",
         "Answer: 'Professor, I have not explored that specific aspect in depth, but based on our statistical findings, my initial hypothesis would be... I would be delighted to research that further as part of our future scope.' (Never fabricate answers or argue blindly).")
    ]

    for q_t, h_t, a_t in tough_questions:
        story.append(Paragraph(f"<b>{q_t}</b>", section_heading))
        story.append(Paragraph(f"<b>{h_t}</b>", body))
        story.append(Paragraph(f"<i>\"{a_t}\"</i>", script_spoken))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # ====================================================
    # PART D: 1-PAGE LAST-MINUTE REVISION CHEAT SHEET
    # ====================================================
    story.append(Paragraph("Part D: 1-Page Last-Minute Examination Revision Cheat Sheet", part_heading))
    story.append(Paragraph("Memorize these verified constants, equations, test outcomes, and core definitions before entering your defense.", subtitle_style))
    story.append(Spacer(1, 2))

    cheat_data = [
        [Paragraph("<b>Category</b>", table_header), Paragraph("<b>Key Formula / Model Equation</b>", table_header), Paragraph("<b>Verified Project Value / Result</b>", table_header), Paragraph("<b>Exam Defense Key Takeaway</b>", table_header)],
        [Paragraph("Dataset Profile", table_cell), Paragraph("UCI ID 477, Sindian, Taiwan", table_cell), Paragraph("n = 414, 8 cols, 0 missing, 0 dupes", table_cell), Paragraph("Target is price per unit area (10,000 NTD/Ping). No floor area.", table_cell)],
        [Paragraph("Target Price Y", table_cell), Paragraph("Mean, Med, Mode, IQR", table_cell), Paragraph("x̄ = 37.980, M = 38.450, IQR = 18.900", table_cell), Paragraph("Symmetric body, max outlier at 117.50 units.", table_cell)],
        [Paragraph("Transit Dist X3", table_cell), Paragraph("Mean vs Median", table_cell), Paragraph("x̄ = 1,083.89 m, Med = 492.23 m", table_cell), Paragraph("Extreme right-skewness (Mean > 2× Median).", table_cell)],
        [Paragraph("95% Conf Interval", table_cell), Paragraph("CI = x̄ ± t_{α/2, n-1} * (s/√n)", table_cell), Paragraph("[36.666, 39.295], MoE = 1.315", table_cell), Paragraph("Student's t with df = 413, t* = 1.9657.", table_cell)],
        [Paragraph("Welch's t-Test", table_cell), Paragraph("Near (≤492m) vs Far (>492m)", table_cell), Paragraph("t = 15.995, df = 399.78, p = 4.06e-45", table_cell), Paragraph("Reject H₀. +57.1% premium for transit proximity.", table_cell)],
        [Paragraph("Mann-Whitney U", table_cell), Paragraph("Rank-sum robustness check", table_cell), Paragraph("U = 37,669.0, p = 1.195e-40", table_cell), Paragraph("Confirms t-test significance is immune to outliers.", table_cell)],
        [Paragraph("One-Way ANOVA", table_cell), Paragraph("Age Tertiles: Young, Mid, Old", table_cell), Paragraph("F = 32.062, df = (2, 411), p = 1.15e-13", table_cell), Paragraph("Reject H₀. Significant age group differences exist.", table_cell)],
        [Paragraph("Tukey HSD", table_cell), Paragraph("Pairwise comparisons", table_cell), Paragraph("Young vs Mid: p<0.001 | Mid vs Old: p=0.286", table_cell), Paragraph("Depreciation plateau: older homes do not drop further.", table_cell)],
        [Paragraph("Correlations", table_cell), Paragraph("Pearson r & Spearman ρ", table_cell), Paragraph("MRT: r = -0.674, ρ = -0.776; Age: r = -0.211", table_cell), Paragraph("MRT is dominant; Spearman stronger due to curvature.", table_cell)],
        [Paragraph("Simple Regression", table_cell), Paragraph("Ŷ = β₀ + β₁ * Age", table_cell), Paragraph("Ŷ = 42.4347 - 0.2515*Age, R² = 0.0443", table_cell), Paragraph("Significant slope, but age explains only 4.4% variance.", table_cell)],
        [Paragraph("Multiple Regression", table_cell), Paragraph("Ŷ = β₀ + β₁*Age + β₂*MRT", table_cell), Paragraph("Ŷ = 49.8856 - 0.2310*Age - 0.0072*MRT", table_cell), Paragraph("R² = 0.4911 (11× gain). VIF = 1.001 (Zero collinearity).", table_cell)],
        [Paragraph("Predictive Evaluation", table_cell), Paragraph("Held-out 20% test (n = 83)", table_cell), Paragraph("MLR Test MAE = 6.248, Test R² = 0.5756", table_cell), Paragraph("MLR cuts MAE by 41.2% over SLR (10.62 -> 6.25).", table_cell)],
        [Paragraph("Sample Valuation", table_cell), Paragraph("New transit condo (2y, 150m)", table_cell), Paragraph("Predicted: 48.51 units (485,100 NTD/Ping)", table_cell), Paragraph("Captures realistic market transit premium.", table_cell)]
    ]
    t_cheat = Table(cheat_data, colWidths=[90, 130, 130, 130])
    t_cheat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_cheat)

    doc.build(story, canvasmaker=DemoNumberedCanvas)
    
    reader = pypdf.PdfReader(output_pdf)
    num_pages = len(reader.pages)
    print(f"Presentation Script & Demo Guide PDF successfully created at: {output_pdf}")
    print(f"Total Page Count: {num_pages} pages")
    return output_pdf, num_pages

if __name__ == '__main__':
    build_demo_guide_pdf()

