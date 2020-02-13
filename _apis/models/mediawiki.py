import requests
from log import log
from config import Config
import time


class MediaWiki():
    def __init__(self, url=Config('BASICS.WIKI.API_URL').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.url = url
        self.setup_done = True if url else False
        self.help = 'https://www.mediawiki.org/wiki/API:Main_page'

    @property
    def config(self):
        return Config('BASICS.WIKI').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            if not self.url:
                # try to find the url based on the website domain
                domain = Config('WEBSITE.DOMAIN').value
                if domain and requests.get('https://'+domain+'/api.php').status_code == 200:
                    self.url = 'https://' + domain + '/api.php'
                else:
                    show_messages(
                        ['Let\'s add your hackspaces Wiki to the search!'])

                    show_message(
                        'What is the API URL of your Wiki?')
                    self.url = input()
                    while not self.url:
                        self.url = input()

                with open('config.json') as json_config:
                    config = json.load(json_config)
                    config['BASICS']['WIKI']['API_URL'] = self.url

                with open('config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('MediaWiki setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

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
