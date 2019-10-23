# by Marco Bartsch
from django.core.management.base import BaseCommand
from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.marry import speak


class Command(BaseCommand):
    help = "Make Marry speak! (Noisebridge specific)"

    def add_arguments(self, parser):
        parser.add_argument('str_text', type=str)

    def handle(self, *args, **options):
        speak(text=options['str_text'], intro='')
