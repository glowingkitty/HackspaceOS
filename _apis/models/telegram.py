import os
from secrets import Secret
from log import log
import time
import requests


class Telegram():
    def __init__(self, bot_token=Secret('TELEGRAM.BOT_TOKEN').value, group_chatID=Secret('TELEGRAM.GROUP_CHATID').value, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.bot_token = bot_token
        self.group_chatID = group_chatID
        self.setup_done = True if bot_token and group_chatID else False
        self.help = 'https://core.telegram.org'

    @property
    def config(self):
        return Secret('TELEGRAM').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from asci_art import show_message, show_messages
        import json

        try:
            if not self.bot_token or not self.group_chatID:
                show_messages(
                    ['Let\'s setup Telegram - to notify your hackspace about upcoming events, new created events and whatever else you want!'])

                if not self.bot_token:
                    show_message(
                        'Message https://t.me/botfather to create a new bot for your hackspace. When you are done: What is the token for your bot?')
                    self.bot_token = input()
                    while not self.bot_token:
                        self.bot_token = input()

                if not self.group_chatID:
                    show_message('Add your bot to your Telegram group.')
                    self.group_chatID = self.get_group_chatID()
                    while not self.group_chatID:
                        time.sleep(2)
                        self.group_chatID = self.get_group_chatID()

                with open('secrets.json') as json_secrets:
                    secrets = json.load(json_secrets)
                    secrets['TELEGRAM']['BOT_TOKEN'] = self.bot_token
                    secrets['TELEGRAM']['GROUP_CHATID'] = self.group_chatID

                with open('secrets.json', 'w') as outfile:
                    json.dump(secrets, outfile, indent=4)

            show_message('Telegram setup complete.')

        except KeyboardInterrupt:
            show_message('Ok, canceled setup.')

    @property
    def updates(self):
        response = requests.get(
            'https://api.telegram.org/bot'+self.bot_token+'/getUpdates')
        return response.json()

    def get_group_chatID(self):
        updates = self.updates
        for message in updates['result']:
            if message['message']['chat']['type'] == 'supergroup':
                return str(message['message']['chat']['id'])
        return None

    def message(self, message):
        self.log('message(message)')
        response = requests.get('https://api.telegram.org/bot'+self.bot_token +
                                '/sendMessage?chat_id='+self.group_chatID+'&parse_mode=Markdown&text='+message)
        if response.json()['ok'] == True:
            return True
        else:
            self.log('-> ERROR: {}'.format(response.json()))
            return False
