from django.http import HttpResponse
from _website.views.view import View
from _apis.models import HackspaceOS


class HackspaceOSapiView(View):
    def get(self, request, sub_page=None):
        if self.path == 'page' and sub_page:
            return HackspaceOS().page(sub_page, request)

        elif self.path == 'load_more' and sub_page:
            return HackspaceOS().load_more(sub_page, request)

        elif self.path == 'events_slider':
            return HackspaceOS().events_slider(request)

        elif self.path == 'open_status':
            return HackspaceOS().open_status(request)

        elif self.path == 'event_overlap':
            return HackspaceOS().event_overlap(request)

        elif self.path == 'meeting_duration':
            return HackspaceOS().meeting_duration(request)

        elif self.path == 'translate':
            return HackspaceOS().translate(request)

        elif self.path == 'remove_keyword':
            return HackspaceOS().remove_keyword(request)

        elif self.path == 'save':
            return HackspaceOS().save(request)

        elif self.path == 'search':
            return HackspaceOS().search(request)

        elif self.path == 'upload_image':
            return HackspaceOS().upload_image(request)

        elif self.path == 'create_event':
            return HackspaceOS().create_event(request)

        elif self.path == 'approve_event':
            return HackspaceOS().approve_event(request)

        elif self.path == 'delete':
            return HackspaceOS().delete(request)

        elif self.path == 'create_meeting':
            return HackspaceOS().create_meeting(request)

        elif self.path == 'logout':
            return HackspaceOS().logout(request)
