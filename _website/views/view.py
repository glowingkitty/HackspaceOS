from django.views import View
import time
from log import log
from secrets import Secret
from config import Config


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
