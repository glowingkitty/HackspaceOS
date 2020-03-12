import json
from _setup.tests.test_setup import SetupTestConfig
from _setup.models import Log
from _setup.models import Secret
import secrets


class SetupNew():
    def __init__(self, test=False):
        self.test = test

        Log().show_messages([
            'Let\'s setup your new hackspace website!'
        ])

        self.config = self.get_template('config')
        self.secrets = self.get_template('secrets')

        self.setup_config()
        self.setup_secrets()
        self.setup_scraper()
        self.setup_database()
        self.setup_cronjobs()
        self.setup_superuser()

        Log().show_messages([
            '✅ Yeahh we are done! I saved your config.json and secrets.json files in the main directory. So you can easily change them any time. Also I created cronjobs to keep your Hackspace website running properly and initiated your database.',
        ])

    def get_template(self, which):
        import json
        file_path = '_setup/'+which+'_template.json'
        with open(file_path) as json_file:
            template = json.load(json_file)
        return template

    def setup_config(self):
        from _setup.models.setup_functions.new_functions.languages import SetupLanguages
        from _setup.models.setup_functions.new_functions.riseuppad import SetupNewRiseupPad
        from _setup.models.setup_functions.new_functions.location import SetupNewLocation
        from _setup.models.setup_functions.new_functions.latlon_timezone import SetupNewLatLonTimezone
        from _setup.models.setup_functions.new_functions.event_footer import SetupNewEventFooter

        later_then_config = 'Guess later then... Open your config.json at any time to make changes.'

        self.config = Secret().set_secret(SetupTestConfig('BASICS.NAME').value if self.test else 'input', self.config, later_then_config,
                                          'First: What is the name of your hackspace?', 'BASICS', 'NAME')
        self.config = SetupLanguages(self.config, self.test).config
        self.config = SetupNewRiseupPad(self.config).config
        self.config = SetupNewLocation(
            self.config, later_then_config, self.test).config
        self.config = SetupNewLatLonTimezone(self.config).config

        self.config = Secret().set_secret(SetupTestConfig('SOCIAL.HASHTAG').value if self.test else 'input', self.config, later_then_config,
                                          'What #hashtag do people use when they talk online about your hackspace on Twitter or Instagram? (Example: #noisebridge)', 'SOCIAL', 'HASHTAG')
        self.config = Secret().set_secret(SetupTestConfig('BASICS.DONATION_URLs.MONEY').value if self.test else 'input', self.config, later_then_config,
                                          'Do you have a donation page, where people can donate money online? If yes, please enter the url. (or press Enter to skip)', 'BASICS', 'DONATION_URLs', 'MONEY')
        self.config = Secret().set_secret(None if self.test else 'input', self.config, later_then_config,
                                          'Did you clone the HackspaceOS template and want people to make changes to your clone? Then enter the GIT URL now (for example from Github).', 'WEBSITE', 'WEBSITE_GIT')
        self.config = Secret().set_secret(SetupTestConfig('WEBSITE.DOMAIN').value, self.config, later_then_config,
                                          'What domain will you use for your new hackspace website? (Just the domain. Example: "noisebridge.net")', 'WEBSITE', 'DOMAIN')

        self.config = SetupNewEventFooter(self.config).config

        self.config = Secret().set_secret(SetupTestConfig('CSS.PRIMARY_COLOR').value, self.config, later_then_config,
                                          'And the last question: What should be your website\'s primary color (for buttons for example). Recommended: a color in your hackspace logo?', 'CSS', 'PRIMARY_COLOR')

        with open('_setup/config.json', 'w') as outfile:
            json.dump(self.config, outfile, indent=4)

    def setup_secrets(self):
        from _apis.models import Search, Meetup, Notify, Flickr, GooglePhotos, Instagram, Aws, Twitter

        # then setup secrets.json
        later_then_secrets = 'Guess later then... Open your secrets.json at any time to make changes.'

        self.secrets['DJANGO']['SECRET_KEY'] = secrets.token_urlsafe(50)
        self.secrets['DJANGO']['ADMIN_URL'] = secrets.token_urlsafe(20)

        with open('_setup/secrets.json', 'w') as outfile:
            json.dump(self.secrets, outfile, indent=4)

        Log().show_messages([
            'Awesome! Let\'s complete the setup by saving your secrets (API keys, etc.)'
        ])

        apis = (Search, Meetup, Notify, Flickr,
                GooglePhotos, Instagram, Twitter, Aws)
        for api in apis:
            if not api().setup_done:
                api(test=self.test).setup()

    def setup_scraper(self):
        from _apis.models import Scraper
        if not Scraper().setup_done:
            Scraper().setup()

    def setup_database(self):
        from django.core.management import call_command
        call_command('migrate')
        call_command('update_database')

    def setup_cronjobs(self):
        from _setup.models import Cronjob
        Cronjob().setup()

    def setup_superuser(self):
        from django.contrib.auth import get_user_model

        # test if superuser already exists
        User = get_user_model()
        if User.objects.count() == 0:
            User.objects.create_superuser(
                self.config['BASICS.NAME']+'SuperMember', None, secrets.token_urlsafe(50))
            Log().show_message('Created admin user (see _setup/secrets.json for the login details)')
