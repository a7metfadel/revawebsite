from django import forms
from .models import PersonalInfo, AdditionalInfo, AcademicQualification, GeneralInfo

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['first_name', 'last_name', 'father_name', 'mother_name', 'email', 'phone_number', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }

class AdditionalInfoForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=True
    )
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=True
    )

    class Meta:
        model = AdditionalInfo
        fields = ['gender', 'id_number', 'address', 'marital_status', 'number_of_children']
        widgets = {
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'number_of_children': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class AcademicQualificationForm(forms.ModelForm):
    class Meta:
        model = AcademicQualification
        fields = ['qualification_name', 'specialization', 'institution', 'average', 'graduation_date']
        widgets = {
            'qualification_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'average': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'required': True}),
            'graduation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
        }

class GeneralInfoForm(forms.ModelForm):
    previous_application = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'btn-check'})
    )
    health_problems = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'btn-check'})
    )
    is_smoker = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'btn-check'})
    )
    has_relatives = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'btn-check'})
    )

    class Meta:
        model = GeneralInfo
        fields = ['previous_application', 'previous_application_date', 'health_problems', 
                 'health_problems_details', 'is_smoker', 'has_relatives', 'relative_name', 
                 'relative_phone', 'additional_information']
        widgets = {
            'previous_application_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'health_problems_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'relative_name': forms.TextInput(attrs={'class': 'form-control'}),
            'relative_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }