from django.test import TestCase
from _apis.models import Discourse


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
