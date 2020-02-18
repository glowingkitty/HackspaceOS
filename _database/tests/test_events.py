from django.test import TestCase
from _database.models import Event


class EventsTestCase(TestCase):
    def setUp(self):
        Event.objects.import_from_meetup('noisebridge')

    def test_import_from_discourse(self):
        pass

    def test_import_from_meetup(self):
        pass

    def test_create_event_manually(self):
        pass

    def test_create_event_from_meetup(self):
        pass

    def test_QUERYSET__next_meeting(self):
        pass

    def test_QUERYSET__now(self):
        pass

    def test_QUERYSET__in_timeframe(self):
        pass

    def test_JSON__overlapping_events(self):
        pass

    def test_QUERYSET__in_space(self):
        pass

    def test_QUERYSET__by_host(self):
        pass

    def test_QUERYSET__by_guilde(self):
        pass

    def test_QUERYSET__not_approved(self):
        pass

    def test_QUERYSET__older_then_24h(self):
        pass

    def test_QUERYSET__upcoming(self):
        pass

    def test_LIST__in_minutes(self):
        pass

    def test_LIST__search_results(self):
        pass

    def test_RESPONSE__JSON(self):
        pass
