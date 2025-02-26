from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import JobApplication, PersonalInfo, AdditionalInfo, AcademicQualification, GeneralInfo
from django.http import JsonResponse
from .forms import PersonalInfoForm, AdditionalInfoForm, AcademicQualificationForm, GeneralInfoForm
from django.db import transaction

def cv_form(request):
    if request.method == 'POST':
        personal_form = PersonalInfoForm(request.POST)
        additional_form = AdditionalInfoForm(request.POST)
        general_form = GeneralInfoForm(request.POST)
        
        # جمع جميع الشهادات من النموذج
        qualification_forms = []
        qualification_data = {}
        
        # تجميع بيانات الشهادات من النموذج
        for key, value in request.POST.items():
            if key.startswith('qualification_'):
                parts = key.split('_')
                if len(parts) >= 3:
                    form_num = parts[1]
                    field_name = '_'.join(parts[2:])
                    if form_num not in qualification_data:
                        qualification_data[form_num] = {}
                    qualification_data[form_num][field_name] = value
        
        # إنشاء نماذج للشهادات
        for form_num, data in qualification_data.items():
            form = AcademicQualificationForm(data)
            qualification_forms.append(form)

        if all([personal_form.is_valid(), additional_form.is_valid(), 
               general_form.is_valid()] + [form.is_valid() for form in qualification_forms]):
            try:
                with transaction.atomic():
                    # حفظ المعلومات الشخصية
                    personal_info = personal_form.save()
                    
                    # حفظ المعلومات الإضافية
                    additional_info = additional_form.save(commit=False)
                    additional_info.personal_info = personal_info
                    additional_info.save()
                    
                    # حفظ المؤهلات الأكاديمية
                    for qual_form in qualification_forms:
                        qualification = qual_form.save(commit=False)
                        qualification.personal_info = personal_info
                        qualification.save()
                    
                    # حفظ المعلومات العامة
                    general_info = general_form.save(commit=False)
                    general_info.personal_info = personal_info
                    general_info.save()
                    
                    messages.success(request, 'تم حفظ معلوماتك بنجاح! سيتم مراجعة طلبك والتواصل معك قريباً.')
                    return redirect('job_catalog')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء حفظ البيانات: {str(e)}')
        else:
            # عرض رسائل الخطأ للمستخدم
            for form in [personal_form, additional_form, general_form] + qualification_forms:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        personal_form = PersonalInfoForm()
        additional_form = AdditionalInfoForm()
        qualification_form = AcademicQualificationForm()
        general_form = GeneralInfoForm()
    
    context = {
        'personal_form': personal_form,
        'additional_form': additional_form,
        'qualification_form': qualification_form,
        'general_form': general_form,
    }
    return render(request, 'cv_form1.html', context)

def job_catalog(request):
    # Get search query and department filter
    search_query = request.GET.get('search', '')
    department = request.GET.get('department', '')
    
    # Get all jobs
    jobs = JobApplication.objects.all().order_by('-created_at')
    
    # Apply filters if present
    if search_query:
        jobs = jobs.filter(
            Q(job_title__icontains=search_query) |
            Q(job_description__icontains=search_query)
        )
    
    if department:
        jobs = jobs.filter(job_department__iexact=department)
    
    # Pagination
    paginator = Paginator(jobs, 6)  # Show 6 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    return render(request, 'job_catalog.html', {'jobs': jobs})

def open_job(request):
    if request.method == 'POST':
        try:
            job_title = request.POST.get('job_title')
            job_department = request.POST.get('job_department')
            job_description = request.POST.get('job_description')
            job_photo = request.FILES.get('job_photo')

            # Create and save the new job
            job = JobApplication(
                job_title=job_title,
                job_department=job_department,
                job_description=job_description,
                job_photo=job_photo
            )
            job.save()
            
            messages.success(request, 'Job opening added successfully!')
            return redirect('job_catalog')
        except Exception as e:
            messages.error(request, f'Error adding job opening: {str(e)}')
    
    return render(request, 'job_open_application.html')


def cv_catalog(request):
    # جلب جميع السير الذاتية مرتبة حسب تاريخ الإنشاء
    cv_list = PersonalInfo.objects.all().order_by('-created_at')
    
    # إضافة البحث
    search_query = request.GET.get('search', '')
    if search_query:
        cv_list = cv_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # إضافة الترتيب
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by:
        cv_list = cv_list.order_by(sort_by)
    
    # إضافة التصفح
    paginator = Paginator(cv_list, 10)  # 10 سير ذاتية في كل صفحة
    page = request.GET.get('page')
    cvs = paginator.get_page(page)
    
    context = {
        'cvs': cvs,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'cv_catalog.html', context)

def cv_catalog_archive(request):
    return render(request, 'cv_catalog_archive.html')