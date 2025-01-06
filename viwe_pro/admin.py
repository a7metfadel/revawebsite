from django.contrib import admin
from .models import Products

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pro_name', 'pro_type')  # الحقول التي ستظهر في قائمة المنتجات
    list_filter = ('pro_type',)  # إضافة فلتر حسب نوع المنتج
    search_fields = ('pro_name', 'pro_description')  # إمكانية البحث في اسم ووصف المنتج
    list_per_page = 20  # عدد المنتجات في كل صفحة
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('pro_name', 'pro_type', 'pro_photo')
        }),
        ('Detailed Information', {
            'fields': ('pro_description', 'pro_composition'),
            'classes': ('collapse',)
        }),
    )
