import time
from pyprintplus import Log


class Request():
    def __init__(self, request=None, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.request = request
        self.url = request.build_absolute_uri() if request else None
        self.hash = self.url.split(
            '#')[1] if self.url and '#' in self.url else None
        self.user = request.user if request else None
        self.search = request.GET.get('search', None) if request else None

        if request and request.GET.get('lang', None):
            self.language = request.GET.get('lang', None)
        elif request and request.COOKIES.get('lang', None):
            self.language = request.COOKIES.get('lang', None)
        else:
            self.language = 'english'

        self.in_space = True if request and (request.COOKIES.get(
            'in_space') or request.GET.get('in_space', None) == 'True') else False

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)
