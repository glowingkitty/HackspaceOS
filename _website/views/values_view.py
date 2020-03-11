from _website.views.view import View
from _setup.models import Secret
from _setup.models import Config
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class ValuesView(View):
    def get_context(self, request):
        self.log('ValuesView.get_context()')
        request = Request(request)
        self.context = {
            'view': 'values_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/values',
            'page_git_url': '/tree/master/_website/templates/values_view.html',
            'page_name': self.space_name+' | Values',
            'page_description': 'Our values at '+self.space_name
        }

    def get(self, request):
        self.log('ValuesView.get()')
        self.get_context(request)
        return render(request, 'page.html', self.context)

    def html(self):
        self.log('ValuesView.html()')
        return get_template(self.context['view']+'.html').render(self.context)
