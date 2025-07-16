# accounts/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Import signals after apps are ready
        logger.info("AccountsConfig ready() called")
        import accounts.signals  # noqa