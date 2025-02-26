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

    pro_name = models.CharField(max_length=100, verbose_name="Product Name")
    pro_type = models.CharField(max_length=50, choices=PRODUCT_TYPES, verbose_name="Product Type")
    pro_Therapeutic_Category = models.CharField(
        max_length=50, 
        choices=THERAPEUTIC_CATEGORIES, 
        verbose_name="Therapeutic Category",
        null=True,
        blank=True
    )
    pro_photo = models.ImageField(upload_to='products/', verbose_name="Product Photo", null=True, blank=True)
    pro_composition = models.TextField(verbose_name="Product Composition", null=True, blank=True)
    pro_Indications = models.TextField(verbose_name="Indications", null=True, blank=True)
    pro_Contraindications = models.TextField(verbose_name="Contraindications", null=True, blank=True)
    pro_Drug_Interactions = models.TextField(verbose_name="Drug Interactions", null=True, blank=True)
    pro_pregnancy_lactation = models.TextField(verbose_name="Pregnancy and Lactation", null=True, blank=True)
    pro_dosage_administration = models.TextField(verbose_name="Dosage and Administration", null=True, blank=True)

    def __str__(self):
        return self.pro_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
