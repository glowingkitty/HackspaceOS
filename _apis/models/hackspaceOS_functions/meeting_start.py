class MeetingStart():
    def __init__(self, request):
        from django.http import JsonResponse
        from django.template.loader import get_template
        from _website.models import Request

        self.value = JsonResponse(
            {
                'success': True,
                'html': get_template(
                    'components/body/meetings/current_meeting.html').render({
                        'language': Request(request).language,
                    })
            }
        )
