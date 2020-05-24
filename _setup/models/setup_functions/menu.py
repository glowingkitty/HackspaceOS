import os
from pyprintplus import Log
from _setup.models.setup_functions.new import SetupNew
from _setup.models.setup_functions.import_setup import SetupImport
from _setup.models.setup_functions.export import SetupExport
from _setup.models.setup_functions.delete import SetupDelete


class SetupMenu():
    def __init__(self, backup_files, test=False):
        self.backup_files = backup_files
        self.test = test
        self.options = ['Create a new website']
        self.options_string = '1 - Create a new website'
        self.counter = 1

        # add additional menu options
        self.add_existing_backup_options()
        self.add_import_backup_options()

        # if only "Create a new website" as an option, auto proceed with that
        if self.counter == 1:
            SetupNew()
        else:
            self.show_menu()

    @property
    def boolean_files_exist(self):
        from os import path
        for file_path in self.backup_files:
            file_exist = path.exists(file_path)
            if file_exist == True:
                return file_exist
        else:
            return False

    def add_existing_backup_options(self):
        # if any file in self.backup_files exist, show "export setup" and "delete current setup"
        if self.boolean_files_exist == True:
            self.counter += 1
            new_option = 'Export current setup'
            self.options.append(new_option)
            self.options_string += ', '+str(self.counter)+' - '+new_option

            self.counter += 1
            new_option = 'Delete current setup'
            self.options.append(new_option)
            self.options_string += ', '+str(self.counter)+' - '+new_option

    def add_import_backup_options(self):
        # if any folders in "backup" folder, show "import backup"
        folders = os.listdir()
        folder_options = ''
        backups_counter = 1
        for file_name in folders:
            if 'setup_backup__' in file_name:
                backups_counter += 1

        if backups_counter > 1:
            self.counter += 1
            new_option = 'Import backup'
            self.options.append(new_option)
            self.options_string += ', '+str(self.counter)+' - '+new_option

    def show_menu(self):
        Log().show_message(
            'Welcome! How can I help you? (enter a number) '+self.options_string)
        selection_processed = False
        while selection_processed == False:
            try:
                selection = 1 if self.test else input()
                selector_number = int(selection)-1
                if self.options[selector_number] == 'Create a new website':
                    if self.test:
                        break
                    SetupNew()
                    selection_processed = True
                elif self.options[selector_number] == 'Export current setup':
                    SetupExport(self.backup_files)
                    selection_processed = True
                elif self.options[selector_number] == 'Delete current setup':
                    SetupDelete(self.backup_files)
                    selection_processed = True
                elif self.options[selector_number] == 'Import backup':
                    SetupImport(self.backup_files)
                    selection_processed = True
                else:
                    Log().show_message(
                        'ERROR: That option doesn\'t exist. How can I help you? (enter a number) '+self.options_string)
            except KeyboardInterrupt:
                break
            except (IndexError, ValueError):
                Log().show_message(
                    'ERROR: That option doesn\'t exist. How can I help you? (enter a number) '+self.options_string)
