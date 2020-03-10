import json
import os
import time


class Secret():
    def __init__(self, target=None, username_for=None, file_path='_setup/secrets.json', show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.file_path = file_path

        with open(file_path) as json_file:
            self.value = json.load(json_file)

        if target:
            path = target.split('.')
            for part in path:
                if part in self.value:
                    self.value = self.value[part]
                else:
                    self.value = None

        self.exists = True if self.value else False

    def log(self, text):
        from _setup.models import Log
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def set_secret(self, input_text, json_secrets, later_then_message, message, str_level_0, str_level_1=None, str_level_2=None, str_level_3=None):
        from _setup.models import Log
        if str_level_3:
            Log().show_message(message)
            json_secrets[str_level_0][str_level_1][str_level_2][str_level_3] = input(
            ) if input_text == 'input' else input_text
            if not json_secrets[str_level_0][str_level_1][str_level_2][str_level_3]:
                json_secrets[str_level_0][str_level_1][str_level_2][str_level_3] = None
                Log().show_message(later_then_message)

        elif str_level_2:
            Log().show_message(message)
            json_secrets[str_level_0][str_level_1][str_level_2] = input(
            ) if input_text == 'input' else input_text
            if not json_secrets[str_level_0][str_level_1][str_level_2]:
                json_secrets[str_level_0][str_level_1][str_level_2] = None
                Log().show_message(later_then_message)

        elif str_level_1:
            Log().show_message(message)
            json_secrets[str_level_0][str_level_1] = input(
            ) if input_text == 'input' else input_text
            if not json_secrets[str_level_0][str_level_1]:
                json_secrets[str_level_0][str_level_1] = None
                Log().show_message(later_then_message)

        elif str_level_0:
            Log().show_message(message)
            json_secrets[str_level_0] = input(
            ) if input_text == 'input' else input_text
            if not json_secrets[str_level_0]:
                json_secrets[str_level_0] = None
                Log().show_message(later_then_message)

        return json_secrets

    def set_secrets(self, json_secrets, later_then_message, str_set_what):
        from _setup.models import Log
        location = str_set_what.upper()
        for parameter in json_secrets[location]:
            if json_secrets[location][parameter] == None:
                Log().show_message(
                    'Please enter your '+parameter+' for '+str_set_what+' (or add it later and press Enter now)')
                json_secrets[location][parameter] = input()
                if not json_secrets[location][parameter]:
                    json_secrets[location][parameter] = None
                    Log().show_message(later_then_message)
                    break

            elif json_secrets[location][parameter] != None:
                for sub_paramter in json_secrets[location][parameter]:
                    Log().show_message(
                        'Please enter your '+parameter+' '+sub_paramter+' for '+str_set_what+' (or add it later and press Enter now)')
                    json_secrets[location][parameter][sub_paramter] = input()
                    if not json_secrets[location][parameter][sub_paramter]:
                        json_secrets[location][parameter][sub_paramter] = None
                        Log().show_message(later_then_message)
                        break

        return json_secrets
