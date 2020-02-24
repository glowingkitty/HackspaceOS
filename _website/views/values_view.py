from _website.views.view import View
from secrets import Secret
from config import Config
from django.shortcuts import render
from _website.models import Request, Response


class ValuesView(View):
    def get(self, request):
        self.log('ValuesView.get()')

        request = Request(request)
        context = {
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
        return render(request.request, 'page.html', context)
