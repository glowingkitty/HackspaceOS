from django.test import TestCase
from _apis.models import MediaWiki


class MediaWikiTestCase(TestCase):
    def test_seach(self):
        search_results = MediaWiki().search('electronic')
        self.assertTrue(type(search_results) == list)
        self.assertTrue(len(search_results) ==
                        0 or 'name' in search_results[0])
