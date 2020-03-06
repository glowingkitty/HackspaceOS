from _setup.asci_art import show_message


class SetupNewName():
    def __init__(self, config):
        self.config = config

        show_message('First: What is the name of your hackerspace?')
        self.name = input()
        if self.name:
            self.config['BASICS']['NAME'] = self.name
