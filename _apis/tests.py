from django.test import TestCase
from _apis.models import *
from _database.models import Event
import time
import unittest


class DiscourseTestCase(TestCase):
    def test_search(self):
        search_results = Discourse().search('3d print')
        self.assertTrue(len(search_results) > 0)
        self.assertTrue(search_results[0]['name'])

    def test_create_and_delete_post(self):
        new_post_url = Discourse().create_post('This is an automated test',
                                               'Unittests are awesome.', 'events')
        self.assertTrue(type(new_post_url) == str)
        self.assertTrue(Discourse().delete_post(new_post_url) == True)

    def test_get_categories(self):
        categories = Discourse().get_categories()
        self.assertTrue(type(categories) == list)
        self.assertTrue(len(categories) > 0)

    def test_get_category_id(self):
        category_id = Discourse().get_category_id('events')
        self.assertTrue(category_id == None or type(category_id) == int)

    def test_get_category_posts(self):
        self.assertTrue(type(Discourse().get_category_posts('events')) == list)

    def test_get_post_details(self):
        # get a post
        categories = Discourse().get_categories()
        posts = Discourse().get_category_posts(categories[0])
        slug = posts[0]['slug']
        post_details = Discourse().get_post_details(slug)
        self.assertTrue('id' in post_details)
        self.assertTrue('cooked' in post_details)

    def test_get_users(self):
        users = Discourse().get_users()
        self.assertTrue(type(users) == list)
        self.assertTrue('user' in users[0])


class GooglePhotosTestCase(TestCase):
    def test_photos(self):
        photos = GooglePhotos(
            ['https://photos.google.com/share/AF1QipNdUmxDzWRLtsxIcWIugAjr5gN_GBPd18XpfSkeSWteXPwqJC-c5_HTYjy-dQJPXQ?key=WVA4ekpWZE1HMlNvdzdSVkJGLS1yZTZaQ1Q3bW13']).photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)


class InstagramTestCase(TestCase):
    def test_photos(self):
        photos = Instagram('noisebridgehackerspace',
                           '#noisebridgehackerspace').photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)


class TwitterTestCase(TestCase):
    def test_photos(self):
        photos = Twitter('noisebridge', '#noisebridge').photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)


class TelegramTestCase(TestCase):
    def test_message(self):
        if Telegram().setup_done:
            response = Telegram().message('This is a test. Hello World.')
            self.assertEqual(response, True)


class AwsTestCase(TestCase):
    def test_s3_upload_and_delete(self):
        with open('README.md', 'rb') as f:
            file_url = Aws().upload(f)
            self.assertTrue(type(file_url) == str)
            Aws().delete('README.md')


class FlickrTestCase(TestCase):
    def test_photos(self):
        photos = Flickr(
            'https://www.flickr.com/groups/noisebridge/pool/', page=1).photos
        self.assertTrue(len(photos) > 0)
        self.assertTrue(len(photos[0]['URL_image']) > 20)
        self.assertTrue(len(photos[0]['URL_post']) > 20)
        self.assertTrue(photos[0]['INT_UNIX_taken'] != None)


class MediaWikiTestCase(TestCase):
    def test_seach(self):
        search_results = MediaWiki().search('electronic')
        self.assertTrue(type(search_results) == list)
        self.assertTrue(len(search_results) ==
                        0 or 'name' in search_results[0])


class MeetupTestCase(TestCase):
    def test_events(self):
        events = Meetup('noisebridge').events
        self.assertTrue(len(events) > 0)
        self.assertTrue(events[0]['str_name_en_US'] != None)
        self.assertTrue(events[0]['url_meetup_event'] != None)

    def test_create_and_delete(self):
        event = Event.objects.all()[0]
        int_start_time = event.int_UNIXtime_event_start
        event.int_UNIXtime_event_start = round(time.time()+600)

        event = Meetup().create(event=event, publish_status='draft')
        self.assertTrue(event.url_meetup_event != None)

        event = Meetup().delete(event=event)
        event.int_UNIXtime_event_start = int_start_time
        self.assertTrue(event.url_meetup_event == None)


class SearchTestCase(TestCase):
    def test_query(self):
        search_results = Search().query('electronic')
        self.assertTrue(type(search_results) == list)
        self.assertTrue(len(search_results) ==
                        0 or 'name' in search_results[0])
