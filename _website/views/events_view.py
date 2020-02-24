from _website.views.view import View
from django.shortcuts import render
from _website.models import Request


class EventsView(View):
    def all_results(self, request):
        self.log('-> EventsView().all_results()')
        from _database.models import Event
        all_results = Event.objects.QUERYSET__upcoming()[:10]
        return {
            'view': 'events_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/events',
            'page_git_url': '/tree/master/_website/templates/results_list.html',
            'page_name': self.space_name+' | Events',
            'page_description': 'At '+self.space_name+' we have all kinds of cool events - organized by your fellow hackers!',
            'headline': 'Events',
            'description': self.space_name+' is a place where people come together ...',
            'add_new_requires_user': False,
            'addnew_url': '/event/new',
            'addnew_text': 'Organize an event',
            'addnew_target': 'same_tab',
            'addnew_menu_selected': 'menu_h_events',
            'all_results': all_results if all_results else True,
            'results_count': Event.objects.count(),
            'show_more': 'events'
        }

    def result(self, request, sub_page):
        self.log('-> EventsView().result()')
        from _database.models import Event, Photo

        if 'event/' not in sub_page:
            sub_page = 'event/'+sub_page
        selected = Event.objects.filter(str_slug=sub_page).first()

        return {
            'view': 'event_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/event/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/event_view.html',
            'page_name': self.space_name+' | Event | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected,
            'photos': Photo.objects.latest()[:33]
        }

    def banner(self, request, sub_page):
        self.log('-> EventsView().banner()')
        from _database.models import Event, Photo

        if 'event/' not in sub_page:
            sub_page = 'event/'+sub_page
        selected = Event.objects.filter(str_slug=sub_page).first()

        return {
            'view': 'event_banner_view',
            'user': request.user,
            'language': request.language,
            'selected': selected,
        }

    def new(self, request, sub_page):
        self.log('-> EventsView().new()')
        from _database.models import Event, Photo, Space, Guilde
        from config import Config
        from django.middleware.csrf import get_token
        EVENTS_SPACE_DEFAULT = Config('EVENTS.EVENTS_SPACE_DEFAULT').value

        return {
            'view': 'event_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/event/new',
            'page_git_url': '/tree/master/_database/templates/event_new_view.html',
            'page_name': self.space_name+' | New event',
            'page_description': 'Organize an event at '+self.space_name,
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:4],
            'default_space': Space.objects.filter(str_name_en_US=EVENTS_SPACE_DEFAULT).first(),
            'all_spaces': Space.objects.exclude(str_name_en_US=EVENTS_SPACE_DEFAULT),
            'all_guildes': Guilde.objects.all(),
            'csrf_token': get_token(request)
        }

    def get(self, request):
        self.log('EventsView.get()')
        request = Request(request)

        # process all events view
        if self.path == 'all':
            context = self.all_results(request)

        # process single event view
        elif self.path == 'result' and 'sub_page' in self.args and self.args['sub_page']:
            context = self.result(request, self.args['sub_page'])

        # process get banner
        elif self.path == 'banner' and 'sub_page' in self.args and self.args['sub_page']:
            context = self.banner(request, self.args['sub_page'])

        # process create event view
        elif self.path == 'new':
            context = self.new(request)

        return render(request.request, 'page.html', context)
