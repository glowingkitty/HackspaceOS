class MeetingEnd():
    def __init__(self, request):
        from _database.models import MeetingNote
        from django.http import JsonResponse

        current_meeting = MeetingNote.objects.current()
        if current_meeting:
            current_meeting.end()
            response = JsonResponse(
                {'meeting_url': '/meeting/'+current_meeting.text_date})

        else:
            response = JsonResponse({'alert': 'No current meeting found'})
            response.status_code = 500

        self.value = response
