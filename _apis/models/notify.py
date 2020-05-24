from pyprintplus import Log
import time


class Notify():
    def __init__(self, show_log=True, test=False):
        self.logs = ['self.__init__']
        self.show_log = show_log
        self.started = round(time.time())
        self.test = test

    @property
    def setup_done(self):
        from _apis.models import Slack, Telegram
        return True if Slack().setup_done or Telegram().setup_done else False

    @property
    def config(self):
        from _apis.models import Slack, Telegram
        if Slack().setup_done:
            return {"selected": "Slack", "config": Slack().config}
        elif Telegram().setup_done:
            return {"selected": "Telegram", "config": Telegram().config}
        else:
            return {}

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from pyprintplus import Log
        from _apis.models import Slack, Telegram
        try:
            if not Slack().setup_done and not Telegram().setup_done:
                Log().show_messages(
                    ['Let\'s setup notifications for your new website!'])

                Slack(test=self.test).setup()

                if not Slack().setup_done and not Telegram().setup_done:
                    Telegram(test=self.test).setup()

            Log().show_message('Notify setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    def send(self, message):
        self.log('send()')
        from _apis.models import Slack, Telegram

        if Slack().setup_done:
            return Slack().message(message)
        elif Telegram().setup_done:
            return Telegram().message(message)
        else:
            self.log('-> ERROR: Notify setup not completed')
