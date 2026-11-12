"""
Script to generate outputs/Final_Project_Presentation.pptx
Target: 12 professionally styled widescreen (16:9) slides.
Visual explanations, cards, KPI callouts, actual embedded charts, clear typography.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_pptx = os.path.join(base_dir, "outputs", "Final_Project_Presentation.pptx")
    figures_dir = os.path.join(base_dir, "outputs", "figures")
    
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette
    c_navy = RGBColor(26, 54, 93)       # #1A365D - Primary Header
    c_blue = RGBColor(43, 108, 176)     # #2B6CB0 - Subhead & Accents
    c_charcoal = RGBColor(45, 55, 72)   # #2D3748 - Body
    c_light_bg = RGBColor(248, 250, 252)# Card background
    c_white = RGBColor(255, 255, 255)
    c_red = RGBColor(197, 48, 48)       # Highlights
    c_green = RGBColor(47, 133, 90)     # Positive KPI
    c_border = RGBColor(226, 232, 240)
    
    blank_layout = prs.slide_layouts[6]
    
    def add_header(slide, title_text, category_text="Probability & Statistics | Course Project"):
        # Header banner shape
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_navy
        top_bar.line.color.rgb = c_navy
        
        # Category label
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(144, 205, 244) # Soft blue
        
        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = c_white
        
        # Footer
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = c_border
        footer_line.line.color.rgb = c_border
        
        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.3))
        tf_foot = tb_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "UCI Machine Learning Repository (Dataset ID: 477) | Target: Price per Unit Area (10,000 NTD/Ping)"
        p_foot.font.name = "Arial"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = RGBColor(113, 128, 150)

    def add_card(slide, left, top, width, height, bg_color=c_light_bg, border_color=c_border):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ====================================================
    # SLIDE 1: Title Slide
    # ====================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.color.rgb = c_navy
    
    # Inner banner card
    card1 = add_card(s1, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5), bg_color=c_white, border_color=c_blue)
    
    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.733), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "COLLEGE OF ENGINEERING & TECHNOLOGY | DEPARTMENT OF CSE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.alignment = PP_ALIGN.CENTER
    
    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.8), Inches(9.733), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "House Area, Age and Property Price Prediction"
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "An Empirical Statistical Investigation, Hypothesis Testing & Predictive Modeling Study"
    p2.font.name = "Arial"
    p2.font.size = Pt(16)
    p2.font.color.rgb = c_charcoal
    p2.alignment = PP_ALIGN.CENTER
    
    # Meta box
    tb_meta = s1.shapes.add_textbox(Inches(2.5), Inches(3.7), Inches(8.333), Inches(2.2))
    tf_meta = tb_meta.text_frame
    
    meta_lines = [
        ("Course:", "Probability and Statistics (Academic Year 2025–2026)"),
        ("Dataset:", "Real Estate Valuation Dataset (UCI Repository ID: 477, n = 414)"),
        ("Student Details:", "[Student Name & Roll Number Placeholder]"),
        ("Faculty Guide:", "[Faculty Guide / Department Professor Placeholder]"),
        ("Key Context:", "Target: Property Price per Unit Area (10,000 NTD/Ping) | Location: Sindian, Taiwan")
    ]
    for lbl, val in meta_lines:
        p_m = tf_meta.add_paragraph()
        p_m.text = f"{lbl}  {val}"
        p_m.font.name = "Arial"
        p_m.font.size = Pt(12)
        p_m.font.color.rgb = c_charcoal
        p_m.spaceAfter = Pt(4)

    # ====================================================
    # SLIDE 2: Introduction & Problem Statement
    # ====================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Introduction & Problem Statement")
    
    # Left Card: Background & Motivation
    add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Project Motivation & Context"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(12)
    
    bullets_s2_left = [
        "Residential property valuation is pivotal for homeowners, banks, and urban municipal planning.",
        "Traditional comparable-sales methods are qualitative and vulnerable to appraisal bias.",
        "Statistical learning bridges theory and practice by quantifying how property features explain valuation.",
        "Focus of this study: Examine the empirical impact of structural building age and mass transit accessibility."
    ]
    for b in bullets_s2_left:
        p_b = tf.add_paragraph()
        p_b.text = "• " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = c_charcoal
        p_b.spaceAfter = Pt(10)
        
    # Right Card: Problem Statement & Questions
    add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p_r = tf_r.paragraphs[0]
    p_r.text = "Core Research Questions"
    p_r.font.name = "Arial"
    p_r.font.size = Pt(18)
    p_r.font.bold = True
    p_r.font.color.rgb = c_navy
    p_r.spaceAfter = Pt(12)
    
    bullets_s2_right = [
        "Q1 (Inference): What are the reliable population bounds for property valuation in this market?",
        "Q2 (Transit Effect): Do properties close to MRT stations command a statistically significant valuation premium?",
        "Q3 (Depreciation): Does property price decay linearly across building age cohorts?",
        "Q4 (Prediction): Can multiple linear regression accurately predict valuations on unseen test data?"
    ]
    for b in bullets_s2_right:
        p_b = tf_r.add_paragraph()
        p_b.text = "• " + b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = c_charcoal
        p_b.spaceAfter = Pt(10)

    # ====================================================
    # SLIDE 3: Dataset Description & Crucial Limitation
    # ====================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Dataset Provenance & Crucial Boundaries")
    
    # Top Warning Card - Critical Limitation
    add_card(s3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(1.3), bg_color=RGBColor(254, 242, 242), border_color=c_red)
    tb_warn = s3.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(1.1))
    tf_warn = tb_warn.text_frame
    tf_warn.word_wrap = True
    p_w = tf_warn.paragraphs[0]
    p_w.text = "CRUCIAL DATASET LIMITATION & ACADEMIC CLARIFICATION"
    p_w.font.name = "Arial"
    p_w.font.size = Pt(13)
    p_w.font.bold = True
    p_w.font.color.rgb = c_red
    p_w.spaceAfter = Pt(4)
    
    p_w2 = tf_warn.add_paragraph()
    p_w2.text = (
        "The project title refers to 'House Area, Age and Property Price Prediction.' However, the UCI dataset "
        "contains NO total house floor area and NO total property transaction price. The actual target variable is "
        "price per unit area (10,000 NTD/Ping, where 1 Ping ≈ 3.3 m²). We do NOT invent or fabricate house area or total price. "
        "All models and statistical tests predict and analyze unit-area valuation."
    )
    p_w2.font.name = "Arial"
    p_w2.font.size = Pt(11)
    p_w2.font.color.rgb = c_charcoal

    # Bottom 3 Cards: Dataset Attributes
    # Card 1: Provenance
    add_card(s3, Inches(0.8), Inches(2.9), Inches(3.7), Inches(3.9))
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(3.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Dataset Source"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    for line in [
        "Repository: UCI ML Repository (ID 477)",
        "Author: Prof. I-Cheng Yeh (2018)",
        "Location: Sindian District, New Taipei City, Taiwan",
        "Timeframe: 2012–2013 transactions",
        "License: CC BY 4.0 Open Access"
    ]:
        p_l = tf.add_paragraph()
        p_l.text = "• " + line
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = c_charcoal
        p_l.spaceAfter = Pt(5)

    # Card 2: Sample Size & Integrity
    add_card(s3, Inches(4.8), Inches(2.9), Inches(3.7), Inches(3.9))
    tb = s3.shapes.add_textbox(Inches(5.0), Inches(3.1), Inches(3.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Sample Integrity"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    for line in [
        "Observations: 414 transactions",
        "Missing Values: Exactly 0 in all columns",
        "Duplicates: Exactly 0 duplicate rows",
        "Identifier: 'No' (1 to 414) cleanly excluded",
        "All features are numerical (int64/float64)"
    ]:
        p_l = tf.add_paragraph()
        p_l.text = "• " + line
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = c_charcoal
        p_l.spaceAfter = Pt(5)

    # Card 3: Key Features
    add_card(s3, Inches(8.8), Inches(2.9), Inches(3.7), Inches(3.9))
    tb = s3.shapes.add_textbox(Inches(9.0), Inches(3.1), Inches(3.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Analyzed Variables"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    for line in [
        "Target Y: Price per Unit Area",
        "X2: House Age (0 to 43.8 years)",
        "X3: Distance to Nearest MRT Station (m)",
        "X4: Nearby Convenience Stores (count)",
        "X5/X6: Geographic Latitude & Longitude"
    ]:
        p_l = tf.add_paragraph()
        p_l.text = "• " + line
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = c_charcoal
        p_l.spaceAfter = Pt(5)

    # ====================================================
    # SLIDE 4: Exploratory Data Analysis & Distributions
    # ====================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Exploratory Data Analysis & Distributions")
    
    # Images: Hist Price and Hist Age
    img1_path = os.path.join(figures_dir, "06_hist_price_unit_area.png")
    img2_path = os.path.join(figures_dir, "08_hist_house_age.png")
    
    if os.path.exists(img1_path):
        s4.shapes.add_picture(img1_path, Inches(0.8), Inches(1.5), width=Inches(5.7))
    if os.path.exists(img2_path):
        s4.shapes.add_picture(img2_path, Inches(6.8), Inches(1.5), width=Inches(5.7))
        
    # Bottom Takeaway Card
    add_card(s4, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.7))
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.333), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Distributional Findings & Outlier Identification"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(4)
    
    for pt in [
        "Unit Price Distribution: Symmetrical central bulk (Mean = 37.98, Median = 38.45, IQR = 18.90). Prominent upper outlier at 117.50 units.",
        "House Age Bimodality: Prominent spike of brand-new properties (< 5 years, Mode = 0.0), followed by a mature cluster around 25–35 years.",
        "Data Reliability: No missing records or artificial distortions; non-parametric tests will be used alongside parametric tests to verify outlier robustness."
    ]:
        p_pt = tf.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(3)

    # ====================================================
    # SLIDE 5: Descriptive Statistical Summary
    # ====================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Comprehensive Descriptive Statistics")
    
    # 4 KPI Cards along top
    kpi_defs = [
        ("TARGET PRICE MEAN", "37.98", "10,000 NTD / Ping", c_blue),
        ("TARGET MEDIAN", "38.45", "10,000 NTD / Ping", c_navy),
        ("MRT DISTANCE MEDIAN", "492.2 m", "Mean: 1,083.9 m (Skewed)", c_red),
        ("MEAN HOUSE AGE", "17.7 yrs", "Range: 0 to 43.8 yrs", c_green),
    ]
    for idx, (title, val, sub, col) in enumerate(kpi_defs):
        left_pos = Inches(0.8 + idx * 3.0)
        add_card(s5, left_pos, Inches(1.4), Inches(2.733), Inches(1.3))
        tb = s5.shapes.add_textbox(left_pos, Inches(1.5), Inches(2.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(9.5)
        p_t.font.bold = True
        p_t.font.color.rgb = RGBColor(113, 128, 150)
        p_t.alignment = PP_ALIGN.CENTER
        
        p_v = tf.add_paragraph()
        p_v.text = val
        p_v.font.name = "Arial"
        p_v.font.size = Pt(22)
        p_v.font.bold = True
        p_v.font.color.rgb = col
        p_v.alignment = PP_ALIGN.CENTER
        
        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.name = "Arial"
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = c_charcoal
        p_s.alignment = PP_ALIGN.CENTER

    # Table of Detailed Statistics
    add_card(s5, Inches(0.8), Inches(2.9), Inches(11.733), Inches(3.9))
    tb_t = s5.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(11.333), Inches(3.6))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "Detailed Descriptive Parameters (n = 414 Transactions)"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    
    table_lines = [
        "• House Age (X2): Mean = 17.71 yrs | Std Dev = 11.39 yrs | Min = 0.0 yrs | Max = 43.8 yrs | IQR = 19.13 yrs",
        "• MRT Distance (X3): Mean = 1,083.89 m | Median = 492.23 m | Std Dev = 1,262.11 m | Min = 23.38 m | Max = 6,488.02 m",
        "• Convenience Stores (X4): Mean = 4.09 stores | Median = 4.0 stores | Min = 0 | Max = 10 stores | IQR = 5.0 stores",
        "• House Price per Unit Area (Y): Mean = 37.98 units | Median = 38.45 units | Std Dev = 13.61 units | IQR = 18.90 units",
        "• Core Statistical Takeaway: Distance to nearest MRT station features extreme right-skewness (Mean > 2× Median).",
        "  Target property price per unit area exhibits stable central tendency with high dispersion in outlying locations."
    ]
    for line in table_lines:
        p_l = tf_t.add_paragraph()
        p_l.text = line
        p_l.font.name = "Arial"
        p_l.font.size = Pt(11.5)
        p_l.font.color.rgb = c_charcoal
        p_l.spaceAfter = Pt(5)

    # ====================================================
    # SLIDE 6: Confidence Interval & Welch's t-Test
    # ====================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Confidence Interval & Transit Proximity Hypothesis Test")
    
    # Left Card: 95% Confidence Interval
    add_card(s6, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "95% Student's t Confidence Interval"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(10)
    
    ci_pts = [
        "Formula: CI = x̄ ± t_{α/2, n-1} × (s / √n)",
        "Sample Mean (x̄): 37.980 (10,000 NTD / Ping)",
        "Sample Std Dev (s): 13.606 | df: 413",
        "Critical t-value: t* = 1.9657 (two-tailed 95%)",
        "Margin of Error (MoE): 1.315 units",
        "Calculated 95% CI: [36.666, 39.295]",
        "Academic Meaning: Under repeated sampling, 95% of constructed intervals contain true population mean μ.",
        "Caveat: Undocumented sampling mechanism limits unconstrained population generalization."
    ]
    for pt in ci_pts:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(4)

    # Right Card: Welch's Two-Sample t-Test
    add_card(s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    tb_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Welch's Two-Sample t-Test (MRT Distance)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(10)
    
    ttest_pts = [
        "Hypothesis H₀: μ_Near = μ_Far (No price difference)",
        "Median Split Threshold: Distance = 492.23 metres",
        "Near MRT Group (≤ 492 m): n₁ = 210, Mean = 46.265 units",
        "Far MRT Group (> 492 m): n₂ = 204, Mean = 29.452 units",
        "Valuation Difference: +16.813 units (+57.1% premium)",
        "Test Statistic: t = 15.995 (Welch df = 399.78)",
        "p-value: 4.065 × 10⁻⁴⁵  --->  REJECT H₀",
        "Robustness: Mann-Whitney U test p = 1.195 × 10⁻⁴⁰ confirms transit proximity dominates property pricing."
    ]
    for pt in ttest_pts:
        p_pt = tf_r.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(4)

    # ====================================================
    # SLIDE 7: One-Way ANOVA & Correlation Analysis
    # ====================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. One-Way ANOVA (Age Tertiles) & Correlation")
    
    # Left Card: ANOVA
    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tb_l = s7.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "One-Way ANOVA: House Age Tertiles"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    
    anova_pts = [
        "Tertile Cohorts: Younger (≤13y), Middle (13-26.6y), Older (>26.6y)",
        "Group Means: Younger = 44.91 | Middle = 33.34 | Older = 35.69",
        "ANOVA F-statistic: F = 32.062 (df = 2, 411)",
        "p-value: 1.150 × 10⁻¹³  --->  REJECT H₀",
        "Tukey HSD Post-Hoc Pairwise Analysis:",
        "  - Younger vs. Middle: Diff = +11.57 (p < 0.001, Significant)",
        "  - Younger vs. Older: Diff = +9.22 (p < 0.001, Significant)",
        "  - Middle vs. Older: Diff = -2.35 (p = 0.286, Not Significant)",
        "Takeaway: Age depreciation occurs in the first decade; older properties plateau in value."
    ]
    for pt in anova_pts:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(3)

    # Right Card: Correlation Matrix
    add_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    tb_r = s7.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Bivariate Correlation Structure"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    
    corr_pts = [
        "MRT Distance (X3): Pearson r = -0.674 | Spearman ρ = -0.776 (p = 1.81 × 10⁻⁸⁴). Decisive negative monotonic decay.",
        "Convenience Stores (X4): Pearson r = +0.571 | Spearman ρ = +0.617. Commercial co-location around transit nodes.",
        "House Age (X2): Pearson r = -0.211 | Spearman ρ = -0.282. Weak negative association.",
        "Why Spearman > Pearson for MRT: Non-linear curvature—rapid initial price drops followed by distance plateau.",
        "Causation Warning: High correlation with stores and MRT reflects spatial urban agglomeration, not direct causation."
    ]
    for pt in corr_pts:
        p_pt = tf_r.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(4)

    # ====================================================
    # SLIDE 8: Regression Analysis (SLR vs MLR)
    # ====================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Simple vs. Multiple Linear Regression")
    
    # Left Card: SLR
    add_card(s8, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tb_l = s8.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Simple Linear Regression (House Age)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    
    slr_pts = [
        "Equation: Ŷ = 42.4347 - 0.2515 × (House Age)",
        "Intercept (β₀): 42.43 units (New property baseline)",
        "Slope (β₁): -0.2515 units/year (p = 1.56 × 10⁻⁵)",
        "R-squared: R² = 0.0443 (Only 4.4% variance explained)",
        "Adjusted R²: 0.0420 | Residual Std Error: 13.318",
        "Diagnostic Flaw: Over 95.5% of price variation is unexplained by building age alone. Bivariate model is inadequate."
    ]
    for pt in slr_pts:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(4)

    # Right Card: MLR
    add_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    tb_r = s8.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Multiple Linear Regression (Age + MRT)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(8)
    
    mlr_pts = [
        "Equation: Ŷ = 49.8856 - 0.2310 × Age - 0.0072 × MRT_Dist",
        "House Age Coeff: -0.2310 (t = -5.50, p = 1.05 × 10⁻⁷)",
        "MRT Dist Coeff: -0.0072 (t = -19.01, p = 2.44 × 10⁻⁵³)",
        "R-squared: R² = 0.4911 (49.1% variance explained!)",
        "Adjusted R²: 0.4887 | F-statistic: 198.3 (p = 2.65 × 10⁻⁶⁰)",
        "Multicollinearity: VIF(Age) = 1.001, VIF(MRT) = 1.001 (Zero collinearity concerns; predictors are orthogonal).",
        "Key Gain: Adding transit proximity yields an 11× increase in explained variance."
    ]
    for pt in mlr_pts:
        p_pt = tf_r.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(4)

    # ====================================================
    # SLIDE 9: Train-Test Predictive Evaluation
    # ====================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Out-of-Sample Predictive Evaluation (80:20 Split)")
    
    # Image: Test Actual vs Predicted
    img_eval_path = os.path.join(figures_dir, "18_test_actual_vs_predicted.png")
    if os.path.exists(img_eval_path):
        s9.shapes.add_picture(img_eval_path, Inches(0.8), Inches(1.4), width=Inches(6.2))
        
    # Right Performance Comparison Card
    add_card(s9, Inches(7.3), Inches(1.4), Inches(5.2), Inches(5.3))
    tb_perf = s9.shapes.add_textbox(Inches(7.5), Inches(1.6), Inches(4.8), Inches(4.9))
    tf_p = tb_perf.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "Held-Out Test Set Results (n = 83)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.spaceAfter = Pt(10)
    
    eval_pts = [
        "Mean Absolute Error (MAE):",
        "  - SLR (Age): 10.621 units",
        "  - MLR (Age + MRT): 6.248 units (41.2% Reduction!)",
        "Mean Squared Error (MSE):",
        "  - SLR: 165.205  vs.  MLR: 71.206 (56.9% Drop)",
        "Root Mean Squared Error (RMSE):",
        "  - SLR: 12.853 units  vs.  MLR: 8.438 units (34.4% Drop)",
        "Coefficient of Determination (Test R²):",
        "  - SLR: 0.0152 (1.5% explained on test set)",
        "  - MLR: 0.5756 (57.6% explained on test set!)",
        "Predictive Takeaway: The multiple regression model strongly generalizes to unseen data, cutting prediction errors by over 40%."
    ]
    for pt in eval_pts:
        p_pt = tf_p.add_paragraph()
        p_pt.text = pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(3)

    # ====================================================
    # SLIDE 10: Sample Predictions & Scenario Analysis
    # ====================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Practical Valuation Scenarios")
    
    # 3 Scenario Cards
    scenarios = [
        ("SCENARIO A: PRIME TRANSIT CONDO", "Age: 2.0 yrs | MRT: 150 m", "48.51", "485,100 NTD / Ping",
         "Premium valuation driven by minimal age wear and immediate walking proximity to metro transit hub.", c_green),
        ("SCENARIO B: SUBURBAN RESIDENCE", "Age: 15.0 yrs | MRT: 600 m", "42.27", "422,700 NTD / Ping",
         "Moderate valuation representing a typical mid-age apartment located in an established residential pocket.", c_blue),
        ("SCENARIO C: PERIPHERAL OLDER HOUSE", "Age: 32.0 yrs | MRT: 2,200 m", "27.05", "270,500 NTD / Ping",
         "Severe double discount (-44.2% vs Scenario A) reflecting combined age depreciation and distance from transit.", c_red),
    ]
    for idx, (title, params, price, equiv, desc, col) in enumerate(scenarios):
        left_pos = Inches(0.8 + idx * 4.0)
        add_card(s10, left_pos, Inches(1.5), Inches(3.733), Inches(4.0))
        tb = s10.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.333), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.spaceAfter = Pt(6)
        
        p_par = tf.add_paragraph()
        p_par.text = params
        p_par.font.size = Pt(10)
        p_par.font.color.rgb = RGBColor(113, 128, 150)
        p_par.spaceAfter = Pt(10)
        
        p_pr = tf.add_paragraph()
        p_pr.text = price
        p_pr.font.size = Pt(28)
        p_pr.font.bold = True
        p_pr.font.color.rgb = c_navy
        
        p_eq = tf.add_paragraph()
        p_eq.text = equiv
        p_eq.font.size = Pt(10.5)
        p_eq.font.bold = True
        p_eq.font.color.rgb = c_charcoal
        p_eq.spaceAfter = Pt(10)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = c_charcoal

    # Bottom Note
    add_card(s10, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.1))
    tb_n = s10.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.333), Inches(0.9))
    tf_n = tb_n.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = "Practical Property Valuation Note:"
    p_n.font.name = "Arial"
    p_n.font.size = Pt(11)
    p_n.font.bold = True
    p_n.font.color.rgb = c_navy
    p_n.spaceAfter = Pt(2)
    p_n2 = tf_n.add_paragraph()
    p_n2.text = (
        "Model outputs provide unit-area estimates (10,000 NTD/Ping). Total property acquisition costs cannot be calculated "
        "because total floor area is unobserved in the UCI dataset. Predictions strictly adhere to empirical predictor ranges."
    )
    p_n2.font.size = Pt(10)
    p_n2.font.color.rgb = c_charcoal

    # ====================================================
    # SLIDE 11: Limitations & Future Scope
    # ====================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. Project Limitations & Future Scope")
    
    # Left Card: Limitations
    add_card(s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    tb_l = s11.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Dataset & Analytical Limitations"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_red
    p.spaceAfter = Pt(10)
    
    lim_pts = [
        "No House Area Data: Target is price per Ping, not total transaction price. Total floor area is unobserved.",
        "Geographic Confinement: Data reflects only Sindian District, New Taipei City; cannot generalize globally.",
        "Historical Window: Transactions occurred in 2012–2013; macroeconomic cycles and inflation have shifted.",
        "Undocumented Sampling: Sampling protocol is not detailed in UCI documentation, constraining broad inference.",
        "Omitted Variables: Crucial determinants (floor level, interior condition, elevators, parking, school zones) are absent."
    ]
    for pt in lim_pts:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(6)

    # Right Card: Future Scope
    add_card(s11, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    tb_r = s11.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Future Research & Engineering Scope"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = c_green
    p.spaceAfter = Pt(10)
    
    scope_pts = [
        "Incorporate Floor Area & Total Cost: Collect datasets containing floor space, layout, and building unit count.",
        "Non-Linear & Spatial Modeling: Apply spatial hedonic models, Generalized Additive Models (GAMs), and Random Forests.",
        "Contemporary Time-Series Data: Update valuation models using post-2024 transaction records across diverse cities.",
        "Computer Vision & Satellite Integration: Incorporate street-view imagery and satellite land-use features.",
        "Deployment: Build interactive valuation dashboards for prospective homebuyers and lending appraisers."
    ]
    for pt in scope_pts:
        p_pt = tf_r.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = c_charcoal
        p_pt.spaceAfter = Pt(6)

    # ====================================================
    # SLIDE 12: Conclusion & Q&A
    # ====================================================
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = c_navy
    bg12.line.color.rgb = c_navy
    
    card12 = add_card(s12, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5), bg_color=c_white, border_color=c_blue)
    
    tb = s12.shapes.add_textbox(Inches(1.8), Inches(1.3), Inches(9.733), Inches(1.0))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Conclusions & Academic Summary"
    p.font.name = "Arial"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.alignment = PP_ALIGN.CENTER
    
    tb_c = s12.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.333), Inches(3.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    conc_pts = [
        "1. Transit Accessibility Dominates: Distance to MRT is the single strongest factor (r = -0.674, t = 15.995, p < 10⁻⁴⁴).",
        "2. House Age is Non-Linear: Significant depreciation occurs in the first decade; age alone explains only 4.4% of price variance.",
        "3. Multiple Regression Delivers Generalization: Combining Age and MRT explains 57.6% of test variance, cutting error by 41.2%.",
        "4. Methodological Rigor: Complete adherence to verified data, explicit limitation reporting, and robust assumptions testing."
    ]
    for pt in conc_pts:
        p_c = tf_c.add_paragraph()
        p_c.text = pt
        p_c.font.name = "Arial"
        p_c.font.size = Pt(13)
        p_c.font.color.rgb = c_charcoal
        p_c.spaceAfter = Pt(8)
        
    tb_qa = s12.shapes.add_textbox(Inches(1.8), Inches(5.3), Inches(9.733), Inches(0.8))
    tf_qa = tb_qa.text_frame
    p_qa = tf_qa.paragraphs[0]
    p_qa.text = "Thank You! | Questions & Discussion Welcome"
    p_qa.font.name = "Arial"
    p_qa.font.size = Pt(18)
    p_qa.font.bold = True
    p_qa.font.color.rgb = c_blue
    p_qa.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx)
    print(f"Presentation successfully created at: {output_pptx}")
    print(f"Total Slides Created: {len(prs.slides)} slides (Target: 10-12 slides)")
    return output_pptx, len(prs.slides)

if __name__ == '__main__':
    create_presentation()

