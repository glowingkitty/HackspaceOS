from _setup.asci_art import show_message, show_messages


class SetupExport():
    def __init__(self, backup_files, test=False):
        self.backup_files = backup_files
        self.test = test

        show_messages([
            'Hello! It seems you want to export your current settings? (your config.json, secrets.json and important images)'
        ])

        show_message(
            'If that\'s the case, enter now a name for the exported folder. (or press Enter to exit)')

        folder_name = 'unittest' if self.test else input()

        if not folder_name:
            show_message('Ok, got it. Maybe another time.')
            exit()
        else:
            from zipfile import ZipFile, ZIP_DEFLATED

            # copy files into folder
            with ZipFile('setup_backup__'+folder_name+'.zip', 'w', ZIP_DEFLATED) as zip:
                # writing each file one by one
                for file in self.backup_files:
                    try:
                        zip.write(file)
                    except:
                        pass

                show_message('✅Done! Exported "'+folder_name +
                             '" ('+self.get_size('setup_backup__'+folder_name+'.zip')+')')

    def get_size(self, file_path):
        import os
        return str(round(os.path.getsize(file_path)/1000000, 1))+' MB'
