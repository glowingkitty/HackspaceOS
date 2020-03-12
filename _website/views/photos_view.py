from _website.views.view import View
from _setup.models import Secret
from _setup.models import Config
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class PhotosView(View):
    def get_context(self, request):
        self.log('PhotosView.get_context()')
        from _database.models import Photo

        request = Request(request)
        self.context = {
            'view': 'photos_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/photos',
            'page_git_url': '/tree/master/_website/templates/photos_view.html',
            'page_name': self.space_name+' | Photos',
            'page_description': 'Explore '+self.space_name+'\'s history in photos!',
            'photos': Photo.objects.latest()[:30]
        }

    def get(self, request):
        self.log('PhotosView.get()')
        self.get_context(request)
        return render(request, 'page.html', self.context)

    def html(self):
        self.log('PhotosView.html()')
        return {
            'html': get_template(self.context['view']+'.html').render(self.context),
            'page_name': self.context['page_name']
        }
