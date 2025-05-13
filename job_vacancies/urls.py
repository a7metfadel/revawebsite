from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_catalog, name='job_catalog'),
    path('apply/', views.job_application_view, name='job_apply'),
    path('open-job/', views.open_job, name='open_job'),
    path('success/', views.success_view, name='success'),
]