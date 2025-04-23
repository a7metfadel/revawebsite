from django.contrib import admin
from django.utils.html import format_html
from .models import Products

# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # القائمة الرئيسية
    list_display = ('id_pro', 'pro_name', 'pro_type', 'get_therapeutic_category', 'get_product_line')
    list_filter = ('pro_type', 'pro_Therapeutic_Category', 'pro_line')
    search_fields = ('id_pro', 'pro_name', 'pro_type', 'pro_Therapeutic_Category', 'pro_line')
    ordering = ('id_pro',)
    list_per_page = 20

    def get_therapeutic_category(self, obj):
        return dict(Products.THERAPEUTIC_CATEGORIES).get(obj.pro_Therapeutic_Category, '')
    get_therapeutic_category.short_description = 'Therapeutic Category'

    def get_product_line(self, obj):
        colors = {
            'General': '#4CAF50',  # Green
            'Penicillins': '#2196F3',  # Blue
            'Cephalosporins': '#FF9800',  # Orange
            'Other': '#9E9E9E'  # Grey
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.pro_line, '#9E9E9E'),
            obj.get_pro_line_display()
        )
    get_product_line.short_description = 'Product Line'

    # تنظيم حقول الإدخال
    fieldsets = (
        ('معلومات أساسية', {
            'fields': (
                'id_pro',
                'pro_name',
                'pro_type',
                'pro_Therapeutic_Category',
                'pro_line',
                'pro_photo'
            ),
            'description': 'المعلومات الأساسية للمنتج والتصنيف العلاجي'
        }),
        ('التركيب والاستطبابات', {
            'fields': ('pro_composition', 'pro_Indications'),
            'classes': ('collapse',)
        }),
        ('موانع الاستعمال والتفاعلات', {
            'fields': ('pro_Contraindications', 'pro_Drug_Interactions'),
            'classes': ('collapse',)
        }),
        ('الحمل والجرعات', {
            'fields': ('pro_pregnancy_lactation', 'pro_dosage_administration'),
            'classes': ('collapse',)
        }),
    )

    # جعل حقل id_pro للقراءة فقط
    readonly_fields = ('id_pro',)

    # تحسين البحث والتصفية
    radio_fields = {
        'pro_Therapeutic_Category': admin.VERTICAL,
        'pro_line': admin.HORIZONTAL  # عرض خيارات Product Line بشكل أفقي
    }
