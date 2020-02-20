from django.test import TestCase
from _database.models import Person


class PersonsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.import_from_discourse(
            DISCOURSE_URL='https://discuss.noisebridge.info')

    def test_import_from_discourse(self):
        self.assertTrue(Person.objects.count() > 0)
