# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from .tasks import send_immediate_job_alerts
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Job)
def new_job_handler(sender, instance, created, **kwargs):
    logger.info(f"Job post_save signal triggered. Created: {created}, Active: {instance.is_active}")
    if created and instance.is_active:
        logger.info(f"New active job created, sending alerts for job ID: {instance.id}")
        send_immediate_job_alerts(instance.id)