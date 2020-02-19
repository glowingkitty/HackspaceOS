from django.test import TestCase
from _database.models import Event, Space
import time


class EventsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Space(str_name_en_US='Hackatorium').save()
        Event.objects.import_from_meetup('noisebridge')

    def test_import_from_discourse(self):
        Event.objects.import_from_discourse(
            'https://discuss.noisebridge.info/')

    def test_QUERYSET__next_meeting(self):
        Event.objects.QUERYSET__next_meeting()

    def test_QUERYSET__now(self):
        Event.objects.QUERYSET__now()

    def test_QUERYSET__in_timeframe(self):
        from_time = time.time()
        up_to = from_time+(60*60*24*7)
        self.assertTrue(
            len(Event.objects.QUERYSET__in_timeframe(from_time, up_to)) > 0)

    def test_JSON__overlapping_events(self):
        # get event and then see if it shows up as overlapping
        event = Event.objects.QUERYSET__upcoming()[0]
        self.assertTrue(len(Event.objects.JSON__overlapping_events(
            event.int_UNIXtime_event_start, 120, 'Hackatorium')['overlapping_events']) > 0)

    def test_QUERYSET__in_space(self):
        event = Event.objects.QUERYSET__upcoming()[0]
        event.one_space = Space.objects.all()[0]
        event.save()
        self.assertTrue(
            len(Event.objects.QUERYSET__in_space(one_space=event.one_space)) > 0)

    def test_LIST__in_minutes(self):
        self.assertTrue(type(Event.objects.LIST__in_minutes(10)) == list)

    def test_LIST__search_results(self):
        self.assertTrue(
            type(Event.objects.all().LIST__search_results()) == list)
