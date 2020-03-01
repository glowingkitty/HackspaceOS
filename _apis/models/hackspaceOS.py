import time
from secrets import Secret
from log import log
from django.http import JsonResponse


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
        self.log('page()')
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

    def photos(self):
        self.log('photos()')

    def load_more(self):
        self.log('loadmore()')

    def events_slider(self):
        self.log('events_slider()')

    def open_status(self):
        self.log('open_status()')

    def event_overlap(self):
        self.log('event_overlap()')

    def meeting_duration(self):
        self.log('meeting_duration()')

    def translate(self):
        self.log('translate()')

    def remove_keyword(self):
        self.log('remove_keyword()')

    def save(self):
        self.log('save()')

    def search(self):
        self.log('search()')

    def upload_image(self, image):
        self.log('upload_image()')

    def create_event(self):
        self.log('create_event()')

    def approve_event(self):
        # requires user loggedin
        self.log('approve_event()')

    def delete(self, file_name):
        self.log('delete()')

    def create_meeting(self):
        self.log('create_meeting()')

    def logout(self):
        # requires user loggedin
        self.log('logout()')
