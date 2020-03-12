from django.test import TestCase
from _apis.models import Meetup
from _database.models import Event
import time


class MeetupTestCase(TestCase):
    def setUp(self):
        Event.objects.import_from_meetup(slug='noisebridge')

    def test_events(self):
        events = Meetup('noisebridge').events
        self.assertTrue(len(events) > 0)
        self.assertTrue(events[0]['str_name_en_US'] != None)
        self.assertTrue(events[0]['url_meetup_event'] != None)

    def test_create_and_delete(self):
        event = Event.objects.all()[0]
        int_start_time = event.int_UNIXtime_event_start
        event.int_UNIXtime_event_start = round(time.time()+600)

        event = Meetup().create(event=event, publish_status='draft')
        self.assertTrue(event.url_meetup_event != None)

        event = Meetup().delete(event=event)
        event.int_UNIXtime_event_start = int_start_time
        self.assertTrue(event.url_meetup_event == None)
