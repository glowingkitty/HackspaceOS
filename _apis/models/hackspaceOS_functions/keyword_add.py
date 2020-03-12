class KeywordAdd():
    def __init__(self, keyword, request):
        from django.http import JsonResponse
        from _database.models import MeetingNote

        text_date = request.META['HTTP_REFERER'].split('/')[-1]
        if keyword and request.META['HTTP_REFERER'] and MeetingNote.objects.filter(text_date=text_date).exists():
            meeting = MeetingNote.objects.filter(text_date=text_date).first()

            meeting.keyword_add(keyword)
            response = JsonResponse({'success': True})
        else:
            response = JsonResponse({'error': 'Request incomplete or wrong'})
            response.status_code = 404

        self.value = response
