from _setup.models import Log


class SetupLanguages():
    def __init__(self, config, test=False):
        self.config = config
        self.test = test

        Log().show_messages(
            'Besides english - what languages should your website support? Currently available: hebrew.')
        input_languages = ['hebrew'] if self.test else input().replace(
            ', ', ',').split(',')
        self.config['WEBSITE']['LANGUAGES'] = ['english']
        if 'hebrew' in input_languages:
            self.config['WEBSITE']['LANGUAGES'].append('hebrew')
        else:
            # remove hebrew text options
            for element in self.config['BASICS']['HACKERSPACE_IS_SENTENCES']:
                element.pop('hebrew', None)
            for element in self.config['PHYSICAL_SPACE']['ADDRESS']:
                element.pop('HOW_TO_FIND_US__hebrew', None)
