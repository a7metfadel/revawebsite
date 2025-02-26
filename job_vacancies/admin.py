from django.contrib import admin
from .models import JobApplication, PersonalInfo, AdditionalInfo, AcademicQualification, GeneralInfo

# Register your models here.

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_department', 'job_location', 'created_at')
    list_filter = ('job_department', 'job_location', 'created_at')
    search_fields = ('job_title', 'job_description')
    readonly_fields = ('created_at',)
    list_per_page = 20

class AdditionalInfoInline(admin.StackedInline):
    model = AdditionalInfo
    can_delete = False

class AcademicQualificationInline(admin.StackedInline):
    model = AcademicQualification
    extra = 0

class GeneralInfoInline(admin.StackedInline):
    model = GeneralInfo
    can_delete = False

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'birth_date', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('created_at',)
    inlines = [AdditionalInfoInline, AcademicQualificationInline, GeneralInfoInline]
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'gender', 'id_number', 'marital_status')
    list_filter = ('gender', 'marital_status')
    search_fields = ('id_number', 'address')

@admin.register(AcademicQualification)
class AcademicQualificationAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'qualification_name', 'specialization', 'institution', 'average', 'graduation_date')
    list_filter = ('graduation_date',)
    search_fields = ('qualification_name', 'specialization', 'institution')

@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'previous_application', 'health_problems', 'is_smoker', 'has_relatives')
    list_filter = ('previous_application', 'health_problems', 'is_smoker', 'has_relatives')
    search_fields = ('relative_name', 'health_problems_details')
