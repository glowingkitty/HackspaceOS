from django.test import TestCase
from _database.models import Guilde


class GuildesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Guilde(str_name_en_US='Laser Guilde').save()

    def test_LIST__search_results(self):
        self.assertTrue(len(Guilde.objects.LIST__search_results()) > 0)
