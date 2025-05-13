from django.contrib import admin
from django.http import HttpResponse
from django.utils.timezone import localtime
from .models import JobApplication, JobApplicant
import pandas as pd
from io import BytesIO

# --------------------- JobApplication Admin ---------------------

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_department', 'job_location', 'created_at', 'applicants_count')
    list_filter = ('job_department', 'job_location', 'created_at')
    search_fields = ('job_title', 'job_description')
    readonly_fields = ('created_at',)
    list_per_page = 20

    def applicants_count(self, obj):
        return JobApplicant.objects.filter(job=obj).count()
    applicants_count.short_description = 'Number of Applicants'


# --------------------- JobApplicant Admin ---------------------

@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_job_title', 'phone', 'email', 'birth_date', 'submitted_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('job__job_title', 'gender', 'marital_status', 'is_graduate', 'has_health_issues')
    readonly_fields = ('submitted_at',)
    list_per_page = 20
    actions = ['export_all_grouped', 'export_filtered_job_title']

    def get_job_title(self, obj):
        return obj.job.job_title if obj.job else ''
    get_job_title.short_description = 'Job Title'

    def export_all_grouped(self, request, queryset):
        grouped = {}
        for obj in queryset:
            title = obj.job.job_title if obj.job else 'Unknown'
            if title not in grouped:
                grouped[title] = []
            grouped[title].append(self._extract_applicant_data(request, obj))

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            for title, records in grouped.items():
                df = pd.DataFrame(records)
                sheet = title[:31]
                df.to_excel(writer, index=False, sheet_name=sheet)
                worksheet = writer.sheets[sheet]
                workbook = writer.book
                format_header = workbook.add_format({'bold': True, 'bg_color': '#dce6f1'})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, format_header)
                    worksheet.set_column(col_num, col_num, 22)

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Applicants_Export_All.xlsx"'
        return response

    export_all_grouped.short_description = "Export All Applicants (Grouped by Job Title)"

    def export_filtered_job_title(self, request, queryset):
        if not queryset:
            return HttpResponse("No applicants selected.")
        job = queryset.first().job
        filtered = queryset.filter(job=job)

        df = pd.DataFrame([self._extract_applicant_data(request, obj) for obj in filtered])
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Applicants')
            worksheet = writer.sheets['Applicants']
            workbook = writer.book
            format_header = workbook.add_format({'bold': True, 'bg_color': '#f9f9f9'})
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, format_header)
                worksheet.set_column(col_num, col_num, 22)

        buffer.seek(0)
        filename = f"Applicants_{job.job_title.replace(' ', '_')}.xlsx"
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    export_filtered_job_title.short_description = "Export Applicants for Selected Job Title Only"
    
    def _extract_applicant_data(self, request, obj):
        return {
            "Full Name": obj.full_name,
            "Job Title": obj.job.job_title if obj.job else '',
            "Phone": obj.phone,
            "Email": obj.email,
            "Birth Date": obj.birth_date.strftime('%Y-%m-%d') if obj.birth_date else '',
            "Gender": obj.gender,
            "Marital Status": obj.marital_status,
            "Is Graduate": obj.is_graduate,
            "Specialization": obj.specialization,
            "Scientific Certificate": obj.scientific_certificate,
            "Graduation Institution": obj.graduation_institution,
            "Experiences": obj.experiences,
            "Has Health Issues": obj.has_health_issues,
            "Health Issue Description": obj.health_issue_description or '',
            "Previous Application": obj.previous_application,
            "Previous Application Date": obj.previous_application_date.strftime('%Y-%m-%d') if obj.previous_application_date else '',
            "Has Relatives": obj.has_relatives,
            "Relative Name": obj.relative_name or '',
            "Relative Phone": obj.relative_phone or '',
            "Additional Info": obj.additional_information or '',
            "CV File": f'=HYPERLINK("{request.build_absolute_uri(obj.cv_file.url)}", "Download CV")' if obj.cv_file else '',
            "ID File": f'=HYPERLINK("{request.build_absolute_uri(obj.id_file.url)}", "Download ID")' if obj.id_file else '',
            "Submitted At": localtime(obj.submitted_at).strftime('%Y-%m-%d %H:%M:%S') if obj.submitted_at else ''
        }