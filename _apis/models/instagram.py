import time
from config import Config
from log import log


class Instagram():
    def __init__(self, username=Config('SOCIAL.SOCIAL_NETWORKS', username_for='instagram.com').value, hashtag=Config('SOCIAL.HASHTAG').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.help = 'https://github.com/rarcega/instagram-scraper'
        self.username = username
        self.hashtag = hashtag.replace('#', '') if hashtag else None
        self.setup_done = True if username or hashtag else False

    @property
    def config(self):
        return {"username": Config('SOCIAL.SOCIAL_NETWORKS', username_for='instagram.com').value, "hashtag": Config('SOCIAL.HASHTAG').value}

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            if not self.username or not self.hashtag:
                show_messages(
                    ['Let\'s setup Instagram - to automatically import photos from Instagram into your websites photo section.'])

                if not self.username:
                    show_message(
                        'What is the username of your hackspace on Instagram?')
                    self.username = input()
                    if 'instagram.com/' in self.username:
                        self.username = self.username.split(
                            'instagram.com/')[1].replace('/', '')

                if not self.hashtag:
                    show_message(
                        'What hashtag does your hackspace use on Instagram (and Twitter)?')
                    self.hashtag = input().replace('#', '')

                with open('config.json') as json_config:
                    config = json.load(json_config)

                    if self.username:
                        for entry in config['SOCIAL']['SOCIAL_NETWORKS']:
                            if 'instagram.com/' in entry['url']:
                                break
                        else:
                            config['SOCIAL']['SOCIAL_NETWORKS'].append({
                                "name": "Instagram",
                                "url": "https://www.instagram.com/"+self.username+'/'
                            })

                    config['SOCIAL']['HASHTAG'] = self.hashtag

                with open('config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('Instagram setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    @property
    def photos(self):
        # get photos from downloaded json from scraper
        # make sure cronjob is setup, to keep photos updated
        import json
        import os

        photos = []
        filepaths = []

        if self.username:
            os.system("instagram-scraper '"+self.username +
                      "' --media-metadata --media-types none --destination '_apis/models/instagram/users'")
            filepaths.append('_apis/models/instagram/users/' +
                             self.username.lower()+'.json')
        if self.hashtag:
            os.system("instagram-scraper '"+self.hashtag +
                      "' --tag --media-metadata --media-types none --destination '_apis/models/instagram/hashtags'")
            filepaths.append('_apis/models/instagram/hashtags/' +
                             self.hashtag.lower()+'.json')

        for path in filepaths:
            if os.path.isfile(path):
                with open(path) as json_file:
                    data = json.load(json_file)
                    photos = photos + [{
                        'URL_image': x['display_url'],
                        'URL_post':'https://www.instagram.com/p/'+x['shortcode'],
                        'TEXT_description':x['edge_media_to_caption']['edges'][0]['node']['text'] if len(x['edge_media_to_caption']['edges']) > 0 else None,
                        'INT_UNIX_taken':x['taken_at_timestamp']
                    } for x in data['GraphImages']]

        return photos

    def import_photos(self, test=False):
        self.log('import_photos()')
        from _database.models import Photo

        if test:
            photos = self.photos[:5]
        else:
            photos = self.photos
        if photos:
            for json_entry in photos:
                if Photo.objects.filter(url_post=json_entry['URL_post']).exists() == False:
                    Photo(
                        text_description_en_US=json_entry['TEXT_description'],
                        url_image=json_entry['URL_image'],
                        url_post=json_entry['URL_post'],
                        str_source='Instagram',
                        int_UNIXtime_created=json_entry['INT_UNIX_taken'],
                    ).save()
                    self.log('-> new photo saved')
                else:
                    self.log('-> Photo already exists')
