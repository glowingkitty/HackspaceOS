class Search():
    def __init__(self, request):
        from django.http import JsonResponse
        from _apis.models import Search
        from _website.models import Request
        from django.template.loader import get_template

        language = Request(request).language
        search_results = Search().query(request.GET.get(
            'q', None), request.GET.get('filter', None))
        self.value = JsonResponse(
            {
                'num_results': len(search_results),
                'html': get_template(
                    'components/search/search_results.html').render({
                        'language': language,
                        'search_results': search_results
                    }) if not request.GET.get('filter', None) else get_template('components/body/event_new/hosts_search_results.html').render({
                        'language': language,
                        'all_hosts': search_results[:4],
                    }) if request.GET.get('filter', None) == 'hosts' else get_template('components/body/results_list_entries.html').render({
                        'language': language,
                        'all_results': search_results[:4],
                    }),
            }
        )
