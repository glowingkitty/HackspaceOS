from _setup.asci_art import show_message, show_messages
import json
import requests
from _setup.config import Config
from _setup.tests.test_setup import SetupTestConfig


class MeetupSetup():
    def __init__(self, group, test):
        self.group = group
        self.test = test

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

                    show_message('What is the URL of your Meetup group?')
                    self.group = SetupTestConfig(
                        'EVENTS.MEETUP_GROUP').value if self.test else input()
                    if not self.group and not self.test:
                        raise KeyboardInterrupt

                with open('_setup/config.json') as json_config:
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

                with open('_setup/config.json', 'w') as outfile:
                    json.dump(config, outfile, indent=4)

            show_message('Meetup setup complete.')
        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')
