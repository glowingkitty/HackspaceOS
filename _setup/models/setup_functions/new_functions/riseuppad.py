from _setup.models import Log


class SetupNewRiseupPad():
    def __init__(self, config):
        self.config = config

        if self.config['BASICS']['NAME']:
            Log().show_message(
                'Ok, great! Give me a seconds, so I can try to setup your RISEUPPAD_MEETING_PATH, and MEETUP_GROUP as well...')

            # if hackerspace name saved, also save other config defaults based on name
            self.config['MEETINGS']['RISEUPPAD_MEETING_PATH'] = self.config['BASICS']['NAME'].lower() + \
                '-meetings'
