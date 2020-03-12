from django.core.management.base import BaseCommand
from _database.models import Event


class Command(BaseCommand):
    help = "Announce upcoming events (Noisebridge specific)"

    def handle(self, *args, **options):
        Event.objects.QUERYSET__upcoming().announce()
