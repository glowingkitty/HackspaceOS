from django.test import TestCase
from _apis.models import Twitter


class TwitterTestCase(TestCase):
    def test_photos(self):
        photos = Twitter('noisebridge', '#noisebridge').photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)
