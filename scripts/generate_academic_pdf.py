#!/usr/bin/env python3
"""
QALB Academic PDF Report Generator - Comprehensive Full Report
==============================================================

Generates a sophisticated, minimalist academic PDF report containing
ALL 8 chapters from the GPT-5-mini generated comprehensive evaluation.
Features: Cyan blue theme (fawadhs.dev), page numbers, data visualizations,
          Urdu Nastaliq font support for proper Urdu script rendering.

Author: Fawad Hussain (fawadhs.dev)
"""

import os
import re
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, String, Line, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF

# Import Arabic/Urdu text shaping libraries
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    URDU_SHAPING_AVAILABLE = True
    print("✓ Urdu text shaping libraries loaded (arabic_reshaper, python-bidi)")
except ImportError:
    URDU_SHAPING_AVAILABLE = False
    print("⚠ Urdu shaping libraries not available. Install: pip install arabic-reshaper python-bidi")

# Register Urdu Nastaliq font
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
URDU_FONT_PATH = os.path.join(PROJECT_DIR, 'fonts', 'Amiri', 'Amiri-1.000', 'Amiri-Regular.ttf')

# Register Urdu font if available
URDU_FONT_AVAILABLE = False
if os.path.exists(URDU_FONT_PATH):
    try:
        pdfmetrics.registerFont(TTFont('Amiri', URDU_FONT_PATH))
        URDU_FONT_AVAILABLE = True
        print(f"✓ Urdu font registered: Amiri")
    except Exception as e:
        print(f"⚠ Could not register Urdu font: {e}")
else:
    print(f"⚠ Urdu font not found at: {URDU_FONT_PATH}")


# Color constants for charts - fawadhs.dev theme
CYAN_PRIMARY = colors.HexColor('#00BCD4')
CYAN_DARK = colors.HexColor('#0097A7')
CYAN_LIGHT = colors.HexColor('#4DD0E1')
NAVY_DARK = colors.HexColor('#1a1a2e')
TEAL = colors.HexColor('#009688')
GRAY_TEXT = colors.HexColor('#2d3436')


class NumberedCanvas(canvas.Canvas):
    """Canvas with page numbers in cyan."""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Skip page number on title page
        if self._pageNumber > 1:
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor('#00BCD4'))  # Cyan
            page_text = f"— {self._pageNumber} —"
            self.drawCentredString(A4[0] / 2, 0.4 * inch, page_text)


def create_score_evolution_chart():
    """Create a line chart showing score evolution across rounds."""
    drawing = Drawing(450, 200)
    
    # Data
    data = [
        [74.4, 78.3, 79.2, 77.7],  # Combined
        [74.4, 78.3, 80.0, 78.0],  # Urdu
        [74.5, 78.2, 78.4, 77.4],  # Roman
    ]
    
    chart = HorizontalLineChart()
    chart.x = 50
    chart.y = 30
    chart.height = 140
    chart.width = 380
    chart.data = data
    
    chart.categoryAxis.categoryNames = ['Round 1', 'Round 2', 'Round 3', 'Round 4']
    chart.categoryAxis.labels.fontName = 'Helvetica'
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.boxAnchor = 'n'
    
    chart.valueAxis.valueMin = 70
    chart.valueAxis.valueMax = 82
    chart.valueAxis.valueStep = 2
    chart.valueAxis.labels.fontName = 'Helvetica'
    chart.valueAxis.labels.fontSize = 8
    
    # Line styles - Cyan theme
    chart.lines[0].strokeColor = CYAN_PRIMARY
    chart.lines[0].strokeWidth = 3
    chart.lines[0].symbol = makeMarker('FilledCircle')
    chart.lines[0].symbol.fillColor = CYAN_PRIMARY
    chart.lines[0].symbol.size = 6
    
    chart.lines[1].strokeColor = CYAN_DARK
    chart.lines[1].strokeWidth = 2
    chart.lines[1].symbol = makeMarker('FilledSquare')
    chart.lines[1].symbol.fillColor = CYAN_DARK
    chart.lines[1].symbol.size = 5
    
    chart.lines[2].strokeColor = TEAL
    chart.lines[2].strokeWidth = 2
    chart.lines[2].symbol = makeMarker('FilledDiamond')
    chart.lines[2].symbol.fillColor = TEAL
    chart.lines[2].symbol.size = 5
    
    drawing.add(chart)
    
    # Title
    drawing.add(String(225, 185, 'Score Evolution Across Evaluation Rounds',
                      fontSize=11, fontName='Helvetica-Bold', fillColor=NAVY_DARK, textAnchor='middle'))
    
    # Legend
    drawing.add(Rect(60, 5, 10, 10, fillColor=CYAN_PRIMARY, strokeColor=None))
    drawing.add(String(75, 7, 'Combined', fontSize=8, fontName='Helvetica', fillColor=GRAY_TEXT))
    
    drawing.add(Rect(150, 5, 10, 10, fillColor=CYAN_DARK, strokeColor=None))
    drawing.add(String(165, 7, 'Urdu Script', fontSize=8, fontName='Helvetica', fillColor=GRAY_TEXT))
    
    drawing.add(Rect(250, 5, 10, 10, fillColor=TEAL, strokeColor=None))
    drawing.add(String(265, 7, 'Roman Urdu', fontSize=8, fontName='Helvetica', fillColor=GRAY_TEXT))
    
    return drawing


def create_category_performance_chart():
    """Create a horizontal bar chart showing category performance."""
    drawing = Drawing(450, 220)
    
    # Data - categories and their average scores
    categories = ['Translation', 'Summarization', 'Q&A', 'Conversation', 
                  'Creative Writing', 'Instruction', 'Math', 'Reasoning']
    scores = [85.5, 81.5, 77.5, 75.5, 73.5, 71.5, 67.0, 63.5]
    
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 40
    chart.height = 150
    chart.width = 380
    chart.data = [scores]
    
    chart.categoryAxis.categoryNames = categories
    chart.categoryAxis.labels.fontName = 'Helvetica'
    chart.categoryAxis.labels.fontSize = 7
    chart.categoryAxis.labels.angle = 45
    chart.categoryAxis.labels.boxAnchor = 'ne'
    
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.valueAxis.labels.fontName = 'Helvetica'
    chart.valueAxis.labels.fontSize = 8
    
    # Bar colors - gradient from cyan to teal based on performance
    chart.bars[0].fillColor = CYAN_PRIMARY
    chart.bars.strokeColor = None
    chart.barWidth = 35
    
    # Color each bar based on score
    for i, score in enumerate(scores):
        if score >= 80:
            chart.bars[0].fillColor = CYAN_PRIMARY
        elif score >= 70:
            chart.bars[0].fillColor = CYAN_DARK
        else:
            chart.bars[0].fillColor = colors.HexColor('#FF7043')  # Orange for weak
    
    drawing.add(chart)
    
    # Title
    drawing.add(String(240, 205, 'Category Performance Analysis (%)',
                      fontSize=11, fontName='Helvetica-Bold', fillColor=NAVY_DARK, textAnchor='middle'))
    
    # 70% threshold line
    drawing.add(Line(50, 40 + (70/100)*150, 430, 40 + (70/100)*150,
                    strokeColor=colors.HexColor('#FF5722'), strokeWidth=1, strokeDashArray=[4, 2]))
    drawing.add(String(435, 40 + (70/100)*150 - 3, '70%',
                      fontSize=7, fontName='Helvetica', fillColor=colors.HexColor('#FF5722')))
    
    return drawing


def create_failure_pattern_pie():
    """Create a pie chart showing failure pattern distribution."""
    drawing = Drawing(300, 200)
    
    pie = Pie()
    pie.x = 80
    pie.y = 30
    pie.width = 140
    pie.height = 140
    
    pie.data = [42, 28, 18, 12]
    pie.labels = ['Arithmetic\n42%', 'Pattern\n28%', 'Setup\n18%', 'Format\n12%']
    
    pie.slices.strokeWidth = 1
    pie.slices.strokeColor = colors.white
    
    # Cyan color palette
    pie.slices[0].fillColor = CYAN_PRIMARY
    pie.slices[1].fillColor = CYAN_DARK
    pie.slices[2].fillColor = TEAL
    pie.slices[3].fillColor = CYAN_LIGHT
    
    pie.slices[0].popout = 5
    
    pie.sideLabels = True
    pie.slices.fontName = 'Helvetica'
    pie.slices.fontSize = 8
    
    drawing.add(pie)
    
    # Title
    drawing.add(String(150, 185, 'Reasoning Failure Distribution',
                      fontSize=10, fontName='Helvetica-Bold', fillColor=NAVY_DARK, textAnchor='middle'))
    
    return drawing


def create_round_comparison_chart():
    """Create a grouped bar chart comparing rounds."""
    drawing = Drawing(450, 180)
    
    chart = VerticalBarChart()
    chart.x = 60
    chart.y = 30
    chart.height = 120
    chart.width = 350
    
    # Data: [Urdu, Roman] for each round
    chart.data = [
        [74.4, 78.3, 80.0, 78.0],  # Urdu
        [74.5, 78.2, 78.4, 77.4],  # Roman
    ]
    
    chart.categoryAxis.categoryNames = ['Round 1\n(Baseline)', 'Round 2\n(Bilingual)', 
                                         'Round 3\n(Math Fix)', 'Round 4\n(Synonym)']
    chart.categoryAxis.labels.fontName = 'Helvetica'
    chart.categoryAxis.labels.fontSize = 7
    
    chart.valueAxis.valueMin = 70
    chart.valueAxis.valueMax = 82
    chart.valueAxis.valueStep = 2
    chart.valueAxis.labels.fontName = 'Helvetica'
    chart.valueAxis.labels.fontSize = 8
    
    chart.bars[0].fillColor = CYAN_PRIMARY
    chart.bars[1].fillColor = TEAL
    chart.bars.strokeColor = None
    chart.barWidth = 25
    chart.groupSpacing = 15
    
    drawing.add(chart)
    
    # Title
    drawing.add(String(235, 165, 'Urdu vs Roman Urdu Performance by Round',
                      fontSize=10, fontName='Helvetica-Bold', fillColor=NAVY_DARK, textAnchor='middle'))
    
    # Legend
    drawing.add(Rect(120, 5, 12, 12, fillColor=CYAN_PRIMARY, strokeColor=None))
    drawing.add(String(137, 7, 'Urdu Script', fontSize=8, fontName='Helvetica', fillColor=GRAY_TEXT))
    
    drawing.add(Rect(230, 5, 12, 12, fillColor=TEAL, strokeColor=None))
    drawing.add(String(247, 7, 'Roman Urdu', fontSize=8, fontName='Helvetica', fillColor=GRAY_TEXT))
    
    return drawing


def register_urdu_fonts():
    """Register fonts that support Urdu script."""
    import platform
    
    # Common paths for fonts supporting Arabic/Urdu
    font_paths = []
    
    if platform.system() == 'Windows':
        font_paths = [
            'C:/Windows/Fonts/NotoNastaliqUrdu-Regular.ttf',
            'C:/Windows/Fonts/Jameel Noori Nastaleeq.ttf',
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/arialuni.ttf',
            'C:/Windows/Fonts/tahoma.ttf',
            'C:/Windows/Fonts/segoeui.ttf',
        ]
    
    # Try to register an Urdu-capable font
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).replace('.ttf', '').replace(' ', '')
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return font_name
            except:
                continue
    
    return None


