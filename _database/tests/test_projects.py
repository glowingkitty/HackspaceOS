from django.test import TestCase
from _database.models import Project


class ProjectsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.import_from_discourse(
            DISCOURSE_URL='https://discuss.noisebridge.info')

    def test_LIST__search_results(self):
        self.assertTrue(len(Project.objects.LIST__search_results()) > 0)
