import time
from _setup.models import Config
from _setup.models import Log
from _setup.tests.test_setup import SetupTestConfig
from selenium.webdriver.common.keys import Keys


class GooglePhotos():
    def __init__(
            self,
            urls=Config('SOCIAL.GOOGLE_PHOTOS_ALBUM_URLS').value,
            show_log=True,
            test=False):
        self.logs = ['self.__init__']
        self.test = test
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
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _setup.models import Log
        import json

        try:
            if not self.urls:
                Log().show_messages(
                    ['Let\'s setup Google Photos - to automatically import photos from Google Photos into your websites photo section.'])

                Log().show_message(
                    'Enter the URLs on Google Photos which we should scrape - for example an album: (separated by ,)')
                self.urls = SetupTestConfig(
                    'SOCIAL.GOOGLE_PHOTOS_ALBUM_URLS').value[0] if self.test else input()
                if not self.urls and not self.test:
                    raise KeyboardInterrupt

                with open('_setup/config.json') as json_config:
                    config = json.load(json_config)
                    config['SOCIAL']['GOOGLE_PHOTOS_ALBUM_URLS'] = self.urls.replace(', ', ',').split(
                        ',')

                with open('_setup/config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            Log().show_message('Google Photos setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    def import_photos(self, test=False):
        from _database.models import Photo

        # check if google photos urls exist
        if len(self.urls) > 0:
            self.log(
                '-> ✅ Found GOOGLE_PHOTOS_ALBUM_URLS - Start importing photos from Google Photos ...')
        else:
            self.log('-> ERROR: Can\'t find GOOGLE_PHOTOS_ALBUM_URLS in your config.json. Will skip importing photos from Google Photos for now.')
            return

        from _apis.models import Scraper
        from dateutil.parser import parse

        photos = []
        if not self.urls:
            self.log('-> ERROR: url not defined')
            return None

        for URL in self.urls:
            self.scraper = Scraper(
                URL, scraper_type='selenium', auto_close_selenium=False)

            # open first photo
            self.scraper.selenium.find_element_by_class_name('RY3tic').click()
            time.sleep(2)

            # get most important informations from photo page
            self.scraper.selenium.find_element_by_xpath(
                "//button[@title='Info']").click()
            time.sleep(1)

            # add photo
            previous_url = ''
            while self.scraper.selenium.current_url != previous_url:
                tried = 0
                while tried < 3:
                    try:
                        new_photo = {
                            'URL_image': self.scraper.selenium.find_elements_by_class_name(
                                'ukWswc')[1].find_element_by_class_name('SzDcob').get_attribute('src'),
                            'URL_post': self.scraper.selenium.current_url,
                            'INT_UNIX_taken': round(parse(self.scraper.selenium.find_elements_by_class_name(
                                'ukWswc')[1].find_element_by_class_name('SzDcob').get_attribute('aria-label').split(' – ')[-1]).timestamp())
                        }
                        photos.append(new_photo)
                        self.log('Scraped {} photos...'.format(
                            len(photos)))
                        previous_url = self.scraper.selenium.current_url

                        # load next photo & repeat
                        self.scraper.selenium.find_element_by_tag_name(
                            'body').send_keys(Keys.ARROW_RIGHT)
                        time.sleep(1)

                        if Photo.objects.filter(url_post=new_photo['URL_post']).exists() == False:
                            Photo(
                                url_image=new_photo['URL_image'],
                                url_post=new_photo['URL_post'],
                                str_source='Google Photos',
                                int_UNIXtime_created=new_photo['INT_UNIX_taken']
                            ).save()
                            self.log('--> New photo saved')
                        else:
                            self.log('--> Photo exist. Skipped...')

                        tried = 0
                    except:
                        tried += 1
                        time.sleep(1)

            self.scraper.selenium.close()
