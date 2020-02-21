import time


class Request():
    def __init__(self, request, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log
        self.request = request

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    @property
    def language(self):
        if self.request.GET.get('lang', None):
            return self.request.GET.get('lang', None)
        elif self.request.COOKIES.get('lang', None):
            return self.request.COOKIES.get('lang', None)
        else:
            return 'english'

    @property
    def in_space(self):
        if self.request.COOKIES.get('in_space') or self.request.GET.get('in_space', None) == 'True':
            return True
        else:
            return False

    @property
    def hash(self):
        if '#' in self.request.build_absolute_uri():
            return self.request.build_absolute_uri().split('#')[1]
        else:
            return None

    @property
    def user(self):
        return self.request.user

    @property
    def search(self):
        return self.request.GET.get('search', None)
