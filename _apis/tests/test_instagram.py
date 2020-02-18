from django.test import TestCase
from _apis.models import Instagram


class InstagramTestCase(TestCase):
    def test_photos(self):
        photos = Instagram('noisebridgehackerspace',
                           '#noisebridgehackerspace').photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)
