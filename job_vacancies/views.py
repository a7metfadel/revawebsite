from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import JobApplication, JobApplicant
from .forms import JobApplicantForm

# عرض كتالوج الوظائف
def job_catalog(request):
    search_query = request.GET.get('search', '')
    department = request.GET.get('department', '')
    
    jobs = JobApplication.objects.all().order_by('-created_at')
    
    if search_query:
        jobs = jobs.filter(
            Q(job_title__icontains=search_query) |
            Q(job_description__icontains=search_query)
        )
    
    if department:
        jobs = jobs.filter(job_department__iexact=department)
    
    paginator = Paginator(jobs, 6)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    return render(request, 'job_catalog.html', {'jobs': jobs})


# فتح شاغر وظيفي جديد من خلال نموذج
def open_job(request):
    if request.method == 'POST':
        try:
            job_title = request.POST.get('job_title')
            job_department = request.POST.get('job_department')
            job_description = request.POST.get('job_description')
            job_photo = request.FILES.get('job_photo')

            job = JobApplication(
                job_title=job_title,
                job_department=job_department,
                job_description=job_description,
                job_photo=job_photo
            )
            job.save()
            
            messages.success(request, 'تم إضافة الشاغر الوظيفي بنجاح!')
            return redirect('job_catalog')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
    
    return render(request, 'job_open_application.html')


def job_application_view(request):
    success = False
    error_message = None

    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES

            job_id = data.get('job_id')
            job = JobApplication.objects.get(id=job_id) if job_id else None

            JobApplicant.objects.create(
                job = job,
                full_name = data.get('full_name'),
                birth_place = data.get('birth_place'),
                birth_date = data.get('birth_date'),
                current_residence = data.get('current_residence'),
                phone = data.get('phone'),
                phone_backup = data.get('phone_backup'),
                email = data.get('email'),
                gender = data.get('gender'),
                marital_status = data.get('marital_status'),
                scientific_certificate = data.get('scientific_certificate'),
                specialization = data.get('Specialization'),
                is_graduate = data.get('is_graduate'),
                graduation_institution = data.get('graduation_institution'),
                experiences = data.get('experiences'),
                has_health_issues = data.get('has_health_issues'),
                health_issue_description = data.get('health_issue_description'),
                previous_application = data.get('previous_application'),
                previous_application_date = data.get('previous_application_date') or None,
                has_relatives = data.get('has_relatives'),
                relative_name = data.get('relative_name'),
                relative_phone = data.get('relative_phone'),
                additional_information = data.get('additional_information'),
                cv_file = files.get('cv_file'),
                id_file = files.get('id_file'),
            )
            success = True

        except Exception as e:
            error_message = str(e)

    return render(request, 'apply_form.html', {
        'success': success,
        'error': error_message
    })

# صفحة نجاح بعد التقديم
def success_view(request):
    return render(request, 'success.html')