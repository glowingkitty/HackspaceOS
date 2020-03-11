from _website.views.view import View
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class ConsensusView(View):
    def get_context(self, request):
        self.log('ConsensusView.get_context()')
        from _database.models import Consensus

        request = Request(request)
        self.context = {
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

    def get(self, request):
        self.log('ConsensusView.get()')
        self.get_context(request)
        return render(request, 'page.html', self.context)

    def html(self):
        self.log('ConsensusView.html()')
        return get_template(self.context['view']+'.html').render(self.context)
