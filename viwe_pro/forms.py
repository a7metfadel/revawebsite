from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        print("Form cleaning data:", cleaned_data)  # للتحقق من البيانات
        return cleaned_data

    class Meta:
        model = Products
        fields = ['pro_name', 'pro_type', 'pro_description', 'pro_composition', 'pro_photo']
        
        widgets = {
            'pro_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المنتج'
            }),
            'pro_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل نوع المنتج'
            }),
            'pro_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل وصف المنتج',
                'rows': '3'
            }),
            'pro_composition': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل تركيبة المنتج',
                'rows': '6'
            }),
            'pro_photo': forms.FileInput(attrs={
                'class': 'file-uploader bg-secondary',
                'accept': 'image/png, image/jpeg'
            })
        }
        
        labels = {
            'pro_name': 'اسم المنتج',
            'pro_type': 'نوع المنتج',
            'pro_description': 'وصف المنتج',
            'pro_composition': 'تركيبة المنتج',
            'pro_photo': 'صورة المنتج'
        }
