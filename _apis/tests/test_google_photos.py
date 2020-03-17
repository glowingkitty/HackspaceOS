from django.test import TestCase
from _apis.models import GooglePhotos


class GooglePhotosTestCase(TestCase):
    def test_photos(self):
        GooglePhotos(
            ['https://photos.google.com/share/AF1QipNdUmxDzWRLtsxIcWIugAjr5gN_GBPd18XpfSkeSWteXPwqJC-c5_HTYjy-dQJPXQ?key=WVA4ekpWZE1HMlNvdzdSVkJGLS1yZTZaQ1Q3bW13'], test=True).import_photos()
