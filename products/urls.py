from django.urls import path
from . import views

urlpatterns = [  
    path('product_catalog/', views.product_catalog, name='product_catalog'),
    path('benicillins/', views.benicillins, name='benicillins'),
    path('General/', views.General, name='General'),
    path('cephalosporins/', views.cephalosporins, name='cephalosporins'),
]
