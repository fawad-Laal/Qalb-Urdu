"""
QALB Evaluation - Professional PDF Report Generator
====================================================

Generates a minimalist, professional PDF report with fawadhs.dev branding.
Cyan blue (#00BCD4) branding in bottom-right corner.

Author: Fawad Hussain (fawadhs.dev)
"""

import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas


# Brand Colors
CYAN_BLUE = colors.HexColor("#00BCD4")
DARK_GRAY = colors.HexColor("#333333")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
WHITE = colors.white


class QalbReportGenerator:
    """Generate professional PDF reports for Qalb LLM evaluation."""
    
    def __init__(self, data_path: str = "data/final_report.json"):
        self.data_path = data_path
        self.data = self._load_data()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _load_data(self) -> dict:
        """Load evaluation data from JSON."""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_placeholder_data()
    
    def _get_placeholder_data(self) -> dict:
        """Placeholder data for report structure."""
        return {
            "report_date": datetime.now().strftime("%B %d, %Y"),
            "model_name": "Qalb-1.0-8B-Instruct",
            "model_version": "enstazao/qalb:8b-instruct-fp16",
            "total_tests": 0,
            "summary": {
                "overall_accuracy": 0.0,
                "urdu_script_accuracy": 0.0,
                "roman_urdu_accuracy": 0.0,
                "avg_response_time": 0.0,
                "urdu_purity": 0.0
            },
            "categories": {},
            "recommendations": []
        }
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=DARK_GRAY,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.gray,
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=CYAN_BLUE,
            spaceBefore=20,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='ReportBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=DARK_GRAY,
            spaceAfter=8,
            leading=14
        ))
        
        # Metric value
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=CYAN_BLUE,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Metric label
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.gray,
            alignment=TA_CENTER
        ))
    
    def _add_branding(self, canvas, doc):
        """Add fawadhs.dev branding to every page."""
        canvas.saveState()
        
        # Bottom-right corner branding
        canvas.setFillColor(CYAN_BLUE)
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(
            A4[0] - 20*mm,  # Right margin
            15*mm,          # Bottom margin
            "fawadhs.dev"
        )
        
        # Page number
        canvas.setFillColor(colors.gray)
        canvas.setFont('Helvetica', 8)
        page_num = canvas.getPageNumber()
        canvas.drawCentredString(A4[0]/2, 15*mm, f"Page {page_num}")
        
        # Top line
        canvas.setStrokeColor(LIGHT_GRAY)
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
        
        canvas.restoreState()
    
    def _create_cover_page(self) -> list:
        """Create the cover page elements."""
        elements = []
        
        # Spacer for vertical centering
        elements.append(Spacer(1, 2*inch))
        
        # Main title
        elements.append(Paragraph(
            "QALB LLM",
            self.styles['ReportTitle']
        ))
        
        elements.append(Paragraph(
            "Evaluation Report",
            self.styles['ReportSubtitle']
        ))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        elements.append(Paragraph(
            "Comprehensive Testing of Urdu Large Language Model",
            self.styles['ReportSubtitle']
        ))
        
        elements.append(Paragraph(
            "Urdu Script (اردو) & Roman Urdu Analysis",
            self.styles['ReportSubtitle']
        ))
        
        elements.append(Spacer(1, 1*inch))
        
        # Report info table
        info_data = [
            ["Report Date:", self.data.get("report_date", datetime.now().strftime("%B %d, %Y"))],
            ["Model:", self.data.get("model_name", "Qalb-1.0-8B-Instruct")],
            ["Version:", self.data.get("model_version", "8b-instruct-fp16")],
            ["Total Tests:", str(self.data.get("total_tests", "N/A"))],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.gray),
            ('TEXTCOLOR', (1, 0), (1, -1), DARK_GRAY),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        
        elements.append(PageBreak())
        return elements
    
    def _create_executive_summary(self) -> list:
        """Create executive summary section."""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
        elements.append(Spacer(1, 0.2*inch))
        
        summary = self.data.get("summary", {})
        
        # Key metrics boxes
        metrics = [
            ("Overall\nAccuracy", f"{summary.get('overall_accuracy', 0):.1f}%"),
            ("Urdu Script\nAccuracy", f"{summary.get('urdu_script_accuracy', 0):.1f}%"),
            ("Roman Urdu\nAccuracy", f"{summary.get('roman_urdu_accuracy', 0):.1f}%"),
            ("Urdu\nPurity", f"{summary.get('urdu_purity', 0):.1f}%"),
        ]
        
        metric_cells = []
        for label, value in metrics:
            cell_content = [
                Paragraph(value, self.styles['MetricValue']),
                Paragraph(label, self.styles['MetricLabel'])
            ]
            metric_cells.append(cell_content)
        
        metrics_table = Table([metric_cells], colWidths=[1.5*inch]*4)
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
            ('BOX', (0, 0), (-1, -1), 1, CYAN_BLUE),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, WHITE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(metrics_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary text
        elements.append(Paragraph(
            f"This report presents a comprehensive evaluation of the <b>Qalb-1.0-8B-Instruct</b> "
            f"Urdu Large Language Model across {self.data.get('total_tests', 'multiple')} test cases. "
            f"Testing covered both <b>Urdu Script (اردو)</b> and <b>Roman Urdu</b> inputs "
            f"across 7 benchmark categories.",
            self.styles['BodyText']
        ))
        
        elements.append(PageBreak())
        return elements
    
    def _create_results_section(self) -> list:
        """Create detailed results section."""
        elements = []
        
        elements.append(Paragraph("Detailed Results", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
        elements.append(Spacer(1, 0.2*inch))
        
        # Results by category
        categories = self.data.get("categories", {})
        
        if categories:
            # Create results table
            table_data = [["Category", "Urdu Script", "Roman Urdu", "Overall"]]
            
            for cat_name, cat_data in categories.items():
                table_data.append([
                    cat_name.replace("_", " ").title(),
                    f"{cat_data.get('urdu_accuracy', 0):.1f}%",
                    f"{cat_data.get('roman_accuracy', 0):.1f}%",
                    f"{cat_data.get('overall', 0):.1f}%"
                ])
            
            results_table = Table(table_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            results_table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), CYAN_BLUE),
                ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                # Body
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                # Alternating rows
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(results_table)
        else:
            elements.append(Paragraph(
                "<i>No test data available yet. Run tests to generate results.</i>",
                self.styles['BodyText']
            ))
        
        elements.append(PageBreak())
        return elements
    
    def _create_recommendations_section(self) -> list:
        """Create recommendations section."""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
        elements.append(Spacer(1, 0.2*inch))
        
        recommendations = self.data.get("recommendations", [
            "Use Qalb for formal Urdu text generation tasks",
            "Consider preprocessing Roman Urdu inputs for better accuracy",
            "Implement few-shot prompting for complex reasoning tasks",
            "Monitor Urdu purity in production deployments",
            "Use appropriate system prompts for specific use cases"
        ])
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(
                f"<b>{i}.</b> {rec}",
                self.styles['BodyText']
            ))
        
        return elements
    
    def generate(self, output_path: str = "reports/qalb_evaluation_report.pdf"):
        """Generate the complete PDF report."""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=25*mm,
            bottomMargin=25*mm
        )
        
        # Build content
        elements = []
        elements.extend(self._create_cover_page())
        elements.extend(self._create_executive_summary())
        elements.extend(self._create_results_section())
        elements.extend(self._create_recommendations_section())
        
        # Build PDF with branding
        doc.build(elements, onFirstPage=self._add_branding, onLaterPages=self._add_branding)
        
        print(f"✅ Report generated: {output_path}")
        return output_path


def main():
    """Generate the PDF report."""
    generator = QalbReportGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
