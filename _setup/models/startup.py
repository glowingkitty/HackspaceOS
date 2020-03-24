import json
import os
import time

from git import Repo

from _setup.models import Config, Log, Setup


class Startup():
    def __init__(self):
        self.logs = ['self.__init__']
        self.started = round(time.time())

    def log(self, text):
        from _setup.models import Log
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def check_code_update(self):
        # check if the code base is up to date - else execute git pull
        repo = Repo()
        self.log('Checking for updates via git.fetch ...')

        branches = repo.remotes.origin.fetch()
        for branch in branches:
            if branch.flags == 2 or branch.flags == 64:
                Log().show_message('There is an update available for HackspaceOS. Want to update it now? (Enter Y to update now or anything else to update later)')
                update = input()
                if update.lower() == 'y':
                    repo.remotes.origin.pull()
                    Log().show_message('Update complete!')
                else:
                    Log().show_message('Ok, skipped update for now.')
                break
        else:
            self.log('No updates available.')

    def check_setup_complete(self):
        # Check once on starting the server
        # Check if setup is completed
        if not Setup().complete:
            Setup()._menu()
        elif not Setup().database_exists:
            from django.core.management import call_command
            call_command('migrate')
            call_command('update_database')

    def check_config_uptodate(self, file):
        self.log('Checking if {}.json is up to date ...'.format(file))

        # for every field in config_template - if field in config, copy config value over
        with open('_setup/{}_template.json'.format(file)) as template:
            config_template = json.load(template)

            with open('_setup/{}.json'.format(file)) as config_json:
                config = json.load(config_json)
                config_original = config

                for field in config_template:
                    if field.isupper() and field in config:

                        if type(config_template[field]) == dict:
                            for sub_field in config_template[field]:
                                if sub_field.isupper() and sub_field in config[field]:

                                    if type(config_template[field][sub_field]) == dict:
                                        for sub_sub_field in config_template[field][sub_field]:
                                            if sub_sub_field.isupper() and sub_sub_field in config[field][sub_field]:
                                                # get field content from config if exists
                                                config_template[field][sub_field][sub_sub_field] = config[
                                                    field][sub_field][sub_sub_field]
                                            else:
                                                # get field content from config if exists
                                                config_template[field][sub_field] = config[field][sub_field]
                                                break

                                    else:
                                        # get field content from config if exists
                                        config_template[field][sub_field] = config[field][sub_field]

                        else:
                            # get field content from config if exists
                            config_template[field] = config[field]

                # if original config.json different from updated one - save new file
                if config != config_template:
                    self.log(
                        '{} layout has changed! Saving updated {}...'.format(file, file))
                    with open('_setup/{}.json'.format(file), 'w') as outfile:
                        json.dump(config_template, outfile, indent=4)
                else:
                    self.log(
                        '{} layout unchanged'.format(file))

    def check_mode_testing(self):
        # ask if user is sure about running server in TEST mode?
        self.log('Checking MODE ...')
        MODE = Config('MODE.SELECTED').value
        if MODE != 'PRODUCTION':
            Log().show_message('MODE in _setup/config.json is set to TESTING - this makes your server easy to attack, if you use that option on a deployed server that is accessible via the internet. Do you want to continue? (Enter Y to continue)')
            are_you_sure = input()
            if are_you_sure.lower() != 'y':
                Log().show_message(
                    'Ok, stopped server. You can change the mode in your _setup/config.json file.')
                exit()
