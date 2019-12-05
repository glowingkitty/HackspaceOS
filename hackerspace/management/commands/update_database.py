from django.core.management.base import BaseCommand
from hackerspace.models import Event, Consensus, Person, Wish, Photo
from getConfig import get_config


class Command(BaseCommand):
    help = "Update the database"

    def handle(self, *args, **options):
        print('Update Persons ...')
        Person.objects.pull_from_discourse()

        print('Update Events ...')
        Event.objects.pull_from_meetup()
        for group in get_config('EVENTS.EXTRA_MEETUP_GROUPS'):
            Event.objects.pull_from_meetup(group)

        print('Update Consensus Items ...')
        Consensus.objects.pull_from_discourse()

        print('Update Photos ...')
        Photo.objects.import_from_twitter()
        Photo.objects.import_from_wiki()
        Photo.objects.import_from_instagram()
        Photo.objects.import_from_instagram_tag()
        Photo.objects.import_from_flickr()

        # print('Update Wishes ...')
        # Wish.objects.pull_from_discourse()
