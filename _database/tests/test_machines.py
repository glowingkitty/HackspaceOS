from django.test import TestCase
from _database.models import Machine


class MachinesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Machine(str_name_en_US='Laser Cutter').save()

    def test_LIST__search_results(self):
        self.assertTrue(len(Machine.objects.LIST__search_results()) > 0)
