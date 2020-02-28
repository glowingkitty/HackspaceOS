from _website.views.view import View
from django.shortcuts import render
from _website.models import Request


class MeetingsView(View):
    def all_results(self, request):
        self.log('-> MeetingsView().all_results()')
        from _database.models import MeetingNote, Event
        return render(request.request, 'page.html', {
            'view': 'meetings_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/meetings',
            'page_git_url': '/tree/master/_database/templates/meetings_view.html',
            'page_name': self.space_name+' | Meetings',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current(),
            'next_meeting': Event.objects.QUERYSET__next_meeting(),
            'past_meetings': MeetingNote.objects.past()[:10]
        })

    def result(self, request, sub_page):
        self.log('-> MeetingsView().result()')
        from _database.models import MeetingNote, Event

        selected = MeetingNote.objects.filter(
            text_date=sub_page).first()
        return render(request.request, 'page.html', {
            'view': 'meeting_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/meeting/'+selected.text_date,
            'page_git_url': '/tree/master/_database/templates/meeting_view.html',
            'page_name': self.space_name+' | Meeting | '+selected.text_date,
            'page_description': 'Join our weekly meetings!',
            'selected': selected,
            'next_meeting': Event.objects.QUERYSET__next_meeting(),
            'past_meetings': MeetingNote.objects.past(selected)[:10]
        })

    def present(self, request):
        self.log('-> MeetingsView().present()')
        from _database.models import MeetingNote
        return render(request.request, 'meeting_present.html', {
            'user': request.user,
            'language': request.language,
            'slug': '/meeting/present',
            'page_name': self.space_name+' | Meeting | Presentation mode',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current()
        })

    def get(self, request):
        self.log('MeetingsView.get()')
        request = Request(request)

        # process all guildes view
        if self.path == 'all':
            return self.all_results(request)

        # process single event view
        elif self.path == 'result' and 'sub_page' in self.args and self.args['sub_page']:
            return self.result(request, self.args['sub_page'])

        # process present
        elif self.path == 'present':
            return self.present(request)
