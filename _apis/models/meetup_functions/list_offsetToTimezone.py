from datetime import datetime
import pytz


class MeetupListOffsetToTimezone():
    def __init__(self, offset_ms):
        now = datetime.now(pytz.utc)  # current time
        self.value = [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
                      if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]
