from django.core.management.base import BaseCommand
from _database.models import Event
from pyprintplus import Log


class Command(BaseCommand):
    help = "Publish new events after 24hour"

    def handle(self, *args, **options):
        Log().print('publish_events.py')
        Event.objects.QUERYSET__not_approved().QUERYSET__older_then_24h().publish()
