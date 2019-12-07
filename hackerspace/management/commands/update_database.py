from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the database"

    def handle(self, *args, **options):
        from hackerspace.models import Event, Consensus, Person, Wish, Photo, Project
        from getConfig import get_config
        from getKey import STR__get_key
        from asci_art import show_message
        import time
        import requests

        show_message('I will now start to update your database, based on your secrets.json and config.json. Depending on your settings, amount of events & photos & Discourse entries from your hackerspace this can take everything from seconds to hours (?). But you can already test your website - by opening a new terminal window and run "python manage.py runserver 0.0.0.0:8000" - and open 0.0.0.0:8000 in your web browser.')
        time.sleep(8)

        # import data from Discourse
        Person.objects.pull_from_discourse()
        Consensus.objects.pull_from_discourse()
        Project.objects.pull_from_discourse()
        # TODO Adding Wishlist
        # Wish.objects.pull_from_discourse()

        # import events from Meetup
        Event.objects.pull_from_meetup()
        extra_groups = get_config('EVENTS.EXTRA_MEETUP_GROUPS')
        if extra_groups:
            show_message(
                'Import events from additional Meetup groups ...')
            time.sleep(2)
            for group in extra_groups:
                Event.objects.pull_from_meetup(group)

        # import photos
        show_message('Start importing your existing photos from the web ...')
        time.sleep(2)

        Photo.objects.import_from_twitter()
        Photo.objects.import_from_wiki()
        Photo.objects.import_from_instagram()
        Photo.objects.import_from_instagram_tag()
        Photo.objects.import_from_flickr()

        show_message(
            '✅ Done! I updated the database')
        time.sleep(2)
