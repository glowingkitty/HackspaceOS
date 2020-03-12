from django.test import TestCase
from _database.models import Space


class SpacesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Space(str_name_en_US='Hackatorium').save()
        Space(str_name_en_US='Turing Room').save()

    def test_LIST__search_results(self):
        self.assertTrue(len(Space.objects.LIST__search_results()) > 0)
