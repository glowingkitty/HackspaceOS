from _website.views.view import View
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class SpacesView(View):
    def all_results(self, request):
        self.log('-> SpacesView().all_results()')
        from _database.models import Space
        request = Request(request)
        all_results = Space.objects.all()[:10]

        self.context = {
            'view': 'spaces_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/spaces',
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': self.space_name+' | Spaces',
            'page_description': self.space_name+' has many awesome spaces!',
            'headline': 'Spaces',
            'description': 'At {} fellow hackers created all kind of awesome spaces...'.format(self.space_name),
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/space/add/'.format(self.admin_url),
            'addnew_text': 'Add space',
            'all_results': all_results if all_results else True,
            'results_count': Space.objects.count(),
            'show_more': 'spaces'
        }

    def result(self, request, sub_page):
        self.log('-> SpacesView().result()')
        from _database.models import Space
        request = Request(request)

        if 'space/' not in sub_page:
            sub_page = 'space/'+sub_page
        selected = Space.objects.filter(str_slug=sub_page).first()

        self.context = {
            'view': 'space_view',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/space/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/space_view.html',
            'page_name': self.space_name+' | Space | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        }

    def get(self, request):
        self.log('SpacesView.get()')

        # process all guildes view
        if self.path == 'all':
            self.all_results(request)

        # process single event view
        elif self.path == 'result' and 'sub_page' in self.args and self.args['sub_page']:
            self.result(request, self.args['sub_page'])

        return render(request, 'page.html', self.context)

    def html(self):
        self.log('SpacesView.html()')
        return get_template('page.html').render(self.context)
