import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(json_file, output_filename):
    with open(json_file, 'r') as f: data = json.load(f)
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()

    # --- COVER PAGE ---
    c.setFillColor(colors.HexColor("#1A365D"))
    c.rect(0, 0, width, height, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width/2, height/2 + 40, "TLS INFRASTRUCTURE AUDIT")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height/2 - 10, "Cybersecurity Assessment | UNAL 2026")
    c.showPage()

    # --- DATA PAGES ---
    y = height - 80
    for host in data:
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Audit Target: {host['server']}")
        y -= 30
        
        # Summary Table
        summary = [["Technical Metric", "Value"], ["Severity Level", host['severity']], ["Public Key Specs", host['key_info']], ["Cert Expiration", host['cert_expiry']]]
        t1 = Table(summary, colWidths=[150, 330])
        t1.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')]))
        tw, th = t1.wrapOn(c, 50, y); t1.drawOn(c, 50, y - th); y -= (th + 30)

        # Actionable Items Table
        items = [["Vulnerability", "Hardening Strategy"]]
        for f, r in zip(host['findings'], host['recommendations']):
            items.append([Paragraph(f, styles["BodyText"]), Paragraph(r, styles["BodyText"])])

        t2 = Table(items, colWidths=[240, 240])
        t2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2D3748")), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        tw, th = t2.wrapOn(c, 50, y); t2.drawOn(c, 50, y - th); y -= (th + 50)
        
        if y < 150: c.showPage(); y = height - 80

    c.save()
