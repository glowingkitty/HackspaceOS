import time
from _setup.config import Config
from _setup.log import log


class GooglePhotos():
    def __init__(self, urls=Config('SOCIAL.GOOGLE_PHOTOS_ALBUM_URLS').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.setup_done = True if urls else False
        self.urls = urls

    @property
    def config(self):
        return {"GOOGLE_PHOTOS_ALBUM_URLS": Config('SOCIAL.GOOGLE_PHOTOS_ALBUM_URLS').value}

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _setup.asci_art import show_message, show_messages
        import json

        try:
            if not self.urls:
                show_messages(
                    ['Let\'s setup Google Photos - to automatically import photos from Google Photos into your websites photo section.'])

                show_message(
                    'Enter the URLs on Google Photos which we should scrape - for example an album: (separated by ,)')
                self.urls = input()
                while not self.urls:
                    self.urls = input()

                with open('config.json') as json_config:
                    config = json.load(json_config)
                    config['SOCIAL']['GOOGLE_PHOTOS_ALBUM_URLS'] = self.urls.replace(', ', ',').split(
                        ',')

                with open('config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('Google Photos setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    @property
    def photos(self):
        from _apis.models import Scraper
        from dateutil.parser import parse

        photos_details = []
        if not self.urls:
            self.log('-> ERROR: url not defined')
            return None

        for URL in self.urls:
            self.scraper = Scraper(
                URL, scraper_type='selenium', scroll_down=5)
            photos = self.scraper.select('RY3tic', 'class')

            photos_details = photos_details + [{
                'URL_image': str(x['data-latest-bg']).split('=')[0],
                'URL_post':'https://photos.google.com'+x.parent['href'][1:],
                'TEXT_description':None,
                'INT_UNIX_taken':parse(x.parent['aria-label'].split(' - ')[-1]).timestamp()
            } for x in photos]

        return photos_details

    def import_photos(self, test=False):
        from _database.models import Photo

        # check if google photos urls exist
        if len(self.urls) > 0:
            self.log(
                '-> ✅ Found GOOGLE_PHOTOS_ALBUM_URLS - Start importing photos from Google Photos ...')
        else:
            self.log('-> ERROR: Can\'t find GOOGLE_PHOTOS_ALBUM_URLS in your config.json. Will skip importing photos from Google Photos for now.')
            return

        photos = self.photos
        for photo in photos:
            if Photo.objects.filter(url_post=photo['URL_post']).exists() == False:
                Photo(
                    url_image=photo['URL_image'],
                    url_post=photo['URL_post'],
                    str_source='Google Photos',
                    int_UNIXtime_created=photo['INT_UNIX_taken']
                ).save()
                self.log('--> New photo saved')
            else:
                self.log('--> Photo exist. Skipped...')
