from _website.views.view import View
from django.shortcuts import render
from _website.models import Request


class MachinesView(View):
    def all_results(self, request):
        self.log('-> MachinesView().all_results()')
        from _database.models import Machine
        request = Request(request)
        all_results = Machine.objects.all()[:10]
        return render(request.request, 'page.html', {
            'view': 'spaces_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/machines',
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': self.space_name+' | Machines',
            'page_description': self.space_name+' has all kinds of awesome machines!',
            'headline': 'Machines',
            'description': 'We have many useful machines ...',
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/machine/add/'.format(self.admin_url),
            'addnew_text': 'Add machine',
            'all_results': all_results if all_results else True,
            'results_count': Machine.objects.count(),
            'show_more': 'machines'
        })

    def result(self, request, sub_page):
        self.log('-> MachinesView().result()')
        from _database.models import Machine
        request = Request(request)

        if 'machine/' not in sub_page:
            sub_page = 'machine/'+sub_page
        selected = Machine.objects.filter(str_slug=sub_page).first()

        return render(request.request, 'page.html', {
            'view': 'machine_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/machine/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/machine_view.html',
            'page_name': self.space_name+' | Machine | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        })

    def get(self, request):
        self.log('MachinesView.get()')

        # process all guildes view
        if self.path == 'all':
            return self.all_results(request)

        # process single event view
        elif self.path == 'result' and 'sub_page' in self.args and self.args['sub_page']:
            return self.result(request, self.args['sub_page'])
