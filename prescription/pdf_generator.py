from io import BytesIO
from reportlab.lib.pagesizes import A4  # Import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle,Table,Flowable
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader


def draw_border(canvas, doc, border_thickness=1, margin=10):
    width, height = A4
    canvas.saveState()
    canvas.setLineWidth(border_thickness)
    canvas.setStrokeColor(colors.black)
    canvas.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    canvas.restoreState()



class HorizontalLine(Flowable):
    def __init__(self, width, thickness=1, color=colors.black):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(190 * mm, 15 * mm, text)  # Adjust for A4 layout

def add_watermark(canvas, watermark_path, page_width, page_height, scale_factor=.71):
    if watermark_path:
        watermark = ImageReader(watermark_path)
        watermark_width = page_width * scale_factor
        watermark_height = page_height * scale_factor
        x_position = (page_width - watermark_width) / 2
        y_position = (page_height - watermark_height) / 2
        canvas.saveState()
        canvas.translate(x_position + watermark_width / 2, y_position + watermark_height / 2)
        canvas.rotate(360)
        canvas.drawImage(watermark, -watermark_width / 2, -watermark_height / 2, 
                         width=watermark_width, height=watermark_height, mask='auto')
        canvas.restoreState()

def add_footer(canvas, doc, footer_text, logo_path):
    canvas.saveState()
    width, height = A4  # Change to A4
    canvas.setFont('Helvetica', 10)  # Adjust font size for A4
    canvas.drawString(1 * inch, 0.5 * inch, footer_text)
    if logo_path:
        logo = ImageReader(logo_path)
        canvas.drawImage(logo, width - 1.5 * inch, 0.3 * inch, width=1.2 * inch, height=0.7 * inch, mask='auto')  # Adjust size and position
    canvas.restoreState()

def generate_prescription_pdf(prescription, watermark_path=None, logo_path=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)  # Change to A4

    styles = getSampleStyleSheet()
    custom_heading_style = styles['Heading3'].clone('custom_heading_style')
    custom_heading_style.textColor = colors.darkblue

    # Bullet style configuration
    bullet_style = ParagraphStyle(
        name='BulletStyle',
        fontName='Helvetica-Bold',
        fontSize=12,  # Adjust font size for A4
        leftIndent=15,
        bulletFontName='Helvetica-Bold',
        bulletFontSize=12,  # Adjust font size for A4
        spaceAfter=8
    )

    # Custom style for additional lines with more space
    instruction_style = ParagraphStyle(
        name='AdditionalLineStyle',
        fontName='Helvetica',
        fontSize=12,  # Adjust font size for A4
        leftIndent=25,
        spaceBefore=8,
        spaceAfter=15
    )
    
    profile_style = ParagraphStyle(
        name='ProfileStyle',
        fontName='Helvetica',
        fontSize=12,  # Adjust font size for A4
        spaceBefore=8,
        spaceAfter=8
    )
    
    
    detail_style = ParagraphStyle(
        name='DetailStyle',
        fontName='Helvetica',
        fontSize=12,  # Adjust font size for A4
        spaceAfter=15
    )

    story = []

    # Title
    story.append(Paragraph(f"<b>Prescription Of </b> {prescription.patient_name.title()} Age: {prescription.patient_age} Years", styles['Title']))   
    story.append(Spacer(1, 15))  
    doctor_info = [
        [Paragraph(f"<b>DR. {prescription.prescription_req.doctor.name}</b>", detail_style)],
        [Paragraph(f"BMDC NO: {prescription.prescription_req.doctor.doc_profile.bmdc_no}", profile_style)],
        [Paragraph(f"<b>{prescription.prescription_req.doctor.doc_profile.specialization}</b>", profile_style)]
    ]

    # Pharmacy and Patient Information (right-aligned)
    pharmacy_patient_info = [
        [Paragraph(f"<b>Date:</b> {prescription.prescription_date.strftime('%d-%m-%Y')}", detail_style)],
        [Paragraph(f"<b>Pharmacy Name:</b> {prescription.prescription_req.call_record.pharmacy_id.name}", detail_style)],
        [Paragraph(f"<b>Patient Phone:</b> {prescription.patient_phone_no}", detail_style)]
    ]

    # Create a table with two columns: left column for doctor info, right column for pharmacy and patient info
    data = [
        [
            doctor_info,
            pharmacy_patient_info
        ]
    ]

    # Define table style
    table = Table(data, colWidths=[3.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),   # Align first column (doctor info) to the left
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Align second column (pharmacy/patient info) to the right
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertical alignment to the top for both columns
        ('LEFTPADDING', (0, 0), (-1, -1), 0), # Remove padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(table)
    story.append(Spacer(1, 15))    
    story.append(HorizontalLine(width=doc.width, thickness=1, color=colors.ReportLabBlue))
    story.append(Spacer(1, 15))    
    # Complaint
    story.append(Paragraph("Complain:", custom_heading_style))
    story.append(Paragraph(f"{prescription.problem or 'N/A'}", instruction_style))
    
    # Medicines
    story.append(Paragraph("Medicines:", custom_heading_style))

    for item in prescription.items.all():
        strength = f" - {item.brand_name.strength}" if item.brand_name.strength else "" 
        conditionInstruction = f" - {item.condition_instruction.instruction}" if item.condition_instruction else "" 
        medicine_name = f"{item.brand_name.dosage_form_id.name} {item.brand_name.name} {strength} {conditionInstruction}"
        dosage = item.dosage
        dosage_instruction=item.dosage_instruction
        meal_instructions = item.get_meal_instructions_display()
        duration = item.duration
        # Format the text with bullet points and spacing
        bullet_point = f"• {medicine_name}"
        instructions_text = (
            f"&nbsp;&nbsp;&nbsp;{dosage}&nbsp;&nbsp;&nbsp; {dosage_instruction} &nbsp;&nbsp;&nbsp;{meal_instructions}&nbsp;&nbsp;&nbsp;{duration}"
        )

        # Add the bullet point and the instructions
        story.append(Paragraph(bullet_point, bullet_style))
        story.append(Paragraph(instructions_text, instruction_style))

    # Investigations
    story.append(Paragraph("Investigations:", custom_heading_style))
    for test in prescription.prescription_tests.all():
        bullet_point = f"• {test.test_name.name}"
        story.append(Paragraph(bullet_point, bullet_style))
        
    story.append(Spacer(1, 15))    
    story.append(Paragraph(f"<b>Advice:</b> {prescription.advice or 'N/A'}", detail_style))    
    follow_up = prescription.follow_up.strip() if prescription.follow_up else None

    # Check if the follow-up is valid and not unwanted like 'null 0'
    if follow_up and follow_up.lower() != "null 0":
        story.append(Paragraph(f"<b>Follow-up:</b> {follow_up}", detail_style))
    else:
        story.append(Paragraph("<b>Follow-up:</b> N/A", detail_style))
    # Footer information
    footer_text = "This is a system generated prescription by shastokotha - shastokotha.com"
    
    def on_first_page(canvas, doc):
        width, height = A4  # Change to A4
        draw_border(canvas, doc) 
        if watermark_path:
            add_watermark(canvas, watermark_path, width, height)
        add_footer(canvas, doc, footer_text, logo_path)

    def on_later_pages(canvas, doc):
        width, height = A4  # Change to A4
        draw_border(canvas, doc) 
        if watermark_path:
            add_watermark(canvas, watermark_path, width, height)
        add_footer(canvas, doc, footer_text, logo_path)
        add_page_number(canvas, doc)

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    buffer.seek(0)
    return buffer.getvalue()
