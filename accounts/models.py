from django.db import models
import enum
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class RoleEnum(enum.Enum):
    JOBSEEKER = "jobseeker"
    EMPLOYER = "employer"

class User(AbstractUser):
    ROLE_CHOICES = (
        (RoleEnum.JOBSEEKER.value, 'Job Seeker'),
        (RoleEnum.EMPLOYER.value, 'Employer'),
    )

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="")
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("========1========")
    if created:
        print(created,"========2========")
        if instance.role == RoleEnum.JOBSEEKER.value:
            JobseekerProfile.objects.get_or_create(user=instance)
        elif instance.role == RoleEnum.EMPLOYER.value:
            EmployerProfile.objects.get_or_create(user=instance)

class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile', limit_choices_to= {'role' : RoleEnum.JOBSEEKER.value})
    resume = models.FileField(upload_to='resumes/%Y/%m/%d/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], null=True, blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    desired_salary = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.full_name}'s Job Seeker Profile"
    
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile', limit_choices_to= {'role' : RoleEnum.EMPLOYER.value})
    company_name = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/%Y/%m/%d/', null=True, blank=True)
    company_website = models.URLField(blank=True)
    company_size = models.CharField(
        max_length=20,
        choices=[
            ('1-10', '1-10 employees'),
            ('11-50', '11-50 employees'),
            ('51-200', '51-200 employees'),
            ('201-500', '201-500 employees'),
            ('501-1000', '501-1000 employees'),
            ('1000+', '1000+ employees'),
        ],
        blank=True
    )
    industry = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user}'s Employer Profile"
    

class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]

    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"