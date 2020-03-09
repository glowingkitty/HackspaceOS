from _setup.config import Config
import requests
import time
from _setup.log import log


class MeetupCreate():
    def __init__(self, access_token, group, event, announce, publish_status):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.access_token = access_token
        self.group = group

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
            self.value = event
        else:
            self.log('--> '+str(response.status_code) +
                     ' response: '+str(response.json()))
            self.value = None

    def log(self, text):
        import os
        self.logs.append(text)
        log('{}'.format(text), os.path.basename(__file__), self.started)
