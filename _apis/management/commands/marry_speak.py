from django.core.management.base import BaseCommand
from _apis.models.marryspeak import MarrySpeak


class Command(BaseCommand):
    help = "Make Marry speak! (Noisebridge specific)"

    def add_arguments(self, parser):
        parser.add_argument('str_text', type=str)

    def handle(self, *args, **options):
        speak(text=options['str_text'], intro='')
