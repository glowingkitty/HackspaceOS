import requests
import random
from pyprintplus import Log


class MarrySpeak():
    def __init__(self, show_log=True):
        self.logs = ['self.__init__']
        self.show_log = show_log
        self.url = 'http://pegasus.noise:5000'
        self.facts = [
            'Every Tuesday before the General Meeting we have an extended tour at Noisebridge. Learn all kinds of exciting secrets about Noisebridge and how to give a great tour. Ask Ryan for more details',
            'The door bell makes different sounds, depending on if someone rings downstairs or upstairs',
            'You can controll what I say. Just visit pegasus.noise:5000 and enter a text',
            'You can display text, images and videos on Flaschentaschen. Just visit pegasus.noise:9000 and enter a text or upload an image or video',
            'We have a library with all kinds of awesome books!',
            'Hackspaces exist all over the world. And the movement actually started in Germany. See a map of all s on s.org',
            'Everyone can organize events at Noisebridge. In fact its a great way to introduce more people to Noisebridge',
            'Every Tuesday evening we have our weekly General Meeting. Where we talk about Noisebridge, announcements and more. In case you want to organize an event at Noisebridge, this is also a great chance to announce your event.'
        ]
        self.help = 'http://pegasus.noise'

    def log(self, text):
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text))

    def speak(self, text, intro='Did you know?'):
        try:
            self.log('speak()')
            # make marry speak
            parts = text.split('. ')
            if intro:
                requests.get(self.url+'?text='+intro)
            for part in parts:
                requests.get(self.url+'?text='+part.replace('.',
                                                            ' dot ').replace(':', ' colon '))
            self.log('-> Success')

        except:
            self.log(
                '-> ERROR: Couldnt talk to marry. Make sure to deactivate your VPN connection and be in the local Noisebridge network.')

    def interestingFacts(self):
        self.log('interestingFacts()')
        entry_num = random.randint(0, len(facts)-1)
        self.speak(facts[entry_num])

    def weeklyMeetingReminder(self):
        self.log('weeklyMeetingReminder()')
        self.speak(
            'Attention attention everyone. The Weekly General Meeting happens in 10 minutes in the Hackatorium. Please join us')
