from django.test import TestCase

from _apis.models import Flickr


class FlickrTestCase(TestCase):
    def test_photos(self):
        photos = Flickr(
            'https://www.flickr.com/groups/noisebridge/pool/', test=True).photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)
