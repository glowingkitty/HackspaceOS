from django.core.management.base import BaseCommand
from _setup.models import Setup


class Command(BaseCommand):
    help = "start the setup"

    def handle(self, *args, **options):
        Setup()._menu()
