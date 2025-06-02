from django.db import models

class Products(models.Model):
    id_pro = models.BigAutoField(primary_key=True)

    PRODUCT_TYPES = [
        ('Oral Suspension', 'Oral Suspension'),
        ('Capsule', 'Capsule'),
        ('tablets', 'Tablets'),
        ('Syrup', 'Syrup'),
        ('Suppositories', 'Suppositories'),
        ('Oral Drops', 'Oral Drops'),
    ]

    THERAPEUTIC_CATEGORIES = [
        ('Analgesic', 'Analgesic Antipyretic and Muscle-Relaxants'),
        ('Antibiotics', 'Antibiotics'),
        ('Anti_Cold', 'Anti Cold and Cough'),
        ('Antifungal', 'Antifungal'),
        ('Antifungal_Antiprotozoal', 'Antifungal Antiprotozoal'),
        ('Bronchodilator', 'Bronchodilator'),
        ('Corticosteroids', 'Corticosteroids'),
        ('Vitamin', 'Vitamin Supplement'),
        ('NSAID', 'Nonsteroidal anti-inflammatory drugs'),
        ('Cardiovascular', 'Cardiovascular Drugs'),
        ('Antihistamines', 'Antihistamines'),
        ('Antiseptics', 'Antiseptics'),
        ('Fluid_Electrolyte', 'Fluid & Electrolyte replacement'),
        ('Gynecology', 'Gynecology and Genitourinary'),
        ('Gastrointestinal', 'Gastrointestinal Drugs'),
        ('Hemorrhoids', 'Hemorrhoids Medication'),
        ('Anti_diabetic', 'Anti-diabetic drugs'),
    ]

    PRODUCT_LINES = [
        ('General', 'General'),
        ('Penicillins', 'Penicillin\'s'),
        ('Cephalosporins', 'Cephalosporins'),
        ('Other', 'Other'),
    ]

    # English fields
    pro_name_en = models.CharField(max_length=100, verbose_name="Product Name (EN)")
    pro_composition_en = models.TextField(verbose_name="Composition (EN)", null=True, blank=True)
    pro_Indications_en = models.TextField(verbose_name="Indications (EN)", null=True, blank=True)
    pro_Contraindications_en = models.TextField(verbose_name="Contraindications (EN)", null=True, blank=True)
    pro_Drug_Interactions_en = models.TextField(verbose_name="Drug Interactions (EN)", null=True, blank=True)
    pro_pregnancy_lactation_en = models.TextField(verbose_name="Pregnancy & Lactation (EN)", null=True, blank=True)
    pro_dosage_administration_en = models.TextField(verbose_name="Dosage & Administration (EN)", null=True, blank=True)
    pro_photo_en = models.ImageField(upload_to='products/en/', verbose_name="Image (EN)", null=True, blank=True)

    # Arabic fields
    pro_name_ar = models.CharField(max_length=100, verbose_name="اسم المنتج (AR)")
    pro_composition_ar = models.TextField(verbose_name="التركيب (AR)", null=True, blank=True)
    pro_Indications_ar = models.TextField(verbose_name="الاستطبابات (AR)", null=True, blank=True)
    pro_Contraindications_ar = models.TextField(verbose_name="موانع الاستعمال (AR)", null=True, blank=True)
    pro_Drug_Interactions_ar = models.TextField(verbose_name="التداخلات الدوائية (AR)", null=True, blank=True)
    pro_pregnancy_lactation_ar = models.TextField(verbose_name="الحمل والرضاعة (AR)", null=True, blank=True)
    pro_dosage_administration_ar = models.TextField(verbose_name="الجرعة وطريقة الاستعمال (AR)", null=True, blank=True)
    pro_photo_ar = models.ImageField(upload_to='products/ar/', verbose_name="الصورة (AR)", null=True, blank=True)

    # Common fields
    pro_type = models.CharField(max_length=50, choices=PRODUCT_TYPES, verbose_name="Product Type")
    pro_Therapeutic_Category = models.CharField(
        max_length=50, 
        choices=THERAPEUTIC_CATEGORIES, 
        verbose_name="Therapeutic Category",
        null=True,
        blank=True
    )
    pro_line = models.CharField(
        max_length=20,
        choices=PRODUCT_LINES,
        verbose_name="Product Line",
        default='Other'
    )
    pdf = models.FileField(upload_to='product_pdfs/', blank=True, null=True)

    def __str__(self):
        return self.pro_name_en  # or switch based on lang context

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
