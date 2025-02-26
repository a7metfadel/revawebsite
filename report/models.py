from django.db import models

# Create your models here.

class Report(models.Model):
    # خيارات نوع التقرير
    REPORT_TYPE_CHOICES = [
        ('our_product', 'شكوى على منتج'),
        ('our_team', 'شكوى على موظف'),
    ]
    
    # خيارات نوع مقدم الشكوى
    COMPLAINANT_TYPE_CHOICES = [
        ('doctor', 'طبيب'),
        ('pharmacist', 'صيدلي'),
        ('patient', 'مريض'),
        ('other', 'آخر'),
    ]
    
    # الحقول الأساسية
    report_id = models.AutoField(primary_key=True, verbose_name="رقم الشكوى")
    name = models.CharField(max_length=100, verbose_name="اسم مقدم الشكوى")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    
    # نوع التقرير والشاكي
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        verbose_name="نوع الشكوى"
    )
    complainant_type = models.CharField(
        max_length=20,
        choices=COMPLAINANT_TYPE_CHOICES,
        verbose_name="المكانة الطبية"
    )
    
    # تفاصيل الشكوى
    description = models.TextField(verbose_name="تفاصيل الشكوى")
    
    # تاريخ ووقت التقرير
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ ووقت الشكوى")
    
    class Meta:
        verbose_name = "تقرير"
        verbose_name_plural = "التقارير"
        ordering = ['-created_at']  # ترتيب تنازلي حسب التاريخ
    
    def __str__(self):
        return f"شكوى رقم {self.report_id} - {self.name}"
