import time

from _setup.models import Config, Log


class Flickr():
    def __init__(
            self,
            url=Config('SOCIAL.FLICKR_URL').value,
            page=None,
            show_log=True,
            test=False):
        from PyWebScraper import Scraper
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.page = 1 if test else page
        self.setup_done = True if url else False
        self.url = url
        self.test = test

    @property
    def config(self):
        return {"FLICKR_URL": Config('SOCIAL.FLICKR_URL').value}

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
                Log().show_messages(
                    ['Let\'s setup Flickr - to automatically import photos from Flickr into your websites photo section.'])

                Log().show_message(
                    'Enter the URL on Flickr which we should scrape - for example an album:')
                self.url = None if self.test else input()
                if not self.url and not self.test:
                    raise KeyboardInterrupt

                with open('_setup/config.json') as json_config:
                    config = json.load(json_config)
                    config['SOCIAL']['FLICKR_URL'] = self.url

                with open('_setup/config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            Log().show_message('Flickr setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    @property
    def photos(self):
        from PyWebScraper import Scraper
        from dateutil.parser import parse

        photos_list = []

        if not self.url:
            self.log('-> ERROR: Flickr URL not defined')
            return None

        if self.page:
            pages = [self.page]
        else:
            pages = range(1, 101)

        for page in pages:
            self.log('-> process page '+str(page))
            # get all the photos from the page
            if self.url.endswith('/'):
                url = self.url+'page'+str(page)
            else:
                url = self.url+'/page'+str(page)
            photos = Scraper(url, scraper_type='selenium').select(
                'view photo-list-photo-view requiredToShowOnServer awake', 'class')

            if len(photos) == 0:
                return photos_list

            for photo in photos:
                details = {
                    'URL_image': 'https://'+photo['style'].split('background-image:')[-1][7:-3],
                    'URL_post': 'https://flickr.com'+photo.findChildren('div')[0].findChildren('div')[0].findChildren('a')[0]['href']
                }
                # open the photo detail page for the remaining details
                self.log('-> Processing detail page: ' +
                         str(details['URL_post']))
                detail_page = Scraper(details['URL_post'])
                if len(detail_page.select('meta-field photo-desc')) > 0:
                    details['TEXT_description'] = detail_page.select(
                        'meta-field photo-desc')[0].text.replace('\n', '')
                else:
                    details['TEXT_description'] = None

                details['INT_UNIX_taken'] = round(parse(detail_page.select(
                    'date-taken-label')[0].text.replace('\n', '').replace('\t', '').split(' on ')[1]).timestamp())
                photos_list.append(details)

        return photos_list

    def import_photos(self):
        self.log('import_photos()')
        from _database.models import Photo

        photos = self.photos
        if photos:
            for json_entry in photos:
                if Photo.objects.filter(url_post=json_entry['URL_post']).exists() == False:
                    Photo(
                        text_description_en_US=json_entry['TEXT_description'],
                        url_image=json_entry['URL_image'],
                        url_post=json_entry['URL_post'],
                        str_source='Flickr',
                        int_UNIXtime_created=json_entry['INT_UNIX_taken'],
                    ).save()
                    self.log('-> new photo saved')
                else:
                    self.log('-> Photo already exists')
