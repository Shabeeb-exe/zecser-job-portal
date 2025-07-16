# management/commands/send_job_alerts.py
from django.core.management.base import BaseCommand
from accounts.models import Job, JobseekerProfile
from accounts.utils import send_job_alert_email
from datetime import date

class Command(BaseCommand):
    help = 'Sends email alerts to job seekers about matching jobs'

    def handle(self, *args, **options):
        job_seekers = JobseekerProfile.objects.filter(
            is_available=True,
            user__is_verified=True,
            receive_job_alerts=True
        ).select_related('user')

        jobs = Job.objects.filter(
            is_active=True,
            application_deadline__gte=date.today()
        )

        for seeker in job_seekers:
            matching_jobs = self.get_matching_jobs(seeker, jobs)
            if matching_jobs:
                send_job_alert_email(seeker.user.email, matching_jobs)

    def get_matching_jobs(self, seeker, jobs):
        from accounts.tasks import is_job_match  # Reuse the same matching logic
        return [job for job in jobs if is_job_match(seeker, job)]