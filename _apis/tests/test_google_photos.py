from django.test import TestCase
from _apis.models import GooglePhotos


class GooglePhotosTestCase(TestCase):
    def test_photos(self):
        photos = GooglePhotos(
            ['https://photos.google.com/share/AF1QipNdUmxDzWRLtsxIcWIugAjr5gN_GBPd18XpfSkeSWteXPwqJC-c5_HTYjy-dQJPXQ?key=WVA4ekpWZE1HMlNvdzdSVkJGLS1yZTZaQ1Q3bW13']).photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)
