
from django.db import models

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
        ('edlib', 'Edlib'),
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


class JobApplicant(models.Model):
    job = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applicants', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    current_residence = models.CharField(max_length=100, blank=True, null=True)
    phone_backup = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10)
    scientific_certificate = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    is_graduate = models.CharField(max_length=10)
    graduation_institution = models.CharField(max_length=255, blank=True, null=True)
    experiences = models.TextField(blank=True, null=True)
    has_health_issues = models.CharField(max_length=10)
    health_issue_description = models.TextField(blank=True, null=True)
    previous_application = models.CharField(max_length=10)
    previous_application_date = models.DateField(blank=True, null=True)
    has_relatives = models.CharField(max_length=10)
    relative_name = models.CharField(max_length=255, blank=True, null=True)
    relative_phone = models.CharField(max_length=20, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    cv_file = models.FileField(upload_to='cvs/')
    id_file = models.FileField(upload_to='ids/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
