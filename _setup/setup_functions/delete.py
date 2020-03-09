from _setup.asci_art import show_message
import os


class SetupDelete():
    def __init__(self, backup_files, test=False):
        self.backup_files = backup_files
        self.test = test

        show_message(
            'WARNING: Are you sure you want to delete your current setup? This will delete the config.json, secrets.json and your logos & favicons. Enter "delete" to delete the current setup.')
        confirm = input()
        if confirm == 'delete':
            for file_path in self.backup_files:
                if os.path.exists(file_path):
                    os.remove(file_path)

            show_message('✅Done! I deleted the current setup.')

        else:
            show_message('Ok. I won\'t delete anything.')
