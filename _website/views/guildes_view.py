from _website.views.view import View
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class GuildesView(View):
    def all_results(self, request):
        self.log('-> GuildesView().all_results()')
        from _database.models import Guilde
        request = Request(request)
        all_results = Guilde.objects.all()[:10]
        self.context = {
            'view': 'results_list',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/guildes',
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': self.space_name+' | Guildes',
            'page_description': 'Join a guilde at '+self.space_name+'!',
            'headline': 'Guildes',
            'description': 'A guilde is ...',
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/guilde/add/'.format(self.admin_url),
            'addnew_text': 'Add guilde',
            'all_results': all_results if all_results else True,
            'results_count': Guilde.objects.count(),
            'show_more': 'guildes'
        }

    def result(self, request, sub_page):
        self.log('-> GuildesView().result()')
        from _database.models import Guilde
        request = Request(request)

        if 'guilde/' not in sub_page:
            sub_page = 'guilde/'+sub_page
        selected = Guilde.objects.filter(str_slug=sub_page).first()

        self.context = {
            'view': 'guilde_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/guilde/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/guilde_view.html',
            'page_name': self.space_name+' | Guilde | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        }

    def get(self, request):
        self.log('GuildesView.get()')

        # process all guildes view
        if self.path == 'all':
            self.all_results(request)

        # process single event view
        elif self.path == 'result' and 'sub_page' in self.args and self.args['sub_page']:
            self.result(request, self.args['sub_page'])

        return render(request, 'page.html', self.context)

    def html(self):
        self.log('GuildesView.html()')
        return get_template(self.context['view']+'.html').render(self.context)
