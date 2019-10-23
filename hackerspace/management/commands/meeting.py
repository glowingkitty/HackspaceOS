# by Marco Bartsch
from django.core.management.base import BaseCommand
from hackerspace.website.meeting_notes import startMeeting, endMeeting


class Command(BaseCommand):
    help = "Quickly start or end a meeting"

    def add_arguments(self, parser):
        parser.add_argument('str_command', type=str)

    def handle(self, *args, **options):
        if options['str_command'] == 'start':
            startMeeting()

        elif options['str_command'] == 'end':
            endMeeting()
