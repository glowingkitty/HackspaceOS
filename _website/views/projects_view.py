from _website.views.view import View
from django.shortcuts import render
from _website.models import Request
from django.template.loader import get_template


class ProjectsView(View):
    def get_context(self, request):
        self.log('ProjectsView.get_context()')
        from _database.models import Project
        from _setup.models import Secret

        request = Request(request)

        all_results = Project.objects.all()[:10]
        self.context = {
            'view': 'results_list',
            'in_space': request.in_space,
            'hash': request.hash,
            'ADMIN_URL': self.admin_url,
            'user': request.user,
            'language': request.language,
            'auto_search': request.search,
            'slug': '/projects',
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': self.space_name+' | Projects',
            'page_description': 'People at '+self.space_name+' created all kinds of awesome projects!',
            'headline': 'Projects',
            'description': 'At {} fellow hackers created awesome projects...'.format(self.space_name),
            'wiki_url': None,
            'add_new_requires_user': False,
            'addnew_url': '{}c/projects/'.format(Secret('DISCOURSE.DISCOURSE_URL').value),
            'addnew_text': 'Add project',
            'all_results': all_results if all_results else True,
            'results_count': Project.objects.count(),
            'show_more': 'projects'
        }

    def get(self, request):
        self.log('ProjectsView.get()')
        self.get_context(request)
        return render(request, 'page.html', self.context)

    def html(self):
        self.log('ProjectsView.html()')
        return {
            'html': get_template(self.context['view']+'.html').render(self.context),
            'page_name': self.context['page_name']
        }
