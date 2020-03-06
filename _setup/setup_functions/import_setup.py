from _setup.asci_art import show_message
import os


class SetupImport():
    def __init__(self, backup_files):
        self.backup_files = backup_files

        folders = os.listdir()
        folder_options = ''
        counter = 1
        backups = []
        for file_name in folders:
            if 'setup_backup__' in file_name:
                backups.append(file_name)
                if counter > 1:
                    folder_options += ', '
                folder_options += str(counter)+' - ' + \
                    file_name.split('setup_backup__')[1].split('.zip')[0]
                counter += 1

        if counter == 1:
            show_message('No backups found.')
        else:
            show_message(
                'Which setup would you like to import? '+folder_options)
            selected_folder = input()

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

                show_message('✅Done! Imported "'+folder_name.split('setup_backup__')
                             [1].split('.zip')[0] + '" ('+self.get_size(folder_name)+')')

            except:
                show_message(
                    'ERROR: The folder doesnt exist. Please enter a correct number.')

    def get_size(self, file_path):
        import os
        return str(round(os.path.getsize(file_path)/1000000, 1))+' MB'
