from _website.views.view import View
from secrets import Secret
from config import Config
from django.shortcuts import render
from _website.models import Request


class ConsensusView(View):
    def get(self, request):
        self.log('ConsensusView.get()')
        from _database.models import Consensus

        request = Request(request)
        context = {
            'view': 'consensus_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/consensus',
            'page_git_url': '/tree/master/_website/templates/consensus_view.html',
            'page_name': self.space_name+' | Big-C consensus items',
            'page_description': 'When you want to do something that would drastically change '+self.space_name+' (or need a lot of money from Noisebridge for a project) - suggest a Big-C consensus item!',
            'all_current_items': Consensus.objects.current(),
            'all_current_items_count': Consensus.objects.current().count(),
            'all_archived_items': Consensus.objects.archived(),
            'all_archived_items_count': Consensus.objects.archived().count(),
        }
        return render(request.request, 'page.html', context)
