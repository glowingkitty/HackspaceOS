import os
import slack
from secrets import Secret
from log import log
import time


class Slack():
    def __init__(self, api_token=Secret('SLACK.API_TOKEN').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.api_token = api_token
        self.setup_done = True if api_token else False
        self.help = 'https://github.com/slackapi/python-slackclient'

    @property
    def config(self):
        return Secret('SLACK').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            show_messages(
                ['Let\'s setup Slack - to notify your hackspace about upcoming events, new created events and whatever else you want!'])
            show_message(
                'Go to https://api.slack.com/apps and create an app. Once you are done: What is your API token?')
            self.api_token = input()
            while not self.api_token:
                self.api_token = input()

            with open('secrets.json') as json_secrets:
                secrets = json.load(json_secrets)
                secrets['SLACK']['API_TOKEN'] = self.api_token

            with open('secrets.json', 'w') as outfile:
                json.dump(secrets, outfile, indent=4)

            show_message('Slack setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    def message(self, message, channel='#general'):
        self.log('message(message, channel={})'.format(channel))
        if not self.api_token:
            self.log(
                '--> KEY MISSING: SLACK.API_TOKEN not defined. Couldnt sent notification via Slack.')
        else:
            client = slack.WebClient(token=self.api_token)

            # see https://github.com/slackapi/python-slackclient#sending-a-message-to-slack
            response = client.chat_postMessage(channel=channel, text=message)

            if response['ok'] == True:
                self.log('--> Success! Sent message to Slack')
                return True
            else:
                self.log('--> ERROR: Failed!')
                return False
