from django.core.management import BaseCommand
from mailing.mailing import start_scheduler, scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        if scheduler.running:
            scheduler.shutdown()
        start_scheduler()