class MeetupTextSeriesTiming():
    def __init__(self, event):
        if 'series' in event and 'weekly' in event['series']:
            self.value = 'weekly: '+str(event['series']['weekly'])
        elif 'series' in event and 'monthly' in event['series']:
            self.value = 'monthly: '+str(event['series']['monthly'])
        else:
            self.value = None
