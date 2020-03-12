from datetime import datetime
import pytz


class MeetupIntTimezoneToOffset():
    def __init__(self, timezone_name):
        self.value = int(datetime.now(pytz.timezone(
            timezone_name)).utcoffset().total_seconds()*1000)
