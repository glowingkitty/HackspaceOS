from _setup.models import Log, Cronjob
import os
from django.contrib.auth import get_user_model


class SetupImport():
    def __init__(self, backup_files, test=False):
        self.backup_files = backup_files
        self.test = test

        folders = os.listdir()
        folder_options = ''
        counter = 1
        backups = []
        for file_name in folders:
            if 'setup_backup__' in file_name:
                backups.append(file_name)
                if self.test and file_name == 'setup_backup__unittest.zip':
                    unittest_zip_counter = counter

                if counter > 1:
                    folder_options += ', '
                folder_options += str(counter)+' - ' + \
                    file_name.split('setup_backup__')[1].split('.zip')[0]
                counter += 1

        if counter == 1:
            Log().show_message('No backups found.')
        else:
            Log().show_message(
                'Which setup would you like to import? '+folder_options)
            selected_folder = unittest_zip_counter if self.test else input()

            # test if folder exist
            try:
                from zipfile import ZipFile

                selected_num = int(selected_folder)-1
                folder_name = backups[selected_num]

                # first delete existing files
                for file_path in self.backup_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)

                # copy files into folder
                with ZipFile(folder_name, 'r') as zip:
                    # extracting all the files
                    zip.extractall()

                # make sure cronjobs are also setup
                Cronjob().setup()

                # test if superuser already exists
                User = get_user_model()
                if User.objects.count() == 0:
                    User.objects.create_superuser(
                        self.config['BASICS.NAME']+'SuperMember', None, secrets.token_urlsafe(50))
                    Log().show_message('Created admin user (see _setup/secrets.json for the login details)')

                Log().show_message('✅Done! Imported "'+folder_name.split('setup_backup__')
                                   [1].split('.zip')[0] + '" ('+self.get_size(folder_name)+') and created cronjobs to keep your database up to date!')

            except:
                Log().show_message(
                    'ERROR: The folder doesnt exist. Please enter a correct number.')

    def get_size(self, file_path):
        import os
        return str(round(os.path.getsize(file_path)/1000000, 1))+' MB'
