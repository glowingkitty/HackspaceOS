from _setup.tests.test_setup import SetupTestConfig
from _setup.asci_art import set_secret
from googletrans import Translator
translator = Translator()


class SetupNewLocation():
    def __init__(self, config, later_then_config, test=False):
        self.config = config
        self.test = test

        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.CITY').value if self.test else 'input', self.config, later_then_config,
                                 'Ok, great. And in what city is your hackerspace? (Just the city name itself)', 'PHYSICAL_SPACE', 'ADDRESS', 'CITY')
        if self.config['PHYSICAL_SPACE']['ADDRESS']['CITY']:
            self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['english'][0] = self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['english'][0].replace(
                '{{ CITY }}', self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'])

            # if hebrew in languages, add translation
            if 'hebrew' in self.config['WEBSITE']['LANGUAGES']:
                self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['hebrew'][0] = self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['hebrew'][0].replace(
                    '{{ CITY }}', translator.translate(
                        text=self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'],
                        dest='he').text)

        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.STREET').value if self.test else 'input', self.config, later_then_config,
                                 'Enter your hackerspace street & house number.', 'PHYSICAL_SPACE', 'ADDRESS', 'STREET')
        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.ZIP').value if self.test else 'input', self.config, later_then_config,
                                 'Enter your hackerspace ZIP code.', 'PHYSICAL_SPACE', 'ADDRESS', 'ZIP')
        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.STATE').value if self.test else 'input', self.config, later_then_config,
                                 'Enter your hackerspace state. (California for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'STATE')
        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.COUNTRYCODE').value if self.test else 'input', self.config, later_then_config,
                                 'Enter your hackerspace country code (US or DE for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'COUNTRYCODE')
        self.config = set_secret(SetupTestConfig('PHYSICAL_SPACE.ADDRESS.HOW_TO_FIND_US__english').value if self.test else 'input', self.config, later_then_config,
                                 'Anything else people have to know to find your hackerspace?', 'PHYSICAL_SPACE', 'ADDRESS', 'HOW_TO_FIND_US__english')
        self.config = set_secret(SetupTestConfig('BASICS.EMBEDDED_MAP_URL').value if self.test else 'input', self.config, later_then_config,
                                 'Please enter the URL of your embedded map, to show people where your hackerspace is. My suggestion: go to https://www.google.com/maps - select your hackerspace, press the "Share" button -> "Embed a map" and enter here the "scr" URL of the iframe code.', 'BASICS', 'EMBEDDED_MAP_URL')
