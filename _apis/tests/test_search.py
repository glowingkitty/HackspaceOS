from django.test import TestCase
from _apis.models import Search


class SearchTestCase(TestCase):
    def test_query(self):
        search_results = Search().query('electronic')
        self.assertTrue(type(search_results) == list)
        self.assertTrue(len(search_results) ==
                        0 or 'name' in search_results[0])
