from django import forms
from .models import JobApplicant

class JobApplicantForm(forms.ModelForm):
    class Meta:
        model = JobApplicant
        fields = '__all__'  # ← التصحيح هنا
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'previous_application_date': forms.DateInput(attrs={'type': 'date'}),
        }