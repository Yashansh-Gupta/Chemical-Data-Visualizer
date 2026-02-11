from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(dataset, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Chemical Dataset Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Dataset: {dataset.name}")
    y -= 20
    c.drawString(40, y, f"Uploaded at: {dataset.uploaded_at}")
    y -= 30

    summary = dataset.summary

    for key, value in summary.items():
        c.drawString(40, y, f"{key}: {value}")
        y -= 15

        if y < 50:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 10)

    c.showPage()
    c.save()
