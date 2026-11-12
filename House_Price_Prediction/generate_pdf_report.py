"""
Script to generate outputs/Final_Project_Report.pdf
Target: 18-25 pages professional academic PDF with ReportLab.
Numbered Canvas for Page X of Y, Running Headers/Footers, Figures, Tables, Equations.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

class NumberedCanvas(canvas.Canvas):
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
        if self._pageNumber == 1:
            return  # Suppress headers and footers on cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Running Header
        header_text = "House Area, Age and Property Price Prediction | Academic Project Report"
        self.drawString(54, 800, header_text)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Running Footer
        footer_text = "Course: Probability & Statistics (UCI Dataset ID: 477)"
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.line(54, 48, 541, 48)
        self.drawString(54, 38, footer_text)
        self.drawRightString(541, 38, page_text)
        self.restoreState()

def build_pdf_report():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(base_dir, "outputs", "Final_Project_Report.pdf")
    figures_dir = os.path.join(base_dir, "outputs", "figures")
    
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1A365D")    # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0")  # Slate Blue
    c_dark = colors.HexColor("#2D3748")       # Charcoal Body
    c_accent = colors.HexColor("#C53030")     # Dark Red
    c_bg_light = colors.HexColor("#F7FAFC")   # Light gray-white
    c_callout_bg = colors.HexColor("#EDF2F7") # Light box
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=25
    )
    
    cover_meta = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=c_dark,
        alignment=1
    )
    
    h1 = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2 = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=7
    )
    
    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )
    
    caption_style = ParagraphStyle(
        'CustomCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#4A5568"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#2C5282")
    )
    
    eq_style = ParagraphStyle(
        'EquationStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        alignment=1, # Center
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=6
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

    def make_callout(text, width=480):
        p = Paragraph(f"<b>Important Clarification:</b> {text}", callout_style)
        t = Table([[p]], colWidths=[width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
            ('BOX', (0,0), (-1,-1), 1, c_secondary),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # ----------------------------------------------------
    # 1. COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("COLLEGE OF ENGINEERING & TECHNOLOGY", cover_meta))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", cover_meta))
    story.append(Spacer(1, 50))
    story.append(Paragraph("HOUSE AREA, AGE AND PROPERTY PRICE PREDICTION", title_style))
    story.append(Paragraph("A Comprehensive Statistical Analysis, Hypothesis Testing, and Predictive Evaluation Study", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=c_secondary, spaceBefore=10, spaceAfter=25))
    story.append(Spacer(1, 40))
    
    cover_table_data = [
        [Paragraph("<b>Course:</b>", table_cell), Paragraph("Probability and Statistics", table_cell)],
        [Paragraph("<b>Dataset:</b>", table_cell), Paragraph("Real Estate Valuation Dataset (UCI ML Repository ID: 477)", table_cell)],
        [Paragraph("<b>Dataset Author:</b>", table_cell), Paragraph("Prof. I-Cheng Yeh (Tamkang University, Taiwan, 2018)", table_cell)],
        [Paragraph("<b>Student Name:</b>", table_cell), Paragraph("[Student Name Placeholder]", table_cell)],
        [Paragraph("<b>Roll / Registration No:</b>", table_cell), Paragraph("[Roll Number Placeholder]", table_cell)],
        [Paragraph("<b>Faculty Guide:</b>", table_cell), Paragraph("[Faculty Name / Guide Placeholder]", table_cell)],
        [Paragraph("<b>Academic Year:</b>", table_cell), Paragraph("2025–2026", table_cell)],
        [Paragraph("<b>Submission Date:</b>", table_cell), Paragraph("November 2026", table_cell)],
    ]
    t_cover = Table(cover_table_data, colWidths=[150, 250])
    t_cover.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 50))
    story.append(Paragraph("<i>Note: This study is based strictly on genuine historical property transactions. All computed values are derived programmatically from verified Jupyter notebooks.</i>", cover_meta))
    story.append(PageBreak())

    # ----------------------------------------------------
    # TABLE OF CONTENTS / OUTLINE
    # ----------------------------------------------------
    story.append(Paragraph("Table of Contents", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=4, spaceAfter=12))
    
    toc_data = [
        [Paragraph("<b>Section</b>", table_header), Paragraph("<b>Title & Core Content</b>", table_header), Paragraph("<b>Page</b>", table_header)],
        [Paragraph("1", table_cell_center), Paragraph("Abstract", table_cell), Paragraph("3", table_cell_center)],
        [Paragraph("2", table_cell_center), Paragraph("Introduction, Motivation & Problem Statement", table_cell), Paragraph("3", table_cell_center)],
        [Paragraph("3", table_cell_center), Paragraph("Dataset Provenance, Description & Crucial Boundaries", table_cell), Paragraph("4", table_cell_center)],
        [Paragraph("4", table_cell_center), Paragraph("Exploratory Data Analysis & Verification", table_cell), Paragraph("6", table_cell_center)],
        [Paragraph("5", table_cell_center), Paragraph("Descriptive Statistical Analysis", table_cell), Paragraph("7", table_cell_center)],
        [Paragraph("6", table_cell_center), Paragraph("Probability & Statistical Inference (95% Confidence Interval)", table_cell), Paragraph("9", table_cell_center)],
        [Paragraph("7", table_cell_center), Paragraph("Hypothesis Testing I: Proximity to Mass Transit (Welch's t-test)", table_cell), Paragraph("10", table_cell_center)],
        [Paragraph("8", table_cell_center), Paragraph("Hypothesis Testing II: House-Age Tertiles (One-Way ANOVA & Tukey HSD)", table_cell), Paragraph("12", table_cell_center)],
        [Paragraph("9", table_cell_center), Paragraph("Bivariate Correlation Analysis (Pearson & Spearman)", table_cell), Paragraph("14", table_cell_center)],
        [Paragraph("10", table_cell_center), Paragraph("Simple Linear Regression Modelling (House Age)", table_cell), Paragraph("15", table_cell_center)],
        [Paragraph("11", table_cell_center), Paragraph("Multiple Linear Regression Modelling & Multicollinearity (VIF)", table_cell), Paragraph("16", table_cell_center)],
        [Paragraph("12", table_cell_center), Paragraph("Train-Test Evaluation (80:20 Split) & Predictive Comparison", table_cell), Paragraph("18", table_cell_center)],
        [Paragraph("13", table_cell_center), Paragraph("Sample Valuation Predictions & Scenario Analysis", table_cell), Paragraph("19", table_cell_center)],
        [Paragraph("14", table_cell_center), Paragraph("Synthesis of Statistical Findings", table_cell), Paragraph("20", table_cell_center)],
        [Paragraph("15", table_cell_center), Paragraph("Project Limitations & Analytical Caveats", table_cell), Paragraph("21", table_cell_center)],
        [Paragraph("16", table_cell_center), Paragraph("Conclusions & Academic Learnings", table_cell), Paragraph("22", table_cell_center)],
        [Paragraph("17", table_cell_center), Paragraph("References & Citations", table_cell), Paragraph("22", table_cell_center)]
    ]
    t_toc = Table(toc_data, colWidths=[45, 390, 45])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light])
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 14))

    # ----------------------------------------------------
    # SECTION 1: ABSTRACT
    # ----------------------------------------------------
    story.append(Paragraph("1. Abstract", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    abstract_text = (
        "Real estate valuation represents a fundamental domain in applied econometrics, urban geography, "
        "and applied statistics. This project conducts an empirical, rigorous statistical investigation "
        "into the factors governing property price per unit area using the benchmark Real Estate Valuation "
        "Dataset (UCI Machine Learning Repository ID: 477), comprising 414 historical property transactions "
        "from Sindian District, New Taipei City, Taiwan (2012–2013). "
        "Applying a principled statistical methodology, we perform comprehensive descriptive analysis, "
        "construct a 95% Student's t-confidence interval for the population mean valuation ([36.666, 39.295] "
        "in 10,000 NTD/Ping), and conduct two formal hypothesis tests. A Welch two-sample independent t-test "
        "demonstrates that properties within median walking distance (≤ 492.23 m) of a Mass Rapid Transit (MRT) "
        "station command an average premium of 57.1% over more distant properties (t = 15.995, p = 4.065e-45), "
        "corroborated by a non-parametric Mann-Whitney U test (p = 1.195e-40). A one-way ANOVA across house-age "
        "tertiles reveals significant valuation differentials (F = 32.062, p = 1.150e-13), with Tukey HSD post-hoc "
        "tests isolating this effect to newly built properties versus mature structures. Bivariate correlation "
        "confirms a decisive negative association with MRT distance (Pearson r = -0.674, Spearman rho = -0.776). "
        "Finally, predictive modeling via Ordinary Least Squares (OLS) demonstrates that Simple Linear Regression "
        "using house age explains only 4.4% of total price variation (test R² = 0.0152), whereas Multiple Linear Regression "
        "incorporating MRT proximity increases explained variance to 49.11% (test R² = 0.5756), reducing held-out "
        "Mean Absolute Error (MAE) by 41.2% (from 10.621 to 6.248 units). Crucially, the target variable is price per "
        "unit area, and total floor area is unobserved in the data. All findings reflect genuine, verified executions "
        "and illustrate both the capabilities and the boundaries of classical statistical inference."
    )
    story.append(Paragraph(abstract_text, body))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 2: INTRODUCTION & PROBLEM STATEMENT
    # ----------------------------------------------------
    story.append(Paragraph("2. Introduction, Motivation & Problem Statement", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Residential property pricing constitutes one of the most critical economic decisions for households, financial "
        "institutions, urban planners, and municipal governments. In traditional appraisal practices, property values "
        "have frequently been estimated using qualitative impressions or fragmented comparable-sales methods. However, modern "
        "statistical science and machine learning provide tools to quantify exactly how spatial, structural, and temporal "
        "attributes systematically influence market prices.",
        body
    ))
    story.append(Paragraph(
        "<b>Project Motivation:</b> While college curricula frequently treat statistical concepts—such as confidence "
        "intervals, two-sample t-tests, ANOVA, and linear regression—as isolated formulas, real-world data science requires "
        "synthesizing these tools into a unified analytical narrative. This project bridges textbook theory with genuine empirical "
        "investigation, verifying each assumption and validating predictive performance on unseen data.",
        body
    ))
    story.append(Paragraph(
        "<b>Problem Statement:</b> Given historical property transaction data, to what extent do property age and proximity "
        "to public transit explain differences in residential property valuation? Does proximity to transportation infrastructure "
        "yield a statistically significant and economically substantial price premium? How accurately can unit-area price be "
        "predicted using linear models on unseen data?",
        body
    ))
    story.append(Paragraph(
        "<b>Project Scope & Objectives:</b>", h2
    ))
    story.append(Paragraph("• <b>Data Hygiene:</b> Verify complete observation integrity, confirm missing-value and duplicate counts, and enforce exclusion of non-predictive identifiers.", bullet_style))
    story.append(Paragraph("• <b>Descriptive Profiling:</b> Compute central tendency, dispersion, range, and interquartile metrics for key variables.", bullet_style))
    story.append(Paragraph("• <b>Inferential Estimation:</b> Estimate population valuation parameters using Student's t-distribution confidence intervals.", bullet_style))
    story.append(Paragraph("• <b>Hypothesis Testing:</b> Empirically test transit proximity effects (Welch's t-test) and building age effects (One-Way ANOVA with Tukey HSD).", bullet_style))
    story.append(Paragraph("• <b>Predictive Modeling:</b> Fit and diagnose Simple and Multiple Linear Regressions, verifying multicollinearity via VIF.", bullet_style))
    story.append(Paragraph("• <b>Generalization Validation:</b> Evaluate generalization performance strictly on held-out test data (80:20 split) using MAE, MSE, RMSE, and R².", bullet_style))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 3: DATASET PROVENANCE & DESCRIPTION
    # ----------------------------------------------------
    story.append(Paragraph("3. Dataset Provenance, Description & Crucial Boundaries", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "The project employs the official <b>Real Estate Valuation Dataset</b> from the UCI Machine Learning Repository (Dataset ID: 477). "
        "The dataset was collected and published by Prof. I-Cheng Yeh from the Department of Civil Engineering at Tamkang University, Taiwan.",
        body
    ))
    story.append(Paragraph(
        "<b>Official Citation:</b> Yeh, I. (2018). Real Estate Valuation [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5J30W. Distributed under the Creative Commons Attribution 4.0 International (CC BY 4.0) License.",
        caption_style
    ))
    story.append(Spacer(1, 4))
    
    # Crucial Limitation Callout Box
    story.append(make_callout(
        "The project title refers to 'House Area, Age and Property Price Prediction.' However, the underlying UCI dataset "
        "<b>does NOT record total house floor area or total transaction price</b>. The genuine target variable provided in the data is "
        "<b>price per unit area</b> (measured in 10,000 New Taiwan Dollars per Ping, where 1 Ping ≈ 3.3 m²). "
        "In accordance with rigorous academic integrity standards, we do NOT fabricate or invent a total house area feature or total price column. "
        "All statistical analyses, regression models, predictions, and inferences in this report strictly and accurately refer to property price per unit area."
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table 1: Description of Dataset Variables & Measurement Units</b>", h3))
    var_table_data = [
        [Paragraph("<b>Original Name</b>", table_header), Paragraph("<b>Statistical Role</b>", table_header), Paragraph("<b>Data Type</b>", table_header), Paragraph("<b>Measurement Unit</b>", table_header), Paragraph("<b>Operational Definition</b>", table_header)],
        [Paragraph("No", table_cell), Paragraph("Identifier", table_cell), Paragraph("int64", table_cell_center), Paragraph("ID Index", table_cell), Paragraph("Transaction serial number (1 to 414). Excluded from models.", table_cell)],
        [Paragraph("X1 transaction date", table_cell), Paragraph("Covariate", table_cell), Paragraph("float64", table_cell_center), Paragraph("Decimal Year", table_cell), Paragraph("Transaction epoch (e.g., 2013.250 = March 2013).", table_cell)],
        [Paragraph("X2 house age", table_cell), Paragraph("Main Predictor", table_cell), Paragraph("float64", table_cell_center), Paragraph("Years", table_cell), Paragraph("Age of structural building at sale date (0.0 to 43.8 yrs).", table_cell)],
        [Paragraph("X3 distance to nearest MRT", table_cell), Paragraph("Main Predictor", table_cell), Paragraph("float64", table_cell_center), Paragraph("Metres", table_cell), Paragraph("Walking distance to nearest Mass Rapid Transit station.", table_cell)],
        [Paragraph("X4 convenience stores", table_cell), Paragraph("Predictor", table_cell), Paragraph("int64", table_cell_center), Paragraph("Integer Count", table_cell), Paragraph("Count of convenience stores within immediate walking radius.", table_cell)],
        [Paragraph("X5 latitude", table_cell), Paragraph("Spatial Feature", table_cell), Paragraph("float64", table_cell_center), Paragraph("Degrees North", table_cell), Paragraph("Geographic latitude coordinate (24.932° to 25.015° N).", table_cell)],
        [Paragraph("X6 longitude", table_cell), Paragraph("Spatial Feature", table_cell), Paragraph("float64", table_cell_center), Paragraph("Degrees East", table_cell), Paragraph("Geographic longitude coordinate (121.474° to 121.566° E).", table_cell)],
        [Paragraph("Y house price of unit area", table_cell), Paragraph("Target (Y)", table_cell), Paragraph("float64", table_cell_center), Paragraph("10,000 NTD/Ping", table_cell), Paragraph("Valuation per unit area (1 Ping ≈ 3.3 m² ≈ 35.58 sq ft).", table_cell)],
    ]
    t_vars = Table(var_table_data, colWidths=[90, 65, 50, 75, 200])
    t_vars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_vars)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Geographical and Historical Context:</b> Data collection occurred specifically within Sindian District, New Taipei City, Taiwan. "
        "Sindian is a major residential suburban district situated immediately south of Taipei City, connected to the urban core via the Taipei Metro Green Line. "
        "The transactions reflect market dynamics during the 2012–2013 macroeconomic window. Readers must recognize that findings cannot be indiscriminately "
        "transferred to differing cities or subsequent inflationary environments.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 4: EXPLORATORY DATA ANALYSIS
    # ----------------------------------------------------
    story.append(Paragraph("4. Exploratory Data Analysis & Verification", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Prior to statistical modeling, data integrity was programmatically verified across all 414 observations. "
        "Verification confirmed <b>zero missing values</b> across all 8 columns and <b>zero duplicate rows</b>. "
        "The observation identifier `No` spans from 1 to 414 consecutively and was cleanly isolated from all feature matrices.",
        body
    ))
    story.append(Paragraph(
        "Initial visual exploration focused on understanding univariate distributions and bivariate associations with property price per unit area. "
        "Below are key exploratory figures generated during Stage 1 and Stage 2.",
        body
    ))
    story.append(Spacer(1, 4))

    # Add Figure 06 & 07 (Target Hist & Boxplot)
    fig06_path = os.path.join(figures_dir, "06_hist_price_unit_area.png")
    fig07_path = os.path.join(figures_dir, "07_boxplot_price_unit_area.png")
    if os.path.exists(fig06_path) and os.path.exists(fig07_path):
        img_table = [
            [Image(fig06_path, width=235, height=145), Image(fig07_path, width=235, height=145)],
            [Paragraph("<b>Figure 1:</b> Distribution Histogram of Unit Price (Mean=37.98, Med=38.45)", caption_style),
             Paragraph("<b>Figure 2:</b> Boxplot of Unit Price Showing Outlier at 117.5 units", caption_style)]
        ]
        t_img1 = Table(img_table, colWidths=[240, 240])
        t_img1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(t_img1)
    
    story.append(Paragraph(
        "<b>Interpretation of Target Distribution:</b> As displayed in Figure 1 and Figure 2, the bulk of property transactions fall within "
        "25 to 50 units (250,000 to 500,000 NTD/Ping). The sample mean (37.980) and median (38.450) are closely aligned, indicating general symmetry "
        "across the interquartile range (IQR = 18.900). However, the boxplot clearly highlights a single extreme outlier at 117.500 units—a luxury or commercial "
        "redevelopment transaction transacted at more than three times the central market value.",
        body
    ))
    story.append(PageBreak())

    # Add Figure 08 & 09 (House Age Hist & Boxplot)
    story.append(Paragraph("Structural and Spatial Feature Distributions", h2))
    fig08_path = os.path.join(figures_dir, "08_hist_house_age.png")
    fig09_path = os.path.join(figures_dir, "09_boxplot_house_age.png")
    if os.path.exists(fig08_path) and os.path.exists(fig09_path):
        img_table_age = [
            [Image(fig08_path, width=235, height=145), Image(fig09_path, width=235, height=145)],
            [Paragraph("<b>Figure 3:</b> Bimodal Histogram of House Age (Years)", caption_style),
             Paragraph("<b>Figure 4:</b> Boxplot of House Age (No Outliers, Max=43.8 yrs)", caption_style)]
        ]
        t_img2 = Table(img_table_age, colWidths=[240, 240])
        t_img2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(t_img2)

    story.append(Paragraph(
        "<b>Interpretation of House Age:</b> Figure 3 and Figure 4 reveal that property age exhibits a distinctly bimodal distribution. "
        "There is a notable clustering of brand-new properties (age < 5 years, with the mode being exactly 0.0 years), followed by a second concentration "
        "of mature properties aged 25 to 40 years. This reflects cyclical construction waves in Sindian District.",
        body
    ))
    story.append(Spacer(1, 8))

    # Add Figure 10 & 11 (Scatter Plots)
    fig10_path = os.path.join(figures_dir, "10_scatter_age_vs_price.png")
    fig11_path = os.path.join(figures_dir, "11_scatter_mrt_vs_price.png")
    if os.path.exists(fig10_path) and os.path.exists(fig11_path):
        img_table_scatter = [
            [Image(fig10_path, width=235, height=145), Image(fig11_path, width=235, height=145)],
            [Paragraph("<b>Figure 5:</b> Scatter Plot: House Age vs. Unit Price", caption_style),
             Paragraph("<b>Figure 6:</b> Scatter Plot: Distance to Nearest MRT vs. Unit Price", caption_style)]
        ]
        t_img3 = Table(img_table_scatter, colWidths=[240, 240])
        t_img3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(t_img3)

    story.append(Paragraph(
        "<b>Contrasting Predictor Relationships:</b> In Figure 5, the relationship between house age and unit price is subtle and non-linear. "
        "Brand-new properties command high prices, but middle-aged properties plateau, and select mature properties sustain elevated values. "
        "In sharp contrast, Figure 6 reveals an unambiguous, non-linear decaying relationship between MRT distance and unit price. "
        "Properties situated within 500 metres of an MRT station consistently command the highest prices, whereas properties situated beyond "
        "2,000 metres drop to a baseline below 30 units.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 5: DESCRIPTIVE STATISTICAL ANALYSIS
    # ----------------------------------------------------
    story.append(Paragraph("5. Descriptive Statistical Analysis", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Descriptive statistics summarize the central location, dispersion, and distributional shape of observed sample data. "
        "Below is the complete, verified numerical summary computed from the 414 historical observations.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 2: Comprehensive Descriptive Statistics of Core Variables (n = 414)</b>", h3))
    stats_table_data = [
        [Paragraph("<b>Metric</b>", table_header), Paragraph("<b>House Age (X2)<br/>(Years)</b>", table_header), Paragraph("<b>MRT Distance (X3)<br/>(Metres)</b>", table_header), Paragraph("<b>Convenience Stores (X4)<br/>(Count)</b>", table_header), Paragraph("<b>Price / Unit Area (Y)<br/>(10,000 NTD/Ping)</b>", table_header)],
        [Paragraph("Mean (x̄)", table_cell), Paragraph("17.713", table_cell_center), Paragraph("1,083.886", table_cell_center), Paragraph("4.094", table_cell_center), Paragraph("37.980", table_cell_center)],
        [Paragraph("Median (M)", table_cell), Paragraph("16.100", table_cell_center), Paragraph("492.231", table_cell_center), Paragraph("4.000", table_cell_center), Paragraph("38.450", table_cell_center)],
        [Paragraph("Mode", table_cell), Paragraph("0.000", table_cell_center), Paragraph("289.325", table_cell_center), Paragraph("0.000", table_cell_center), Paragraph("24.700", table_cell_center)],
        [Paragraph("Variance (s²)", table_cell), Paragraph("129.789", table_cell_center), Paragraph("1,592,920.631", table_cell_center), Paragraph("8.676", table_cell_center), Paragraph("185.137", table_cell_center)],
        [Paragraph("Std Dev (s)", table_cell), Paragraph("11.392", table_cell_center), Paragraph("1,262.110", table_cell_center), Paragraph("2.946", table_cell_center), Paragraph("13.606", table_cell_center)],
        [Paragraph("Minimum", table_cell), Paragraph("0.000", table_cell_center), Paragraph("23.383", table_cell_center), Paragraph("0.000", table_cell_center), Paragraph("7.600", table_cell_center)],
        [Paragraph("Maximum", table_cell), Paragraph("43.800", table_cell_center), Paragraph("6,488.021", table_cell_center), Paragraph("10.000", table_cell_center), Paragraph("117.500", table_cell_center)],
        [Paragraph("Range", table_cell), Paragraph("43.800", table_cell_center), Paragraph("6,464.638", table_cell_center), Paragraph("10.000", table_cell_center), Paragraph("109.900", table_cell_center)],
        [Paragraph("Q1 (25th percentile)", table_cell), Paragraph("9.025", table_cell_center), Paragraph("289.325", table_cell_center), Paragraph("1.000", table_cell_center), Paragraph("27.700", table_cell_center)],
        [Paragraph("Q3 (75th percentile)", table_cell), Paragraph("28.150", table_cell_center), Paragraph("1,454.279", table_cell_center), Paragraph("6.000", table_cell_center), Paragraph("46.600", table_cell_center)],
        [Paragraph("Interquartile Range (IQR)", table_cell), Paragraph("19.125", table_cell_center), Paragraph("1,164.954", table_cell_center), Paragraph("5.000", table_cell_center), Paragraph("18.900", table_cell_center)],
    ]
    t_stats = Table(stats_table_data, colWidths=[120, 90, 90, 90, 90])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Analytical Takeaways from Descriptive Statistics:</b>", h3
    ))
    story.append(Paragraph("1. <b>Scale & Dispersion Disparity:</b> Distance to nearest MRT station features an immense variance (s² = 1.59 million m²), ranging from 23.4 metres to nearly 6.5 kilometres. By contrast, house age spans a compact range from 0 to 43.8 years.", bullet_style))
    story.append(Paragraph("2. <b>Severe Skewness in Transit Proximity:</b> The mean distance to an MRT station (1,083.89 m) is more than double the median distance (492.23 m). This massive positive gap proves heavy right-skewness: while over half the properties are within 500 m, a long tail of outlying properties is located several kilometres away.", bullet_style))
    story.append(Paragraph("3. <b>Convenience Store Distribution:</b> Nearby convenience stores range from 0 to 10 with a mean of 4.094 and median of 4.000. Exactly 50% of properties have between 1 and 6 stores within easy walking access.", bullet_style))
    story.append(Paragraph("4. <b>Unit Price Symmetry and Outlier Impact:</b> Target price per unit area exhibits a median of 38.450 and mean of 37.980, with an IQR of 18.900. The standard deviation of 13.606 units indicates substantial pricing dispersion, partly inflated by the maximum transaction at 117.500.", bullet_style))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 6: PROBABILITY & STATISTICAL INFERENCE
    # ----------------------------------------------------
    story.append(Paragraph("6. Probability & Statistical Inference: 95% Confidence Interval", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Statistical inference allows researchers to make probabilistic statements about an unobserved population based on "
        "a representative sample. When the population standard deviation σ is unknown, the standard normal distribution (Z) "
        "is replaced by Student's t-distribution with n - 1 degrees of freedom.",
        body
    ))
    story.append(Paragraph(
        "<b>Mathematical Formulation:</b> The 100(1 - α)% confidence interval for population mean μ is defined as:",
        body
    ))
    story.append(Paragraph(
        "CI = x̄ ± t_{α/2, n-1} × SE = x̄ ± t_{α/2, n-1} × (s / √n)",
        eq_style
    ))
    story.append(Paragraph(
        "where x̄ is the sample mean, s is the sample standard deviation, n is sample size, and SE = s / √n is the standard error.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 3: Exact Step-by-Step 95% Confidence Interval Computation</b>", h3))
    ci_table_data = [
        [Paragraph("<b>Step / Parameter</b>", table_header), Paragraph("<b>Symbol / Formula</b>", table_header), Paragraph("<b>Computed Value</b>", table_header), Paragraph("<b>Academic Interpretation</b>", table_header)],
        [Paragraph("Sample Size", table_cell), Paragraph("n", table_cell_center), Paragraph("414", table_cell_center), Paragraph("Total valid residential transactions", table_cell)],
        [Paragraph("Sample Mean", table_cell), Paragraph("x̄", table_cell_center), Paragraph("37.980", table_cell_center), Paragraph("Point estimate of mean unit price (10,000 NTD/Ping)", table_cell)],
        [Paragraph("Sample Standard Deviation", table_cell), Paragraph("s", table_cell_center), Paragraph("13.606", table_cell_center), Paragraph("Sample dispersion with Bessel's correction (ddof=1)", table_cell)],
        [Paragraph("Degrees of Freedom", table_cell), Paragraph("df = n - 1", table_cell_center), Paragraph("413", table_cell_center), Paragraph("Degrees of freedom for Student's t-distribution", table_cell)],
        [Paragraph("Standard Error of Mean", table_cell), Paragraph("SE = s / √n", table_cell_center), Paragraph("0.669", table_cell_center), Paragraph("Estimated standard deviation of the sampling mean", table_cell)],
        [Paragraph("Critical t-value", table_cell), Paragraph("t_{0.025, 413}", table_cell_center), Paragraph("1.9657", table_cell_center), Paragraph("Two-tailed 95% critical threshold from t-distribution", table_cell)],
        [Paragraph("Margin of Error", table_cell), Paragraph("MoE = t* × SE", table_cell_center), Paragraph("1.315", table_cell_center), Paragraph("Maximum expected sampling discrepancy at α = 0.05", table_cell)],
        [Paragraph("Lower Confidence Limit", table_cell), Paragraph("LCL = x̄ - MoE", table_cell_center), Paragraph("36.666", table_cell_center), Paragraph("Lower boundary of 95% confidence interval", table_cell)],
        [Paragraph("Upper Confidence Limit", table_cell), Paragraph("UCL = x̄ + MoE", table_cell_center), Paragraph("39.295", table_cell_center), Paragraph("Upper boundary of 95% confidence interval", table_cell)],
    ]
    t_ci = Table(ci_table_data, colWidths=[110, 80, 80, 210])
    t_ci.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_ci)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Rigorous Interpretation of the Confidence Interval:</b><br/>"
        "• <b>Academic Definition:</b> In repeated random sampling under identical conditions, 95% of the confidence intervals constructed "
        "using this methodology will successfully contain the true, fixed population mean property price per unit area μ.<br/>"
        "• <b>Fallacy Avoidance:</b> It is a frequent conceptual error to state that 'there is a 95% probability that the population mean lies "
        "between 36.666 and 39.295.' In frequentist probability, μ is a fixed deterministic constant, not a random variable; the interval either "
        "contains μ or it does not.<br/>"
        "• <b>Sampling Limitation:</b> Because the UCI documentation does not specify the exact sampling protocol (e.g., whether transactions "
        "were drawn via stratified random sampling or selected from specific brokerage firms), generalization beyond this specific dataset must be handled cautiously.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 7: HYPOTHESIS TESTING I (WELCH T-TEST)
    # ----------------------------------------------------
    story.append(Paragraph("7. Hypothesis Testing I: MRT Proximity (Welch's Two-Sample t-Test)", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "We formally investigate whether residential properties situated in close proximity to mass transit stations command "
        "a statistically different mean valuation per unit area compared to properties situated further away.",
        body
    ))
    story.append(Paragraph(
        "<b>Group Partitioning:</b> Using the sample median MRT distance (492.231 metres), the dataset is split into two balanced groups:<br/>"
        "• <b>Near MRT Group:</b> Distance ≤ 492.231 m (n₁ = 210 observations)<br/>"
        "• <b>Far from MRT Group:</b> Distance > 492.231 m (n₂ = 204 observations)",
        body
    ))
    story.append(Paragraph(
        "<b>Statistical Hypotheses:</b><br/>"
        "• <b>Null Hypothesis (H₀):</b> μ_{Near} - μ_{Far} = 0 (No difference in population mean unit price between proximity groups).<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> μ_{Near} - μ_{Far} ≠ 0 (A significant difference exists in population mean unit price).<br/>"
        "• <b>Significance Level:</b> α = 0.05 (two-tailed test).",
        body
    ))
    story.append(Paragraph(
        "Because urban property markets typically display unequal variance across geographic sub-zones (heteroscedasticity), "
        "we utilize <b>Welch's t-test</b>, which computes adjusted degrees of freedom using the Welch-Satterthwaite equation:",
        body
    ))
    story.append(Paragraph(
        "t = (x̄₁ - x̄₂) / √( (s₁² / n₁) + (s₂² / n₂) ),   df = ( (s₁²/n₁) + (s₂²/n₂) )² / [ ((s₁²/n₁)² / (n₁-1)) + ((s₂²/n₂)² / (n₂-1)) ]",
        eq_style
    ))
    story.append(PageBreak())

    story.append(Paragraph("<b>Table 4: Welch's Two-Sample t-Test Results & Group Statistics</b>", h3))
    ttest_table_data = [
        [Paragraph("<b>Group / Test Metric</b>", table_header), Paragraph("<b>Sample Size (n)</b>", table_header), Paragraph("<b>Mean Price (x̄)</b>", table_header), Paragraph("<b>Std Dev (s)</b>", table_header), Paragraph("<b>Statistical Outcome</b>", table_header)],
        [Paragraph("Near MRT (≤ 492.2 m)", table_cell), Paragraph("210", table_cell_center), Paragraph("46.265", table_cell_center), Paragraph("11.758", table_cell_center), Paragraph("Elevated valuation density", table_cell)],
        [Paragraph("Far from MRT (> 492.2 m)", table_cell), Paragraph("204", table_cell_center), Paragraph("29.452", table_cell_center), Paragraph("9.387", table_cell_center), Paragraph("Substantially lower pricing", table_cell)],
        [Paragraph("<b>Difference in Means</b>", table_cell), Paragraph("-", table_cell_center), Paragraph("<b>+16.813</b>", table_cell_center), Paragraph("-", table_cell_center), Paragraph("<b>+57.1% Premium for Near MRT</b>", table_cell)],
        [Paragraph("Welch t-statistic", table_cell), Paragraph("-", table_cell_center), Paragraph("<b>t = 15.995</b>", table_cell_center), Paragraph("-", table_cell_center), Paragraph("Degrees of Freedom df = 399.78", table_cell)],
        [Paragraph("p-value (two-tailed)", table_cell), Paragraph("-", table_cell_center), Paragraph("<b>4.065 × 10⁻⁴⁵</b>", table_cell_center), Paragraph("-", table_cell_center), Paragraph("Far below α = 0.05 threshold", table_cell)],
        [Paragraph("<b>Hypothesis Decision</b>", table_cell), Paragraph("-", table_cell_center), Paragraph("<b>REJECT H₀</b>", table_cell_center), Paragraph("-", table_cell_center), Paragraph("Overwhelming statistical significance", table_cell)],
    ]
    t_ttest = Table(ttest_table_data, colWidths=[130, 80, 80, 70, 120])
    t_ttest.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_ttest)
    story.append(Spacer(1, 8))

    # Add Figure 12 (Comparison Boxplot)
    fig12_path = os.path.join(figures_dir, "12_boxplot_mrt_proximity_comparison.png")
    if os.path.exists(fig12_path):
        story.append(KeepTogether([
            Image(fig12_path, width=320, height=200),
            Paragraph("<b>Figure 7:</b> Comparative Boxplot of Property Price per Unit Area by MRT Proximity Group", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Supplementary Robustness Check (Mann-Whitney U Test):</b><br/>"
        "To ensure that this extreme statistical significance is not an artifact of the upper outlier (117.5 units) or non-normality, "
        "a non-parametric Mann-Whitney U test was performed on the raw transaction rankings. The test yielded U = 37,669.0 with "
        "p = 1.195 × 10⁻⁴⁰. Because both parametric and non-parametric tests produce virtually identical conclusions, "
        "the finding is exceptionally robust.<br/>"
        "<b>Economic Significance:</b> Properties adjacent to transit command an average premium of 168,130 NTD per Ping over distant properties.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 8: HYPOTHESIS TESTING II (ONE-WAY ANOVA)
    # ----------------------------------------------------
    story.append(Paragraph("8. Hypothesis Testing II: House-Age Tertiles (One-Way ANOVA & Post-Hoc)", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "We evaluate whether property valuations per unit area differ across building age cohorts. Rather than imposing arbitrary age "
        "boundaries, we segment the 414 observations into three balanced empirical tertiles (q = 3, n = 138 each):<br/>"
        "• <b>Younger Properties:</b> Age ≤ 13.0 years (n₁ = 138)<br/>"
        "• <b>Middle-Aged Properties:</b> 13.0 < Age ≤ 26.6 years (n₂ = 138)<br/>"
        "• <b>Older Properties:</b> Age > 26.6 years (n₃ = 138)",
        body
    ))
    story.append(Paragraph(
        "<b>ANOVA Hypotheses:</b><br/>"
        "• <b>Null Hypothesis (H₀):</b> μ_{Younger} = μ_{Middle} = μ_{Older} (All three age group population means are equal).<br/>"
        "• <b>Alternative Hypothesis (H₁):</b> At least one group mean is significantly different.<br/>"
        "• <b>Significance Level:</b> α = 0.05.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 5: One-Way ANOVA Summary Table</b>", h3))
    anova_table_data = [
        [Paragraph("<b>Source of Variation</b>", table_header), Paragraph("<b>Sum of Squares (SS)</b>", table_header), Paragraph("<b>df</b>", table_header), Paragraph("<b>Mean Square (MS)</b>", table_header), Paragraph("<b>F-statistic</b>", table_header), Paragraph("<b>p-value</b>", table_header)],
        [Paragraph("Between Groups (Age)", table_cell), Paragraph("10,344.492", table_cell_center), Paragraph("2", table_cell_center), Paragraph("5,172.246", table_cell_center), Paragraph("<b>F = 32.062</b>", table_cell_center), Paragraph("<b>1.150 × 10⁻¹³</b>", table_cell_center)],
        [Paragraph("Within Groups (Error)", table_cell), Paragraph("66,298.679", table_cell_center), Paragraph("411", table_cell_center), Paragraph("161.311", table_cell_center), Paragraph("-", table_cell_center), Paragraph("-", table_cell_center)],
        [Paragraph("Total", table_cell), Paragraph("76,643.171", table_cell_center), Paragraph("413", table_cell_center), Paragraph("-", table_cell_center), Paragraph("-", table_cell_center), Paragraph("-", table_cell_center)],
    ]
    t_anova = Table(anova_table_data, colWidths=[120, 90, 40, 80, 75, 75])
    t_anova.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_anova)
    story.append(PageBreak())

    # Add Figure 13 (ANOVA Diagnostics)
    fig13_path = os.path.join(figures_dir, "13_anova_residual_diagnostics.png")
    if os.path.exists(fig13_path):
        story.append(KeepTogether([
            Image(fig13_path, width=440, height=170),
            Paragraph("<b>Figure 8:</b> ANOVA Residual Diagnostics: Normal Q-Q Plot and Residual Histogram", caption_style)
        ]))

    story.append(Paragraph(
        "<b>ANOVA Diagnostic Tests:</b><br/>"
        "• <b>Normality of Residuals:</b> Shapiro-Wilk test yielded W = 0.9577, p = 8.16 × 10⁻¹⁰, confirming slight departure from strict normality driven by the upper tail.<br/>"
        "• <b>Homogeneity of Variances:</b> Levene's test yielded Stat = 2.060, p = 0.1287. Because p > 0.05, the assumption of equal group variances is tenable.",
        body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Table 6: Tukey HSD Post-Hoc Pairwise Comparisons (Family-wise α = 0.05)</b>", h3))
    tukey_table_data = [
        [Paragraph("<b>Comparison Pair</b>", table_header), Paragraph("<b>Mean Diff (x̄₁ - x̄₂)</b>", table_header), Paragraph("<b>p-adj</b>", table_header), Paragraph("<b>95% CI Lower</b>", table_header), Paragraph("<b>95% CI Upper</b>", table_header), Paragraph("<b>Decision</b>", table_header)],
        [Paragraph("Younger vs. Middle-aged", table_cell), Paragraph("<b>-11.568</b>", table_cell_center), Paragraph("<b>< 0.001</b>", table_cell_center), Paragraph("-15.158", table_cell_center), Paragraph("-7.978", table_cell_center), Paragraph("<b>Significant</b>", table_cell_center)],
        [Paragraph("Younger vs. Older", table_cell), Paragraph("<b>-9.220</b>", table_cell_center), Paragraph("<b>< 0.001</b>", table_cell_center), Paragraph("-12.809", table_cell_center), Paragraph("-5.630", table_cell_center), Paragraph("<b>Significant</b>", table_cell_center)],
        [Paragraph("Middle-aged vs. Older", table_cell), Paragraph("+2.349", table_cell_center), Paragraph("0.286", table_cell_center), Paragraph("-1.241", table_cell_center), Paragraph("+5.938", table_cell_center), Paragraph("Not Significant", table_cell_center)],
    ]
    t_tukey = Table(tukey_table_data, colWidths=[120, 80, 60, 75, 75, 70])
    t_tukey.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_tukey)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Substantive Interpretation:</b> The ANOVA confirms that age cohorts differ in mean valuation (F = 32.062, p = 1.15e-13). "
        "However, Tukey's HSD isolates the pricing premium exclusively to <b>Younger properties (Mean = 44.909 units)</b>. "
        "There is no statistically meaningful price difference between Middle-aged properties (33.341 units) and Older properties (35.690 units) (p = 0.286). "
        "This non-linear plateau indicates that buildings experience most depreciation during their first 15 years.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 9: CORRELATION ANALYSIS
    # ----------------------------------------------------
    story.append(Paragraph("9. Bivariate Correlation Analysis", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Bivariate correlation measures the strength and direction of association between variables. We report both "
        "<b>Pearson product-moment correlation (r)</b>, which quantifies linear association, and <b>Spearman rank correlation (ρ)</b>, "
        "which evaluates monotonic associations without assuming normality.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 7: Bivariate Correlation with Property Price per Unit Area (Y)</b>", h3))
    corr_table_data = [
        [Paragraph("<b>Feature Variable</b>", table_header), Paragraph("<b>Pearson r</b>", table_header), Paragraph("<b>Pearson p-value</b>", table_header), Paragraph("<b>Spearman ρ</b>", table_header), Paragraph("<b>Spearman p-value</b>", table_header), Paragraph("<b>Strength & Direction</b>", table_header)],
        [Paragraph("X3 Distance to Nearest MRT", table_cell), Paragraph("<b>-0.674</b>", table_cell_center), Paragraph("4.64 × 10⁻⁵⁶", table_cell_center), Paragraph("<b>-0.776</b>", table_cell_center), Paragraph("1.81 × 10⁻⁸⁴", table_cell_center), Paragraph("Strong Negative Monotonic", table_cell)],
        [Paragraph("X4 Convenience Stores", table_cell), Paragraph("<b>+0.571</b>", table_cell_center), Paragraph("3.41 × 10⁻³⁷", table_cell_center), Paragraph("<b>+0.617</b>", table_cell_center), Paragraph("7.51 × 10⁻⁴⁵", table_cell_center), Paragraph("Moderate Positive", table_cell)],
        [Paragraph("X2 House Age", table_cell), Paragraph("<b>-0.211</b>", table_cell_center), Paragraph("1.56 × 10⁻⁵", table_cell_center), Paragraph("<b>-0.282</b>", table_cell_center), Paragraph("5.41 × 10⁻⁹", table_cell_center), Paragraph("Weak Negative", table_cell)],
        [Paragraph("X5 Latitude", table_cell), Paragraph("+0.546", table_cell_center), Paragraph("1.39 × 10⁻³³", table_cell_center), Paragraph("+0.574", table_cell_center), Paragraph("1.20 × 10⁻³⁷", table_cell_center), Paragraph("Moderate Positive (Northward)", table_cell)],
        [Paragraph("X6 Longitude", table_cell), Paragraph("+0.523", table_cell_center), Paragraph("1.80 × 10⁻³⁰", table_cell_center), Paragraph("+0.564", table_cell_center), Paragraph("1.11 × 10⁻³⁵", table_cell_center), Paragraph("Moderate Positive (Eastward)", table_cell)],
    ]
    t_corr = Table(corr_table_data, colWidths=[120, 65, 75, 65, 75, 80])
    t_corr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_corr)
    story.append(PageBreak())

    # Add Figure 14 & 15 (Heatmap & Trendlines)
    fig14_path = os.path.join(figures_dir, "14_correlation_heatmap.png")
    fig15_path = os.path.join(figures_dir, "15_scatter_trendlines.png")
    if os.path.exists(fig14_path):
        story.append(KeepTogether([
            Image(fig14_path, width=320, height=220),
            Paragraph("<b>Figure 9:</b> Correlation Matrix Heatmap of Primary Variables", caption_style)
        ]))

    if os.path.exists(fig15_path):
        story.append(KeepTogether([
            Image(fig15_path, width=460, height=140),
            Paragraph("<b>Figure 10:</b> Bivariate Scatter Plots with OLS Trendlines across Key Predictors", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Correlation Insights & Causation Warning:</b><br/>"
        "• <b>Why Spearman Exceeds Pearson on MRT Distance:</b> Spearman's rank correlation (ρ = -0.776) is noticeably stronger than Pearson's (r = -0.674). "
        "This divergence occurs because the relationship is fundamentally non-linear: prices drop sharply within the first 1,000 metres and then taper off.<br/>"
        "• <b>Correlation Does Not Imply Causation:</b> Convenience stores show a strong positive correlation (+0.571), but opening a new store does not "
        "mechanically cause home prices to rise. Rather, transit stations and commercial retailers co-locate in densely populated, affluent commercial cores.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 10: SIMPLE LINEAR REGRESSION
    # ----------------------------------------------------
    story.append(Paragraph("10. Simple Linear Regression Modelling (House Age)", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "We first formulate a Simple Linear Regression (SLR) model predicting property price per unit area ($Y$) solely from building age ($X_2$):",
        body
    ))
    story.append(Paragraph(
        "Y = β₀ + β₁ X₂ + ε,   where ε ~ N(0, σ²)",
        eq_style
    ))
    story.append(Paragraph(
        "Ordinary Least Squares (OLS) minimization yielded the following fitted equation across all 414 observations:",
        body
    ))
    story.append(Paragraph(
        "<b>Fitted SLR Equation:</b>   Ŷ = 42.4347 - 0.2515 × (House Age)",
        eq_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 8: Simple Linear Regression OLS Summary Parameters</b>", h3))
    slr_table_data = [
        [Paragraph("<b>Parameter / Metric</b>", table_header), Paragraph("<b>Coefficient Value</b>", table_header), Paragraph("<b>Standard Error</b>", table_header), Paragraph("<b>t-statistic</b>", table_header), Paragraph("<b>p-value</b>", table_header), Paragraph("<b>95% Confidence Interval</b>", table_header)],
        [Paragraph("Intercept (β₀)", table_cell), Paragraph("42.4347", table_cell_center), Paragraph("1.2110", table_cell_center), Paragraph("35.042", table_cell_center), Paragraph("< 10⁻⁸⁰", table_cell_center), Paragraph("[40.054, 44.815]", table_cell_center)],
        [Paragraph("House Age Slope (β₁)", table_cell), Paragraph("<b>-0.2515</b>", table_cell_center), Paragraph("0.0575", table_cell_center), Paragraph("-4.372", table_cell_center), Paragraph("<b>1.56 × 10⁻⁵</b>", table_cell_center), Paragraph("[-0.364, -0.139]", table_cell_center)],
        [Paragraph("<b>Model Fit Metrics</b>", table_cell), Paragraph("<b>R² = 0.0443</b>", table_cell_center), Paragraph("Adj R² = 0.0420", table_cell_center), Paragraph("F = 19.11", table_cell_center), Paragraph("p = 1.56 × 10⁻⁵", table_cell_center), Paragraph("Residual Std Err = 13.318", table_cell_center)],
    ]
    t_slr = Table(slr_table_data, colWidths=[120, 75, 70, 65, 75, 75])
    t_slr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_slr)
    story.append(PageBreak())

    # Add Figure 16 (SLR Diagnostics)
    fig16_path = os.path.join(figures_dir, "16_slr_diagnostics.png")
    if os.path.exists(fig16_path):
        story.append(KeepTogether([
            Image(fig16_path, width=460, height=145),
            Paragraph("<b>Figure 11:</b> Simple Linear Regression: Fitted Line, Residuals vs. Fitted, and Normal Q-Q Plot", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Interpretation and Severe Shortcomings of the SLR Model:</b><br/>"
        "• <b>Economic Interpretation:</b> The intercept (42.435) implies an estimated baseline price of 424,350 NTD per Ping for a brand-new house (Age = 0). "
        "The slope (-0.2515) indicates that each additional year of building age is associated with an expected drop of 2,515 NTD per Ping.<br/>"
        "• <b>Statistical Significance vs. Explanatory Impotence:</b> While the slope is highly statistically significant (t = -4.37, p = 1.56e-5), "
        "the coefficient of determination is a meagre <b>R² = 0.0443 (4.4%)</b>. Over 95.5% of the variation in price per unit area remains completely "
        "unexplained by building age alone. This demonstrates why bivariate models are inadequate for complex urban valuation.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 11: MULTIPLE LINEAR REGRESSION
    # ----------------------------------------------------
    story.append(Paragraph("11. Multiple Linear Regression Modelling & Multicollinearity (VIF)", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "To address the limitations of the single-predictor model, we formulate a Multiple Linear Regression (MLR) model "
        "incorporating both building age ($X_2$) and distance to the nearest MRT station ($X_3$):",
        body
    ))
    story.append(Paragraph(
        "Y = β₀ + β₁ X₂ + β₂ X₃ + ε",
        eq_style
    ))
    story.append(Paragraph(
        "<b>Fitted Multiple Regression Equation:</b>   Ŷ = 49.8856 - 0.2310 × (House Age) - 0.0072 × (MRT Distance)",
        eq_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 9: Multiple Linear Regression OLS Summary & Coefficients</b>", h3))
    mlr_table_data = [
        [Paragraph("<b>Term</b>", table_header), Paragraph("<b>Coefficient Value</b>", table_header), Paragraph("<b>Std Error</b>", table_header), Paragraph("<b>t-statistic</b>", table_header), Paragraph("<b>p-value</b>", table_header), Paragraph("<b>95% Confidence Interval</b>", table_header)],
        [Paragraph("Intercept (β₀)", table_cell), Paragraph("49.8856", table_cell_center), Paragraph("0.9667", table_cell_center), Paragraph("51.606", table_cell_center), Paragraph("< 10⁻⁸⁰", table_cell_center), Paragraph("[47.985, 51.786]", table_cell_center)],
        [Paragraph("House Age (β₁)", table_cell), Paragraph("<b>-0.2310</b>", table_cell_center), Paragraph("0.0420", table_cell_center), Paragraph("-5.496", table_cell_center), Paragraph("<b>1.05 × 10⁻⁷</b>", table_cell_center), Paragraph("[-0.316, -0.147]", table_cell_center)],
        [Paragraph("MRT Distance (β₂)", table_cell), Paragraph("<b>-0.0072</b>", table_cell_center), Paragraph("0.0004", table_cell_center), Paragraph("-19.006", table_cell_center), Paragraph("<b>2.44 × 10⁻⁵³</b>", table_cell_center), Paragraph("[-0.008, -0.006]", table_cell_center)],
        [Paragraph("<b>Model Fit Metrics</b>", table_cell), Paragraph("<b>R² = 0.4911</b>", table_cell_center), Paragraph("<b>Adj R² = 0.4887</b>", table_cell_center), Paragraph("<b>F = 198.3</b>", table_cell_center), Paragraph("p = 2.65 × 10⁻⁶⁰", table_cell_center), Paragraph("Residual Std Err = 9.729", table_cell_center)],
    ]
    t_mlr = Table(mlr_table_data, colWidths=[110, 75, 70, 65, 80, 80])
    t_mlr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_mlr)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Multicollinearity Assessment via Variance Inflation Factor (VIF):</b><br/>"
        "Multicollinearity arises when predictor variables are highly correlated, inflating parameter variance. "
        "VIF measures the factor by which variance is inflated relative to orthogonal predictors:<br/>"
        "• VIF(House Age) = <b>1.001</b><br/>"
        "• VIF(MRT Distance) = <b>1.001</b><br/>"
        "Because both VIF values are virtually 1.0 (well below the conservative threshold of 5.0), multicollinearity is non-existent. "
        "The empirical correlation between House Age and MRT Distance is r = 0.026.",
        body
    ))
    story.append(PageBreak())

    # Add Figure 17 (MLR Diagnostics)
    fig17_path = os.path.join(figures_dir, "17_mlr_diagnostics.png")
    if os.path.exists(fig17_path):
        story.append(KeepTogether([
            Image(fig17_path, width=460, height=145),
            Paragraph("<b>Figure 12:</b> Multiple Linear Regression Diagnostics: Actual vs. Predicted, Residuals vs. Fitted, and Q-Q Plot", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Detailed Multiple Regression Diagnostic Insights:</b><br/>"
        "• <b>Explanatory Power:</b> Introducing MRT distance elevates R² from 0.0443 to <b>0.4911</b>, an eleven-fold increase in explained variance. "
        "Nearly half of all price-per-unit-area variability across Sindian District is captured by these two variables alone.<br/>"
        "• <b>Controlled Slopes:</b> Holding transit proximity constant, each additional year of building age reduces valuation by 0.2310 units (2,310 NTD/Ping). "
        "Holding age constant, every 100 metres of distance from an MRT station reduces valuation by 0.72 units (7,200 NTD/Ping).<br/>"
        "• <b>Heteroscedasticity Caveat:</b> Figure 12 (center panel) reveals subtle fan-shaped heteroscedasticity, where residual variance is larger "
        "for higher predicted prices. This is a common property market phenomenon where luxury properties fluctuate more widely than entry-level homes.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 12: MODEL EVALUATION (80:20 SPLIT)
    # ----------------------------------------------------
    story.append(Paragraph("12. Train-Test Split (80:20) & Predictive Performance Evaluation", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "A foundational principle of modern statistical learning is that evaluating a model on the data used to train it introduces optimism bias. "
        "To establish true generalizability, the 414 observations were partitioned into an 80% training set (n = 331) and a strictly held-out "
        "20% test set (n = 83) using `random_state=42`. Both models were fitted on the training partition and evaluated on the test partition.",
        body
    ))
    story.append(Paragraph(
        "<b>Evaluation Metrics Defined:</b><br/>"
        "• <b>Mean Absolute Error (MAE):</b> (1/n) Σ |yᵢ - ŷᵢ| — Average magnitude of errors in unit-area price.<br/>"
        "• <b>Mean Squared Error (MSE):</b> (1/n) Σ (yᵢ - ŷᵢ)² — Average squared error, heavily weighting large deviations.<br/>"
        "• <b>Root Mean Squared Error (RMSE):</b> √MSE — Error metric returned to the original units (10,000 NTD/Ping).<br/>"
        "• <b>Test R²:</b> 1 - [Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²] — Proportion of variance in unseen test observations explained by the model.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 10: Comparative Test Set Performance on Held-Out Observations (n = 83)</b>", h3))
    eval_table_data = [
        [Paragraph("<b>Performance Metric</b>", table_header), Paragraph("<b>SLR (House Age Only)</b>", table_header), Paragraph("<b>MLR (House Age + MRT)</b>", table_header), Paragraph("<b>Error Reduction / Improvement</b>", table_header)],
        [Paragraph("Mean Absolute Error (MAE)", table_cell), Paragraph("10.621 units", table_cell_center), Paragraph("<b>6.248 units</b>", table_cell_center), Paragraph("<b>41.2% Error Reduction</b>", table_cell_center)],
        [Paragraph("Mean Squared Error (MSE)", table_cell), Paragraph("165.205", table_cell_center), Paragraph("<b>71.206</b>", table_cell_center), Paragraph("<b>56.9% Error Reduction</b>", table_cell_center)],
        [Paragraph("Root Mean Squared Error (RMSE)", table_cell), Paragraph("12.853 units", table_cell_center), Paragraph("<b>8.438 units</b>", table_cell_center), Paragraph("<b>34.4% Error Reduction</b>", table_cell_center)],
        [Paragraph("Coefficient of Determination (Test R²)", table_cell), Paragraph("0.0152 (1.5%)", table_cell_center), Paragraph("<b>0.5756 (57.6%)</b>", table_cell_center), Paragraph("<b>+0.5604 (37× Higher)</b>", table_cell_center)],
    ]
    t_eval = Table(eval_table_data, colWidths=[140, 110, 110, 120])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_eval)
    story.append(PageBreak())

    # Add Figure 18 (Actual vs Predicted Test)
    fig18_path = os.path.join(figures_dir, "18_test_actual_vs_predicted.png")
    if os.path.exists(fig18_path):
        story.append(KeepTogether([
            Image(fig18_path, width=460, height=180),
            Paragraph("<b>Figure 13:</b> Actual vs. Predicted Unit Price on Held-Out Test Data (n = 83): SLR (Left) vs. MLR (Right)", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Rigorous Evaluation Interpretation:</b><br/>"
        "• <b>Decisive Superiority of MLR:</b> On unseen data, the Multiple Linear Regression model reduces the average absolute prediction error "
        "from 106,210 NTD/Ping to <b>62,480 NTD/Ping</b>—a substantial 41.2% improvement in practical appraisal accuracy.<br/>"
        "• <b>Generalization Test R²:</b> The test R² of 0.5756 confirms that over 57.5% of valuation variance on unseen transactions is captured by "
        "age and transit proximity. By contrast, the SLR model collapses to R² = 0.0152 on test data, proving that building age alone has negligible standalone predictive power.<br/>"
        "• <b>Evaluation Caution:</b> While these test metrics validate generalization within this 80:20 split, they do not guarantee identical accuracy "
        "in current or geographically distant real estate markets.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 13: SAMPLE PREDICTIONS
    # ----------------------------------------------------
    story.append(Paragraph("13. Sample Valuation Predictions & Scenario Analysis", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "To illustrate the practical utility of the trained Multiple Linear Regression model, we evaluate three realistic property profiles "
        "spanning the empirical predictor space of Sindian District. (Extrapolation beyond observed domain ranges is avoided).",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 11: Model Predictions for Illustrative Residential Scenarios</b>", h3))
    scen_table_data = [
        [Paragraph("<b>Scenario Profile</b>", table_header), Paragraph("<b>House Age<br/>(Years)</b>", table_header), Paragraph("<b>MRT Distance<br/>(Metres)</b>", table_header), Paragraph("<b>Predicted Price / Unit Area<br/>(10,000 NTD / Ping)</b>", table_header), Paragraph("<b>Equivalent Valuation<br/>(NTD per Ping)</b>", table_header)],
        [Paragraph("<b>Scenario A:</b> Brand-New, Transit-Adjacent Luxury Condo", table_cell), Paragraph("2.0", table_cell_center), Paragraph("150.0", table_cell_center), Paragraph("<b>48.51</b>", table_cell_center), Paragraph("485,100 NTD / Ping", table_cell)],
        [Paragraph("<b>Scenario B:</b> Mid-Age Suburban Apartment", table_cell), Paragraph("15.0", table_cell_center), Paragraph("600.0", table_cell_center), Paragraph("<b>42.27</b>", table_cell_center), Paragraph("422,700 NTD / Ping", table_cell)],
        [Paragraph("<b>Scenario C:</b> Mature Property Far from Transit Core", table_cell), Paragraph("32.0", table_cell_center), Paragraph("2,200.0", table_cell_center), Paragraph("<b>27.05</b>", table_cell_center), Paragraph("270,500 NTD / Ping", table_cell)],
    ]
    t_scen = Table(scen_table_data, colWidths=[140, 65, 75, 100, 100])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_scen)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Scenario Analysis Discussion:</b> These predictions clearly demonstrate the combined economic penalty of structural age and transit distance. "
        "A property 2.2 km from the MRT station that is 32 years old is predicted to command 27.05 units—a <b>44.2% discount</b> relative to a new property "
        "situated 150 metres from the station. Again, these values represent unit-area pricing, not total property acquisition cost.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 14: SYNTHESIS OF STATISTICAL FINDINGS
    # ----------------------------------------------------
    story.append(Paragraph("14. Synthesis of Statistical Findings", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Table 12 presents the complete, consolidated synthesis of all inferential tests, regression models, and evaluations conducted in this investigation.",
        body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Table 12: Comprehensive Synthesis of All Statistical Techniques & Findings</b>", h3))
    synth_table_data = [
        [Paragraph("<b>Statistical Technique</b>", table_header), Paragraph("<b>Empirical Result / Parameter</b>", table_header), Paragraph("<b>Formal Decision / Interpretation</b>", table_header)],
        [Paragraph("Descriptive Statistics", table_cell), Paragraph("Target Mean = 37.980, Median = 38.450, IQR = 18.900", table_cell), Paragraph("Target distribution is broadly symmetric with a notable upper outlier at 117.50 units.", table_cell)],
        [Paragraph("95% Confidence Interval", table_cell), Paragraph("[36.666, 39.295] (10,000 NTD/Ping)", table_cell), Paragraph("Estimated bounds for population mean unit price (Margin of Error = 1.315 units).", table_cell)],
        [Paragraph("Welch's Two-Sample t-Test", table_cell), Paragraph("t = 15.995, df = 399.78, p = 4.065 × 10⁻⁴⁵", table_cell), Paragraph("Reject H₀. Properties near MRT stations command a statistically significant +57.1% premium.", table_cell)],
        [Paragraph("Mann-Whitney U Test", table_cell), Paragraph("U = 37,669.0, p = 1.195 × 10⁻⁴⁰", table_cell), Paragraph("Reject H₀. Confirms transit premium robustness against outliers and distributional skew.", table_cell)],
        [Paragraph("One-Way ANOVA", table_cell), Paragraph("F = 32.062, df = (2, 411), p = 1.150 × 10⁻¹³", table_cell), Paragraph("Reject H₀. Significant mean price differences exist across house-age tertiles.", table_cell)],
        [Paragraph("Tukey HSD Post-Hoc", table_cell), Paragraph("Younger vs Middle: p < 0.001; Younger vs Older: p < 0.001", table_cell), Paragraph("Valuation premium is isolated to Younger homes; Middle-aged and Older homes do not differ (p = 0.286).", table_cell)],
        [Paragraph("Correlation Analysis", table_cell), Paragraph("MRT r = -0.674, ρ = -0.776; Stores r = +0.571; Age r = -0.211", table_cell), Paragraph("MRT proximity is the dominant monotonic predictor; stores co-locate with commercial density.", table_cell)],
        [Paragraph("Simple Linear Regression", table_cell), Paragraph("Ŷ = 42.4347 - 0.2515*Age, R² = 0.0443, p = 1.56 × 10⁻⁵", table_cell), Paragraph("Slope is significant, but age alone explains only 4.4% of total valuation variance.", table_cell)],
        [Paragraph("Multiple Linear Regression", table_cell), Paragraph("Ŷ = 49.8856 - 0.2310*Age - 0.0072*MRT, R² = 0.4911", table_cell), Paragraph("Adding transit proximity boosts R² to 49.11% with zero multicollinearity (VIF = 1.001).", table_cell)],
        [Paragraph("Test Set Evaluation (80:20)", table_cell), Paragraph("MLR Test MAE = 6.248, RMSE = 8.438, Test R² = 0.5756", table_cell), Paragraph("MLR reduces held-out error by 41.2% over SLR and generalizes strongly on unseen data.", table_cell)],
    ]
    t_synth = Table(synth_table_data, colWidths=[110, 160, 210])
    t_synth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_synth)
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 15: LIMITATIONS & FUTURE SCOPE
    # ----------------------------------------------------
    story.append(Paragraph("15. Project Limitations & Analytical Caveats", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "A critical component of academic research is candidly identifying the analytical boundaries and methodological limitations of the study:",
        body
    ))
    story.append(Paragraph("1. <b>Absence of Total Floor Area & Total Price:</b> As emphasized throughout this study, the dataset does not record total square footage. Predicting total transaction price is impossible without floor area data.", bullet_style))
    story.append(Paragraph("2. <b>Sample Size & Spatial Confinement:</b> The dataset comprises 414 transactions restricted entirely to Sindian District, New Taipei City. Real estate dynamics in rural Taiwan or Western metropolitan centers will diverge substantially.", bullet_style))
    story.append(Paragraph("3. <b>Historical Window:</b> The transactions reflect 2012–2013 conditions. Subsequent macroeconomic shifts, interest rate cycles, and inflationary pressures limit direct application to contemporary markets.", bullet_style))
    story.append(Paragraph("4. <b>Undocumented Sampling Protocol:</b> The original documentation does not specify whether transactions were compiled via random sampling, multiple-listing service scraping, or single-broker records, restricting population-wide inference.", bullet_style))
    story.append(Paragraph("5. <b>Omitted Variable Bias:</b> Crucial structural attributes—such as architectural floor level, presence of elevators, construction quality, building orientation, parking spaces, and school district boundaries—are unobserved.", bullet_style))
    story.append(Paragraph("6. <b>Observational Causality:</b> All regression models demonstrate empirical association, not direct economic causation.", bullet_style))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 16: CONCLUSION
    # ----------------------------------------------------
    story.append(Paragraph("16. Conclusions & Academic Learnings", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "This project successfully executed a complete statistical analysis and predictive modeling workflow on the UCI Real Estate Valuation dataset. "
        "The empirical findings deliver clear statistical and practical insights:<br/>"
        "• <b>Transit Proximity Dominates Pricing:</b> Distance to the nearest MRT station is overwhelmingly the strongest predictor of unit-area price (r = -0.674, ρ = -0.776). Properties within walking proximity of an MRT station enjoy an average valuation premium of 57.1% (t = 15.995, p = 4.065e-45).<br/>"
        "• <b>House Age is Secondary and Non-Linear:</b> While building age is statistically significant, it explains only 4.4% of price variance independently. The age discount is concentrated in the first decade of a building's lifespan, after which valuations stabilize.<br/>"
        "• <b>Predictive Superiority of Multiple Regression:</b> Combining building age and transit distance into an OLS Multiple Linear Regression model captures 49.1% of sample variance and generalizes to explain 57.6% of variance on unseen test data, achieving an out-of-sample MAE of 6.248 units (62,480 NTD/Ping).<br/>"
        "• <b>Pedagogical Value:</b> For second-year engineering students, this project exemplifies the vital difference between statistical significance and practical explanatory power, demonstrating the necessity of multivariate modelling and out-of-sample validation.",
        body
    ))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 17: REFERENCES
    # ----------------------------------------------------
    story.append(Paragraph("17. References & Citations", h1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("1. Yeh, I-Cheng. (2018). <i>Real Estate Valuation Dataset</i>. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5J30W.", bullet_style))
    story.append(Paragraph("2. McKinney, W. (2010). Data Structures for Statistical Computing in Python. <i>Proceedings of the 9th Python in Science Conference</i>, 51–56.", bullet_style))
    story.append(Paragraph("3. Harris, C. R., et al. (2020). Array programming with NumPy. <i>Nature</i>, 585(7825), 357–362.", bullet_style))
    story.append(Paragraph("4. Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. <i>Nature Methods</i>, 17(3), 261–272.", bullet_style))
    story.append(Paragraph("5. Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. <i>Proceedings of the 9th Python in Science Conference</i>.", bullet_style))
    story.append(Paragraph("6. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825–2830.", bullet_style))
    story.append(Paragraph("7. Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. <i>Computing in Science & Engineering</i>, 9(3), 90–95.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Check page count
    reader = pypdf.PdfReader(output_pdf)
    num_pages = len(reader.pages)
    print(f"Final Project Report PDF successfully created at: {output_pdf}")
    print(f"Total Page Count: {num_pages} pages (Target: 18-25 pages)")
    return output_pdf, num_pages

if __name__ == '__main__':
    build_pdf_report()

