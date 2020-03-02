class MeetingDuration():
    def __init__(self, request):
        from django.http import JsonResponse
        from _database.models import MeetingNote
        from _website.models import Request
        marry_messages = []
        meeting = MeetingNote.objects.current()
        running_since = meeting.running_since if meeting else None
        if Request(request).in_space:
            if running_since == '1h 30min':
                marry_messages.append(
                    'Thanks everyone for partipicating in the weekly meeting. The meeting is going on now for 1 hour and 30 minutes')
            elif running_since == '2h 30min':
                marry_messages.append(
                    'I always love people actively discussion topics related to Noisebridge. However, it seems the meeting is going on now for 2 hours and 30 minutes. Please come to an end soon')

        self.value = JsonResponse(
            {
                'html': running_since,
                'marryspeak': marry_messages
            })
