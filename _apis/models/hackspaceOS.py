import time
from log import log
from _apis.models.hackspaceOS_functions.page import Page
from _apis.models.hackspaceOS_functions.load_more import LoadMore
from _apis.models.hackspaceOS_functions.events_slider import EventsSlider
from _apis.models.hackspaceOS_functions.open_status import OpenStatus
from _apis.models.hackspaceOS_functions.event_overlap import EventOverlap
from _apis.models.hackspaceOS_functions.meeting_duration import MeetingDuration
from _apis.models.hackspaceOS_functions.translate import Translate
from _apis.models.hackspaceOS_functions.remove_keyword import RemoveKeyword
from _apis.models.hackspaceOS_functions.save_keyword import SaveKeyword
from _apis.models.hackspaceOS_functions.search import Search
from _apis.models.hackspaceOS_functions.upload_image import UploadImage
from _apis.models.hackspaceOS_functions.create_event import CreateEvent


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

    def upload_image(self, request=None):
        self.log('HackspaceOS().upload_image()')
        return UploadImage(request).value

    def page(self, page, request=None):
        self.log('HackspaceOS().page()')
        return Page(page, request).value

    def load_more(self, what, request=None):
        self.log('HackspaceOS().loadmore()')
        return LoadMore(what, request).value

    def open_status(self, request=None):
        self.log('HackspaceOS().open_status()')
        return OpenStatus(request).value

    def translate(self, request=None):
        self.log('HackspaceOS().translate()')
        return Translate(request).value

    def search(self, request=None):
        self.log('HackspaceOS().search()')
        return Search(request).value

    def remove_keyword(self, request=None):
        self.log('HackspaceOS().remove_keyword()')
        return RemoveKeyword(request).value

    def save_keyword(self, request=None):
        self.log('HackspaceOS().save_keyword()')
        return SaveKeyword(request).value

    def events_slider(self, request=None):
        self.log('HackspaceOS().events_slider()')
        return EventsSlider(request).value

    def create_event(self, request=None):
        self.log('HackspaceOS().create_event()')
        return CreateEvent(request).value

    def approve_event(self, request=None):
        # requires user loggedin
        self.log('HackspaceOS().approve_event()')

    def delete_event(self, request=None):
        # who should be able to delete files
        self.log('HackspaceOS().delete_event()')

    def event_overlap(self, request=None):
        self.log('HackspaceOS().event_overlap()')
        return EventOverlap(request).value

    def meeting_duration(self, request=None):
        self.log('HackspaceOS().meeting_duration()')
        return MeetingDuration(request).value

    def create_meeting(self, request=None):
        self.log('HackspaceOS().create_meeting()')

    def end_meeting(self, request=None):
        self.log('HackspaceOS().end_meeting()')

    def logout(self, request=None):
        # requires user loggedin
        self.log('HackspaceOS().logout()')
