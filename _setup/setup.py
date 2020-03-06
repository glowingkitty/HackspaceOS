class Setup():
    def __init__(self, name=None):
        self.name = name
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

    def _menu(self):
        from _setup.setup_functions.menu import SetupMenu
        SetupMenu(self.backup_files)

    def _new(self):
        from _setup.setup_functions.new import SetupNew
        SetupNew()

    def _export(self):
        from _setup.setup_functions.export import SetupExport
        SetupExport(self.backup_files, self.name)

    def _import(self):
        from _setup.setup_functions.import_setup import SetupImport
        SetupImport(self.backup_files)

    def _delete(self):
        from _setup.setup_functions.delete import SetupDelete
        SetupDelete(self.backup_files)
