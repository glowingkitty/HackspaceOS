from pyprintplus import Log
import time
import re
TAG_RE = re.compile(r'<[^>]+>')


class Response():
    def __init__(self, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    @property
    def description(self):
        from _setup.models import Config
        NAME = Config('BASICS.NAME').value
        HACKERSPACE_IS_SENTENCES = Config(
            'BASICS.HACKERSPACE_IS_SENTENCES').value
        return NAME + ' '+TAG_RE.sub('', HACKERSPACE_IS_SENTENCES['english'][0])+('.' if not TAG_RE.sub('', HACKERSPACE_IS_SENTENCES['english'][0]).endswith('.') else '')
