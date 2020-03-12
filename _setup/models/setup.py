class Setup():
    def __init__(self, test=False):
        self.test = test
        self.backup_files = [
            'db.sqlite3',
            '_setup/config.json',
            '_setup/secrets.json',
            '_website/static/images/logo.svg',
            '_website/static/images/header_logo.jpg',
            '_website/static/images/header_banner.jpg',
            '_website/static/images/favicons/favicon.ico',
            '_website/static/images/favicons/favicon-32x32.png',
            '_website/static/images/favicons/favicon-16x16.png',
            '_website/static/images/favicons/apple-touch-icon.png',
        ]

    @property
    def complete(self):
        import os
        # check if config and secrets file exist
        if os.path.isfile('_setup/config.json') and os.path.isfile('_setup/secrets.json'):
            return True
        else:
            return False

    @property
    def database_exists(self):
        import os
        # check if config and secrets file exist
        if os.path.isfile('db.sqlite3'):
            return True
        else:
            return False

    def _menu(self):
        from _setup.models.setup_functions.menu import SetupMenu
        SetupMenu(self.backup_files, self.test)

    def _new(self):
        from _setup.models.setup_functions.new import SetupNew
        SetupNew(self.test)

    def _export(self):
        from _setup.models.setup_functions.export import SetupExport
        SetupExport(self.backup_files, self.test)

    def _import(self):
        from _setup.models.setup_functions.import_setup import SetupImport
        SetupImport(self.backup_files, self.test)

    def _delete(self):
        from _setup.models.setup_functions.delete import SetupDelete
        SetupDelete(self.backup_files, self.test)
