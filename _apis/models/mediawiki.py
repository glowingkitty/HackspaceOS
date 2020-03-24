import time

import requests

from _setup.models import Config, Log
from _setup.tests.test_setup import SetupTestConfig


class MediaWiki():
    def __init__(self, url=Config('BASICS.WIKI.API_URL').value, show_log=True, test=False):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.url = url
        self.setup_done = True if url else False
        self.help = 'https://www.mediawiki.org/wiki/API:Main_page'
        self.test = test

    @property
    def config(self):
        return Config('BASICS.WIKI').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _setup.models import Log
        import json

        try:
            if not self.url:
                # try to find the url based on the website domain
                domain = Config('WEBSITE.DOMAIN').value
                if domain and requests.get('https://'+domain+'/api.php').status_code == 200:
                    self.url = 'https://' + domain + '/api.php'
                else:
                    Log().show_messages(
                        ['Let\'s add your hackspaces Wiki to the search!'])

                    Log().show_message(
                        'What is the API URL of your Wiki?')
                    self.url = SetupTestConfig(
                        'BASICS.WIKI.API_URL').value if self.test else input()
                    while not self.url:
                        self.url = input()

                with open('_setup/config.json') as json_config:
                    config = json.load(json_config)
                    config['BASICS']['WIKI']['API_URL'] = self.url

                with open('_setup/config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            Log().show_message('MediaWiki setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    def search(self, query, limit=5):
        self.log('search()')

        if not self.url:
            self.log(
                '--> BASICS.WIKI.API_URL not found in config.json -> BASICS - Please add your WIKI.API_URL first.')
            return []

        # search in the Noisebridge wiki -> returns the search suggestions of the mini search bar on the top right
        # test if wiki api is accessible
        response = requests.get(self.url+'?action=opensearch&format=json&formatversion=2&search=' +
                                query+'&namespace=0&limit='+str(limit)+'&suggest=true')
        if (response.status_code != 200) or (self.url != response.url.split('?')[0]):
            self.log('-> ERROR: Wiki API didnt respond correctly. Maybe the URL is wrong? (Statuscode: {}, Response-URL: {})'.format(
                response.status_code, response.url))
            raise

        response_json = response.json()
        result_names = response_json[1]
        result_urls = response_json[3]

        results = []
        for idx, val in enumerate(result_names):
            results.append({
                'icon': 'wiki',
                'name': val,
                'url': result_urls[idx]
            })

        return results

    def boolean_is_image(self, image_url):
        image_url = image_url.lower()

        if image_url.endswith('.jpg') or image_url.endswith('.png'):
            return True
        else:
            return False

    def save_wiki_photo(self, photo):
        from _apis.models import Scraper
        from _database.models import Photo
        from dateutil.parser import parse
        from datetime import datetime
        from _setup.models import Config

        if not self.url:
            self.log(
                '--> BASICS.WIKI.API_URL not found in config.json -> BASICS - Please add your WIKI_API_URL first.')
            return

        if self.boolean_is_image(photo['url']) == True:
            # open url in selenium, test if image is on blocked list, else save low resolution image url
            browser = Scraper(
                photo['descriptionurl'], scraper_type='selenium', auto_close_selenium=False).selenium
            save_image = True
            try:
                pages_with_image = browser.find_element_by_id(
                    'mw-imagepage-section-linkstoimage').text.split('\n', 1)[1]
                for blocked_page in Config('BASICS.WIKI.PHOTOS_IGNORE_PAGES').value:
                    if blocked_page in pages_with_image:
                        save_image = False
                        break
            except:
                self.log(
                    '--> mw-imagepage-section-linkstoimage not found - coudlnt check if image url is blocked')

            if save_image == False:
                self.log('--> Skipped photo. URL on WIKI.PHOTOS_IGNORE_PAGES list')

            elif Photo.objects.filter(url_post=photo['descriptionurl']).exists() == True:
                self.log('--> Skipped photo. Already exists.')
                browser.close()
                return 'Skipped'

            else:
                try:
                    url_image = browser.find_element_by_class_name(
                        'mw-thumbnail-link').get_attribute('href')
                except:
                    url_image = photo['url']

                Photo(
                    text_description_en_US=photo['canonicaltitle'] if 'canonicaltitle' in photo else None,
                    url_image=url_image,
                    url_post=photo['descriptionurl'],
                    str_source='Wiki',
                    int_UNIXtime_created=round(
                        datetime.timestamp(parse(photo['timestamp']))),
                ).save()
                self.log('--> New photo saved')
                browser.close()

                return 'Saved'

    def import_photos(self, WIKI_API_URL=Config('BASICS.WIKI.API_URL').value):
        # API documentation: https://www.mediawiki.org/wiki/API:Allimages
        self.log('import_photos()')
        from _database.models import Photo
        from _setup.models import Config
        from _setup.models import Log
        import requests
        import time

        if WIKI_API_URL:
            Log().show_message(
                '✅ Found BASICS.WIKI.API_URL - Start importing photos from your Wiki ...')
            time.sleep(2)
            if requests.get(WIKI_API_URL).status_code != 200:
                Log().show_message(
                    'WARNING: I can\'t access your Wiki. Is the API_URL correct? Will skip importing photos from your Wiki for now.')
                time.sleep(4)
                return
        else:
            Log().show_message(
                'WARNING: Can\'t find BASICS.WIKI.API_URL in your config.json. Will skip importing photos from your Wiki for now.')
            time.sleep(4)
            return

        parameter = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'list': 'allimages',
            'aisort': 'timestamp',
            'aidir': 'descending',
            'ailimit': '500' if not self.test else '5',
            'aiminsize': '50000',  # minimum 50kb size, to filter out small logos/icons
            'aiprop': 'timestamp|canonicaltitle|url|user'
        }
        response_json = requests.get(WIKI_API_URL, params=parameter).json()

        skipped_photos_counter = 0

        # for every photo...
        for photo in response_json['query']['allimages']:
            if skipped_photos_counter < 5:
                status = self.save_wiki_photo(photo)
                if status == 'Skipped':
                    skipped_photos_counter += 1

        if not self.test:
            while 'continue' in response_json and 'aicontinue' in response_json['continue'] and skipped_photos_counter < 5:
                response_json = requests.get(
                    WIKI_API_URL, params={**parameter, **{'aicontinue': response_json['continue']['aicontinue']}}).json()

                for photo in response_json['query']['allimages']:
                    status = self.save_wiki_photo(photo)
                    if status == 'Skipped':
                        skipped_photos_counter += 1

        if skipped_photos_counter >= 5:
            self.log('No new photos it seems.')

        self.log('Complete! All photos processed! Now {} photos'.format(
            Photo.objects.count()))
