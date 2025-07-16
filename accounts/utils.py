from venv import logger
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import uuid

def send_verification_email(user):
    """
    Send verification email to a new user
    """
    # Ensure user has a valid token
    if not user.verification_token:
        user.verification_token = uuid.uuid4()
        user.verification_token_expires = timezone.now() + timezone.timedelta(days=1)
        user.save()
    
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    verification_url = f"{site_url}/api/auth/verify-email/{user.verification_token}/"
    
    subject = "Verify Your Email Address"
    html_message = render_to_string('emails/verify_email.html', {
        'verification_url': verification_url,
    })
    
    send_mail(
        subject,
        '',  # Empty plain text message
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False
    )

def send_job_alert_email(email, jobs):
    """
    Send job alert email to a single recipient
    """
    subject = f"New Job Matches ({len(jobs)} opportunities)"
    html_message = render_to_string('emails/job_alerts.html', {
        'jobs': jobs,
        'count': len(jobs)
    })
    try:
        send_mail(
            subject,
            '',  # Empty plain text message
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        logger.error(f"Failed to send job alert to {email}: {str(e)}")