from django.contrib import admin
from .models import Invoice, LineItem

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'booking', 'issued_at', 'total_amount', 'paid_at')
    inlines = [LineItemInline]
