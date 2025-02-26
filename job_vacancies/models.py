from django.db import models

# Create your models here.

class JobApplication(models.Model):
    DEPARTMENT_CHOICES = [
        ('production department', 'Production Department'),
        ('research & development department', 'Research & Development Department'),
        ('quality assurance', 'Quality Assurance'),
        ('quality control', 'Quality Control'),
        ('maintance department', 'Maintenance Department'),
        ('finance department', 'Finance Department'),
        ('E-marketing department', 'E-Marketing Department'),
    ]

    LOCATION_CHOICES = [
        ('adlib', 'Adlib'),
        ('hama', 'Hama'),
        ('aleppo', 'Aleppo'),
        ('homs', 'Homs'),
        ('damascus', 'Damascus'),
        ('latakia', 'Latakia'),
        ('tartous', 'Tartous'),
    ]

    job_title = models.CharField(max_length=200)
    job_department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='damascus')
    job_photo = models.ImageField(upload_to='job_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-created_at']


class PersonalInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AdditionalInfo(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    id_number = models.CharField(max_length=50)
    address = models.TextField()
    marital_status = models.CharField(max_length=10)
    number_of_children = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Additional Info for {self.personal_info}"


class AcademicQualification(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    qualification_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    average = models.DecimalField(max_digits=5, decimal_places=2)
    graduation_date = models.DateField()

    def __str__(self):
        return f"{self.qualification_name} - {self.personal_info}"


class GeneralInfo(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE)
    previous_application = models.BooleanField(default=False)
    previous_application_date = models.DateField(null=True, blank=True)
    health_problems = models.BooleanField(default=False)
    health_problems_details = models.TextField(blank=True)
    is_smoker = models.BooleanField(default=False)
    has_relatives = models.BooleanField(default=False)
    relative_name = models.CharField(max_length=100, blank=True)
    relative_phone = models.CharField(max_length=20, blank=True)
    additional_information = models.TextField(blank=True)

    def __str__(self):
        return f"General Info for {self.personal_info}"
