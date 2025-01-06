from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='product'),
    path('add_product/', views.add_products, name='add_product'),
     path('cv/', views.cv, name='cv'),
    
    # أضف هنا المسارات الأخرى الخاصة بالتطبيق
]
