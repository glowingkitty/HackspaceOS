from _website.views.view import View
from _apis.models import HackspaceOS


class HackspaceOSapiView(View):
    def post(self, request, sub_page=None):
        if self.path == 'image_upload':
            return HackspaceOS().image_upload(request)

    def get(self, request, sub_page=None):
        if self.path == 'page' and sub_page:
            return HackspaceOS().page(sub_page, request)

        elif self.path == 'load_more' and sub_page:
            return HackspaceOS().load_more(sub_page, request)

        elif self.path == 'open_status':
            return HackspaceOS().open_status(request)

        elif self.path == 'translate':
            return HackspaceOS().translate(request)

        elif self.path == 'search':
            return HackspaceOS().search(request)

        elif self.path == 'keyword_remove':
            return HackspaceOS().keyword_remove(request)

        elif self.path == 'keyword_add':
            return HackspaceOS().keyword_add(request)

        elif self.path == 'events_slider':
            return HackspaceOS().events_slider(request)

        elif self.path == 'event_create':
            return HackspaceOS().event_create(request)

        elif self.path == 'event_approve':
            return HackspaceOS().event_approve(request)

        elif self.path == 'event_delete':
            return HackspaceOS().event_delete(request)

        elif self.path == 'event_overlap':
            return HackspaceOS().event_overlap(request)

        elif self.path == 'meeting_duration':
            return HackspaceOS().meeting_duration(request)

        elif self.path == 'meeting_create':
            return HackspaceOS().meeting_create(request)

        elif self.path == 'meeting_end':
            return HackspaceOS().meeting_end(request)
