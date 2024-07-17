from django.contrib import admin
from django.http import HttpResponse
import openpyxl

from .models import Order, OrderItem


# Register your models here.

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Orders'
    columns = ['id', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'province',
               'paid', 'created']
    ws.append(columns)
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([
            order.id, order.first_name, order.last_name, order.phone, order.address,
            order.postal_code, order.city, order.province, order.paid, created
        ])
    wb.save(response)
    return response

export_to_excel.short_description = 'Export to Excel'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'province',
                    'paid', 'created']
    list_filter = ['paid', 'created', 'updated', 'city', 'province']
    inlines = [OrderItemInline]
    actions = [export_to_excel]
