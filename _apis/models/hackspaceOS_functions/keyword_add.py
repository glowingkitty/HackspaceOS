class KeywordAdd():
    def __init__(self, request):
        from django.http import JsonResponse
        from _database.models import MeetingNote

        if request.GET.get('keyword', None) and request.GET.get('origin', None) and MeetingNote.objects.filter(text_date=request.GET.get('origin', None).split('/')[1]).exists():
            meeting = MeetingNote.objects.filter(
                text_date=request.GET.get('origin', None).split('/')[1]).first()

            meeting.keyword_add(request.GET.get('keyword'))
            response = JsonResponse({'success': True})
        else:
            response = JsonResponse({'error': 'Request incomplete or wrong'})
            response.status_code = 404

        self.value = response
