class MeetingCreate():
    def __init__(self, request):
        from _database.models import MeetingNote
        from django.http import JsonResponse
        from django.template.loader import get_template
        from _website.models import Request

        new_meeting = MeetingNote()
        new_meeting.save()

        self.value = JsonResponse(
            {
                'success': True,
                'html': get_template(
                    'components/body/meetings/current_meeting.html').render({
                        'language': Request(request).language,
                        'current_meeting': new_meeting
                    })
            }
        )
