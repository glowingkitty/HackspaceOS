import json
import os
import time


class Config():
    def __init__(self, target=None, username_for=None, file_path='_setup/config.json', show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.file_path = file_path

        with open(file_path) as json_file:
            self.value = json.load(json_file)

        if target:
            path = target.split('.')
            for part in path:
                self.value = self.value[part]

            if username_for:
                if username_for.endswith('/'):
                    username_for = username_for[:-1]
                # check if instagram is saved in social channels
                for entry in self.value:
                    if username_for+'/' in entry['url']:
                        self.value = entry['url'].split(
                            username_for+'/')[1].replace('/', '')
                        break
                else:
                    self.value = None

    def log(self, text):
        from _setup.models import Log
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)
