from celery import shared_task
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
from .models import Invoice

@shared_task
def generate_invoice_pdf(invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return f"Invoice {invoice_id} not found"

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw Invoice Header
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, f"INVOICE #{invoice.invoice_number}")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Date: {invoice.issued_at.strftime('%Y-%m-%d')}")
    p.drawString(50, height - 100, f"Guest: {invoice.booking.guest.username}")
    p.drawString(50, height - 120, f"Room: {invoice.booking.room.room_number}")

    # Draw Line Items
    y = height - 160
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Description")
    p.drawString(300, y, "Qty")
    p.drawString(400, y, "Unit Price")
    p.drawString(500, y, "Amount")
    
    y -= 20
    p.line(50, y+15, 550, y+15)
    
    p.setFont("Helvetica", 12)
    for item in invoice.items.all():
        p.drawString(50, y, item.description)
        p.drawString(300, y, str(item.quantity))
        p.drawString(400, y, f"${item.unit_price}")
        p.drawString(500, y, f"${item.amount}")
        y -= 20

    # Total
    y -= 20
    p.line(50, y+15, 550, y+15)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(400, y, "Total:")
    p.drawString(500, y, f"${invoice.total_amount}")

    p.showPage()
    p.save()

    buffer.seek(0)
    
    # Save to model
    filename = f"invoice_{invoice.invoice_number}.pdf"
    invoice.pdf_file.save(filename, ContentFile(buffer.getvalue()), save=True)
    
    return f"PDF generated for Invoice {invoice.invoice_number}"
