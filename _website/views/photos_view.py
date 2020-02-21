from django.http import HttpResponse
from django.views import View
from secrets import Secret
from config import Config
from django.shortcuts import render
import time
from _website.models import Request, Response
from log import log


class PhotosView(View):

    def __init__(self, show_log=True):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.show_log = show_log

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            log('{}'.format(text), os.path.basename(__file__), self.started)

    def get(self, request):
        self.log('PhotosView.get()')
        from _database.models import Photo

        request = Request(request)
        context = {
            'view': 'photos_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': Secret('DJANGO.ADMIN_URL').value,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/photos',
            'page_git_url': '/tree/master/_website/templates/photos_view.html',
            'page_name': Config('BASICS.NAME').value+' | Photos',
            'page_description': 'Explore '+Config('BASICS.NAME').value+'\'s history in photos!',
            'photos': Photo.objects.latest()[:30]
        }
        return render(request.request, 'page.html', context)
