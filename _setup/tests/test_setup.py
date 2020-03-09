from django.test import TestCase
from _setup.setup import Setup
import json
import os


class SetupTestConfig():
    def __init__(self, target):
        with open('_setup/tests/test_new_setup.json') as json_file:
            self.value = json.load(json_file)

        if target:
            path = target.split('.')
            for part in path:
                self.value = self.value[part]


class SetupTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # rename config file to temp backup
        if os.path.isfile('_setup/config.json'):
            os.rename('_setup/config.json', '_setup/config_temp_backup.json')
        if os.path.isfile('_setup/secrets.json'):
            os.rename('_setup/secrets.json', '_setup/secrets_temp_backup.json')

    @classmethod
    def tearDownClass(cls):
        # delete new files and rename temp backup back to normal
        if os.path.isfile('_setup/config.json'):
            os.remove('_setup/config.json')
        if os.path.isfile('_setup/secrets.json'):
            os.remove('_setup/secrets.json')
        if os.path.isfile('setup_backup__unittest.zip'):
            os.remove('setup_backup__unittest.zip')

        if os.path.isfile('_setup/config_temp_backup.json'):
            os.rename('_setup/config_temp_backup.json', '_setup/config.json')
        if os.path.isfile('_setup/secrets_temp_backup.json'):
            os.rename('_setup/secrets_temp_backup.json', '_setup/secrets.json')

        super().tearDownClass()

    def test_menu(self):
        Setup(test=True)._menu()

    def test_new_export_delete_import(self):
        setup = Setup(test=True)

        # create a new setup
        setup._new()

        # then export that new setup
        setup._export()

        # then delete the new setup
        setup._delete()

        # then import the new setup
        setup._import()
