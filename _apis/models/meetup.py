import json
import time

import requests
from MeetupAPI import Meetup

from _setup.models import Config, Log, Secret


class Meetup(Meetup):
    def __init__(self,
                 group=Config('EVENTS.MEETUP_GROUP').value,
                 email=Secret('MEETUP.EMAIL').value,
                 password=Secret('MEETUP.PASSWORD').value,
                 client_id=Secret('MEETUP.CLIENT_ID').value,
                 client_secret=Secret('MEETUP.CLIENT_SECRET').value,
                 redirect_uri=Secret('MEETUP.REDIRECT_URI').value,
                 show_log=True,
                 test=False):
        self.show_log = show_log
        self.group = group
        self.email = email
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret,
        self.redirect_uri = redirect_uri

        self.default_space_name = Config('BASICS.NAME').value
        HACKERSPACE_ADDRESS = Config('PHYSICAL_SPACE.ADDRESS').value
        self.default_space_address = {
            "STREET": HACKERSPACE_ADDRESS['STREET'],
            "ZIP": HACKERSPACE_ADDRESS['ZIP'],
            "CITY": HACKERSPACE_ADDRESS['CITY'],
            "COUNTRYCODE": HACKERSPACE_ADDRESS['COUNTRYCODE'],
        }
        self.default_space_how_to_find_us = Config(
            'PHYSICAL_SPACE.ADDRESS.HOW_TO_FIND_US__english').value
        self.default_space_timezonestring = Config(
            'PHYSICAL_SPACE.TIMEZONE_STRING').value

        self.test = test

    def setup(self):
        from _apis.models.meetup_functions.setup import MeetupSetup
        MeetupSetup(self.group, self.test)

    def one_space(self, event):
        from _apis.models.meetup_functions.one_space import MeetupOneSpace
        return MeetupOneSpace(event).value

    def one_guilde(self, event):
        from _apis.models.meetup_functions.one_guilde import MeetupOneGuilde
        return MeetupOneGuilde(event).value
