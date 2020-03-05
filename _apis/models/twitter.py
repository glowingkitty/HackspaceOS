import time
from _setup.config import Config
from _setup.log import log


class Twitter():
    def __init__(self, username=Config('SOCIAL.SOCIAL_NETWORKS', username_for='twitter.com').value, hashtag=Config('SOCIAL.HASHTAG').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.help = 'https://github.com/bisguzar/twitter-scraper'
        self.username = username
        self.hashtag = hashtag.replace('#', '') if hashtag else None
        self.setup_done = True if username or hashtag else False

    @property
    def config(self):
        return {"username": Config('SOCIAL.SOCIAL_NETWORKS', username_for='twitter.com').value, "hashtag": Config('SOCIAL.HASHTAG').value}

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _setup.asci_art import show_message, show_messages
        import json

        try:
            if not self.username or not self.hashtag:
                show_messages(
                    ['Let\'s setup Twitter - to automatically import photos from Twitter into your websites photo section.'])

                if not self.username:
                    show_message(
                        'What is the username of your hackspace on Twitter?')
                    self.username = input()
                    if 'twitter.com/' in self.username:
                        self.username = self.username.split(
                            'twitter.com/')[1].replace('/', '')

                if not self.hashtag:
                    show_message(
                        'What hashtag does your hackspace use on Twitter (and Instagram)?')
                    self.hashtag = input().replace('#', '')

                with open('config.json') as json_config:
                    config = json.load(json_config)

                    if self.username:
                        for entry in config['SOCIAL']['SOCIAL_NETWORKS']:
                            if 'twitter.com/' in entry['url']:
                                break
                        else:
                            config['SOCIAL']['SOCIAL_NETWORKS'].append({
                                "name": "Twitter",
                                "url": "https://twitter.com/"+self.username+'/'
                            })

                    config['SOCIAL']['HASHTAG'] = self.hashtag

                with open('config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('Twitter setup complete.')

        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    @property
    def photos(self):
        # get photos from twitter page and hashtag
        from twitter_scraper import get_tweets

        tweets = []
        if self.username:
            for tweet in get_tweets(self.username):
                if tweet['text'] and 'pic.twitter.com/' in tweet['text'] and tweet not in tweets and tweet['entries']['photos'] and tweet['time']:
                    tweets.append(tweet)

        if self.hashtag:
            for tweet in get_tweets('#'+self.hashtag):
                if tweet['text'] and 'pic.twitter.com/' in tweet['text'] and tweet not in tweets and tweet['entries']['photos'] and tweet['time']:
                    tweets.append(tweet)

        self.log('-> found {} photos'.format(len(tweets)))
        return [{
            'TEXT_description': x['text'].split('pic.twitter.com/')[0],
            'URL_image':x['entries']['photos'][0],
            'URL_post':'https://pic.twitter.com/'+x['text'].split('pic.twitter.com/')[1],
            'INT_UNIX_taken':round(x['time'].timestamp())
        } for x in tweets]

    def import_photos(self, test=False):
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
                        str_source='Twitter',
                        int_UNIXtime_created=json_entry['INT_UNIX_taken'],
                    ).save()
                    self.log('-> new photo saved')
                else:
                    self.log('-> Photo already exists')
