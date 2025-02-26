from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Report

# Create your views here.
def report_view(request):
    """عرض صفحة إرسال التقرير"""
    return render(request, 'report.html')

def submit_report(request):
    """معالجة إرسال التقرير"""
    if request.method == 'POST':
        try:
            # إنشاء تقرير جديد من البيانات المرسلة
            report = Report(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                report_type=request.POST.get('report_type'),
                complainant_type=request.POST.get('complainant_type'),
                description=request.POST.get('description')
            )
            report.save()
            
            messages.success(request, f'تم إرسال الشكوى بنجاح. رقم الشكوى الخاص بك هو: {report.report_id}')
        except Exception as e:
            messages.error(request, 'حدث خطأ أثناء إرسال الشكوى. يرجى المحاولة مرة أخرى.')
        
        return redirect('report')
    
    return render(request, 'report.html')