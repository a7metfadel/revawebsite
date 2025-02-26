from django.contrib import admin
from .models import Products

# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # القائمة الرئيسية
    list_display = ('id_pro', 'pro_name', 'pro_type', 'get_therapeutic_category')
    list_filter = ('pro_type', 'pro_Therapeutic_Category')
    search_fields = ('id_pro', 'pro_name', 'pro_type', 'pro_Therapeutic_Category')
    ordering = ('id_pro',)
    list_per_page = 20

    def get_therapeutic_category(self, obj):
        return dict(Products.THERAPEUTIC_CATEGORIES).get(obj.pro_Therapeutic_Category, '')
    get_therapeutic_category.short_description = 'Therapeutic Category'

    # تنظيم حقول الإدخال
    fieldsets = (
        ('معلومات أساسية', {
            'fields': (
                'id_pro',
                'pro_name',
                'pro_type',
                'pro_Therapeutic_Category',
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
    radio_fields = {'pro_Therapeutic_Category': admin.VERTICAL}
