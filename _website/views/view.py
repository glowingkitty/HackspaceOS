from django.views import View
import time
from _setup.log import log
from _setup.secrets import Secret
from _setup.config import Config


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
            log('{}'.format(text), os.path.basename(__file__), self.started)
