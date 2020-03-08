import json
import os
import time


class Secret():
    def __init__(self, target=None, username_for=None, file_path='_setup/secrets.json', show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.file_path = file_path

        from _setup.setup import Setup
        if Setup().complete == False:
            Setup()._menu()

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
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)
