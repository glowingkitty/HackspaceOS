class EventsSlider():
    def __init__(self, request):
        from django.http import JsonResponse
        from django.template.loader import get_template
        from _database.models import Event
        from _website.models import Request

        marry_messages = []
        in_space = request.COOKIES.get('in_space')
        if request:
            request = Request(request)
        if in_space:
            events_in_5_minutes = Event.objects.LIST__in_minutes(
                minutes=5, name_only=True)
            events_in_30_minutes = Event.objects.LIST__in_minutes(
                minutes=30, name_only=True)
            if events_in_5_minutes or events_in_30_minutes:
                marry_messages.append('We have some awesome events upcoming')
            for event in events_in_5_minutes:
                marry_messages.append(event+' starts in 5 minutes.')
            for event in events_in_30_minutes:
                marry_messages.append(event+' starts in 30 minutes.')

        self.value = JsonResponse(
            {
                'html': get_template(
                    'components/body/events_slider.html').render({
                        'language': request.language,
                        'upcoming_events': Event.objects.QUERYSET__upcoming()[:5]
                    }),
                'marryspeak': marry_messages
            }
        )
