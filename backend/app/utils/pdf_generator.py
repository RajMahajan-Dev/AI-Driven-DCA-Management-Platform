"""
PDF Report Generation Utilities
Generates comprehensive PDF reports for cases
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
from typing import List
from sqlalchemy.orm import Session

from app.models import Case, DCA


def generate_case_report_pdf(case: Case, db: Session) -> BytesIO:
    """
    Generate a detailed PDF report for a single case.
    
    Args:
        case: Case instance
        db: Database session
        
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#334155'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"Case Report: {case.case_id}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Generated date
    date_text = Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    )
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Case Information Section
    elements.append(Paragraph("Case Information", heading_style))
    case_data = [
        ['Case ID:', case.case_id],
        ['Status:', case.status.value],
        ['Priority:', case.priority.value],
        ['SLA Status:', case.sla_status.value],
        ['Created Date:', case.created_at.strftime('%Y-%m-%d') if case.created_at else 'N/A'],
        ['Assigned Date:', case.assigned_at.strftime('%Y-%m-%d') if case.assigned_at else 'N/A'],
        ['Completed Date:', case.completed_at.strftime('%Y-%m-%d') if case.completed_at else 'N/A'],
    ]
    
    case_table = Table(case_data, colWidths=[2*inch, 4*inch])
    case_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(case_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Customer Information
    elements.append(Paragraph("Customer Information", heading_style))
    customer_data = [
        ['Name:', case.customer_name],
        ['Email:', case.customer_email or 'N/A'],
        ['Phone:', case.customer_phone or 'N/A'],
        ['Address:', case.customer_address or 'N/A'],
    ]
    
    customer_table = Table(customer_data, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Financial Information
    elements.append(Paragraph("Financial Information", heading_style))
    financial_data = [
        ['Overdue Amount:', f"${case.overdue_amount:,.2f}"],
        ['Ageing Days:', str(case.ageing_days)],
        ['SLA Due Date:', case.sla_due_date.strftime('%Y-%m-%d') if case.sla_due_date else 'N/A'],
        ['AI Recovery Score:', f"{case.ai_recovery_score:.2%}" if case.ai_recovery_score else 'N/A'],
    ]
    
    financial_table = Table(financial_data, colWidths=[2*inch, 4*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(financial_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # DCA Information (if assigned)
    if case.dca:
        elements.append(Paragraph("Assigned DCA", heading_style))
        dca_data = [
            ['DCA Name:', case.dca.name],
            ['Contact Person:', case.dca.contact_person or 'N/A'],
            ['Email:', case.dca.email or 'N/A'],
            ['Phone:', case.dca.phone or 'N/A'],
            ['Performance Score:', case.dca.performance_score],
            ['Allocation Reason:', case.allocation_reason or 'N/A'],
        ]
        
        dca_table = Table(dca_data, colWidths=[2*inch, 4*inch])
        dca_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(dca_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Social Media Links
    if case.customer_social_media_instagram or case.customer_social_media_facebook or case.customer_social_media_linkedin:
        elements.append(Paragraph("Social Media Links", heading_style))
        social_data = []
        if case.customer_social_media_instagram:
            social_data.append(['Instagram:', case.customer_social_media_instagram])
        if case.customer_social_media_facebook:
            social_data.append(['Facebook:', case.customer_social_media_facebook])
        if case.customer_social_media_linkedin:
            social_data.append(['LinkedIn:', case.customer_social_media_linkedin])
        if case.customer_website_url:
            social_data.append(['Website:', case.customer_website_url])
        
        if social_data:
            social_table = Table(social_data, colWidths=[2*inch, 4*inch])
            social_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(social_table)
            elements.append(Spacer(1, 0.3*inch))
    
    # Notes
    if case.notes:
        elements.append(Paragraph("Notes", heading_style))
        notes_para = Paragraph(case.notes.replace('\n', '<br/>'), styles['Normal'])
        elements.append(notes_para)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_all_cases_report_pdf(db: Session) -> BytesIO:
    """
    Generate a comprehensive PDF report for all cases.
    
    Args:
        db: Database session
        
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph("All Cases Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Generated date
    date_text = Paragraph(
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    )
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Get all cases
    cases = db.query(Case).all()
    
    # Summary statistics
    total_cases = len(cases)
    total_overdue = sum(case.overdue_amount for case in cases)
    
    summary_data = [
        ['Total Cases:', str(total_cases)],
        ['Total Overdue Amount:', f"${total_overdue:,.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#3b82f6')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Cases table header
    cases_data = [['Case ID', 'Customer', 'Amount', 'Status', 'DCA', 'Ageing']]
    
    # Add case rows
    for case in cases:
        cases_data.append([
            case.case_id,
            case.customer_name[:20] + '...' if len(case.customer_name) > 20 else case.customer_name,
            f"${case.overdue_amount:,.0f}",
            case.status.value,
            case.dca.name[:15] + '...' if case.dca and len(case.dca.name) > 15 else (case.dca.name if case.dca else 'N/A'),
            f"{case.ageing_days}d"
        ])
    
    cases_table = Table(cases_data, colWidths=[1.3*inch, 1.5*inch, 1*inch, 1*inch, 1.3*inch, 0.7*inch])
    cases_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(cases_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
