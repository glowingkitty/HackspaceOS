from _setup.config import Config


class MeetupSTRtimezone():
    def __init__(self, event):
        from _apis.models.meetup_functions.list_offsetToTimezone import MeetupListOffsetToTimezone
        from _apis.models.meetup_functions.int_timezoneToOffset import MeetupIntTimezoneToOffset
        TIMEZONE_STRING = Config('PHYSICAL_SPACE.TIMEZONE_STRING').value

        if 'utc_offset' in event and event['utc_offset'] != MeetupIntTimezoneToOffset(TIMEZONE_STRING).value:
            self.value = MeetupListOffsetToTimezone(event['utc_offset']).value
        else:
            self.value = TIMEZONE_STRING
