import time


class Request():
    def __init__(self, request, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.request = request
        self.url = request.build_absolute_uri()
        self.hash = self.url.split('#')[1] if '#' in self.url else None
        self.user = request.user
        self.search = request.GET.get('search', None)

        if request.GET.get('lang', None):
            self.language = request.GET.get('lang', None)
        elif request.COOKIES.get('lang', None):
            self.language = request.COOKIES.get('lang', None)
        else:
            self.language = 'english'

        self.in_space = True if request.COOKIES.get(
            'in_space') or request.GET.get('in_space', None) == 'True' else False

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)
