# by Marco Bartsch
from django.core.management.base import BaseCommand
from hackerspace.models import Event, Consensus, Person, Wish
from hackerspace.YOUR_HACKERSPACE import EXTRA_MEETUP_GROUPS


class Command(BaseCommand):
    help = "Update the database"

    def handle(self, *args, **options):
        print('Update Persons ...')
        Person.objects.pull_from_discourse()

        print('Update Events ...')
        Event.objects.pull_from_meetup()
        for group in EXTRA_MEETUP_GROUPS:
            Event.objects.pull_from_meetup(group)

        print('Update Consensus Items ...')
        Consensus.objects.pull_from_discourse()

        # print('Update Wishes ...')
        # Wish.objects.pull_from_discourse()
