from django.http import HttpResponse
from _website.views.view import View
from _apis.models import HackspaceOS


class HackspaceOSapiView(View):
    def get(self, request, sub_page=None):
        if self.path == 'page' and sub_page:
            return HackspaceOS().page(sub_page, request)
        elif self.path == 'load_more' and sub_page:
            return HackspaceOS().load_more(sub_page, request)
