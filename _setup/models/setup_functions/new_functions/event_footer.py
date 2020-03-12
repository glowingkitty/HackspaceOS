class SetupNewEventFooter():
    def __init__(self, config):
        self.config = config

        # auto generate the event footer for discourse and meetup
        if self.config['WEBSITE']['DOMAIN'] and self.config['BASICS']['NAME']:
            self.config['EVENTS']['DISCOURSE_AND_MEETUP_EVENT_FOOTER_HTML'] =\
                '<br>------------------<br>'\
                '<br>'+self.config['BASICS']['NAME']+' is funded by YOUR donations. '\
                'So if you want to support '+self.config['BASICS']['NAME']+' - donations are always welcomed - '\
                'money, hardware or time (by organizing or volunteering an event). '\
                'Visit https://' + \
                self.config['WEBSITE']['DOMAIN']+' for more details.'
