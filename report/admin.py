from django.contrib import admin
from .models import Report

# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'name', 'email', 'phone', 'report_type', 'complainant_type', 'created_at')
    list_filter = ('report_type', 'complainant_type', 'created_at')
    search_fields = ('report_id', 'name', 'email', 'phone', 'description')
    readonly_fields = ('report_id', 'created_at')
    fieldsets = (
        ('معلومات مقدم الشكوى', {
            'fields': ('report_id', 'name', 'email', 'phone')
        }),
        ('تفاصيل الشكوى', {
            'fields': ('report_type', 'complainant_type', 'description')
        }),
        ('معلومات النظام', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)
