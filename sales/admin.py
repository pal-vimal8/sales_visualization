
from django.contrib import admin
from .models import Salesperson, SalesRecord

@admin.register(Salesperson)
class SalespersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_sales')

    def total_sales(self, obj):
        sales_records = SalesRecord.objects.filter(salesperson=obj)
        return sum(record.sales_amount for record in sales_records)
    total_sales.short_description = 'Total Sales'

@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('salesperson', 'sales_month', 'sales_amount')