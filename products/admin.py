from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Products

# 1. تعريف resource المخصص للمنتجات
class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products
        import_id_fields = []
        fields = (
            "pro_name_en", "pro_composition_en", "pro_Indications_en", "pro_Contraindications_en",
            "pro_Drug_Interactions_en", "pro_pregnancy_lactation_en", "pro_dosage_administration_en", "pro_photo_en",
            "pro_name_ar", "pro_composition_ar", "pro_Indications_ar", "pro_Contraindications_ar",
            "pro_Drug_Interactions_ar", "pro_pregnancy_lactation_ar", "pro_dosage_administration_ar", "pro_photo_ar",
            "pro_type", "pro_Therapeutic_Category", "pro_line", "pdf"
        )

@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    # 2. فعّل resource_class
    resource_class = ProductsResource

    list_display = ('id_pro', 'pro_name_en', 'pro_type', 'get_therapeutic_category', 'get_product_line')
    list_filter = ('pro_type', 'pro_Therapeutic_Category', 'pro_line')
    search_fields = ('id_pro', 'pro_name_en', 'pro_name_ar', 'pro_type', 'pro_Therapeutic_Category', 'pro_line')
    ordering = ('id_pro',)
    list_per_page = 20

    def get_therapeutic_category(self, obj):
        return dict(Products.THERAPEUTIC_CATEGORIES).get(obj.pro_Therapeutic_Category, '')
    get_therapeutic_category.short_description = 'Therapeutic Category'

    def get_product_line(self, obj):
        colors = {
            'General': '#4CAF50',
            'Penicillins': '#2196F3',
            'Cephalosporins': '#FF9800',
            'Other': '#9E9E9E'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.pro_line, '#9E9E9E'),
            obj.get_pro_line_display()
        )
    get_product_line.short_description = 'Product Line'

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id_pro',
                'pro_name_en', 'pro_name_ar',
                'pro_type',
                'pro_Therapeutic_Category',
                'pro_line',
                'pro_photo_en', 'pro_photo_ar',
                'pdf'
            ),
        }),
        ('Composition and Indications', {
            'fields': (
                'pro_composition_en', 'pro_composition_ar',
                'pro_Indications_en', 'pro_Indications_ar'
            ),
            'classes': ('collapse',)
        }),
        ('Contraindications and Interactions', {
            'fields': (
                'pro_Contraindications_en', 'pro_Contraindications_ar',
                'pro_Drug_Interactions_en', 'pro_Drug_Interactions_ar'
            ),
            'classes': ('collapse',)
        }),
        ('Pregnancy and Dosage', {
            'fields': (
                'pro_pregnancy_lactation_en', 'pro_pregnancy_lactation_ar',
                'pro_dosage_administration_en', 'pro_dosage_administration_ar'
            ),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('id_pro',)

    radio_fields = {
        'pro_Therapeutic_Category': admin.VERTICAL,
        'pro_line': admin.HORIZONTAL
    }
