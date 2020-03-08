from _setup.asci_art import show_message


class SetupLanguages():
    def __init__(self, config):
        self.config = config

        show_message(
            'Besides english - what languages should your website support? Currently available: hebrew.')
        input_languages = input().replace(', ', ',').split(',')
        self.config['WEBSITE']['LANGUAGES'] = ['english']
        if 'hebrew' in input_languages:
            self.config['WEBSITE']['LANGUAGES'].append('hebrew')
        else:
            # remove hebrew text options
            for element in self.config['BASICS']['HACKERSPACE_IS_SENTENCES']:
                element.pop('hebrew', None)
            for element in self.config['PHYSICAL_SPACE']['ADDRESS']:
                element.pop('HOW_TO_FIND_US__hebrew', None)
