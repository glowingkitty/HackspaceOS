# by Marco Bartsch
from log import log
import time
from config import Config
from secrets import Secret
import requests
import json


class Meetup():
    def __init__(self,
                 group=Config('EVENTS.MEETUP_GROUP').value,
                 email=Secret('MEETUP.EMAIL').value,
                 password=Secret('MEETUP.PASSWORD').value,
                 client_id=Secret('MEETUP.CLIENT_ID').value,
                 client_secret=Secret('MEETUP.CLIENT_SECRET').value,
                 redirect_uri=Secret('MEETUP.REDIRECT_URI').value,
                 show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.group = group
        self.response = None
        self.email = email
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret,
        self.redirect_uri = redirect_uri
        self.setup_done = True if group else False
        self.help = 'https://www.meetup.com/meetup_api/docs/'

    @property
    def config(self):
        return {"group": Config('EVENTS.MEETUP_GROUP').value}

    @property
    def access_token(self):
        from _apis.models import Scraper
        from selenium.webdriver.common.by import By
        import requests

        # check if still usable token is saved in secrets.json - else get new one
        if Secret('MEETUP.ACCESS_TOKEN').value and Secret('MEETUP.ACCESS_TOKEN_VALID_UPTO').value > time.time()+60:
            return Secret('MEETUP.ACCESS_TOKEN').value

        # check if required fields exist
        if not self.client_id or not self.client_secret or not self.redirect_uri or not self.email or not self.password:
            self.log('-> ERROR: Meetup secrets incomplete!')
            return None

        # else: following steps to get an API token - see https://www.meetup.com/meetup_api/auth/

        # Step 1: Get code to get access token, by loggin into meetup account
        login_page = Scraper(
            'https://secure.meetup.com/oauth2/authorize?scope=basic+event_management&client_id={}&response_type=code&redirect_uri={}'.format(self.client_id, self.redirect_uri), scraper_type='selenium', auto_close_selenium=False)
        login_page.selenium.find_element(By.LINK_TEXT, 'Continue').click()
        login_page.selenium.find_element_by_id('email').send_keys(self.email)
        login_page.selenium.find_element_by_id(
            'password').send_keys(self.password)
        login_page.selenium.find_element_by_id('loginFormSubmit').click()
        code = login_page.selenium.current_url.split('code=')[1]
        login_page.selenium.close()

        # Step 2: get access token
        self.response_json = requests.post('https://secure.meetup.com/oauth2/access',
                                           params={
                                               'client_id': self.client_id,
                                               'client_secret': self.client_secret,
                                               'code': code,
                                               'response_type': 'code',
                                               'grant_type': 'authorization_code',
                                               'redirect_uri': self.redirect_uri,
                                               'scope': ['basic', 'event_management']
                                           }).json()

        if 'access_token' in self.response_json:
            with open('secrets.json') as json_file:
                secrets = json.load(json_file)
            secrets['MEETUP']['ACCESS_TOKEN'] = self.response_json['access_token']
            secrets['MEETUP']['ACCESS_TOKEN_VALID_UPTO'] = round(
                time.time()+self.response_json['expires_in'])
            with open('secrets.json', 'w') as outfile:
                json.dump(secrets, outfile, indent=4)
            return self.response_json['access_token']
        else:
            self.log(
                '-> ERROR: Failed to get Access Token - {}'.format(self.response_json))
            return None

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            if not self.group:
                ask_input = False
                space_name = Config('BASICS.NAME').value
                if requests.get('https://www.meetup.com/'+space_name.lower()).status_code == 200:
                    show_message(
                        'Is this your hackpace meetup group? (Y/N): https://www.meetup.com/'+space_name.lower())
                    reply = input()
                    if reply.lower() == 'y':
                        self.group = 'https://www.meetup.com/'+space_name.lower()
                    else:
                        ask_input = True
                else:
                    ask_input = True

                if ask_input:
                    show_messages(
                        ['Let\'s setup Meetup.com - so we can automatically import all your events from Meetup and show them on your new website.'])

                    show_message(
                        'What is the URL of your Meetup group? ')
                    self.group = input()
                    while not self.group:
                        self.group = input()

                with open('config.json') as json_config:
                    config = json.load(json_config)

                    if self.group.endswith('/'):
                        self.group = self.group[:-1]
                    config['EVENTS']['MEETUP_GROUP'] = self.group.split(
                        '/')[-1]

                    for entry in config['SOCIAL']['SOCIAL_NETWORKS']:
                        if 'meetup.com/' in entry['url']:
                            break
                    else:
                        config['SOCIAL']['SOCIAL_NETWORKS'].append({
                            "name": "Meetup",
                            "url": self.group
                        })

                with open('config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('Meetup setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    # define functions to get event details based on meetup data
    def str_name_en_US(self, event):
        return event['name']

    def int_UNIXtime_event_start(self, event):
        return round(event['time']/1000)

    def int_UNIXtime_event_end(self, event):
        return round((event['time']/1000)+(event['duration']/1000))

    def int_minutes_duration(self, event):
        return round((event['duration']/1000)/60)

    def url_featured_photo(self, event):
        return event['featured_photo']['photo_link'] if 'featured_photo' in event else event['image_url'] if 'image_url' in event and event['image_url'] else None

    def text_description_en_US(self, event):
        return event['description']

    def str_location(self, event):
        HACKERSPACE_NAME = Config('BASICS.NAME').value
        HACKERSPACE_ADDRESS = Config('PHYSICAL_SPACE.ADDRESS').value
        str_location_name = event['venue']['name'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_NAME
        str_location_street = event['venue']['address_1'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['STREET']
        str_location_zip = event['venue']['zip'] if 'venue' in event and 'zip' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['ZIP']
        str_location_city = event['venue']['city'] if 'venue' in event and 'city' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['CITY']
        str_location_countrycode = event['venue']['country'].upper() if 'venue' in event and 'country' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['COUNTRYCODE']
        return str_location_name+'\n'+str_location_street+'\n'+str_location_zip+', '+str_location_city+', '+str_location_countrycode

    def one_space(self, event):
        from _database.models import Space

        if 'how_to_find_us' in event:
            spaces = Space.objects.all()

            for space in spaces.iterator():
                if space.str_name_en_US.lower() in event['how_to_find_us'].lower():
                    return space

        # else...
        EVENTS_SPACES_OVERWRITE = Config(
            'EVENTS.EVENTS_SPACES_OVERWRITE').value
        for field in EVENTS_SPACES_OVERWRITE:
            if field in event['name']:
                return Space.objects.QUERYSET__by_name(EVENTS_SPACES_OVERWRITE[field])
        else:
            return Space.objects.QUERYSET__by_name(Config('EVENTS.EVENTS_SPACE_DEFAULT').value)

    def one_guilde(self, event):
        from _database.models import Guilde

        EVENTS_GUILDES_OVERWRITE = Config(
            'EVENTS.EVENTS_GUILDES_OVERWRITE').value

        for str_keyword in EVENTS_GUILDES_OVERWRITE:
            if str_keyword in event['name']:
                return Guilde.objects.filter(str_name_en_US=EVENTS_GUILDES_OVERWRITE[str_keyword]).first()
        else:
            return None

    def str_series_id(self, event):
        return event['series']['id'] if 'series' in event else None

    def int_series_startUNIX(self, event):
        return round(event['series']['start_date'] / 1000) if 'series' in event and 'start_date' in event['series'] else None

    def int_series_endUNIX(self, event):
        return round(event['series']['end_date'] / 1000) if 'series' in event and 'end_date' in event['series'] else None

    def text_series_timing(self, event):
        if 'series' in event and 'weekly' in event['series']:
            return 'weekly: '+str(event['series']['weekly'])
        elif 'series' in event and 'monthly' in event['series']:
            return 'monthly: '+str(event['series']['monthly'])
        else:
            return None

    def url_meetup_event(self, event):
        return event['link'] if 'link' in event else None

    def int_UNIXtime_created(self, event):
        return round(event['created']/1000)

    def int_UNIXtime_updated(self, event):
        return round(event['updated']/1000) if 'updated' in event else None

    def int_timezoneToOffset(self, timezone_name):
        from datetime import datetime
        import pytz
        return int(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()*1000)

    def list_offsetToTimezone(self, offset_ms):
        from datetime import datetime
        import pytz
        now = datetime.now(pytz.utc)  # current time
        return [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
                if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]

    def str_timezone(self, event):
        TIMEZONE_STRING = Config('PHYSICAL_SPACE.TIMEZONE_STRING').value

        if 'utc_offset' in event and event['utc_offset'] != self.int_timezoneToOffset(TIMEZONE_STRING):
            return self.list_offsetToTimezone(event['utc_offset'])

        return TIMEZONE_STRING

    @property
    def events(self):
        # Events
        # https://www.meetup.com/meetup_api/docs/:urlname/events/#list
        import requests

        self.log('events()')

        self.response = requests.get('https://api.meetup.com/'+self.group+'/events',
                                     params={
                                         'fields': ['group_key_photo', 'series', 'simple_html_description', 'rsvp_sample'],
                                         'photo-host': 'public',
                                         'page': 200,
                                         'offset': 0
                                     })

        self.response_json = self.response.json()
        if 'errors' in self.response_json and self.response_json['errors'][0]['code'] == 'group_error':
            self.log('-> ERROR: Group name doesnt exist')
            return False
        else:
            return [
                {
                    'str_name_en_US': self.str_name_en_US(event),
                    'int_UNIXtime_event_start': self.int_UNIXtime_event_start(event),
                    'int_UNIXtime_event_end': self.int_UNIXtime_event_end(event),
                    'int_minutes_duration': self.int_minutes_duration(event),
                    'url_featured_photo': self.url_featured_photo(event),
                    'text_description_en_US': self.text_description_en_US(event),
                    'str_location': self.str_location(event),
                    'one_space': self.one_space(event),
                    'one_guilde': self.one_guilde(event),
                    'str_series_id': self.str_series_id(event),
                    'int_series_startUNIX': self.int_series_startUNIX(event),
                    'int_series_endUNIX': self.int_series_endUNIX(event),
                    'text_series_timing': self.text_series_timing(event),
                    'url_meetup_event': self.url_meetup_event(event),
                    'int_UNIXtime_created': self.int_UNIXtime_created(event),
                    'int_UNIXtime_updated': self.int_UNIXtime_updated(event),
                    'str_timezone': self.str_timezone(event)
                } for event in self.response_json
            ]

    def create(self, event, announce=False, publish_status='draft'):
        # API Doc: https://www.meetup.com/meetup_api/docs/:urlname/events/#create
        self.log('create()')

        if not self.access_token:
            self.log('--> No MEETUP.ACCESS_TOKEN')
            self.log('--> return None')
            return None

        response = requests.post('https://api.meetup.com/'+self.group+'/events', params={
            'access_token': self.access_token,
            'sign': True,
            'announce': announce,
            'publish_status': publish_status,  # draft or published
            'description': event.text_description_en_US,
            'duration': event.int_minutes_duration*60*1000,
            'event_hosts': None,  # TODO figure out meetup user IDs and how to add them here
            'fee': {
                'accepts': None,  # TODO add option for paid events later
                'amount': None,
                'currency': None,
                'refund_policy': None
            },
            'guest_limit': 2,  # from 0 to 2
            'how_to_find_us': Config('PHYSICAL_SPACE.ADDRESS.HOW_TO_FIND_US__english').value,
            'lat': event.float_lat,
            'lon': event.float_lon,
            'name': event.str_name_en_US,
            'self_rsvp': False,
            'time': event.int_UNIXtime_event_start*1000,
            'venue_id': None,  # TODO figure out how to get venue id
            'venue_visibility': None  # TODO
        })

        if response.status_code == 201:
            event.url_meetup_event = response.json()['link']
            event.save()
            self.log('--> return event')
            return event
        else:
            self.log('--> '+str(response.status_code) +
                     ' response: '+str(response.json()))
            return None

    def delete(self, event):
        # API Doc: https://www.meetup.com/meetup_api/docs/:urlname/events/:id/#delete
        self.log('delete()')

        if not self.access_token:
            self.log('--> No MEETUP.ACCESS_TOKEN')
            self.log('--> return None')
            return None

        response = requests.delete('https://api.meetup.com/'+self.group+'/events/'+event.url_meetup_event.split('/')[-2], params={
            'access_token': self.access_token,
            'sign': True,
        })

        if response.status_code == 204:
            event.url_meetup_event = None
            event.save()
            self.log('--> return event')
            return event
        else:
            self.log('--> '+str(response.status_code) +
                     ' response: '+str(response.json()))
            return None
