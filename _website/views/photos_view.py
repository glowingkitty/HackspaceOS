from _website.views.view import View
from secrets import Secret
from config import Config
from django.shortcuts import render
from _website.models import Request


class PhotosView(View):
    def get(self, request):
        self.log('PhotosView.get()')
        from _database.models import Photo

        request = Request(request)
        context = {
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
        return render(request.request, 'page.html', context)
