from _setup.models import Config


class MeetupOneGuilde():
    def __init__(self, event):
        from _database.models import Guilde

        EVENTS_GUILDES_OVERWRITE = Config(
            'EVENTS.EVENTS_GUILDES_OVERWRITE').value

        for str_keyword in EVENTS_GUILDES_OVERWRITE:
            if str_keyword in event['name']:
                self.value = Guilde.objects.filter(
                    str_name_en_US=EVENTS_GUILDES_OVERWRITE[str_keyword]).first()
        else:
            self.value = None
