import requests
from _setup.models import Log
import time


class MeetupDelete():
    def __init__(self, access_token, group, event):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.access_token = access_token
        self.group = group

        # API Doc: https://www.meetup.com/meetup_api/docs/:urlname/events/:id/#delete
        self.log('delete()')

        if not self.access_token:
            self.log('--> No MEETUP.ACCESS_TOKEN')
            self.log('--> return None')
            self.value = None

        else:
            response = requests.delete('https://api.meetup.com/'+self.group+'/events/'+event.url_meetup_event.split('/')[-2], params={
                'access_token': self.access_token,
                'sign': True,
            })

            if response.status_code == 204:
                event.url_meetup_event = None
                event.save()
                self.log('--> return event')
                self.value = event
            else:
                self.log('--> '+str(response.status_code) +
                         ' response: '+str(response.json()))
                self.value = None

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
