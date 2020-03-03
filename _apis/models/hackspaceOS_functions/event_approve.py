class EventApprove():
    def __init__(self, request=None):
        from _database.models import Event
        from _apis.models import Notify
        from django.http import JsonResponse
        from config import Config

        if not request or request.user.is_authenticated == False:
            response = JsonResponse(
                {'success': False, 'error': '--> Failed: User not logged in'})
            response.status_code = 403
        elif not request.GET.get('str_slug', None) or Event.objects.filter(boolean_approved=False, str_slug=request.GET.get('str_slug', None)).exists() == False:
            response = JsonResponse(
                {'success': False, 'error': '--> Failed: Result not found'})
            response.status_code = 404
        else:

            DOMAIN = Config('WEBSITE.DOMAIN').value
            # approve event and all upcoming ones
            event = Event.objects.filter(
                boolean_approved=False, str_slug=request.GET.get('str_slug', None)).first()

            upcoming_events = Event.objects.filter(
                boolean_approved=False, str_name_en_US=event.str_name_en_US).all()
            print('--> Approve all upcoming events')
            for event in upcoming_events:
                event.publish()

            # notify that event was approved and by who
            if 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == DOMAIN:
                Notify().send('✅'+str(request.user)+' approved the event "' +
                              event.str_name_en_US+'":\nhttps://'+DOMAIN+'/'+event.str_slug)

            response = JsonResponse({'success': True})
            response.status_code = 200

        self.value = response
