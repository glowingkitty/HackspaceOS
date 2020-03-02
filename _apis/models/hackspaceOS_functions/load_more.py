class LoadMore():
    def __init__(self, what, request):
        from django.http import JsonResponse
        from _database.models import Helper, MeetingNote, Event, Project, Space, Machine, Guilde, Consensus
        if what and request.GET.get('from', None):
            if what == 'meeting_notes':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'meetings/meetings_list.html', MeetingNote.objects.past())
            elif what == 'events':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Event.objects.QUERYSET__upcoming())
            elif what == 'projects':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Project.objects.latest())
            elif what == 'spaces':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Space.objects.all())
            elif what == 'machines':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Machine.objects.all())
            elif what == 'guildes':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'results_list_entries.html', Guilde.objects.all())
            elif what == 'consensus':
                response = Helper().JSON_RESPONSE_more_results(
                    request, 'consensus_items_entries.html', Consensus.objects.latest())
            elif what == 'photos':
                response = Helper().JSON_RESPONSE_more_photos(request)
        else:
            response = JsonResponse({'error': 'Request incomplete or wrong'})
            response.status_code = 404

        self.value = response
