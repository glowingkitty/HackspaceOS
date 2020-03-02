class EventOverlap():
    def __init__(self, request):
        from _database.models import Event
        from django.http import JsonResponse
        from django.template.loader import get_template
        from _website.models import Request

        str_date = request.GET.get('date', None)
        str_time = request.GET.get('time', None)
        str_duration = request.GET.get('duration', None)
        if str_date and str_time and str_duration:
            from _database.models import Helper

            overlapping_events = Event.objects.JSON__overlapping_events(
                Helper().INT__UNIX_from_date_and_time_STR(str_date, str_time),
                Helper().INT__duration_minutes(str_duration),
                request.GET.get('space', None),
            )

            self.value = JsonResponse({
                'int_overlapping_events': len(overlapping_events['overlapping_events']),
                'html': get_template(
                    'components/body/event_new/form_elements/overlapping_events.html').render({
                        'language': Request(request).language,
                        'overlapping_events': overlapping_events
                    })})
        else:
            self.value = JsonResponse({
                'error': 'Variables missing - date, time and duration needed.'})
