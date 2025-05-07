from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from job_vacancies.models import JobApplication
# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'car-finder-about.html')

def contact(request):
    return render(request, 'contact.html')

def job(request):
    jobs = JobApplication.objects.all()
    return render(request, "job_catalog.html", {"jobs": jobs})

def report(request):
    return render(request, 'report.html')

def product_info(request):
    return render(request, 'product_info.html')

def labaratory(request):
    return render(request, 'labaratory.html')

def General(request):
    return render(request, 'General.html')

def cephalosporins(request):
    return render(request, 'cephalosporins.html')

def benicillins(request):
    return render(request, 'benicillins.html')

def job_detail(request, id):
    job = get_object_or_404(JobApplication, id=id)
    return render(request, 'job_detail.html', {'job': job})

def job_detail(request, id):
    job = get_object_or_404(JobApplication, id=id)

    # جلب وظائف مشابهة
    similar_jobs = JobApplication.objects.filter(
        job_department=job.job_department
    ).exclude(id=job.id)[:5]

    return render(request, 'job_detail.html', {
        'job': job,
        'similar_jobs': similar_jobs
    })
 