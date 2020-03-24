from django.test import TestCase

from _database.models import Photo


class PhotosTestCase(TestCase):
    def test_import_from_google_photos(self):
        Photo.objects.import_from_google_photos(test=True)

    def test_import_from_twitter(self):
        Photo.objects.import_from_twitter(test=True)

    def test_import_from_wiki(self):
        Photo.objects.import_from_wiki(test=True)

    def test_import_from_flickr(self):
        Photo.objects.import_from_flickr(test=True)

    def test_import_from_instagram(self):
        Photo.objects.import_from_instagram(test=True)

    def test_count_overview(self):
        self.assertTrue(type(Photo.objects.count_overview()) == dict)

    def test_random(self):
        self.assertTrue(type(Photo.objects.random()) == list)
