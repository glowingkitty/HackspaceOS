from _website.views.view import View
from django.shortcuts import render
from _website.models import Request, Response
from django.template.loader import get_template


class LandingpageView(View):
    def get_context(self, request):
        self.log('LandingpageView.get_context()')
        from _database.models import Event, Photo

        request = Request(request)
        response = Response()
        self.context = {
            'view': 'landingpage_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/',
            'page_git_url': '/tree/master/_website/templates/landingpage_view.html',
            'page_name': self.space_name,
            'page_description': response.description,
            'is_open_status': response.space_open(request.language),
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:5],
            'photos': Photo.objects.latest()[:33]
        }

    def get(self, request):
        self.log('LandingpageView.get()')
        self.get_context(request)
        return render(request, 'page.html', self.context)

    def html(self):
        self.log('LandingpageView.html()')
        return {
            'html': get_template(self.context['view']+'.html').render(self.context),
            'page_name': self.context['page_name']
        }
