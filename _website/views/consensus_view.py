from django.views import View
from secrets import Secret
from config import Config
from django.shortcuts import render
import time
from _website.models import Request
from log import log


class ConsensusView(View):

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
        self.log('ConsensusView.get()')
        from _database.models import Consensus

        request = Request(request)
        context = {
            'view': 'consensus_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': Secret('DJANGO.ADMIN_URL').value,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/consensus',
            'page_git_url': '/tree/master/_website/templates/consensus_view.html',
            'page_name': Config('BASICS.NAME').value+' | Big-C consensus items',
            'page_description': 'When you want to do something that would drastically change '+Config('BASICS.NAME').value+' (or need a lot of money from Noisebridge for a project) - suggest a Big-C consensus item!',
            'all_current_items': Consensus.objects.current(),
            'all_current_items_count': Consensus.objects.current().count(),
            'all_archived_items': Consensus.objects.archived(),
            'all_archived_items_count': Consensus.objects.archived().count(),
        }
        return render(request.request, 'page.html', context)
