from git import Repo

from _setup.models import Config, Log, Setup


class Startup():
    def __init__(self):
        self.check_code_update()
        self.check_setup_complete()
        self.check_config_uptodate()
        self.check_mode_testing()

    def log(self, text):
        from _setup.models import Log
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def check_code_update(self):
        # check if the code base is up to date - else execute git pull
        repo = Repo()
        self.log('Checking for updates via git.fetch ...')
        updates = repo.remotes.origin.fetch()
        if updates:
            self.log('Updating git repo via git.pull ...')
            repo.remotes.origin.pull()

    def check_setup_complete(self):
        # Check once on starting the server
        # Check if setup is completed
        if not Setup().complete:
            Setup()._menu()
        elif not Setup().database_exists:
            from django.core.management import call_command
            call_command('migrate')
            call_command('update_database')

    def check_config_uptodate(self):
        # check if config.json is up to date
        pass

    def check_mode_testing(self):
        # ask if user is sure about running server in TEST mode?
        MODE = Config('MODE.SELECTED').value
        if MODE != 'PRODUCTION':
            Log().show_message('MODE in _setup/config.json is set to TESTING - this makes your server easy to attack, if you use that option on a deployed server that is accessible via the internet. Do you want to continue? (Enter Y to continue)')
            are_you_sure = input()
            if are_you_sure.lower() != 'y':
                Log().show_message(
                    'Ok, stopped server. You can change the mode in your _setup/config.json file.')
                exit()
