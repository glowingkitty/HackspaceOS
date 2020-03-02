import time
from log import log
from _apis.models.hackspaceOS_functions.page import Page
from _apis.models.hackspaceOS_functions.load_more import LoadMore
from _apis.models.hackspaceOS_functions.events_slider import EventsSlider
from _apis.models.hackspaceOS_functions.open_status import OpenStatus
from _apis.models.hackspaceOS_functions.event_overlap import EventOverlap
from _apis.models.hackspaceOS_functions.meeting_duration import MeetingDuration


class HackspaceOS():
    def __init__(self, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def page(self, page, request=None):
        self.log('HackspaceOS().page()')
        return Page(page, request).value

    def load_more(self, what, request=None):
        self.log('HackspaceOS().loadmore()')
        return LoadMore(what, request).value

    def events_slider(self, request=None):
        self.log('HackspaceOS().events_slider()')
        return EventsSlider(request).value

    def open_status(self, request=None):
        self.log('HackspaceOS().open_status()')
        return OpenStatus(request).value

    def event_overlap(self, request=None):
        self.log('HackspaceOS().event_overlap()')
        return EventOverlap(request).value

    def meeting_duration(self, request=None):
        self.log('HackspaceOS().meeting_duration()')
        return MeetingDuration(request).value

    def translate(self, request=None):
        self.log('HackspaceOS().translate()')

    def remove_keyword(self, request=None):
        self.log('HackspaceOS().remove_keyword()')

    def save(self, request=None):
        self.log('HackspaceOS().save()')

    def search(self, request=None):
        self.log('HackspaceOS().search()')

    def upload_image(self, image):
        self.log('HackspaceOS().upload_image()')

    def create_event(self):
        self.log('HackspaceOS().create_event()')

    def approve_event(self):
        # requires user loggedin
        self.log('HackspaceOS().approve_event()')

    def delete(self, file_name):
        self.log('HackspaceOS().delete()')

    def create_meeting(self):
        self.log('HackspaceOS().create_meeting()')

    def logout(self):
        # requires user loggedin
        self.log('HackspaceOS().logout()')
