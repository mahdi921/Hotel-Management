from django.db import models
from bookings.models import Booking

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=20, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    paid_at = models.DateTimeField(blank=True, null=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)

    @property
    def total_amount(self):
        return sum(item.amount for item in self.items.all())

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.booking}"

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def amount(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} (x{self.quantity})"
