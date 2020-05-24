import time

from django.views import View
from pyprintplus import Log

from _setup.models import Config, Secret


class View(View):
    logs = ['self.__init__']
    started = round(time.time())
    show_log = True
    space_name = Config('BASICS.NAME').value
    admin_url = Secret('DJANGO.ADMIN_URL').value
    path = ''

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)
