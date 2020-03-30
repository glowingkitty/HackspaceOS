from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the database"

    def handle(self, *args, **options):
        from _database.models import Event, Space, Consensus, Person, Wish, Photo, Project
        from _setup.models import Config
        from _setup.models import Secret
        from _setup.models import Log
        import time
        import requests

        Log().show_message('I will now start to update your database, based on your secrets.json and config.json. Depending on your settings, amount of events & photos & Discourse entries from your  this can take everything from seconds to hours (?). But you can already test your website - by opening a new terminal window and run "python manage.py runserver 0.0.0.0:8000" - and open 0.0.0.0:8000 in your web browser.')
        time.sleep(5)

        # create default space for events
        if not Space.objects.filter(str_name_en_US=Config('EVENTS.EVENTS_SPACE_DEFAULT').value).exists():
            Space(
                str_name_en_US=Config('EVENTS.EVENTS_SPACE_DEFAULT').value,
                text_description_en_US='Work on cool projects in our largest community area - the {}!'.format(
                    Config('EVENTS.EVENTS_SPACE_DEFAULT').value)
            ).save()

        # import data from Discourse
        Person.objects.import_from_discourse()
        Consensus.objects.import_from_discourse()
        Project.objects.import_from_discourse()

        # import events from Meetup
        Event.objects.import_from_meetup()
        extra_groups = Config('EVENTS.EXTRA_MEETUP_GROUPS').value
        if extra_groups:
            Log().show_message(
                'Import events from additional Meetup groups ...')
            time.sleep(2)
            for group in extra_groups:
                Event.objects.import_from_meetup(group)

        # import photos
        Log().show_message('Start importing your existing photos from the web ...')
        time.sleep(2)

        Photo.objects.import_from_google_photos()
        Photo.objects.import_from_twitter()
        Photo.objects.import_from_wiki()
        Photo.objects.import_from_instagram()
        Photo.objects.import_from_flickr()

        Log().show_message(
            '✅ Done! I updated the database')
        time.sleep(2)
