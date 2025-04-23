from django.urls import path
from . import views

urlpatterns = [  
    path('product_catalog/', views.product_catalog, name='product_catalog'),
    path('benicillins/', views.benicillins, name='benicillins'),
    path('General/', views.General, name='General'),
    path('cephalosporins/', views.cephalosporins, name='cephalosporins'),
    path('product_info/', views.product_info, name='product_info'),
    path('pro_info/', views.pro_info, name='pro_info'),
]
