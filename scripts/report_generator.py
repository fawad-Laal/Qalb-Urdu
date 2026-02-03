"""
QALB Testing Report Generator
=============================

Generates professional, minimalist PDF reports for Qalb LLM testing results.
Branding: fawadhs.dev (cyan blue)

Requirements:
    pip install reportlab pandas
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import os


# ============================================================
# BRAND COLORS
# ============================================================

BRAND_CYAN = colors.HexColor("#06B6D4")  # Cyan 500
BRAND_DARK = colors.HexColor("#0E7490")  # Cyan 700
BRAND_LIGHT = colors.HexColor("#ECFEFF")  # Cyan 50
TEXT_PRIMARY = colors.HexColor("#1F2937")  # Gray 800
TEXT_SECONDARY = colors.HexColor("#6B7280")  # Gray 500
BORDER_COLOR = colors.HexColor("#E5E7EB")  # Gray 200
SUCCESS_COLOR = colors.HexColor("#10B981")  # Green 500
WARNING_COLOR = colors.HexColor("#F59E0B")  # Amber 500
ERROR_COLOR = colors.HexColor("#EF4444")  # Red 500


# ============================================================
# CUSTOM PAGE TEMPLATE WITH BRANDING
# ============================================================

class BrandedDocTemplate(SimpleDocTemplate):
    """Custom document template with fawadhs.dev branding."""
    
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.page_count = 0
    
    def afterPage(self):
        """Called after each page is created."""
        self.page_count += 1


def add_branding(canvas_obj, doc):
    """Add fawadhs.dev branding to each page."""
    canvas_obj.saveState()
    
    # Page dimensions
    width, height = A4
    
    # Bottom right corner branding
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(BRAND_CYAN)
    canvas_obj.drawRightString(width - 20*mm, 15*mm, "fawadhs.dev")
    
    # Page number - bottom center
    canvas_obj.setFillColor(TEXT_SECONDARY)
    canvas_obj.setFont("Helvetica", 8)
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawCentredString(width/2, 15*mm, f"{page_num}")
    
    # Top line accent
    canvas_obj.setStrokeColor(BRAND_CYAN)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(20*mm, height - 15*mm, width - 20*mm, height - 15*mm)
    
    canvas_obj.restoreState()


def add_cover_branding(canvas_obj, doc):
    """Special branding for cover page."""
    canvas_obj.saveState()
    width, height = A4
    
    # Bottom right corner branding
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(BRAND_CYAN)
    canvas_obj.drawRightString(width - 20*mm, 20*mm, "fawadhs.dev")
    
    canvas_obj.restoreState()


# ============================================================
# STYLES
# ============================================================

def get_custom_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()
    
    # Title - Large, bold
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=TEXT_PRIMARY,
        spaceAfter=6*mm,
        spaceBefore=0,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT,
    ))
    
    # Subtitle
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_SECONDARY,
        spaceAfter=20*mm,
        fontName='Helvetica',
        alignment=TA_LEFT,
    ))
    
    # Section Header
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=TEXT_PRIMARY,
        spaceBefore=12*mm,
        spaceAfter=6*mm,
        fontName='Helvetica-Bold',
        borderPadding=0,
    ))
    
    # Subsection Header
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=BRAND_DARK,
        spaceBefore=8*mm,
        spaceAfter=4*mm,
        fontName='Helvetica-Bold',
    ))
    
    # Body Text
    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=TEXT_PRIMARY,
        spaceAfter=4*mm,
        fontName='Helvetica',
        alignment=TA_JUSTIFY,
        leading=14,
    ))
    
    # Metric Value - Large number
    styles.add(ParagraphStyle(
        name='MetricValue',
        parent=styles['Normal'],
        fontSize=32,
        textColor=BRAND_CYAN,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
    ))
    
    # Metric Label
    styles.add(ParagraphStyle(
        name='MetricLabel',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_SECONDARY,
        fontName='Helvetica',
        alignment=TA_CENTER,
        spaceAfter=2*mm,
    ))
    
    # Code/Mono
    styles.add(ParagraphStyle(
        name='Code',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_PRIMARY,
        fontName='Courier',
        backColor=colors.HexColor("#F3F4F6"),
        borderPadding=8,
        spaceAfter=4*mm,
    ))
    
    # Caption
    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles['Normal'],
        fontSize=8,
        textColor=TEXT_SECONDARY,
        fontName='Helvetica-Oblique',
        alignment=TA_CENTER,
        spaceAfter=6*mm,
    ))
    
    return styles


# ============================================================
# TABLE STYLES
# ============================================================

def get_table_style():
    """Minimalist table style."""
    return TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), TEXT_PRIMARY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRIMARY),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        
        # Grid
        ('LINEBELOW', (0, 0), (-1, 0), 1, BRAND_CYAN),
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, BORDER_COLOR),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])


def get_metric_table_style():
    """Style for metric cards."""
    return TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
    ])


# ============================================================
# REPORT GENERATOR CLASS
# ============================================================

class QalbReportGenerator:
    """Generates professional PDF reports for Qalb testing."""
    
    def __init__(self, output_path: str = "reports"):
        self.output_path = output_path
        self.styles = get_custom_styles()
        os.makedirs(output_path, exist_ok=True)
    
    def generate_report(
        self,
        results: Dict[str, Any],
        filename: str = None,
    ) -> str:
        """
        Generate a complete PDF report.
        
        Args:
            results: Dictionary containing test results
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to generated PDF
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qalb_report_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_path, filename)
        
        doc = BrandedDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=25*mm,
            bottomMargin=25*mm,
        )
        
        # Build story (content)
        story = []
        
        # Cover Page
        story.extend(self._build_cover_page(results))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._build_executive_summary(results))
        story.append(PageBreak())
        
        # Key Metrics
        story.extend(self._build_key_metrics(results))
        
        # Benchmark Results
        story.extend(self._build_benchmark_results(results))
        story.append(PageBreak())
        
        # Script Comparison (if available)
        if 'script_comparison' in results:
            story.extend(self._build_script_comparison(results))
        
        # Recommendations
        story.extend(self._build_recommendations(results))
        
        # Appendix
        story.extend(self._build_appendix(results))
        
        # Build PDF
        doc.build(story, onFirstPage=add_cover_branding, onLaterPages=add_branding)
        
        return filepath
    
    def _build_cover_page(self, results: Dict) -> List:
        """Build the cover page."""
        elements = []
        
        # Spacer to center content
        elements.append(Spacer(1, 60*mm))
        
        # Title
        elements.append(Paragraph(
            "QALB Testing Report",
            self.styles['CustomTitle']
        ))
        
        # Subtitle
        subtitle = results.get('title', 'Urdu Large Language Model Evaluation')
        elements.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
        
        # Horizontal line
        elements.append(HRFlowable(
            width="40%",
            thickness=2,
            color=BRAND_CYAN,
            spaceBefore=10*mm,
            spaceAfter=20*mm,
        ))
        
        # Meta info
        meta_data = [
            ["Model", results.get('model_name', 'Qalb-1.0-8B-Instruct')],
            ["Date", datetime.now().strftime("%B %d, %Y")],
            ["Version", results.get('version', '1.0')],
            ["Author", results.get('author', 'Fawad Hussain')],
        ]
        
        meta_table = Table(meta_data, colWidths=[30*mm, 80*mm])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), TEXT_SECONDARY),
            ('TEXTCOLOR', (1, 0), (1, -1), TEXT_PRIMARY),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(meta_table)
        
        return elements
    
    def _build_executive_summary(self, results: Dict) -> List:
        """Build executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        summary = results.get('summary', {})
        
        # Overall score highlight
        overall_score = summary.get('overall_score', 'N/A')
        elements.append(Paragraph(
            f"Overall Performance Score: <font color='#06B6D4'><b>{overall_score}</b></font>",
            self.styles['BodyText']
        ))
        
        # Key findings
        elements.append(Paragraph("Key Findings", self.styles['SubsectionHeader']))
        
        findings = summary.get('key_findings', [
            "Qalb demonstrates state-of-the-art performance on Urdu NLP tasks.",
            "Strong performance in Classification (96.38) and Sentiment Analysis (95.79).",
            "Roman Urdu support requires additional testing and optimization.",
            "Model runs efficiently on CPU via Ollama for evaluation purposes.",
        ])
        
        for finding in findings:
            elements.append(Paragraph(f"• {finding}", self.styles['BodyText']))
        
        return elements
    
    def _build_key_metrics(self, results: Dict) -> List:
        """Build key metrics dashboard."""
        elements = []
        
        elements.append(Paragraph("Key Metrics", self.styles['SectionHeader']))
        
        metrics = results.get('metrics', {
            'overall_score': '90.34',
            'tests_passed': '127/140',
            'urdu_purity': '95.31%',
            'avg_response_time': '45s',
        })
        
        # Create metric cards
        metric_cards = []
        for label, value in metrics.items():
            card_content = [
                [Paragraph(str(value), self.styles['MetricValue'])],
                [Paragraph(label.replace('_', ' ').title(), self.styles['MetricLabel'])],
            ]
            metric_cards.append(Table(card_content, colWidths=[40*mm]))
        
        # Arrange in a row
        if metric_cards:
            metrics_row = Table([metric_cards], colWidths=[42*mm] * len(metric_cards))
            metrics_row.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(metrics_row)
            elements.append(Spacer(1, 10*mm))
        
        return elements
    
    def _build_benchmark_results(self, results: Dict) -> List:
        """Build benchmark results table."""
        elements = []
        
        elements.append(Paragraph("Benchmark Results", self.styles['SectionHeader']))
        
        # Default benchmark data
        benchmarks = results.get('benchmarks', [
            {'task': 'Classification', 'score': 96.38, 'target': 95, 'status': 'Pass'},
            {'task': 'Sentiment Analysis', 'score': 95.79, 'target': 95, 'status': 'Pass'},
            {'task': 'Translation', 'score': 94.41, 'target': 90, 'status': 'Pass'},
            {'task': 'Ethics', 'score': 90.83, 'target': 85, 'status': 'Pass'},
            {'task': 'Reasoning', 'score': 88.59, 'target': 85, 'status': 'Pass'},
            {'task': 'Generation', 'score': 85.97, 'target': 85, 'status': 'Pass'},
            {'task': 'QA', 'score': 80.40, 'target': 75, 'status': 'Pass'},
        ])
        
        # Build table
        table_data = [['Task', 'Score', 'Target', 'Status']]
        for b in benchmarks:
            status_color = SUCCESS_COLOR if b['status'] == 'Pass' else ERROR_COLOR
            table_data.append([
                b['task'],
                f"{b['score']:.2f}" if isinstance(b['score'], float) else str(b['score']),
                str(b['target']),
                b['status'],
            ])
        
        table = Table(table_data, colWidths=[50*mm, 35*mm, 35*mm, 30*mm])
        table.setStyle(get_table_style())
        elements.append(table)
        elements.append(Spacer(1, 6*mm))
        elements.append(Paragraph(
            "Table 1: Benchmark results across 7 evaluation tasks",
            self.styles['Caption']
        ))
        
        return elements
    
    def _build_script_comparison(self, results: Dict) -> List:
        """Build Urdu vs Roman Urdu comparison."""
        elements = []
        
        elements.append(Paragraph("Script Comparison", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "Performance comparison between Urdu Nastaliq script and Roman Urdu (Romanized Urdu).",
            self.styles['BodyText']
        ))
        
        comparison = results.get('script_comparison', [
            {'task': 'QA', 'urdu': 80.40, 'roman': 72.50},
            {'task': 'Translation', 'urdu': 94.41, 'roman': 85.20},
            {'task': 'Sentiment', 'urdu': 95.79, 'roman': 88.30},
            {'task': 'Reasoning', 'urdu': 88.59, 'roman': 75.40},
        ])
        
        table_data = [['Task', 'Urdu Script', 'Roman Urdu', 'Difference']]
        for c in comparison:
            diff = c['urdu'] - c['roman']
            table_data.append([
                c['task'],
                f"{c['urdu']:.2f}",
                f"{c['roman']:.2f}",
                f"{diff:+.2f}",
            ])
        
        table = Table(table_data, colWidths=[40*mm, 35*mm, 35*mm, 35*mm])
        table.setStyle(get_table_style())
        elements.append(table)
        elements.append(Spacer(1, 6*mm))
        elements.append(Paragraph(
            "Table 2: Urdu script vs Roman Urdu performance comparison",
            self.styles['Caption']
        ))
        
        return elements
    
    def _build_recommendations(self, results: Dict) -> List:
        """Build recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        
        recommendations = results.get('recommendations', [
            {
                'title': 'Use Urdu Script for Critical Tasks',
                'description': 'For maximum accuracy, especially in formal applications, use Urdu Nastaliq script inputs.',
            },
            {
                'title': 'Implement Few-Shot Prompting',
                'description': 'Provide 2-3 examples before complex queries to improve response quality.',
            },
            {
                'title': 'Monitor Response Consistency',
                'description': 'Run multiple iterations for critical decisions to ensure consistent outputs.',
            },
            {
                'title': 'Consider Quantized Models for Production',
                'description': 'Use Q4 quantization for faster inference in production environments.',
            },
        ])
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(
                f"{i}. {rec['title']}",
                self.styles['SubsectionHeader']
            ))
            elements.append(Paragraph(rec['description'], self.styles['BodyText']))
        
        return elements
    
    def _build_appendix(self, results: Dict) -> List:
        """Build appendix with technical details."""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("Appendix", self.styles['SectionHeader']))
        
        # Model Configuration
        elements.append(Paragraph("A. Model Configuration", self.styles['SubsectionHeader']))
        
        config = results.get('config', {
            'model': 'enstazao/qalb:8b-instruct-fp16',
            'parameters': '8 Billion',
            'quantization': 'FP16',
            'context_length': '2048 tokens',
            'inference': 'Ollama (CPU)',
        })
        
        config_data = [[k.replace('_', ' ').title(), str(v)] for k, v in config.items()]
        config_table = Table(config_data, colWidths=[50*mm, 100*mm])
        config_table.setStyle(get_table_style())
        elements.append(config_table)
        
        # Test Environment
        elements.append(Paragraph("B. Test Environment", self.styles['SubsectionHeader']))
        
        env = results.get('environment', {
            'os': 'Windows 11',
            'ram': '32 GB',
            'python': '3.11',
            'ollama': 'Latest',
        })
        
        env_data = [[k.upper(), str(v)] for k, v in env.items()]
        env_table = Table(env_data, colWidths=[50*mm, 100*mm])
        env_table.setStyle(get_table_style())
        elements.append(env_table)
        
        # Citation
        elements.append(Paragraph("C. Citation", self.styles['SubsectionHeader']))
        elements.append(Paragraph(
            """Hassan, M.T., Ahmed, J., & Awais, M. (2026). Qalb: Largest State-of-the-Art 
            Urdu Large Language Model for 230M Speakers with Systematic Continued Pre-training. 
            arXiv preprint arXiv:2601.08141.""",
            self.styles['BodyText']
        ))
        
        return elements


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def generate_sample_report(output_path: str = "reports") -> str:
    """Generate a sample report with mock data."""
    
    sample_results = {
        'title': 'Urdu Large Language Model Evaluation',
        'model_name': 'Qalb-1.0-8B-Instruct',
        'version': '1.0',
        'author': 'Fawad Hussain',
        'summary': {
            'overall_score': '90.34',
            'key_findings': [
                "Qalb achieves state-of-the-art performance with 90.34 overall score.",
                "Outperforms previous best model (Alif-1.0) by 3.24 points.",
                "Strong performance in Classification (96.38) and Sentiment Analysis (95.79).",
                "Roman Urdu performance averages 8-12 points lower than Nastaliq script.",
                "Model runs efficiently on CPU via Ollama (~45s per response).",
            ],
        },
        'metrics': {
            'overall_score': '90.34',
            'tests_passed': '127/140',
            'urdu_purity': '95.31%',
            'avg_response': '45s',
        },
        'benchmarks': [
            {'task': 'Classification', 'score': 96.38, 'target': 95, 'status': 'Pass'},
            {'task': 'Sentiment Analysis', 'score': 95.79, 'target': 95, 'status': 'Pass'},
            {'task': 'Translation', 'score': 94.41, 'target': 90, 'status': 'Pass'},
            {'task': 'Ethics', 'score': 90.83, 'target': 85, 'status': 'Pass'},
            {'task': 'Reasoning', 'score': 88.59, 'target': 85, 'status': 'Pass'},
            {'task': 'Generation', 'score': 85.97, 'target': 85, 'status': 'Pass'},
            {'task': 'QA', 'score': 80.40, 'target': 75, 'status': 'Pass'},
        ],
        'script_comparison': [
            {'task': 'QA', 'urdu': 80.40, 'roman': 72.50},
            {'task': 'Translation', 'urdu': 94.41, 'roman': 85.20},
            {'task': 'Sentiment', 'urdu': 95.79, 'roman': 88.30},
            {'task': 'Reasoning', 'urdu': 88.59, 'roman': 75.40},
            {'task': 'Classification', 'urdu': 96.38, 'roman': 89.10},
        ],
        'recommendations': [
            {
                'title': 'Use Urdu Script for Critical Tasks',
                'description': 'For maximum accuracy in formal applications like document processing, legal, or medical contexts, always use Urdu Nastaliq script inputs. The model shows 8-12% higher accuracy with native script.',
            },
            {
                'title': 'Implement Few-Shot Prompting for Roman Urdu',
                'description': 'When Roman Urdu input is unavoidable (e.g., social media analysis), provide 2-3 examples to improve model understanding of spelling variations.',
            },
            {
                'title': 'Chain-of-Thought for Reasoning Tasks',
                'description': 'Use "قدم بہ قدم سوچیں" (think step by step) prompting for mathematical and logical reasoning tasks to improve accuracy.',
            },
            {
                'title': 'Monitor and Log Responses',
                'description': 'Implement response logging to track model behavior over time and identify edge cases requiring attention.',
            },
        ],
        'config': {
            'model': 'enstazao/qalb:8b-instruct-fp16',
            'parameters': '8 Billion',
            'quantization': 'FP16 (16GB)',
            'context_length': '2048 tokens',
            'inference': 'Ollama (CPU)',
            'temperature': '0.1',
            'top_p': '0.9',
        },
        'environment': {
            'os': 'Windows 11',
            'ram': '32 GB',
            'python': '3.11',
            'ollama': 'Latest',
            'test_date': datetime.now().strftime("%Y-%m-%d"),
        },
    }
    
    generator = QalbReportGenerator(output_path)
    return generator.generate_report(sample_results)


def generate_report_from_json(json_path: str, output_path: str = "reports") -> str:
    """Generate report from JSON results file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    generator = QalbReportGenerator(output_path)
    return generator.generate_report(results)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🇵🇰 QALB Testing Report Generator")
    print("   fawadhs.dev")
    print("=" * 60)
    print()
    
    # Generate sample report
    print("📄 Generating sample report...")
    filepath = generate_sample_report()
    print(f"✅ Report generated: {filepath}")
    print()
    print("To generate from actual test results:")
    print("   from report_generator import generate_report_from_json")
    print("   generate_report_from_json('results/test_results.json')")
