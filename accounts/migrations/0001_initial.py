# Generated by Django 5.2.3 on 2025-07-16 18:59

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('role', models.CharField(choices=[('jobseeker', 'Job Seeker'), ('employer', 'Employer')], default='', max_length=10)),
                ('verification_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('verification_token_expires', models.DateTimeField(default=datetime.datetime(2025, 7, 17, 18, 59, 45, 63715, tzinfo=datetime.timezone.utc))),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_logos/%Y/%m/%d/')),
                ('company_website', models.URLField(blank=True)),
                ('company_size', models.CharField(blank=True, choices=[('1-10', '1-10 employees'), ('11-50', '11-50 employees'), ('51-200', '51-200 employees'), ('201-500', '201-500 employees'), ('501-1000', '501-1000 employees'), ('1000+', '1000+ employees')], max_length=20)),
                ('industry', models.CharField(blank=True, max_length=100)),
                ('founded_year', models.PositiveIntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(limit_choices_to={'role': 'employer'}, on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('internship', 'Internship'), ('temporary', 'Temporary')], max_length=20)),
                ('salary', models.CharField(blank=True, max_length=100)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='accounts.employerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='JobseekerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx'])])),
                ('skills', models.TextField(blank=True)),
                ('education', models.TextField(blank=True)),
                ('experience', models.TextField(blank=True)),
                ('portfolio_url', models.URLField(blank=True)),
                ('github_url', models.URLField(blank=True)),
                ('desired_salary', models.PositiveIntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('receive_job_alerts', models.BooleanField(default=True)),
                ('alert_frequency', models.CharField(choices=[('immediate', 'Immediately'), ('daily', 'Daily'), ('weekly', 'Weekly')], default='daily', max_length=10)),
                ('user', models.OneToOneField(limit_choices_to={'role': 'jobseeker'}, on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
