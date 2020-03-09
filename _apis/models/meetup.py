from _setup.log import log
import time
from _setup.config import Config
from _setup.secrets import Secret
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
                 show_log=True,
                 test=False):
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
        self.test = test

    @property
    def config(self):
        return {"group": Config('EVENTS.MEETUP_GROUP').value}

    @property
    def access_token(self):
        from _apis.models.meetup_functions.access_token import MeetupAcessToken
        return MeetupAcessToken(self.email, self.password, self.client_id, self.client_secret, self.redirect_uri).value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _apis.models.meetup_functions.setup import MeetupSetup
        MeetupSetup(self.group, self.test)

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
        from _apis.models.meetup_functions.str_location import MeetupSTRlocation
        return MeetupSTRlocation(event).value

    def one_space(self, event):
        from _apis.models.meetup_functions.one_space import MeetupOneSpace
        return MeetupOneSpace(event).value

    def one_guilde(self, event):
        from _apis.models.meetup_functions.one_guilde import MeetupOneGuilde
        return MeetupOneGuilde(event).value

    def str_series_id(self, event):
        return event['series']['id'] if 'series' in event else None

    def int_series_startUNIX(self, event):
        return round(event['series']['start_date'] / 1000) if 'series' in event and 'start_date' in event['series'] else None

    def int_series_endUNIX(self, event):
        return round(event['series']['end_date'] / 1000) if 'series' in event and 'end_date' in event['series'] else None

    def text_series_timing(self, event):
        from _apis.models.meetup_functions.text_series_timing import MeetupTextSeriesTiming
        return MeetupTextSeriesTiming(event).value

    def url_meetup_event(self, event):
        return event['link'] if 'link' in event else None

    def int_UNIXtime_created(self, event):
        return round(event['created']/1000)

    def int_UNIXtime_updated(self, event):
        return round(event['updated']/1000) if 'updated' in event else None

    def int_timezoneToOffset(self, timezone_name):
        from _apis.models.meetup_functions.int_timezoneToOffset import MeetupIntTimezoneToOffset
        return MeetupIntTimezoneToOffset(timezone_name).value

    def list_offsetToTimezone(self, offset_ms):
        from _apis.models.meetup_functions.list_offsetToTimezone import MeetupListOffsetToTimezone
        return MeetupListOffsetToTimezone(offset_ms).value

    def str_timezone(self, event):
        from _apis.models.meetup_functions.str_timezone import MeetupSTRtimezone
        return MeetupSTRtimezone(event).value

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
        from _apis.models.meetup_functions.create import MeetupCreate
        return MeetupCreate(self.access_token, self.group, event, announce, publish_status).value

    def delete(self, event):
        from _apis.models.meetup_functions.delete import MeetupDelete
        return MeetupDelete(self.access_token, self.group, event).value
