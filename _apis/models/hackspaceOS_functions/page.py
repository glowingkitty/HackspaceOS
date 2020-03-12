class Page():
    def __init__(self, page, request=None):
        from django.http import JsonResponse
        from _website import views

        if page == '__':
            page = 'landingpage'
        else:
            page = page.replace('__', '', 1)

        if '__' in page:
            page, sub_page = page.split('__')
        else:
            sub_page = None

        page = page.replace('__', '_')

        # get pages which can be loaded in the frontend via javascript
        if page == 'landingpage':
            view = views.LandingpageView()
            view.get_context(request)

        elif page == 'values':
            view = views.ValuesView()
            view.get_context(request)

        elif page == 'meetings':
            view = views.MeetingsView()
            view.all_results(request)

        elif page == 'meeting' and sub_page and sub_page == 'present':
            view = views.MeetingsView()
            view.present(request)

        elif page == 'meeting' and sub_page:
            view = views.MeetingsView()
            view.result(request, sub_page)

        elif page == 'guildes':
            view = views.GuildesView()
            view.all_results(request)

        elif page == 'guilde' and sub_page:
            view = views.GuildesView()
            view.result(request, sub_page)

        elif page == 'spaces':
            view = views.SpacesView()
            view.all_results(request)

        elif page == 'space' and sub_page:
            view = views.SpacesView()
            view.result(request, sub_page)

        elif page == 'machines':
            view = views.MachinesView()
            view.all_results(request)

        elif page == 'machine' and sub_page:
            view = views.MachinesView()
            view.result(request, sub_page)

        elif page == 'projects':
            view = views.ProjectsView()
            view.get_context(request)

        elif page == 'events':
            view = views.EventsView()
            view.all_results(request)

        elif page == 'event' and sub_page and sub_page == 'new':
            view = views.EventsView()
            view.new(request)

        elif page == 'event' and sub_page:
            view = views.EventsView()
            view.result(request, sub_page)

        elif page == 'photos':
            view = views.PhotosView()
            view.get_context(request)

        elif page == 'consensus':
            view = views.ConsensusView()
            view.get_context(request)

        print(page)
        self.value = JsonResponse(view.html())
