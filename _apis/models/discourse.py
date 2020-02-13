from log import log
import requests
from secrets import Secret
import time


class Discourse():
    def __init__(
            self,
            url=Secret('DISCOURSE.DISCOURSE_URL').value,
            api_key=Secret('DISCOURSE.API_KEY').value,
            api_username=Secret('DISCOURSE.API_USERNAME').value,
            show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.url = url
        self.api_key = api_key
        self.api_username = api_username
        self.setup_done = True if url else False
        self.help = 'https://docs.discourse.org/'

    @property
    def config(self):
        return Secret('DISCOURSE').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            if not self.url or not self.api_key or not self.api_username:
                show_messages(
                    ['Let\'s setup Discourse - to import projects, events, and more to your website from your Discourse community.'])

            if not self.url:
                show_message(
                    'What is the URL of your Discourse group?')
                self.url = input()
                while not self.url:
                    self.url = input()

            if not self.api_key:
                show_message(
                    'And what is your API key?')
                self.api_key = input()

            if self.api_key:
                show_message(
                    'And your API username?')
                self.api_username = input()

            with open('secrets.json') as json_secrets:
                secrets = json.load(json_secrets)
                secrets['DISCOURSE']['DISCOURSE_URL'] = self.url
                if self.api_key:
                    secrets['DISCOURSE']['API_KEY'] = self.api_key
                if self.api_username:
                    secrets['DISCOURSE']['API_USERNAME'] = self.api_username

            with open('secrets.json', 'w') as outfile:
                json.dump(secrets, outfile, indent=4)

            show_message('Discourse setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    def search(self, query, limit=5):
        self.log('search()')

        results = []
        response_json = requests.get(
            self.url+'/search/query.json?term='+query).json()
        if 'topics' in response_json:
            for post in response_json['topics']:
                results.append({
                    'icon': 'discourse',
                    'name': post['title'],
                    'url': self.url+'/t/'+str(post['id'])
                })

        return results

    def create_post(self, str_headline, str_text, str_category):
        self.log('create_post()')
        from html import unescape
        import emoji

        if not self.api_key:
            self.log('--> Failed: DISCOURSE.API_KEY not set')
            return None

        response = requests.post(self.url+'posts.json',
                                 headers={
                                     'content-type': 'application/json'
                                 }, params={
                                     'api_key': self.api_key,
                                     'api_username': self.api_username,
                                     'title': emoji.get_emoji_regexp().sub(u'', unescape(str_headline)),
                                     'raw': str_text,
                                     'category': self.get_category_id(str_category)
                                     # TODO add event details
                                     #  'event': {'start': '2019-12-13T15:00:00+00:00', 'end': '2019-12-13T19:00:00+00:00'}
                                 })

        if response.status_code == 200:
            response_json = response.json()
            # self.log(response_json)
            if self.url.endswith('/'):
                url = self.url+'t/'+str(response_json['topic_id'])
                self.log('--> Created Discourse post: '+url)
                return url
            else:
                url = self.url+'/t/'+str(response_json['topic_id'])
                self.log('--> Created Discourse post: '+url)
                return url
        else:
            self.log(response.status_code)
            self.log(response.json())
            return False

    def delete_post(self, post_url):
        self.log('delete_post()')
        if not self.api_key:
            self.log('--> Failed: DISCOURSE.API_KEY not set')
            return None

        # get ID of post
        response = requests.get(post_url)
        if response.status_code != 200:
            self.log('--> Couldn\'t find post on Discourse. Skipped deleting.')
            return False
        topic_id = response.url.split('/')[-1]

        response = requests.delete(self.url+'/t/'+topic_id+'.json',
                                   headers={
                                       'content-type': 'application/json'
                                   }, params={
                                       'api_key': self.api_key,
                                       'api_username': self.api_username
                                   })
        if response.status_code == 200:
            self.log('--> Deleted')
            return True
        else:
            self.log('--> Not deleted')
            self.log(response.status_code)
            self.log(response.json())
            return False

    def get_categories(self, output='list'):
        self.log('get_categories()')
        response = requests.get(
            self.url+'categories.json', headers={'Accept': 'application/json'})
        if output == 'list' and response.status_code == 200:
            return [x['slug'] for x in response.json()['category_list']['categories']]
        else:
            return response.json()

    def get_category_id(self, str_name_en_US):
        categories = self.get_categories(output='json')[
            'category_list']['categories']
        for category in categories:
            if category['name'] == str_name_en_US or category['slug'] == str_name_en_US:
                return category['id']
        else:
            return None

    def get_category_posts(self, category, all_pages=False):
        self.log('get_category_posts()')
        response_json = requests.get(
            self.url+'c/'+category+'.json', headers={'Accept': 'application/json'}).json()

        if not 'topic_list' in response_json:
            self.log('-> no posts returned. Category doesnt seem to exist?')
            return []

        if all_pages == True:
            results = response_json['topic_list']['topics']
            page = 1

            while len(response_json['topic_list']['topics']) > 0:
                response_json = requests.get(self.url+'c/'+category +
                                             '.json?page='+str(page), headers={'Accept': 'application/json'}).json()
                results += response_json['topic_list']['topics']
                page += 1

            return results

        return response_json['topic_list']['topics']

    def get_post_details(self, slug):
        print(self.url)
        self.log('get_post_details()')
        if 'http' in slug:
            slug = slug.split('/')[-1]
        response_json = requests.get(
            self.url+'t/'+slug+'.json', headers={'Accept': 'application/json'}).json()

        if not 'post_stream' in response_json:
            self.log('-> No post found')
            return None

        return response_json['post_stream']['posts'][0]

    def get_users(self, sort='days_visited'):
        self.log('get_users()')
        results = []
        response_json = requests.get(
            self.url+'/directory_items.json?period={}&order={}'.format('all', sort), headers={'Accept': 'application/json'}).json()
        results += response_json['directory_items']

        page = 1
        while len(response_json['directory_items']) > 0:
            response_json = requests.get(
                self.url+'/directory_items.json?page={}&period={}&order={}'.format(page, 'all', sort), headers={'Accept': 'application/json'}).json()
            results += response_json['directory_items']
            page += 1

        return results
