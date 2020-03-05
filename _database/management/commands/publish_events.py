from django.core.management.base import BaseCommand
from _database.models import Event
from _setup.log import log


class Command(BaseCommand):
    help = "Publish new events after 24hour"

    def handle(self, *args, **options):
        log('publish_events.py')
        Event.objects.QUERYSET__not_approved().QUERYSET__older_then_24h().publish()
