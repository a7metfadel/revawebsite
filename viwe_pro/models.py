from django.db import models

class Products(models.Model):
    pro_name = models.CharField(max_length=100, verbose_name="Product Name")
    pro_type = models.CharField(max_length=50, verbose_name="Product Type")
    pro_description = models.TextField(verbose_name="Product Description")
    pro_composition = models.TextField(verbose_name="Product Composition")
    pro_photo = models.ImageField(upload_to='products/', verbose_name="Product Photo")

    def __str__(self):
        return self.pro_type

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
