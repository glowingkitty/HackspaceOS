import time
from secrets import Secret
from log import log
from django.http import JsonResponse
from django.template.loader import get_template


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
        from _website import views

        if page == '__':
            page = 'landingpage'
        else:
            page = page.replace('__', '', 1)

        if '__' in page and not page.endswith('__new'):
            page, sub_page = page.split('__')
        else:
            sub_page = None

        page = page.replace('__', '_')

        # get pages which can be loaded in the frontend via javascript
        if page == 'landingpage':
            view = views.LandingpageView()
            view.get_context(request)

        elif page == 'values':
            view = views.ValuesView()
            view.get_context(request)

        elif page == 'meetings':
            view = views.MeetingsView()
            view.all_results(request)

        elif page == 'meeting' and sub_page and sub_page == 'present':
            view = views.MeetingsView()
            view.present(request)

        elif page == 'meeting' and sub_page:
            view = views.MeetingsView()
            view.result(request, sub_page)

        elif page == 'guildes':
            view = views.GuildesView()
            view.all_results(request)

        elif page == 'guilde' and sub_page:
            view = views.GuildesView()
            view.result(request, sub_page)

        elif page == 'spaces':
            view = views.SpacesView()
            view.all_results(request)

        elif page == 'space' and sub_page:
            view = views.SpacesView()
            view.result(request, sub_page)

        elif page == 'machines':
            view = views.MachinesView()
            view.all_results(request)

        elif page == 'machine' and sub_page:
            view = views.MachinesView()
            view.result(request, sub_page)

        elif page == 'projects':
            view = views.ProjectsView()
            view.all_results(request)

        elif page == 'events':
            view = views.EventsView()
            view.all_results(request)

        elif page == 'event' and sub_page and sub_page == 'new':
            view = views.EventsView()
            view.new(request)

        elif page == 'event' and sub_page:
            view = views.EventsView()
            view.result(request, sub_page)

        elif page == 'photos':
            view = views.PhotosView()
            view.get_context(request)

        elif page == 'consensus':
            view = views.ConsensusView()
            view.get_context(request)

        return JsonResponse(
            {
                'html': view.html(),
                'page_name': page
            }
        )

    def load_more(self, what, request=None):
        self.log('HackspaceOS().loadmore()')
        log('load_more_view(request)')
        from _database.models import Helper, MeetingNote, Event, Project, Space, Machine, Guilde, Consensus

        if what and request.GET.get('from', None):
            if what == 'meeting_notes':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'meetings/meetings_list.html', MeetingNote.objects.past())
            elif what == 'events':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Event.objects.QUERYSET__upcoming())
            elif what == 'projects':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Project.objects.latest())
            elif what == 'spaces':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Space.objects.all())
            elif what == 'machines':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Machine.objects.all())
            elif what == 'guildes':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Guilde.objects.all())
            elif what == 'consensus':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'consensus_items_entries.html', Consensus.objects.latest())
            elif what == 'photos':
                response = Helper().JSON_RESPONSE_more_photos(request)
        else:
            response = JsonResponse({'error': 'Request incomplete or wrong'})
            response.status_code = 404

        return response

    def events_slider(self, request=None):
        self.log('HackspaceOS().events_slider()')
        from _database.models import Event
        from _website.models import Request

        marry_messages = []
        in_space = request.COOKIES.get('in_space')
        if request:
            request = Request(request)
        if in_space:
            events_in_5_minutes = Event.objects.LIST__in_minutes(
                minutes=5, name_only=True)
            events_in_30_minutes = Event.objects.LIST__in_minutes(
                minutes=30, name_only=True)
            if events_in_5_minutes or events_in_30_minutes:
                marry_messages.append('We have some awesome events upcoming')
            for event in events_in_5_minutes:
                marry_messages.append(event+' starts in 5 minutes.')
            for event in events_in_30_minutes:
                marry_messages.append(event+' starts in 30 minutes.')

        response = JsonResponse(
            {
                'html': get_template(
                    'components/body/events_slider.html').render({
                        'language': request.language,
                        'upcoming_events': Event.objects.QUERYSET__upcoming()[:5]
                    }),
                'marryspeak': marry_messages
            }
        )

    def open_status(self):
        self.log('HackspaceOS().open_status()')

    def event_overlap(self):
        self.log('HackspaceOS().event_overlap()')

    def meeting_duration(self):
        self.log('HackspaceOS().meeting_duration()')

    def translate(self):
        self.log('HackspaceOS().translate()')

    def remove_keyword(self):
        self.log('HackspaceOS().remove_keyword()')

    def save(self):
        self.log('HackspaceOS().save()')

    def search(self):
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
