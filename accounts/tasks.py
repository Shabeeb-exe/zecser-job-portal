# accounts/tasks.py
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Job, JobseekerProfile

logger = logging.getLogger(__name__)

def is_job_match(seeker, job):
    """Enhanced matching logic with better location and skills matching"""
    matches = []
    logger.info(f"Matching seeker {seeker.user.email} with job {job.id}")
    
    # Location matching (case-insensitive and checks both ways)
    if seeker.location and job.location:
        seeker_locations = [loc.strip().lower() for loc in seeker.location.split(',')]
        job_location = job.location.lower()
        location_match = any(
            job_loc in seeker_loc or seeker_loc in job_loc
            for seeker_loc in seeker_locations
            for job_loc in [job_location]
        )
        matches.append(location_match)
        logger.info(f"Location match: {location_match} (Seeker: {seeker.location}, Job: {job.location})")
    
    # Skills matching (more flexible)
    if seeker.skills and job.requirements:
        seeker_skills = [s.strip().lower() for s in seeker.skills.split(',') if s.strip()]
        job_reqs = job.requirements.lower()
        skills_match = any(
            skill in job_reqs or job_req in seeker_skills
            for skill in seeker_skills
            for job_req in job_reqs.split()
        )
        matches.append(skills_match)
        logger.info(f"Skills match: {skills_match} (Seeker: {seeker.skills}, Job: {job.requirements})")
    
    # Salary matching (90% of desired salary)
    if seeker.desired_salary:
        from .serializers import JobSerializer
        _, job_max = JobSerializer()._parse_salary(job.salary)
        if job_max:
            salary_match = job_max >= seeker.desired_salary * 0.9
            matches.append(salary_match)
            logger.info(f"Salary match: {salary_match} (Seeker wants: {seeker.desired_salary}, Job offers: {job.salary})")
    
    # At least two matches should be True
    result = sum(matches) >= 2 if matches else False
    logger.info(f"Overall match result: {result}")
    return result

def send_job_alert_email(email, jobs):
    """Send job alert email to a single recipient"""
    try:
        logger.info(f"Preparing to send email to {email}")
        subject = f"New Job Matches ({len(jobs)} opportunities)"
        html_message = render_to_string('emails/job_alerts.html', {
            'jobs': jobs,
            'count': len(jobs),
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject,
            '',  # Empty plain text message
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Successfully sent job alert to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}", exc_info=True)
    
# tasks.py
def send_immediate_job_alerts(job_id):
    try:
        job = Job.objects.get(id=job_id)
        
        seekers = JobseekerProfile.objects.filter(
            is_available=True,
            user__is_verified=True,
            receive_job_alerts=True
        ).select_related('user')
        
        for seeker in seekers:
            if is_job_match(seeker, job):
                send_job_alert_email(seeker.user.email, [job])
                
    except Exception as e:
        logger.error(f"Error in send_immediate_job_alerts: {str(e)}", exc_info=True)