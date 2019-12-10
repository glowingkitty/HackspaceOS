from django.core.management.base import BaseCommand
from hackerspace.models import Event
from hackerspace.log import log


class Command(BaseCommand):
    help = "Publish new events after 24hour"

    def handle(self, *args, **options):
        log('publish_events.py')
        Event.objects.QUERYSET__not_approved().QUERYSET__older_then_24h().publish()
