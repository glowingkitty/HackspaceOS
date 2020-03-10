from _setup.models import Log
from _apis.models import Scraper
from selenium.webdriver.common.by import By
import requests
import time
import json
from _setup.models import Secret


class MeetupAcessToken():
    def __init__(self, email, password, client_id, client_secret, redirect_uri):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.email = email
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret,
        self.redirect_uri = redirect_uri

        # check if still usable token is saved in secrets.json - else get new one
        if Secret('MEETUP.ACCESS_TOKEN').value and Secret('MEETUP.ACCESS_TOKEN_VALID_UPTO').value > time.time()+60:
            self.value = Secret('MEETUP.ACCESS_TOKEN').value

        # check if required fields exist
        if not self.client_id or not self.client_secret or not self.redirect_uri or not self.email or not self.password:
            self.log('-> ERROR: Meetup secrets incomplete!')
            self.value = None

        else:
            # else: following steps to get an API token - see https://www.meetup.com/meetup_api/auth/

            # Step 1: Get code to get access token, by loggin into meetup account
            login_page = Scraper(
                'https://secure.meetup.com/oauth2/authorize?scope=basic+event_management&client_id={}&response_type=code&redirect_uri={}'.format(self.client_id, self.redirect_uri), scraper_type='selenium', auto_close_selenium=False)
            login_page.selenium.find_element(By.LINK_TEXT, 'Continue').click()
            login_page.selenium.find_element_by_id(
                'email').send_keys(self.email)
            login_page.selenium.find_element_by_id(
                'password').send_keys(self.password)
            login_page.selenium.find_element_by_id('loginFormSubmit').click()
            time.sleep(10)
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
                with open('_setup/secrets.json') as json_file:
                    secrets = json.load(json_file)
                secrets['MEETUP']['ACCESS_TOKEN'] = self.response_json['access_token']
                secrets['MEETUP']['ACCESS_TOKEN_VALID_UPTO'] = round(
                    time.time()+self.response_json['expires_in'])
                with open('_setup/secrets.json', 'w') as outfile:
                    json.dump(secrets, outfile, indent=4)
                self.value = self.response_json['access_token']
            else:
                self.log(
                    '-> ERROR: Failed to get Access Token - {}'.format(self.response_json))
                self.value = None

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
