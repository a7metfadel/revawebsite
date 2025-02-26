from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_view, name='report'),
    path('submit/', views.submit_report, name='submit_report'),
]
