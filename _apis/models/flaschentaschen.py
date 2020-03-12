import requests
from _setup.models import Log


class Flaschentaschen():
    def __init__(self, show_log=True):
        self.logs = ['self.__init__']
        self.show_log = show_log
        self.url = 'http://pegasus.noise:4444/api'
        self.help = 'https://www.noisebridge.net/Flaschen_Taschen'

    def log(self, text):
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text))

    def showText(self, text):
        try:
            self.log('showText()')
            requests.post(self.url+'/text', {'text': text})
        except:
            self.log('-> ERROR: Couldnt talk to Flaschentaschen. Make sure to deactivate your VPN connection and be in the local Noisebridge network.')
