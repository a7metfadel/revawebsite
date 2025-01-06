from django.urls import path , include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('job/', views.job, name='job'),
    path('report/', views.report, name='report'),
]
