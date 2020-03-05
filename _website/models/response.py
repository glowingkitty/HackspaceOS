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
            log('{}'.format(text), os.path.basename(__file__), self.started)

    @property
    def description(self):
        from _setup.config import Config
        NAME = Config('BASICS.NAME').value
        HACKERSPACE_IS_SENTENCES = Config(
            'BASICS.HACKERSPACE_IS_SENTENCES').value
        return NAME + ' '+TAG_RE.sub('', HACKERSPACE_IS_SENTENCES['english'][0])+('.' if not TAG_RE.sub('', HACKERSPACE_IS_SENTENCES['english'][0]).endswith('.') else '')

    def space_open(self, language):
        from datetime import datetime
        import calendar
        import pytz
        from _setup.config import Config
        from _website.templatetags.translate import landingpage
        from _database.models import Event

        # if an event is happening - show space open. Else use opening hours defined by config.json
        if Event.objects.QUERYSET__now():
            translated_status = landingpage('Open now', language)
            color_indicator = 'green'
        else:
            timezone = pytz.timezone(
                Config('PHYSICAL_SPACE.TIMEZONE_STRING').value)
            today_weekday = calendar.day_name[datetime.now(timezone).weekday()]
            now_hour = datetime.now(timezone).hour
            now_minute = datetime.now(timezone).minute
            status = 'Unknown'

            for status_change in Config('PHYSICAL_SPACE.OPENING_HOURS').value[today_weekday]:
                if now_hour >= status_change[0] and now_minute >= status_change[1]:
                    status = status_change[2]
                    translated_status = landingpage(status, language)
                    color_indicator = status_change[3]
                else:
                    break
        if language == 'hebrew':
            return '<div dir="rtl" align="right">'+translated_status+'</div><div class="status_code_icon '+color_indicator+' rtl"></div>'
        else:
            return '<div class="status_code_icon '+color_indicator+'"></div><div>'+translated_status+'</div>'