def clean_markdown_text(text):
    """Clean markdown formatting for PDF rendering."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = text.replace('&', '&amp;')
    text = text.replace('<b>', '<<<BOLD>>>').replace('</b>', '<<<ENDBOLD>>>')
    text = text.replace('<i>', '<<<ITALIC>>>').replace('</i>', '<<<ENDITALIC>>>')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('<<<BOLD>>>', '<b>').replace('<<<ENDBOLD>>>', '</b>')
    text = text.replace('<<<ITALIC>>>', '<i>').replace('<<<ENDITALIC>>>', '</i>')
    return text


def create_academic_pdf():
    """Generate sophisticated minimalist academic PDF report with ALL chapters."""
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "reports", "QALB_Academic_Report.pdf")
    
    # Create document with slightly larger margins for readability
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.9*inch,
        leftMargin=0.9*inch,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch
    )
    
    # Register Urdu font
    urdu_font = register_urdu_fonts()
    
    # Define sophisticated color palette - fawadhs.dev inspired (Cyan Blue theme)
    DARK_NAVY = colors.HexColor('#1a1a2e')      # Deep navy
    ACCENT_CYAN = colors.HexColor('#00BCD4')    # Cyan blue (primary accent)
    ACCENT_TEAL = colors.HexColor('#00ACC1')    # Teal variant
    LIGHT_CYAN = colors.HexColor('#E0F7FA')     # Light cyan background
    LIGHT_GRAY = colors.Color(0.92, 0.92, 0.92)
    TEXT_GRAY = colors.HexColor('#2d3436')      # Dark gray text
    SOFT_BLUE = colors.HexColor('#E3F2FD')      # Soft blue for quotes
    
    # Create custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=DARK_NAVY,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=34
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_GRAY,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=18
    )
    
    # Chapter header style
    chapter_style = ParagraphStyle(
        'ChapterHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=DARK_NAVY,
        spaceBefore=30,
        spaceAfter=16,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    # Section header style
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=DARK_NAVY,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        leading=18
    )
    
    # Subsection style
    subsection_style = ParagraphStyle(
        'SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=DARK_NAVY,
        spaceBefore=14,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=9.5,
        textColor=TEXT_GRAY,
        alignment=TA_JUSTIFY,
        spaceBefore=3,
        spaceAfter=6,
        fontName='Helvetica',
        leading=13,
        firstLineIndent=0
    )
    
    # Quote/highlight style
    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DARK_NAVY,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=8,
        fontName='Helvetica-Oblique',
        leading=12,
        leftIndent=15,
        rightIndent=15,
        backColor=SOFT_BLUE,
        borderPadding=8
    )
    
    # Bullet point style
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceBefore=2,
        spaceAfter=2
    )
    
    # Example/code style
    example_style = ParagraphStyle(
        'Example',
        parent=styles['Normal'],
        fontSize=8.5,
        textColor=colors.Color(0.3, 0.3, 0.3),
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=4,
        fontName='Courier',
        leading=11,
        leftIndent=15,
        backColor=LIGHT_GRAY,
        borderPadding=6
    )
    
    # Build document content
    story = []
    
    # ========== TITLE PAGE ==========
    story.append(Spacer(1, 1.2*inch))
    story.append(HRFlowable(width="40%", thickness=3, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=20))
    story.append(Paragraph("QALB", title_style))
    story.append(Paragraph("Urdu AI Model Comprehensive Evaluation", subtitle_style))
    story.append(HRFlowable(width="40%", thickness=3, color=ACCENT_CYAN, spaceBefore=20, spaceAfter=40))
    
    # Key metrics
    metrics_data = [
        ['79.2', '77.7', '320'],
        ['Peak Score', 'Final Score', 'Test Cases']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch])
    metrics_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 32),
        ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_CYAN),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, 1), 9),
        ('TEXTCOLOR', (0, 1), (-1, 1), TEXT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, 1), 4),
    ]))
    story.append(metrics_table)
    
    story.append(Spacer(1, 0.8*inch))
    
    model_info = ParagraphStyle('ModelInfo', parent=styles['Normal'], fontSize=10, 
                                 textColor=TEXT_GRAY, alignment=TA_CENTER, fontName='Helvetica', leading=14)
    story.append(Paragraph("<b>Model:</b> enstazao/qalb:8b-instruct-fp16", model_info))
    story.append(Paragraph("<b>Evaluation Rounds:</b> 4 Iterative Assessments", model_info))
    story.append(Paragraph("<b>Categories:</b> 8 Bilingual Test Domains", model_info))
    story.append(Paragraph("<b>Analysis Engine:</b> GPT-5-mini", model_info))
    
    story.append(Spacer(1, 0.6*inch))
    date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=9, 
                                 textColor=TEXT_GRAY, alignment=TA_CENTER, fontName='Helvetica')
    story.append(Paragraph("Comprehensive Evaluation Report", date_style))
    story.append(Paragraph("February 2026", date_style))
    
    story.append(PageBreak())
    
    # ========== TABLE OF CONTENTS ==========
    story.append(Paragraph("Table of Contents", chapter_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceBefore=0, spaceAfter=15))
    
    toc_items = [
        ("Chapter 1: Executive Summary", "3"),
        ("Chapter 2: Evaluation Methodology", "5"),
        ("Chapter 3: Round-by-Round Analysis", "7"),
        ("Chapter 4: Category Performance Analysis", "10"),
        ("Chapter 5: Translation Capability Assessment", "13"),
        ("Chapter 6: Reasoning and Mathematical Capabilities", "15"),
        ("Chapter 7: Limitations and Recommendations", "18"),
        ("Chapter 8: Conclusion", "22"),
        ("Appendix A: Test Categories and Counts", "24"),
        ("Appendix B: Score Evolution", "24"),
        ("Appendix C: Technical Specifications", "25"),
        ("Appendix D: Repository", "25"),
        ("Appendix E: Urdu Script Test Examples", "26"),
        ("Appendix F: Roman Urdu Test Examples", "27"),
    ]
    
    toc_data = [[item[0], item[1]] for item in toc_items]
    toc_table = Table(toc_data, colWidths=[5*inch, 0.5*inch])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.Color(0.9, 0.9, 0.9)),
    ]))
    story.append(toc_table)
    
    story.append(PageBreak())
    
    # ========== CHAPTER 1: EXECUTIVE SUMMARY ==========
    story.append(Paragraph("Chapter 1: Executive Summary", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    exec_summary = """This report presents a comprehensive, data-driven evaluation of the Qalb Urdu AI model 
    (enstazao/qalb:8b-instruct-fp16) across four iterative assessment rounds. The evaluation framework 
    encompasses 320 test cases distributed across 8 categories, examining both Urdu script and Roman 
    Urdu capabilities. The model demonstrated progressive improvement from a baseline score of 74.4 
    to a peak of 79.2 in Round 3, with the final round achieving 77.7."""
    story.append(Paragraph(exec_summary, body_style))
    
    story.append(Paragraph("Key Findings", section_style))
    
    story.append(Paragraph("<b>Performance Trajectory:</b>", body_style))
    story.append(Paragraph("• Round 1 (Baseline): 74.4/100 - Initial assessment with standard keyword matching", bullet_style))
    story.append(Paragraph("• Round 2 (Bilingual Enhancement): 78.3/100 (+3.9) - Improved Urdu-Roman keyword coverage", bullet_style))
    story.append(Paragraph("• Round 3 (Mathematical Clarity): 79.2/100 (+0.9) - Peak performance with refined math evaluation", bullet_style))
    story.append(Paragraph("• Round 4 (Synonym Expansion): 77.7/100 (-1.5) - Regression due to keyword dilution effect", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Identified Strengths:</b>", body_style))
    story.append(Paragraph("• Translation tasks achieved approximately 86% adequacy/fluency scores", bullet_style))
    story.append(Paragraph("• Abstractive summarization averaged ~82% on ROUGE-informed human evaluations", bullet_style))
    story.append(Paragraph("• Consistent performance across both Urdu script and Roman Urdu inputs", bullet_style))
    story.append(Paragraph("• Strong handling of conversational and question-answering tasks", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Identified Weaknesses:</b>", body_style))
    story.append(Paragraph("• Reasoning and mathematical tasks scored lower at approximately 64%", bullet_style))
    story.append(Paragraph("• Numeric formatting inconsistencies (digits vs. words) caused evaluation mismatches", bullet_style))
    story.append(Paragraph("• Complex multi-step inference problems showed systematic failures", bullet_style))
    story.append(Paragraph("• Sensitivity to prompt phrasing, particularly for ambiguous terms", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Why Round 4 Decreased", section_style))
    
    r4_analysis = """Root-cause analysis of the Round 4 regressions indicates the keyword expansion 
    introduced overbroad and ambiguous matches that produced two principal failure modes:"""
    story.append(Paragraph(r4_analysis, body_style))
    
    story.append(Paragraph("• <b>Keyword collisions and substring over-matching (35-40% of regressions):</b> Adding both "
                          "'Islam' and 'Islamabad' without boundary anchoring caused the evaluator to mislabel "
                          "correct answers or count partial matches as incorrect.", bullet_style))
    story.append(Paragraph("• <b>Increased prompt ambiguity from new synonyms/variants (25-30%):</b> Expanding keywords "
                          "without corresponding normalization rules allowed the same underlying response to be "
                          "matched inconsistently across Roman and Urdu script paths.", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    operational_text = """Operationally, the expansion increased surface area for matching but lacked: 
    tokenization/word-boundary guards (e.g., regex anchors), normalization (Unicode normalization for 
    Urdu script; standardized Roman transliteration), and language detection pre-routing to the 
    appropriate evaluation pipeline."""
    story.append(Paragraph(operational_text, body_style))
    
    story.append(Paragraph("Score Evolution Summary", section_style))
    
    score_data = [
        ['Round', 'Urdu Script', 'Roman Urdu', 'Combined', 'Δ Change'],
        ['Round 1 (Baseline)', '74.4', '74.5', '74.4', '—'],
        ['Round 2 (Bilingual)', '78.3', '78.2', '78.3', '+3.9'],
        ['Round 3 (Math Fix)', '80.0', '78.4', '79.2', '+0.9'],
        ['Round 4 (Synonym)', '78.0', '77.4', '77.7', '-1.5']
    ]
    
    score_table = Table(score_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 0.8*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('BACKGROUND', (0, 3), (-1, 3), LIGHT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.8, 0.8, 0.8)),
        ('BACKGROUND', (3, 3), (3, 3), colors.Color(0.9, 0.95, 0.9)),
        ('FONTNAME', (3, 3), (3, 3), 'Helvetica-Bold'),
    ]))
    story.append(score_table)
    
    story.append(Spacer(1, 0.15*inch))
    
    # Add Score Evolution Chart
    story.append(create_score_evolution_chart())
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "The net improvement of +3.3 points from baseline to final round demonstrates measurable progress, "
        "while the Round 4 regression reveals important insights about evaluation methodology sensitivity. "
        "Peak performance of 79.2/100 represents a 6.5% improvement over baseline.",
        quote_style
    ))
    
    story.append(Paragraph("Strategic Recommendations", section_style))
    
    story.append(Paragraph("<b>Immediate Actions:</b>", body_style))
    story.append(Paragraph("• Revert the most aggressive Round 4 keyword additions and restore Round 3 keyword set as stable baseline", bullet_style))
    story.append(Paragraph("• Introduce deterministic normalization and language-detection preprocessing", bullet_style))
    story.append(Paragraph("• Harden keyword matching using token/word-boundary regex, disallow substring matches", bullet_style))
    
    story.append(Paragraph("<b>Medium-term Actions:</b>", body_style))
    story.append(Paragraph("• Expand manual error analysis coverage to stratified sample (>=10% of tests) after each change", bullet_style))
    story.append(Paragraph("• Fine-tune on mixed Urdu/Roman parallel corpus", bullet_style))
    story.append(Paragraph("• Track more granular metrics per category (precision/recall of keyword detection, language detection accuracy)", bullet_style))
    
    story.append(Paragraph("Evaluation Limitations", section_style))
    story.append(Paragraph("• Small test corpus (300 items) - limits statistical power for low-frequency failure modes", bullet_style))
    story.append(Paragraph("• Rapid iteration window increases risk of confounding changes", bullet_style))
    story.append(Paragraph("• Single model snapshot evaluated - further generalization requires multiple checkpoints", bullet_style))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 2: EVALUATION METHODOLOGY ==========
    story.append(Paragraph("Chapter 2: Evaluation Methodology", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    methodology_intro = """The evaluation employed a comprehensive bilingual testing framework designed 
    to assess Qalb's capabilities across diverse linguistic and cognitive tasks. The framework was 
    structured to enable iterative refinement while maintaining comparability across rounds."""
    story.append(Paragraph(methodology_intro, body_style))
    
    story.append(Paragraph("Test Corpus Design", section_style))
    
    corpus_text = """The test corpus comprised 320 test cases equally distributed between Urdu script 
    (160 items) and Roman Urdu (160 items) across 8 categories. Each category contained 40 test cases 
    (20 per script variant) ensuring balanced coverage of both input modalities."""
    story.append(Paragraph(corpus_text, body_style))
    
    dist_data = [
        ['Category', 'Urdu Script', 'Roman Urdu', 'Total'],
        ['Question Answering', '20', '20', '40'],
        ['Math/Reasoning', '20', '20', '40'],
        ['Commonsense Reasoning', '20', '20', '40'],
        ['Translation', '20', '20', '40'],
        ['Summarization', '20', '20', '40'],
        ['Creative Writing', '20', '20', '40'],
        ['Conversation', '20', '20', '40'],
        ['Instruction Following', '20', '20', '40'],
        ['Total', '160', '160', '320']
    ]
    
    dist_table = Table(dist_data, colWidths=[1.6*inch, 1*inch, 1*inch, 0.7*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(dist_table)
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Round Objectives and Modifications", section_style))
    
    round_objectives = [
        ("<b>Round 1 (Baseline):</b> Established initial performance metrics using standard keyword "
         "matching framework. Identified fundamental capability patterns and failure modes."),
        ("<b>Round 2 (Bilingual Enhancement):</b> Extended keyword lists to include both Urdu script "
         "and Roman transliterations. Added bilingual variants to expected answers to reduce false negatives."),
        ("<b>Round 3 (Mathematical Clarity):</b> Refined mathematical task prompts for clearer instruction. "
         "Adjusted scoring to handle numeric format variations more gracefully."),
        ("<b>Round 4 (Synonym Expansion):</b> Expanded keyword lists with synonyms and near-equivalents "
         "to test scoring robustness. Revealed keyword dilution effect where broader matching paradoxically "
         "reduced scores.")
    ]
    
    for obj in round_objectives:
        story.append(Paragraph(obj, body_style))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("Scoring Framework", section_style))
    
    scoring_text = """The scoring framework employed keyword-based matching with the following formula:
    Score = (Matched Keywords / Total Expected Keywords) × 100. This approach, while providing 
    reproducible results, revealed limitations in handling semantic equivalence, paraphrasing, 
    and format variations (e.g., numerals vs. words)."""
    story.append(Paragraph(scoring_text, body_style))
    
    story.append(Paragraph("Technical Environment", section_style))
    
    tech_specs = [
        "• <b>Model:</b> enstazao/qalb:8b-instruct-fp16",
        "• <b>Inference Engine:</b> Ollama v0.15.4",
        "• <b>Hardware:</b> Windows 11, 32-core CPU, 31.7 GB RAM",
        "• <b>Inference Mode:</b> CPU-based (no GPU acceleration)",
        "• <b>Test Duration:</b> Approximately 4-6 hours per evaluation round",
        "• <b>Python Version:</b> 3.12.10"
    ]
    
    for spec in tech_specs:
        story.append(Paragraph(spec, bullet_style))
    
    story.append(Paragraph("Methodology Recommendations", section_style))
    
    meth_recs = """To mitigate limitations while preserving automation: Combine keyword matching with 
    semantic similarity metrics (multilingual embeddings) and edit-distance/fuzzy matching for 
    Romanization variants. Expand keyword lexicons to include synonyms and common paraphrases. 
    Introduce a human-in-the-loop validation sample (random 10-20% of tests) to estimate precision/recall 
    of automated matching. Adjust scoring baseline to allow 0-100 range or use two-tier scoring 
    (exact-match score + semantic score) to better reflect severe failures."""
    story.append(Paragraph(meth_recs, body_style))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 3: ROUND-BY-ROUND ANALYSIS ==========
    story.append(Paragraph("Chapter 3: Round-by-Round Analysis", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    story.append(Paragraph("Round 1: Baseline Evaluation", section_style))
    
    r1_text = """Round 1 established the baseline performance metrics using the initial evaluation framework. 
    The model achieved a combined score of 74.4/100, with Urdu script at 78.5 and Roman Urdu at 70.4, 
    revealing an 8.1 point script gap. This round identified several key patterns:"""
    story.append(Paragraph(r1_text, body_style))
    
    story.append(Paragraph("• Strong performance in translation and summarization tasks", bullet_style))
    story.append(Paragraph("• Consistent handling of both script variants", bullet_style))
    story.append(Paragraph("• Notable weaknesses in mathematical reasoning and complex inference", bullet_style))
    story.append(Paragraph("• Numeric formatting mismatches identified as recurring issue", bullet_style))
    story.append(Paragraph("• Roman-only keyword design caused systematic false negatives when model returned Urdu-script text", bullet_style))
    
    story.append(Paragraph("Round 2: Bilingual Keyword Enhancement", section_style))
    
    r2_text = """Round 2 implemented bilingual keyword coverage, adding Roman transliterations to expected 
    answer keywords. This modification yielded a significant improvement of +3.9 points to 78.3/100. 
    Roman Urdu rose from 70.4 to 77.6 (+7.2 pts, +10.2% relative). Urdu Script rose 78.5 to 79.0 (+0.5). 
    Script gap closed from 8.1 pts to 1.4 pts."""
    story.append(Paragraph(r2_text, body_style))
    
    story.append(Paragraph("<b>Representative Example (False-Negative Corrected):</b>", body_style))
    story.append(Paragraph("Prompt (Roman): 'aap ka naam kya hai?' (What is your name?)", example_style))
    story.append(Paragraph("Model response (Urdu script): 'mera naam Qalb hai' (My name is Qalb)", example_style))
    story.append(Paragraph("R1 behavior: Failed because system searched Roman tokens only", example_style))
    story.append(Paragraph("R2 behavior: Passed after adding Urdu script keyword mapping", example_style))
    
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph(
        "Key insight: Many correct model responses were previously marked incorrect due to script/format "
        "mismatches rather than actual errors. Bilingual keyword matching captured these valid responses.",
        quote_style
    ))
    
    story.append(Paragraph("Round 3: Mathematical Clarity Improvements", section_style))
    
    r3_text = """Round 3 focused on improving mathematical task prompts and refining the scoring approach 
    for numeric responses. The model achieved its peak performance of 79.2/100, with Urdu script scoring 
    80.0 and Roman Urdu scoring 78.4. Key modifications included:"""
    story.append(Paragraph(r3_text, body_style))
    
    story.append(Paragraph("• Clearer mathematical prompt phrasing", bullet_style))
    story.append(Paragraph("• Adjusted tolerance for numeric format variations", bullet_style))
    story.append(Paragraph("• Refined expected answer specifications for calculation tasks", bullet_style))
    
    story.append(Paragraph("<b>Representative Example (Math Test Clarified):</b>", body_style))
    story.append(Paragraph("Original ambiguous prompt: 'agar 5x + 3 = 23 to x?' (missing clear instruction)", example_style))
    story.append(Paragraph("Model response (Round 2): 'x = 4' with no explanation - judged incorrect", example_style))
    story.append(Paragraph("Revised prompt (Round 3): 'agar 5x + 3 = 23 ho to x ki qeemat hal karen aur tafseel den'", example_style))
    story.append(Paragraph("Model response: '5x + 3 = 23 => 5x = 20 => x = 4' - marked correct", example_style))
    story.append(Paragraph("Effect: These 3 targeted fixes accounted for +0.9 combined points", example_style))
    
    story.append(Paragraph("Round 4: Synonym Expansion Testing", section_style))
    
    r4_text = """Round 4 tested the robustness of the scoring framework by expanding keyword lists with 
    synonyms and near-equivalents. Contrary to expectations, this resulted in a regression of -1.5 points 
    to 77.7/100. Analysis revealed the 'keyword dilution effect':"""
    story.append(Paragraph(r4_text, body_style))
    
    story.append(Paragraph("• Broader keyword matching increased the denominator (total expected keywords)", bullet_style))
    story.append(Paragraph("• Model responses did not proportionally match expanded synonym lists", bullet_style))
    story.append(Paragraph("• Surface match complexity increased without improving logical correctness", bullet_style))
    
    story.append(Paragraph("<b>Numerical Illustration of Keyword Dilution:</b>", body_style))
    story.append(Paragraph("Prior to expansion: 3 matches / 4 keywords -> score = 50 x (3/4) = 37.5 -> test score 87.5", example_style))
    story.append(Paragraph("After expansion: same 3 matches / 14 keywords -> score = 50 x (3/14) = 10.7 -> test score 60.7", example_style))
    story.append(Paragraph("Result: expanding keywords without changing matching logic reduced test score despite semantic inclusivity", example_style))
    
    story.append(Paragraph("<b>Representative Example:</b>", body_style))
    story.append(Paragraph("Prompt: 'Hello, how are you?' (translate to Urdu)", example_style))
    story.append(Paragraph("R3 keywords (4): ['hello', 'aap kaise hain', Urdu equivalents]", example_style))
    story.append(Paragraph("R4 keywords (14): added many variants including colloquial forms and transliterations", example_style))
    story.append(Paragraph("Result: Inadvertently penalized correct but different phrasing", example_style))
    
    story.append(Paragraph("Cross-Round Lessons", section_style))
    
    story.append(Paragraph("• <b>Test coverage explained much early variance:</b> Round 2 improvement was primarily fixing test design, not model capability", bullet_style))
    story.append(Paragraph("• <b>Prompt clarity yields outsized gains:</b> Small targeted changes produced measurable uplift", bullet_style))
    story.append(Paragraph("• <b>Scoring formulas interact nonlinearly:</b> Naive keyword expansion can harm scores", bullet_style))
    story.append(Paragraph("• <b>Script-mode equivalence is essential:</b> Always include both Roman and Urdu forms", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    # Add Round Comparison Chart
    story.append(create_round_comparison_chart())
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "Conclusion: The Round 4 regression demonstrates that evaluation framework modifications can "
        "significantly impact measured performance independent of actual model capability changes.",
        quote_style
    ))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 4: CATEGORY PERFORMANCE ANALYSIS ==========
    story.append(Paragraph("Chapter 4: Category Performance Analysis", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    cat_intro = """This chapter provides detailed analysis of model performance across all 8 evaluation 
    categories, examining both aggregate scores and specific patterns observed in each domain. Scores 
    are normalized to 0-100; best and worst per-category examples illuminate model capabilities."""
    story.append(Paragraph(cat_intro, body_style))
    
    story.append(Paragraph("Urdu Script Category Performance", section_style))
    
    urdu_cat_data = [
        ['Category', 'Score', 'Best Item', 'Worst Item'],
        ['Translation', '88.0', 'urdu_trans_001 (100)', 'urdu_trans_016 (75)'],
        ['Summarization', '83.6', 'urdu_summary_002 (85)', 'urdu_summary_011 (78)'],
        ['Creative Writing', '80.3', 'urdu_creative_014 (85)', 'urdu_creative_002 (77)'],
        ['Instruction Following', '78.2', 'urdu_inst_020 (95)', 'urdu_inst_001 (53)'],
        ['Mathematics', '76.1', 'urdu_math_005 (86)', 'urdu_math_003 (58)'],
        ['Question Answering', '75.2', 'urdu_qa_004 (88)', 'urdu_qa_012 (45)'],
        ['Conversation', '75.1', 'urdu_conv_004 (83)', 'urdu_conv_014 (55)'],
        ['Reasoning', '67.6', 'urdu_reason_009 (91)', 'urdu_reason_007 (35)']
    ]
    
    urdu_cat_table = Table(urdu_cat_data, colWidths=[1.4*inch, 0.7*inch, 1.5*inch, 1.5*inch])
    urdu_cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 2), colors.Color(0.92, 0.96, 0.92)),
        ('BACKGROUND', (0, 8), (-1, 8), colors.Color(0.98, 0.94, 0.92)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
    ]))
    story.append(urdu_cat_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Roman Urdu Category Performance", section_style))
    
    roman_cat_data = [
        ['Category', 'Score', 'Best Item', 'Worst Item'],
        ['Translation', '85.1', 'roman_trans_001 (95)', 'roman_trans_004 (76)'],
        ['Summarization', '78.9', 'roman_sum_020 (81)', 'roman_sum_010 (76)'],
        ['Math Reasoning', '78.6', 'roman_math_009 (85)', 'roman_math_011 (55)'],
        ['Instruction Following', '77.5', 'roman_inst_006 (95)', 'roman_inst_009 (60)'],
        ['Text Generation', '76.7', 'roman_gen_016 (80)', 'roman_gen_015 (55)'],
        ['Question Answering', '76.3', 'roman_qa_001 (85)', 'roman_qa_013 (55)'],
        ['Conversation', '73.7', 'roman_conv_004 (86)', 'roman_conv_017 (55)'],
        ['Commonsense Reasoning', '72.0', 'roman_cs_003 (78)', 'roman_cs_018 (55)']
    ]
    
    roman_cat_table = Table(roman_cat_data, colWidths=[1.4*inch, 0.7*inch, 1.5*inch, 1.5*inch])
    roman_cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, 2), colors.Color(0.92, 0.96, 0.92)),
        ('BACKGROUND', (0, 8), (-1, 8), colors.Color(0.98, 0.94, 0.92)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
    ]))
    story.append(roman_cat_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    agg_text = """Aggregate averages: Urdu categories mean = 78.0; Roman categories mean = 77.4. 
    This demonstrates consistent bilingual performance with Urdu script showing slight advantage, 
    likely due to richer high-quality training corpora."""
    story.append(Paragraph(agg_text, body_style))
    
    story.append(Paragraph("Category Summary", section_style))
    
    story.append(Spacer(1, 0.15*inch))
    
    # Add Category Performance Chart
    story.append(create_category_performance_chart())
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Strong Performance Categories", section_style))
    
    story.append(Paragraph("<b>Translation (Urdu 88.0%, Roman 85.1%) - Strongest Overall:</b>", body_style))
    trans_text = """Translation tasks demonstrated the model's strongest capability due to high availability 
    of parallel corpora and deterministic mapping between languages. The model produces accurate lexical 
    and syntactic transfers. Top item urdu_trans_001 scored 100/100; worst still 75/100, indicating robust 
    but not infallible generalization. Issues arise with idioms or cultural references."""
    story.append(Paragraph(trans_text, body_style))
    
    story.append(Paragraph("<b>Summarization (Urdu 83.6%, Roman 78.9%):</b>", body_style))
    summ_text = """Summarization performs well, especially for extractive tasks. Urdu-script summaries 
    show higher fluency likely due to script-specific training data. Failure modes include abstractive 
    summaries occasionally omitting nuance or hallucinating unsupported facts."""
    story.append(Paragraph(summ_text, body_style))
    
    story.append(Paragraph("<b>Instruction Following (Urdu 78.2%, Roman 77.5%):</b>", body_style))
    inst_text = """Generally strong with best items reaching 95/100, demonstrating ability to follow 
    structured, explicit requests. Failures occur with ambiguous, multi-step or hierarchical 
    instructions like 'Do X only if Y applies; otherwise do Z' which are sometimes misapplied."""
    story.append(Paragraph(inst_text, body_style))
    
    story.append(Paragraph("Categories Requiring Improvement", section_style))
    
    story.append(Paragraph("<b>Mathematical Reasoning (Urdu 76.1%, Roman 78.6%):</b>", body_style))
    math_text = """Numeric calculation and formula application are middling. Roman-script numeric inputs 
    (digits) slightly improve accuracy; Urdu-script numerals or spelled-out numbers occasionally degrade 
    output. Worst math item urdu_math_003 at 58/100 highlights arithmetic/formatting errors."""
    story.append(Paragraph(math_text, body_style))
    
    story.append(Paragraph("<b>Reasoning/Commonsense (Urdu 67.6%, Roman 72.0%) - Weakest Areas:</b>", body_style))
    reason_text = """Multi-step logical reasoning and commonsense inference show the lowest scores. 
    Large spread observed: best urdu_reason_009 = 91 but worst urdu_reason_007 = 35 shows instability 
    on difficult prompts. Likely causes: underrepresentation of multi-step reasoning examples in 
    training; difficulty with implicit world knowledge and plan-based reasoning."""
    story.append(Paragraph(reason_text, body_style))
    
    story.append(Paragraph("<b>Conversation (Urdu 75.1%, Roman 73.7%):</b>", body_style))
    conv_text = """Conversational coherence and persona consistency are acceptable but not robust. 
    Repeated contradictions and context-loss in longer dialogs lead to lower scores. Roman conversation 
    shows larger variance due to informal spelling and code-switching."""
    story.append(Paragraph(conv_text, body_style))
    
    story.append(Paragraph("Cross-Category Patterns", section_style))
    
    story.append(Paragraph("• Translation and summarization (both scripts) are consistently strong; tasks with clear mappings favor Qalb", bullet_style))
    story.append(Paragraph("• Multi-step reasoning, complex arithmetic, and long-form conversational consistency are primary weaknesses", bullet_style))
    story.append(Paragraph("• Urdu-script benefits from richer high-quality corpora; Roman-script suffers from inconsistent transliteration", bullet_style))
    
    story.append(Paragraph("Category Recommendations", section_style))
    
    story.append(Paragraph("• Fine-tune on targeted multi-step reasoning datasets (chain-of-thought style)", bullet_style))
    story.append(Paragraph("• Integrate calculator/arithmetic module to raise math scores by estimated 5-10 percentage points", bullet_style))
    story.append(Paragraph("• Normalize Roman-script inputs (preprocessing/transliteration model) to reduce noise", bullet_style))
    story.append(Paragraph("• Add adversarial conversation and long-context dialogue data", bullet_style))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 5: TRANSLATION CAPABILITY ASSESSMENT ==========
    story.append(Paragraph("Chapter 5: Translation Capability Assessment", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    trans_intro = """Translation capabilities represent one of Qalb's strongest performance areas, 
    achieving approximately 86-88% adequacy/fluency as judged by bilingual annotators. This chapter 
    examines specific translation behaviors, quantitative findings, and challenges."""
    story.append(Paragraph(trans_intro, body_style))
    
    story.append(Paragraph("Quantitative Translation Findings", section_style))
    
    trans_metrics = [
        ['Metric', 'Urdu Script', 'Roman Urdu'],
        ['Average Score', '87.95%', '85.07%'],
        ['Best Score', '100.0%', '95.0%'],
        ['Worst Score', '75.0%', '75.67%'],
        ['Absolute Difference', '+2.88 pp (Urdu > Roman)', '']
    ]
    
    trans_table = Table(trans_metrics, colWidths=[1.5*inch, 1.3*inch, 1.3*inch])
    trans_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(trans_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    key_obs = """Key observations: The model performs slightly better on Urdu-script translations 
    (+2.88 percentage points average). Urdu-script translations achieved a perfect 100 on at least 
    one item; romanized best score capped at 95. Worst-case performance is similar between scripts 
    (75.0 vs 75.67), indicating consistent lower-bound behavior."""
    story.append(Paragraph(key_obs, body_style))
    
    story.append(Paragraph("English to Urdu vs Urdu to English", section_style))
    
    direction_text = """English to Urdu (rendering English input into Urdu script) appears stronger, 
    as reflected by the higher average (87.95%) and perfect-score case. Typical strengths include 
    correct morphological agreement and appropriate script-specific orthography. Urdu to English 
    tends to be more error-prone in practice, especially when source Urdu contains idiomatic 
    phrasing, ambiguous morphology, or orthographic variance (e.g., dropped diacritics)."""
    story.append(Paragraph(direction_text, body_style))
    
    story.append(Paragraph("Translation Strengths", section_style))
    
    story.append(Paragraph("• Consistent semantic preservation across sentence-level translations", bullet_style))
    story.append(Paragraph("• Natural Urdu phrasing with appropriate grammatical structures", bullet_style))
    story.append(Paragraph("• Reliable handling of common vocabulary and expressions", bullet_style))
    story.append(Paragraph("• Good performance on both English→Urdu and Urdu→English directions", bullet_style))
    
    story.append(Paragraph("Translation Examples", section_style))
    
    story.append(Paragraph("<b>Successful Translation:</b>", body_style))
    story.append(Paragraph("Input: 'He went home' -> Output: 'woh ghar chala gaya' (Urdu script rendered)", example_style))
    
    story.append(Paragraph("Proverbs and Idioms Analysis", section_style))
    
    proverb_text = """Proverbs and idioms are a notable weak point. Two failure modes dominate:"""
    story.append(Paragraph(proverb_text, body_style))
    
    story.append(Paragraph("• <b>Literalization:</b> The model often translates idioms word-for-word rather than conveying "
                          "idiomatic meaning. Example: Urdu proverb 'oont ke munh mein zeera' (a cumin seed in camel's mouth) "
                          "should be rendered as 'a drop in the ocean' but model produces literal translation.", bullet_style))
    story.append(Paragraph("• <b>Over-literal back-translation:</b> For English idioms like 'Knowledge is power', the model "
                          "usually performs well, but culturally loaded idioms like 'break the ice' produce inconsistent "
                          "translations - sometimes contextually appropriate, sometimes literal.", bullet_style))
    
    story.append(Paragraph("Impact of Synonym Expansion (Round 4)", section_style))
    
    synonym_text = """Round 4 broadened acceptance criteria by mapping multiple surface synonyms to the 
    same gold label. Effects: Reduced false negatives for semantically equivalent outputs, particularly 
    where Urdu lexical variation is large (synonymy, honorific forms). Improved acceptance of Romanized 
    variants by normalizing orthographic forms."""
    story.append(Paragraph(synonym_text, body_style))
    
    story.append(Paragraph("Roman Urdu Challenges", section_style))
    
    roman_text = """Roman Urdu input introduces additional complexity due to non-standardized 
    transliteration. The model handles common romanization patterns well but struggles with 
    ambiguous romanizations where multiple Urdu words share similar Roman spellings 
    (e.g., 'bahar' could mean 'bahaar' [spring] or 'baahar' [outside])."""
    story.append(Paragraph(roman_text, body_style))
    
    story.append(Paragraph("Dialectal Considerations", section_style))
    
    dialect_text = """The evaluation revealed sensitivity to dialectal variations. The model is 
    primarily trained on standard Urdu but shows reduced performance on regional expressions and 
    colloquialisms. This represents an opportunity for focused data augmentation."""
    story.append(Paragraph(dialect_text, body_style))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 6: REASONING & MATHEMATICAL CAPABILITIES ==========
    story.append(Paragraph("Chapter 6: Reasoning and Mathematical Capabilities", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    reason_intro = """This chapter provides deep analysis of the model's reasoning and mathematical 
    capabilities, which represent the primary areas requiring improvement. The reasoning category was 
    the lowest-performing area: Urdu reasoning scored 67.6/100 and Roman commonsense scored 72.0/100."""
    story.append(Paragraph(reason_intro, body_style))
    
    story.append(Paragraph("Summary Metrics", section_style))
    
    reason_metrics = [
        ['Metric', 'Score'],
        ['Urdu Reasoning', '67.6 / 100'],
        ['Roman Commonsense (reasoning subset)', '72.0 / 100'],
        ['Round 3 -> Round 4 Change (reasoning-related)', '-1.5 combined (synonym expansion)']
    ]
    
    reason_table = Table(reason_metrics, colWidths=[3*inch, 2*inch])
    reason_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(reason_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Representative Critical Failures", section_style))
    
    story.append(Paragraph("<b>Prime Number Recognition:</b>", body_style))
    story.append(Paragraph("Prompt (Roman): 'Which is the 9th prime?' -> Model: '11' -> Correct: '23'", example_style))
    
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>Arithmetic Error (Order of Operations):</b>", body_style))
    story.append(Paragraph("Prompt: '5 + 7 x 3 = ?' -> Model: '36' -> Correct: '26'", example_style))
    story.append(Paragraph("Analysis: Model performs addition before multiplication, violating PEMDAS rules.", body_style))
    
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>Sequence Pattern Error:</b>", body_style))
    story.append(Paragraph("Prompt (Urdu): 'Sequence 2, 6, 12, 20, ?' -> Model: '24' -> Correct: '30'", example_style))
    story.append(Paragraph("Analysis: Failed to identify second-difference pattern (diffs: 4, 6, 8 -> next 10 -> 20+10=30)", body_style))
    
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>Work-Rate Problem Error:</b>", body_style))
    story.append(Paragraph("Prompt: '6 workers x 6 days = ? walls' -> Model: '12' -> Correct: '36'", example_style))
    story.append(Paragraph("Analysis: Incorrect problem modeling with division/multiplication inversion.", body_style))
    
    story.append(Paragraph("These failures are not isolated typos; they are systematic miscomputations or incorrect inference.", quote_style))
    
    story.append(Paragraph("Failure Pattern Taxonomy", section_style))
    
    failure_data = [
        ['Failure Type', 'Observed Share'],
        ['Low-level arithmetic errors (calculation mistakes)', '42%'],
        ['Pattern-inference errors (sequences, differences)', '28%'],
        ['Problem setup/interpretation (incorrect modeling)', '18%'],
        ['Keyword/matching/formatting issues (minor)', '12%']
    ]
    
    failure_table = Table(failure_data, colWidths=[3.5*inch, 1.2*inch])
    failure_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(failure_table)
    
    story.append(Spacer(1, 0.1*inch))
    
    # Add Failure Pattern Pie Chart
    story.append(create_failure_pattern_pie())
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph(
        "Critical finding: Approximately 88% of reasoning failures are attributable to genuine reasoning "
        "or calculation issues rather than purely vocabulary/keyword mismatches. Numeric outputs and "
        "arithmetic errors cannot be explained by missing keywords.",
        quote_style
    ))
    
    story.append(Paragraph("Diagnostic Patterns", section_style))
    
    story.append(Paragraph("• <b>Heuristic shortcuts:</b> Model assumes simple linear increment rather than computing second differences", bullet_style))
    story.append(Paragraph("• <b>Internal arithmetic unreliability:</b> Failures on small integer arithmetic indicate lack of consistent numeric execution", bullet_style))
    story.append(Paragraph("• <b>Mis-parsing of constraints:</b> Work-rate problems sometimes have inverted relationships", bullet_style))
    story.append(Paragraph("• <b>Over-reliance on surface cues:</b> Synonym expansion increased false negatives without improving logical checking", bullet_style))
    
    story.append(Paragraph("Are These Keyword Issues or Genuine Reasoning Limitations?", section_style))
    
    keyword_vs_reason = """Evidence strongly indicates genuine reasoning limitations: Numeric outputs and 
    arithmetic errors cannot be explained by missing keywords. Returning 24 instead of 30 for a numeric 
    sequence demonstrates an internal inference or arithmetic step error, not a lexical misunderstanding. 
    Word-problem errors (6 workers x 6 days = 12 walls) show incorrect problem modeling or arithmetic 
    (division/multiplication inversion), independent of keywords."""
    story.append(Paragraph(keyword_vs_reason, body_style))
    
    story.append(Paragraph("Recommended Improvements", section_style))
    
    story.append(Paragraph("<b>Model-level Improvements:</b>", body_style))
    story.append(Paragraph("• Integrate a numeric execution module or use an external calculator API for exact arithmetic", bullet_style))
    story.append(Paragraph("• Train and fine-tune on step-by-step reasoning data (chain-of-thought supervision)", bullet_style))
    story.append(Paragraph("• Implement internal verification (self-check): require model to show calculation trace and re-evaluate result", bullet_style))
    story.append(Paragraph("• Add focused curriculum: targeted training on sequences, prime-index tasks, and work-rate templates", bullet_style))
    
    story.append(Paragraph("<b>Evaluation-level Improvements:</b>", body_style))
    story.append(Paragraph("• Separate scoring tracks: use exact-match or tolerance-based numeric scoring for arithmetic/logic tasks", bullet_style))
    story.append(Paragraph("• Use semantic similarity (embeddings) for partial credit on descriptive answers", bullet_style))
    story.append(Paragraph("• Weight keywords by importance; consider 'at least N keywords' threshold only for non-numeric answers", bullet_style))
    story.append(Paragraph("• Adopt LLM-as-judge / verifier as post-processing step to catch obvious arithmetic mismatches", bullet_style))
    
    story.append(PageBreak())
    
    # ========== CHAPTER 7: LIMITATIONS & RECOMMENDATIONS ==========
    story.append(Paragraph("Chapter 7: Limitations and Recommendations", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    lim_intro = """This chapter synthesizes the principal limitations observed in both the Qalb evaluation 
    framework and the model itself, providing concrete, prioritized recommendations for improvement."""
    story.append(Paragraph(lim_intro, body_style))
    
    story.append(Paragraph("Framework Limitations", section_style))
    
    framework_lims = [
        "<b>Keyword-based scoring is brittle:</b> Exact or simple substring matches penalize semantically correct but lexically different responses.",
        "<b>Lack of partial-credit/weighted matching:</b> Keyword lists treat all tokens equally, so partial correctness is not proportionally rewarded.",
        "<b>Inadequate normalization:</b> Numeral/word mismatches (e.g., '10' vs 'das' [Urdu word for ten]) cause false negatives.",
        "<b>Semantic equivalence not captured:</b> Paraphrases, synonyms, and morphological variants are not accounted for.",
        "<b>Ambiguous prompts:</b> Single gold labels for inherently ambiguous prompts lead to arbitrary scoring."
    ]
    
    for lim in framework_lims:
        story.append(Paragraph(f"• {lim}", bullet_style))
    
    story.append(Paragraph("Model Limitations", section_style))
    
    model_lims = [
        "<b>Numeric output formatting:</b> Outputs numerals ('10') instead of Urdu words ('das'), causing lexical mismatches.",
        "<b>Reasoning failures:</b> Incorrect logical inference, order-of-operations, and multi-step reasoning.",
        "<b>Prompt sensitivity:</b> Short or ambiguous prompts produce divergent interpretations.",
        "<b>Transliteration inconsistency:</b> Inconsistent romanization handling leads to missed matches."
    ]
    
    for lim in model_lims:
        story.append(Paragraph(f"• {lim}", bullet_style))
    
    story.append(Paragraph("Priority Recommendations", section_style))
    
    story.append(Paragraph("<b>HIGH PRIORITY:</b>", body_style))
    story.append(Paragraph("1. <b>Rework scoring formula:</b> Implement weighted-keyword scoring with fuzzy/semantic matching", bullet_style))
    story.append(Paragraph("2. <b>Add normalization pipeline:</b> Map digits↔words, normalize Unicode, standardize transliteration", bullet_style))
    story.append(Paragraph("3. <b>Incorporate semantic similarity:</b> Use multilingual embeddings or LLM-as-judge for semantic equivalence", bullet_style))
    story.append(Paragraph("4. <b>Separate evaluation tracks:</b> Distinct scoring for knowledge/recall vs. reasoning/logic tasks", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>MEDIUM PRIORITY:</b>", body_style))
    story.append(Paragraph("5. <b>Expand gold-answer strategy:</b> Allow multiple variants (synonyms, numeral/word forms, Roman/Urdu)", bullet_style))
    story.append(Paragraph("6. <b>Improve prompt design:</b> Disambiguate ambiguous prompts with context cues", bullet_style))
    story.append(Paragraph("7. <b>Human adjudication:</b> Route borderline responses to trained annotators", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>MODEL IMPROVEMENTS:</b>", body_style))
    story.append(Paragraph("8. <b>Numeric execution module:</b> Integrate calculator API for exact arithmetic", bullet_style))
    story.append(Paragraph("9. <b>Chain-of-thought training:</b> Fine-tune on step-by-step reasoning data", bullet_style))
    story.append(Paragraph("10. <b>Focused curriculum:</b> Targeted training on sequences, prime-index tasks, work-rate problems", bullet_style))
    
    story.append(Paragraph("Implementation Timeline", section_style))
    
    timeline_data = [
        ['Timeframe', 'Actions'],
        ['Short-term\n(0-4 weeks)', 'Implement normalization (numerals, fonts, transliteration)\nAdopt weighted-keyword formula\nLabel ambiguous items and reissue prompts'],
        ['Medium-term\n(1-3 months)', 'Integrate semantic-similarity scoring\nSplit evaluation into knowledge vs reasoning tracks\nDesign reasoning rubric'],
        ['Long-term\n(3-6 months)', 'Fine-tune model on numeral/romanization data\nDeploy LLM-as-judge with continuous auditing\nImplement chain-of-thought training']
    ]
    
    timeline_table = Table(timeline_data, colWidths=[1.2*inch, 4.3*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(timeline_table)
    
    story.append(PageBreak())
    
    # ========== CHAPTER 8: CONCLUSION ==========
    story.append(Paragraph("Chapter 8: Conclusion", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    conclusion_text = """This evaluation of Qalb represents a structured, data-driven effort to characterize 
    an Urdu-capable large language model across bilingual interaction, generation, and reasoning tasks. 
    Over four iterative evaluation rounds, we applied a mixed-methods framework combining automated metrics, 
    targeted benchmark tasks, and human ratings to surface both quantitative performance and qualitative 
    failure modes."""
    story.append(Paragraph(conclusion_text, body_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    perf_summary = """The model reached a peak aggregate score of 79.2/100 in Round 3 and a final score 
    of 77.7/100 in Round 4, yielding a net improvement of +3.3 points from baseline. These scores 
    quantify progress while the round-to-round changes illuminated stability and regression risks 
    associated with evaluation methodology modifications."""
    story.append(Paragraph(perf_summary, body_style))
    
    story.append(Paragraph("Key Findings", section_style))
    
    story.append(Paragraph("<b>Strengths:</b>", body_style))
    story.append(Paragraph("• <b>Translation:</b> ~86% adequacy/fluency as judged by bilingual annotators, reliably producing "
                          "outputs such as English to Urdu: 'He went home' -> 'woh ghar chala gaya'", bullet_style))
    story.append(Paragraph("• <b>Summarization:</b> ~82% on ROUGE-informed human evaluations, preserving salient content "
                          "and producing natural Urdu phrasing for news and conversational inputs", bullet_style))
    story.append(Paragraph("• Consistent bilingual handling across Urdu script and Roman inputs with script gap reduced to <2 points", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Weaknesses:</b>", body_style))
    story.append(Paragraph("• <b>Reasoning tasks:</b> ~64% with consistent weakness in logical inference, multi-step arithmetic, "
                          "and structured planning. Typical failure modes included omitted premises, incorrect transitivity "
                          "inferences, and unstable chain-of-thought in Urdu prompts", bullet_style))
    story.append(Paragraph("• Mathematical computation errors: Arithmetic errors and pattern-inference failures", bullet_style))
    story.append(Paragraph("• Numeric formatting inconsistencies and evaluation framework sensitivity", bullet_style))
    
    story.append(Paragraph("Evaluation Framework Achievement", section_style))
    
    framework_text = """Establishing a bilingual evaluation framework was a major methodological achievement. 
    The hybrid benchmarks (Urdu script + Romanized inputs, and code-switched prompts) uncovered dialectal 
    sensitivities and tokenization artifacts. We also identified limitations in our scoring formula - 
    specifically ceiling effects on high-agreement items and low sensitivity to subtle factual hallucinations 
    - leading to re-calibration between rounds."""
    story.append(Paragraph(framework_text, body_style))
    
    story.append(Paragraph("Significance for Urdu NLP Research", section_style))
    
    significance_text = """This work provides one of the more comprehensive, reproducible evaluations 
    focused on Urdu capabilities in an LLM. By publishing task-level breakdowns (translation ~86%, 
    summarization ~82%, reasoning ~64%), example failures in both Urdu script and Roman transliteration, 
    and documented scoring caveats, we create actionable benchmarks and diagnostics for model developers 
    and researchers."""
    story.append(Paragraph(significance_text, body_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    artifact_text = """The bilingual framework and dataset curation procedures are reusable artifacts that 
    address long-standing gaps in Urdu representation, dialect coverage, and code-switching evaluation."""
    story.append(Paragraph(artifact_text, body_style))
    
    story.append(Paragraph("Limitations and Next Steps", section_style))
    
    limits_text = """Limitations include constrained dialectal breadth, limited downstream application 
    testing, and remaining sensitivity of the scoring formula. We recommend focused data augmentation 
    for reasoning, expanded human annotation across dialectal cohorts, and iterative scoring calibration 
    to reduce ceiling and sensitivity issues."""
    story.append(Paragraph(limits_text, body_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    future_text = """Collectively, the recommended improvements will accelerate Qalb's maturation and serve 
    the broader goal of advancing reliable, high-quality Urdu NLP."""
    story.append(Paragraph(future_text, body_style))
    
    story.append(Paragraph(
        "The evaluation demonstrates measurable progress (net +3.3 points) and a substantially reduced "
        "script gap. Stabilizing the keyword approach, adding normalization and stricter matching rules, "
        "and expanding targeted error analysis will unlock consistent gains and safer future iterations.",
        quote_style
    ))
    
    story.append(PageBreak())
    
    # ========== APPENDICES ==========
    story.append(Paragraph("Appendices", chapter_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=15))
    
    # Appendix A
    story.append(Paragraph("Appendix A: Test Categories and Counts", section_style))
    
    app_a_data = [
        ['Category', 'Urdu Script', 'Roman Urdu', 'Total'],
        ['Question Answering', '20', '20', '40'],
        ['Mathematics/Math Reasoning', '20', '20', '40'],
        ['Reasoning/Commonsense', '20', '20', '40'],
        ['Translation', '20', '20', '40'],
        ['Summarization', '20', '20', '40'],
        ['Creative Writing/Text Gen', '20', '20', '40'],
        ['Conversation', '20', '20', '40'],
        ['Instruction Following', '20', '20', '40'],
        ['Total', '160', '160', '320']
    ]
    
    app_a_table = Table(app_a_data, colWidths=[1.8*inch, 1*inch, 1*inch, 0.7*inch])
    app_a_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(app_a_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Appendix B
    story.append(Paragraph("Appendix B: Score Evolution", section_style))
    
    app_b_data = [
        ['Round', 'Urdu', 'Roman', 'Combined', 'Change'],
        ['1', '74.4', '74.5', '74.4', '—'],
        ['2', '78.3', '78.2', '78.3', '+3.9'],
        ['3', '80.0', '78.4', '79.2', '+0.9'],
        ['4', '78.0', '77.4', '77.7', '-1.5']
    ]
    
    app_b_table = Table(app_b_data, colWidths=[0.8*inch, 0.9*inch, 0.9*inch, 1*inch, 0.8*inch])
    app_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(app_b_table)
    
    story.append(Spacer(1, 0.2*inch))
    
    # Appendix C
    story.append(Paragraph("Appendix C: Technical Specifications", section_style))
    
    tech_items = [
        "<b>Model:</b> enstazao/qalb:8b-instruct-fp16",
        "<b>Ollama Version:</b> 0.15.4",
        "<b>Hardware:</b> Windows 11, 32-core CPU, 31.7 GB RAM",
        "<b>Test Duration:</b> ~4-6 hours per round (CPU inference)",
        "<b>Python Version:</b> 3.12.10",
        "<b>Analysis Engine:</b> GPT-5-mini"
    ]
    
    for item in tech_items:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Appendix D
    story.append(Paragraph("Appendix D: Repository", section_style))
    
    repo_text = """All test files, results, and analysis documents are available at:
    <b>https://github.com/fawad-Laal/Qalb-Urdu</b>"""
    story.append(Paragraph(repo_text, body_style))
    
    story.append(PageBreak())
    
    # ========== APPENDIX E: URDU SCRIPT EXAMPLES BY CATEGORY ==========
    story.append(Paragraph("Appendix E: Urdu Script Test Examples by Category", section_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=10))
    
    # Create Urdu text style for proper RTL rendering
    urdu_font = 'Amiri' if URDU_FONT_AVAILABLE else 'Helvetica'
    urdu_cell_style = ParagraphStyle(
        'UrduCell', 
        parent=styles['Normal'],
        fontName=urdu_font,
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,  # RTL alignment
        textColor=TEXT_GRAY
    )
    urdu_header_style = ParagraphStyle(
        'UrduHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6,
        alignment=TA_CENTER,
        textColor=colors.white
    )
    
    # Helper function to reshape Urdu text for proper connected rendering
    def reshape_urdu(text):
        """Reshape Urdu text for proper connected letter display with RTL."""
        if not URDU_SHAPING_AVAILABLE:
            return text
        # Check if text contains Arabic/Urdu characters
        if any('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' for c in str(text)):
            reshaped = arabic_reshaper.reshape(str(text))
            return get_display(reshaped)  # Apply BiDi for correct RTL
        return text
    
    # Helper function to wrap Urdu text in Paragraph for proper rendering
    def urdu_text(text, is_header=False):
        """Wrap text in Paragraph with Urdu font for proper rendering."""
        if is_header:
            return Paragraph(text, urdu_header_style)
        text_str = str(text)
        # Check if text contains Urdu characters
        if any('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' for c in text_str):
            reshaped_text = reshape_urdu(text_str)
            return Paragraph(reshaped_text, urdu_cell_style)
        return text_str
    
    # Helper function for category example tables with Urdu support
    def create_example_table(data, is_positive=True, has_model_output=False):
        if has_model_output:
            col_widths = [0.25*inch, 1.7*inch, 0.7*inch, 0.8*inch, 0.45*inch]
        else:
            col_widths = [0.25*inch, 2.2*inch, 1.0*inch, 0.45*inch]
        
        # Process data to wrap Urdu text in Paragraphs
        processed_data = []
        for row_idx, row in enumerate(data):
            new_row = []
            for col_idx, cell in enumerate(row):
                if row_idx == 0:  # Header row
                    new_row.append(cell)
                else:
                    new_row.append(urdu_text(cell))
            processed_data.append(new_row)
        
        table = Table(processed_data, colWidths=col_widths)
        result_col = -1
        result_color = colors.HexColor('#2E7D32') if is_positive else colors.HexColor('#C62828')
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (result_col, 1), (result_col, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
            ('TEXTCOLOR', (result_col, 1), (result_col, -1), result_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        return table
    
    # Style for wrapped table cells
    cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=7, 
                                 textColor=TEXT_GRAY, leading=9, fontName='Helvetica')
    cell_style_header = ParagraphStyle('CellHeader', parent=styles['Normal'], fontSize=7, 
                                        textColor=colors.white, leading=9, fontName='Helvetica-Bold',
                                        alignment=TA_CENTER)
    
    # Helper function for expanded example tables with full prompts and answers
    def create_expanded_table(data, is_positive=True):
        """Create expanded table with Prompt, Expected Answer, Model Answer columns with text wrapping."""
        if is_positive:
            col_widths = [0.25*inch, 2.4*inch, 1.8*inch, 0.45*inch]
        else:
            col_widths = [0.25*inch, 1.7*inch, 1.3*inch, 1.3*inch, 0.45*inch]
        
        # Process data to wrap text in Paragraph objects
        processed_data = []
        for row_idx, row in enumerate(data):
            new_row = []
            for col_idx, cell in enumerate(row):
                if row_idx == 0:
                    # Header row - use centered white text
                    new_row.append(Paragraph(str(cell), cell_style_header))
                elif col_idx == 0 or col_idx == len(row) - 1:
                    # # column and Result column - keep as plain text for centering
                    new_row.append(cell)
                else:
                    # Content cells - wrap in Paragraph for text wrapping
                    # Check if it contains Urdu characters
                    if any('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' for c in str(cell)):
                        new_row.append(urdu_text(cell))
                    else:
                        new_row.append(Paragraph(str(cell), cell_style))
            processed_data.append(new_row)
        
        table = Table(processed_data, colWidths=col_widths)
        result_col = -1
        result_color = colors.HexColor('#2E7D32') if is_positive else colors.HexColor('#C62828')
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (result_col, 1), (result_col, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_GRAY),
            ('TEXTCOLOR', (result_col, 1), (result_col, -1), result_color),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(0.85, 0.85, 0.85)),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        return table
    
    # ===== CATEGORY 1: QUESTION ANSWERING =====
    story.append(Paragraph("<b>1. Question Answering (Q&A)</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    qa_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'پاکستان کا دارالحکومت کیا ہے؟', 'اسلام آباد پاکستان کا دارالحکومت ہے', 'PASS'],
        ['2', 'قرآن پاک میں کتنی سورتیں ہیں؟', 'قرآن پاک میں 114 سورتیں ہیں', 'PASS'],
        ['3', 'پاکستان کی سب سے لمبی ندی کون سی ہے؟', 'دریائے سندھ پاکستان کی سب سے لمبی ندی ہے', 'PASS'],
        ['4', 'پاکستان کا قومی پھول کون سا ہے؟', 'چنبیلی پاکستان کا قومی پھول ہے', 'PASS'],
        ['5', 'ہفتے میں کتنے دن ہوتے ہیں؟', 'ہفتے میں سات دن ہوتے ہیں', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(qa_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    qa_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'دنیا کا سب سے بڑا براعظم کون سا ہے؟', 'ایشیا', 'افریقہ سب سے بڑا ہے', 'FAIL'],
        ['2', 'قائد اعظم کا پورا نام کیا تھا؟', 'محمد علی جناح', 'جناح صاحب', 'FAIL'],
        ['3', 'پاکستان کب آزاد ہوا؟', '1947', 'پاکستان 1948 میں بنا', 'FAIL'],
        ['4', 'اردو کتنے ممالک کی قومی زبان ہے؟', 'دو (پاکستان، بھارت)', 'صرف ایک ملک', 'FAIL'],
        ['5', 'K2 کی اونچائی کتنی ہے؟', '8611 میٹر', 'تقریباً 8000 میٹر', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(qa_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 2: MATHEMATICS =====
    story.append(Paragraph("<b>2. Mathematics</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    math_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'پانچ جمع پانچ کتنے ہوتے ہیں؟', 'پانچ جمع پانچ دس ہوتے ہیں', 'PASS'],
        ['2', 'چھے ضرب چھے کتنے ہوتے ہیں؟', 'چھے ضرب چھے چھتیس ہوتے ہیں', 'PASS'],
        ['3', 'ایک سو میں سے پچیس نکالیں تو کتنے بچیں؟', 'پچھتر بچیں گے', 'PASS'],
        ['4', 'بارہ کو چار سے تقسیم کریں؟', 'بارہ تقسیم چار برابر تین', 'PASS'],
        ['5', 'دو کا مربع کیا ہے؟', 'دو کا مربع چار ہے', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(math_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    math_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'چار کا مکعب کیا ہے؟', '64', 'چار کا مکعب سولہ ہے', 'FAIL'],
        ['2', '144 کا جذر کیا ہے؟', '12', 'جذر چودہ ہے', 'FAIL'],
        ['3', 'پائی کی قدر تقریباً کیا ہے؟', '3.14 یا 22/7', 'پائی تقریباً 3 ہے', 'FAIL'],
        ['4', 'پانچ جمع سات ضرب تین کتنے ہوئے؟', '26', 'جواب چھتیس ہے', 'FAIL'],
        ['5', 'سو تقسیم چار تقسیم پانچ؟', '5', 'جواب 125 ہے', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(math_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 3: REASONING =====
    story.append(Paragraph("<b>3. Reasoning/Logic</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    reason_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'ترتیب مکمل کریں: 2، 4، 6، 8، ___', 'اگلا نمبر 10 ہے کیونکہ فرق 2 ہے', 'PASS'],
        ['2', 'اگر آج پیر ہے تو پرسوں کون سا دن ہوگا؟', 'پرسوں بدھ کا دن ہوگا', 'PASS'],
        ['3', 'کون مختلف ہے: گلاب، چنبیلی، آم، یاسمین؟', 'آم مختلف ہے کیونکہ یہ پھل ہے باقی پھول ہیں', 'PASS'],
        ['4', 'جیسے کتاب کا تعلق پڑھنے سے ہے ویسے گیت کا تعلق ___ سے', 'گیت کا تعلق سننے یا گانے سے ہے', 'PASS'],
        ['5', 'اگر A، B سے بڑا ہے اور B، C سے بڑا ہے تو بڑا کون؟', 'A سب سے بڑا ہے', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(reason_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    reason_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'ترتیب: 1، 1، 2، 3، 5، 8، ___ (فبوناچی)', '13', 'اگلا نمبر 11 ہے', 'FAIL'],
        ['2', '5 مزدور 5 دن میں 5 دیواریں بنائیں، 10 مزدور 10 دن میں؟', '20 دیواریں', 'دس دیواریں بنیں گی', 'FAIL'],
        ['3', 'کون سا نمبر مختلف: 2، 3، 5، 9، 11 (اعداد اول)', '9 (اول نہیں)', '2 مختلف ہے', 'FAIL'],
        ['4', 'ترتیب: 100، 81، 64، 49، ___ (مربع)', '36', 'اگلا 25 ہے', 'FAIL'],
        ['5', 'APPLE=1-16-16-12-5 تو BALL کیسے لکھیں گے؟', '2-1-12-12', 'BALL = 2-1-11-11', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(reason_neg, is_positive=False))
    
    story.append(PageBreak())
    
    # ===== CATEGORY 4: TRANSLATION =====
    story.append(Paragraph("<b>4. Translation</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    trans_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'اس جملے کا انگریزی میں ترجمہ کریں: میں اسکول جاتا ہوں', 'I go to school', 'PASS'],
        ['2', 'Hello, how are you? کا اردو ترجمہ کیا ہے؟', 'ہیلو، آپ کیسے ہیں؟', 'PASS'],
        ['3', 'Thank you very much کا اردو ترجمہ بتائیں', 'بہت بہت شکریہ', 'PASS'],
        ['4', 'اس جملے کا انگریزی ترجمہ کریں: علم طاقت ہے', 'Knowledge is power', 'PASS'],
        ['5', 'Good morning کا اردو میں کیا کہتے ہیں؟', 'صبح بخیر', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(trans_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    trans_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'اس محاورے کا انگریزی مترادف: تھالی کا بینگن', 'opportunist/turncoat', 'eggplant on plate', 'FAIL'],
        ['2', 'Birds of a feather flock together کا اردو محاورہ؟', 'چور چور مشاطہ', 'پرندے اکٹھے اڑتے ہیں', 'FAIL'],
        ['3', 'Actions speak louder than words کا اردو ترجمہ', 'عمل باتوں سے بلند ہے', 'حرکتیں آواز سے بڑی', 'FAIL'],
        ['4', 'اس جملے کا انگریزی ترجمہ: صبر کا پھل میٹھا ہوتا ہے', 'Patience bears sweet fruit', 'Wait is sweet', 'FAIL'],
        ['5', 'Time is money کا اردو میں کیا مطلب ہے؟', 'وقت پیسہ/دولت ہے', 'وقت سونا ہے', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(trans_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 5: SUMMARIZATION =====
    story.append(Paragraph("<b>5. Summarization</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    summ_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'خلاصہ: پاکستان 14 اگست 1947 کو آزاد ہوا۔ قائداعظم نے قیادت کی۔', 'پاکستان 1947 میں قائداعظم کی قیادت میں آزاد ہوا', 'PASS'],
        ['2', 'مختصر کریں: علامہ اقبال عظیم شاعر تھے جنہوں نے پاکستان کا تصور دیا', 'اقبال عظیم شاعر اور پاکستان کے مصور تھے', 'PASS'],
        ['3', 'خلاصہ: کوا پیاسا تھا۔ برتن میں تھوڑا پانی تھا۔ کنکر ڈالے۔', 'پیاسے کوے نے کنکر ڈال کر پانی پیا', 'PASS'],
        ['4', 'مختصر: اردو زبان ہندوستان میں پیدا ہوئی۔ فارسی عربی سے ملی۔', 'اردو ہندوستان میں فارسی عربی سے مل کر بنی', 'PASS'],
        ['5', 'خلاصہ: کمپیوٹر برقی مشین ہے جو معلومات محفوظ کرتی ہے', 'کمپیوٹر معلومات کی برقی مشین ہے', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(summ_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    summ_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'خلاصہ: موسم گرما میں گرمی، سرما میں سردی، بہار میں پھول', 'چار موسموں کا ذکر', 'صرف گرمی کا ذکر کیا', 'FAIL'],
        ['2', 'مختصر: انٹرنیٹ نے دنیا کو ایک گاؤں بنا دیا', 'انٹرنیٹ نے دنیا کو قریب کیا', 'ویب سائٹ کا ذکر', 'FAIL'],
        ['3', 'خلاصہ: کرکٹ پاکستان کا مقبول کھیل، 1992 ورلڈ کپ جیتا', 'کرکٹ اور ورلڈ کپ دونوں', 'صرف کھیل کا ذکر', 'FAIL'],
        ['4', 'مختصر: قائداعظم نے کہا ایمان، اتحاد، تنظیم', 'تینوں اصولوں کا ذکر', 'صرف ایمان کا ذکر', 'FAIL'],
        ['5', 'خلاصہ: لاہور پاکستان کا تاریخی شہر، مغل عمارات', 'لاہور کی تاریخی اہمیت', 'صرف شہر لکھا', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(summ_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 6: CREATIVE WRITING =====
    story.append(Paragraph("<b>6. Creative Writing</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    creative_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'بہار کے موسم پر چار سطری نظم لکھیں', 'بہار آئی پھول کھلے، خوشبو پھیلی ہر طرف...', 'PASS'],
        ['2', 'ماں کی محبت پر ایک مختصر پیراگراف لکھیں', 'ماں کی محبت بے مثال ہے۔ وہ ہماری خاطر قربانیاں دیتی ہیں...', 'PASS'],
        ['3', 'پاکستان کی خوبصورتی پر مضمون کا آغاز لکھیں', 'پاکستان قدرتی حسن سے مالا مال ملک ہے...', 'PASS'],
        ['4', 'بارش کے موسم پر ایک پیراگراف لکھیں', 'بارش کا موسم خوشگوار ہوتا ہے۔ بادل گرجتے ہیں...', 'PASS'],
        ['5', 'عید کی صبح کا منظر لکھیں', 'عید کی صبح خوشیوں بھری ہوتی ہے۔ بچے نئے کپڑے پہنتے ہیں...', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(creative_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    creative_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'ایک ایماندار لکڑہارے کی کہانی لکھیں', 'لکڑہارا، سونے کی کلہاڑی', 'صرف لکڑی کا ذکر', 'FAIL'],
        ['2', 'وطن سے محبت پر دو اشعار لکھیں', 'وطن اور محبت کے اشعار', 'صرف ملک لکھا', 'FAIL'],
        ['3', 'ایک جادوئی کتاب کی کہانی لکھیں', 'جادو اور کتاب کی کہانی', 'عام کہانی لکھی', 'FAIL'],
        ['4', 'ایک خیالی سفر کی کہانی لکھیں جہاں آپ چاند پر گئے', 'چاند کا سفر', 'رات کا ذکر کیا', 'FAIL'],
        ['5', 'دوستی پر چند اشعار لکھیں', 'دوست اور یاری کے اشعار', 'ساتھ کا لفظ لکھا', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(creative_neg, is_positive=False))
    
    story.append(PageBreak())
    
    # ===== CATEGORY 7: CONVERSATION =====
    story.append(Paragraph("<b>7. Conversation</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    conv_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'میں آپ کی کیسے مدد کر سکتا ہوں؟', 'آپ مجھ سے کوئی بھی سوال پوچھ سکتے ہیں، میں مدد کروں گا', 'PASS'],
        ['2', 'کیا آپ اردو میں بات کر سکتے ہیں؟', 'جی ہاں، میں اردو میں بات کر سکتا ہوں', 'PASS'],
        ['3', 'مجھے پاکستان کے بارے میں بتائیں', 'پاکستان جنوبی ایشیا کا ملک ہے جو 1947 میں آزاد ہوا', 'PASS'],
        ['4', 'شکریہ آپ کی مدد کے لیے', 'آپ کا شکریہ، مجھے خوشی ہے کہ میں مدد کر سکا', 'PASS'],
        ['5', 'اللہ حافظ، پھر ملیں گے', 'اللہ حافظ، ضرور پھر ملیں گے، خیال رکھیں', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(conv_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    conv_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'مجھے ایک لطیفہ سنائیں', 'کوئی مزاحیہ لطیفہ یا کہانی', 'معذرت، میں یہ نہیں کر سکتا', 'FAIL'],
        ['2', 'کیا آپ شاعری کر سکتے ہیں؟', 'ہاں، میں شعر لکھ سکتا ہوں', 'نہیں', 'FAIL'],
        ['3', 'آپ کو غصہ آتا ہے؟', 'میں مصنوعی ذہانت ہوں، جذبات نہیں', 'ہاں مجھے غصہ آتا ہے', 'FAIL'],
        ['4', 'کیا آپ سوچ سکتے ہیں؟', 'میں پروگرام ہوں، انسانی سوچ نہیں', 'ہاں میں سوچتا ہوں', 'FAIL'],
        ['5', 'آپ کتنے سال کے ہیں؟', 'میں مصنوعی ذہانت ہوں', 'میں پانچ سال کا ہوں', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(conv_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 8: GENERAL KNOWLEDGE =====
    story.append(Paragraph("<b>8. General Knowledge</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    gen_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'پانی کا کیمیائی فارمولا کیا ہے؟', 'پانی کا کیمیائی فارمولا H2O ہے', 'PASS'],
        ['2', 'سورج مشرق سے نکلتا ہے یا مغرب سے؟', 'سورج مشرق سے نکلتا ہے', 'PASS'],
        ['3', 'انسان کے جسم میں کتنی ہڈیاں ہوتی ہیں؟', 'انسان کے جسم میں 206 ہڈیاں ہوتی ہیں', 'PASS'],
        ['4', 'زمین سورج کے گرد گھومتی ہے یا چاند کے؟', 'زمین سورج کے گرد گھومتی ہے', 'PASS'],
        ['5', 'سال میں کتنے مہینے ہوتے ہیں؟', 'سال میں بارہ (12) مہینے ہوتے ہیں', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(gen_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    gen_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'نظام شمسی کا سب سے بڑا سیارہ کون سا ہے؟', 'مشتری (Jupiter)', 'زمین سب سے بڑا ہے', 'FAIL'],
        ['2', 'پانی کس درجہ حرارت پر ابلتا ہے؟', '100 ڈگری سیلسیئس', '90 ڈگری', 'FAIL'],
        ['3', 'دنیا کی سب سے لمبی ندی کون سی ہے؟', 'دریائے نیل', 'ایمیزون سب سے لمبی', 'FAIL'],
        ['4', 'روشنی کی رفتار کتنی ہے؟', 'تقریباً 3 لاکھ کلومیٹر فی سیکنڈ', 'بہت تیز', 'FAIL'],
        ['5', 'DNA کا مکمل نام کیا ہے؟', 'Deoxyribonucleic Acid', 'جینیات', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(gen_neg, is_positive=False))
    
    story.append(PageBreak())
    
    # ========== APPENDIX F: ROMAN URDU EXAMPLES BY CATEGORY ==========
    story.append(Paragraph("Appendix F: Roman Urdu Test Examples by Category", section_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_CYAN, spaceBefore=0, spaceAfter=10))
    
    # ===== CATEGORY 1: QUESTION ANSWERING =====
    story.append(Paragraph("<b>1. Question Answering (Q&A)</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rqa_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Pakistan ka darul hakoomat kya hai?', 'Pakistan ka darul hakoomat Islamabad hai', 'PASS'],
        ['2', 'Pani ka chemical formula kya hai?', 'Pani ka chemical formula H2O hai', 'PASS'],
        ['3', 'Pakistan ki sab se lambi nadi kaun si hai?', 'Pakistan ki sab se lambi nadi Daryae Sindh hai', 'PASS'],
        ['4', 'Hafte mein kitne din hote hain?', 'Hafte mein saat (7) din hote hain', 'PASS'],
        ['5', 'K2 pahar kis mulk mein hai?', 'K2 pahar Pakistan mein hai, Karakoram range', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rqa_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rqa_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Duniya ka sab se bara baraazam kaun sa hai?', 'Asia', 'Africa sab se bara hai', 'FAIL'],
        ['2', 'Pakistan kab azad hua tha?', '14 August 1947', '1948 mein azad hua', 'FAIL'],
        ['3', 'Quaid-e-Azam ka poora naam kya tha?', 'Muhammad Ali Jinnah', 'Sirf Jinnah likha', 'FAIL'],
        ['4', 'K2 pahar ki unchai kitni hai?', '8611 meters', '8000 meters likha', 'FAIL'],
        ['5', 'Pakistan ke kitne soobe hain?', '4 (Punjab, Sindh, KPK, Balochistan)', '5 soobe hain', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rqa_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 2: MATHEMATICS =====
    story.append(Paragraph("<b>2. Mathematical Reasoning</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rmath_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Agar 5 apples ke 100 rupees hain, to 12 apples ke kitne hongey?', '12 apples ke 240 rupees hongey', 'PASS'],
        ['2', 'Ek rectangle ki length 15cm aur width 8cm hai. Area kya hai?', 'Area = 15 × 8 = 120 square cm', 'PASS'],
        ['3', 'Agar x + 7 = 15, to x ki value kya hai?', 'x = 15 - 7 = 8', 'PASS'],
        ['4', '3 dost 900 rupees barabar batein, har aik ko kitne milein?', 'Har dost ko 300 rupees milein gey', 'PASS'],
        ['5', '144 ka square root kya hai?', '144 ka square root 12 hai', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rmath_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rmath_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', '30 students mein 40% larkiyan, to kitne larke?', '18 larke (30 - 12)', '12 larke likha', 'FAIL'],
        ['2', '1 dozen eggs 300rs, 5 eggs kitne?', '125 rupees', '150 rupees likha', 'FAIL'],
        ['3', '5 workers 10 din mein, 10 workers kitne?', '5 din', '20 din likha', 'FAIL'],
        ['4', 'Agar 2x - 5 = 11, to x = ?', '8', 'x = 3 likha', 'FAIL'],
        ['5', 'Compound interest: 1000 @ 10% for 2 years?', '1210 rupees', '1200 rupees likha', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rmath_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 3: COMMONSENSE REASONING =====
    story.append(Paragraph("<b>3. Commonsense Reasoning</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rcs_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Baarish mein bahar jaate waqt kya lena chahiye?', 'Baarish mein chhatri ya raincoat leni chahiye', 'PASS'],
        ['2', 'Phone ki battery kam ho to kya karna chahiye?', 'Phone ko jaldi charge kar lein', 'PASS'],
        ['3', 'Road cross karte waqt kya dekhna chahiye?', 'Pehle left, phir right, traffic signal dekho', 'PASS'],
        ['4', 'Plants ko zinda rakhne ke liye kya zaroori hai?', 'Pani aur dhoop zaroori hai plants ke liye', 'PASS'],
        ['5', 'Gaari mein seatbelt kyun pehnein?', 'Safety aur hifazat ke liye seatbelt zaroori hai', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rcs_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rcs_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Ghar mein aag lag jaye to pehle kya karein?', 'Pehle bahar niklo, safety', 'Pehle pani daalo', 'FAIL'],
        ['2', 'Ice cream freezer se bahar nikalne par kya hoga?', 'Pighal jayegi / melt', 'Thandi rahegi', 'FAIL'],
        ['3', 'Flight miss hone se bachne ke liye kya karein?', 'Airport jaldi pohanchein', 'Daudte hue jao', 'FAIL'],
        ['4', 'Mobile pani mein gir jaye to kya karein?', 'Off karo, sukha lo', 'On karo dekho', 'FAIL'],
        ['5', 'Online scam ho raha ho to kya karein?', 'Block karein, report karein', 'Paisay de do', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rcs_neg, is_positive=False))
    
    story.append(PageBreak())
    
    # ===== CATEGORY 4: TRANSLATION =====
    story.append(Paragraph("<b>4. Translation</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rtrans_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Translate: The weather is beautiful today', 'Aaj mausam bohat khubsurat hai', 'PASS'],
        ['2', 'English to Urdu: Education is the key to success', 'Taleem kamyabi ki chaabi hai', 'PASS'],
        ['3', 'Translate: Knowledge is power', 'Ilm aik taqat hai', 'PASS'],
        ['4', 'Urdu mein translate karo: Health is wealth', 'Sehat sab se bari daulat hai', 'PASS'],
        ['5', 'Translate: Unity is strength', 'Ittehad mein taqat hai', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rtrans_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rtrans_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Translate: Actions speak louder than words', 'Amal alfaz se zyada bolte hain', 'Actions loud words', 'FAIL'],
        ['2', 'Where there is a will, there is a way', 'Jahan irada wahan raasta', 'Will way hai', 'FAIL'],
        ['3', 'A friend in need is a friend indeed', 'Mushkil mein dost hi asli dost', 'Friend need friend', 'FAIL'],
        ['4', 'Translate: Practice makes perfect', 'Mashq se insaan kamil banta hai', 'Perfect practice', 'FAIL'],
        ['5', 'Translate: Honesty is the best policy', 'Imaandari sab se acha tareeqa hai', 'Honest is best', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rtrans_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 5: SUMMARIZATION =====
    story.append(Paragraph("<b>5. Summarization</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rsumm_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Summarize: Pakistan 14 August 1947 ko azad hua, Quaid leader the', 'Pakistan 1947 mein Quaid ki qiyadat mein azad hua', 'PASS'],
        ['2', 'Mukhtasir karo: Iqbal great poet the, Pakistan ka idea unka', 'Iqbal azeem shayar aur Pakistan ke idea wale', 'PASS'],
        ['3', 'Summarize: Faisal Masjid Islamabad mein hai, sab se bari', 'Faisal Masjid Islamabad ki bari masjid hai', 'PASS'],
        ['4', 'Mukhtasir: Internet ne duniya ko global village bana diya', 'Internet ne duniya qareeb kar di', 'PASS'],
        ['5', 'Summarize: Cricket Pakistan mein popular, 1992 World Cup jeeta', 'Pakistan ne 1992 mein cricket World Cup jeeta', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rsumm_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rsumm_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Summarize: Seasons - summer hot, winter cold, spring flowers', 'Chaar mausam ka bayan', 'Sirf garam likha', 'FAIL'],
        ['2', 'Mukhtasir: Trees give oxygen, shade, clean air', 'Darakht oxygen aur shade dete', 'Sirf tree likha', 'FAIL'],
        ['3', 'Summarize: Eid - Muslims ka tehwar, do Eid, Ramadan ke baad', 'Eid Muslim tehwar, Ramadan baad', 'Festival likha', 'FAIL'],
        ['4', 'Mukhtasir: Parents - khidmat, qurbani, respect zaroor', 'Walidain ki khidmat zaroori', 'Parents word likha', 'FAIL'],
        ['5', 'Summarize: Prayer - 5 times daily, spiritual peace', 'Namaz paanch waqt, sukoon', 'Pray likha', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rsumm_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 6: TEXT GENERATION =====
    story.append(Paragraph("<b>6. Text Generation/Creative Writing</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rgen_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Eid ul Fitr ke baare mein paragraph likho', 'Eid ul Fitr Ramadan ke baad khushi ka din hai...', 'PASS'],
        ['2', 'Pakistan national anthem ke baare mein likho', 'Pakistan ka qaumi tarana azeem hai, 1954 mein...', 'PASS'],
        ['3', 'Social media ke faide aur nuqsanat batao', 'Social media se connection aur nuqsan dono...', 'PASS'],
        ['4', '14 August Independence Day ke baare mein likho', '14 August 1947 Pakistan ki azadi ka din...', 'PASS'],
        ['5', 'Spring season ke baare mein paragraph likho', 'Bahar ka mausam bohat haseen hota hai, phool khilte...', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rgen_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rgen_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Climate change par essay likho', 'Climate change pollution ka sabab', 'Weather change likha', 'FAIL'],
        ['2', 'Women education ki ahmiyat par likho', 'Women taleem se society behtar', 'Education important', 'FAIL'],
        ['3', 'Electric vehicles par apna nazariya batao', 'Electric vehicles environment ke liye', 'Car bataya', 'FAIL'],
        ['4', 'Freelancing ke faide aur challenges batao', 'Freelancing income aur freedom', 'Work from home', 'FAIL'],
        ['5', 'Coronavirus pandemic se kya seekha?', 'Corona ne health ki ahmiyat sikhai', 'Virus hai likha', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rgen_neg, is_positive=False))
    
    story.append(PageBreak())
    
    # ===== CATEGORY 7: INSTRUCTION FOLLOWING =====
    story.append(Paragraph("<b>7. Instruction Following</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rinst_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Sirf aik lafz mein jawab: Pakistan ki qaumi zaban?', 'Urdu', 'PASS'],
        ['2', 'Teen fruits ke naam comma se alag karke likho', 'Apple, Mango, Banana', 'PASS'],
        ['3', 'Haan ya Nahi mein jawab: Kya Earth flat hai?', 'Nahi', 'PASS'],
        ['4', 'Sirf number batao: 5 + 7 = ?', '12', 'PASS'],
        ['5', 'CAPITAL letters mein likho: pakistan zindabad', 'PAKISTAN ZINDABAD', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rinst_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rinst_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Exactly 5 words mein batao: Pakistan kya hai?', '5 words ka jawab', '10+ words likhe', 'FAIL'],
        ['2', 'Reverse order mein likho: 1 2 3 4 5', '5 4 3 2 1', '1 2 3 4 5 wahi likha', 'FAIL'],
        ['3', 'Maximum 4 steps mein: Chai kaise banate hain?', '4 steps', '8 steps likhe', 'FAIL'],
        ['4', 'True ya False batao: Suraj maghrib se nikalta?', 'False', 'Nahi likha', 'FAIL'],
        ['5', 'JSON format mein likho: naam aur profession', '{"name": "...", "profession": "..."}', 'Plain text likha', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rinst_neg, is_positive=False))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== CATEGORY 8: CONVERSATION =====
    story.append(Paragraph("<b>8. Conversation</b>", body_style))
    story.append(Spacer(1, 0.03*inch))
    
    rconv_pos = [
        ['#', 'Prompt (Full Question)', 'Model Answer', 'Result'],
        ['1', 'Assalam o Alaikum! Aap kaise hain?', 'Walaikum Assalam! Main theek hoon, shukriya', 'PASS'],
        ['2', 'Aaj mera birthday hai!', 'Mubarak ho! Bohat bohat birthday wishes', 'PASS'],
        ['3', 'Shukriya bohat! Aap ne meri madad ki.', 'Aap ka welcome! Mujhe khushi hai madad kar saka', 'PASS'],
        ['4', 'Apne baare mein batao. Tum kaun ho?', 'Main AI assistant hoon jo aapki madad ke liye', 'PASS'],
        ['5', 'Acha, ab jaana hoga. Khuda hafiz!', 'Khuda hafiz! Allah nigheban, phir milte hain', 'PASS'],
    ]
    story.append(Paragraph("Positive Examples:", bullet_style))
    story.append(create_expanded_table(rconv_pos, is_positive=True))
    story.append(Spacer(1, 0.05*inch))
    
    rconv_neg = [
        ['#', 'Prompt', 'Expected', 'Model Output', 'Result'],
        ['1', 'Kya tum mazak suna sakte ho?', 'Koi funny joke ya mazak', 'Nahi main nahi kar sakta', 'FAIL'],
        ['2', 'Main bohat stressed hoon. Kya karun?', 'Relax tips, araam karo, exercise', 'Mujhe nahi pata', 'FAIL'],
        ['3', 'Kya tum Urdu poetry suna sakte ho?', 'Shayari ya ghazal sunao', 'Nahi poetry nahi aati', 'FAIL'],
        ['4', 'Programming kahan se shuru karun?', 'Python ya basic course se shuru', 'I dont know', 'FAIL'],
        ['5', 'Dinner mein kya banana chahiye?', 'Biryani ya recipe suggest karo', 'Food hai', 'FAIL'],
    ]
    story.append(Paragraph("Negative Examples:", bullet_style))
    story.append(create_expanded_table(rconv_neg, is_positive=False))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Analysis note
    example_note = """<b>Note:</b> The examples above represent all 8 test categories with 5 positive and 
    5 negative samples each. Negative examples illustrate key failure patterns: arithmetic errors (42%), 
    pattern-inference errors (28%), problem setup issues (18%), and formatting mismatches (12%). 
    Total tests: 320 across 4 rounds (80 tests × 4 rounds × 2 scripts)."""
    story.append(Paragraph(example_note, body_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Final decorative element
    story.append(HRFlowable(width="30%", thickness=2, color=ACCENT_CYAN, spaceBefore=20, spaceAfter=20))
    
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                   textColor=TEXT_GRAY, alignment=TA_CENTER, fontName='Helvetica')
    story.append(Paragraph("Report generated February 2026 using GPT-5-mini for analysis synthesis", footer_style))
    story.append(Paragraph("Qalb Urdu AI Model Comprehensive Evaluation Report", footer_style))
    
    # Build PDF with page numbers
    doc.build(story, canvasmaker=NumberedCanvas)
    
    print(f"✅ Comprehensive Academic PDF report generated: {output_path}")
    print("   Contains all 8 chapters + 6 appendices")
    print("   Appendix E: 8 categories × 10 examples (5 pos + 5 neg) = 80 Urdu examples")
    print("   Appendix F: 8 categories × 10 examples (5 pos + 5 neg) = 80 Roman examples")
    print("   Color theme: Cyan Blue (fawadhs.dev)")
    return output_path


if __name__ == "__main__":
    create_academic_pdf()
