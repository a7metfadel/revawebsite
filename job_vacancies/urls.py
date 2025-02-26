from django.urls import path
from . import views



urlpatterns = [  # الصفحة الرئيسية لعرض الوظائف
    path('cv_form/', views.cv_form, name='cv_form'),
    path('save_cv/', views.cv_form, name='save_cv'),  # إضافة المسار الجديد
    path('open_job/', views.open_job, name='open_job'),
    path('catalog/', views.job_catalog, name='job_catalog'),
    path('cv_catalog/', views.cv_catalog, name='cv_catalog'),
    path('cv_catalog_archive/', views.cv_catalog_archive, name='cv_catalog_archive'),
    # أضف هنا المسارات الأخرى الخاصة بالتطبيق
]
