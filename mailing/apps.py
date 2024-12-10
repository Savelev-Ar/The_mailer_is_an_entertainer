from django.apps import AppConfig

from time import sleep


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from mailing.mailing import start_scheduler
        sleep(1)
        start_scheduler()
