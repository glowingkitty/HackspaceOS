class EventCreate():
    def __init__(self, request=None):
        from _apis.models import Notify
        from _database.models import Helper, Event, Space, Guilde, Person
        from config import Config
        from secrets import Secret
        from django.http import JsonResponse

        DOMAIN = Config('WEBSITE.DOMAIN').value

        int_UNIXtime_event_start = Helper().INT__UNIX_from_date_and_time_STR(
            request.POST.get('date', None), request.POST.get('time', None))
        int_minutes_duration = Helper().INT__duration_minutes(
            request.POST.get('duration', None))

        try:
            if request.FILES['images[0]'].content_type == 'image/jpeg' or request.FILES['images[0]'].content_type == 'image/png':
                image = request.FILES['images[0]']
            else:
                image = None
        except:
            image = None

        uploaded_photo_url = request.POST.get('photo', None)

        new_event = Event(
            boolean_approved=request.user.is_authenticated,
            str_name_en_US=request.POST.get('name_english', None),
            str_name_he_IL=request.POST.get('name_hebrew', None),
            int_UNIXtime_event_start=int_UNIXtime_event_start,
            int_minutes_duration=int_minutes_duration,
            int_UNIXtime_event_end=int_UNIXtime_event_start +
            (60*int_minutes_duration),
            url_featured_photo=uploaded_photo_url if 'https' in uploaded_photo_url else None,
            image_featured_photo=image,
            text_description_en_US=request.POST.get(
                'description_english', None),
            text_description_he_IL=request.POST.get(
                'description_hebrew', None),
            one_space=Space.objects.QUERYSET__by_name(
                request.POST.get('space', None)),
            one_guilde=Guilde.objects.QUERYSET__by_name(
                request.POST.get('guilde', None)),
            str_crowd_size=request.POST.get('expected_crowd', None),
            str_welcomer=request.POST.get('event_welcomer', None),
            boolean_looking_for_volunteers=True if request.POST.get(
                'volunteers', None) == 'yes' else False
        )
        if request.POST.get('location', None):
            if request.POST.get('location', None) != Config('BASICS.NAME').value:
                new_event.str_location = request.POST.get('location', None)
        if request.POST.get('repeating', None):
            # if repeating, mark as such and auto generate new upcoming events with "update_database" command
            str_repeating_how_often = request.POST.get('repeating', None)
            str_repeating_up_to = request.POST.get('repeating_up_to', None)

            if str_repeating_how_often and str_repeating_how_often != '':
                new_event.int_series_startUNIX = new_event.int_UNIXtime_event_start
                new_event.str_series_repeat_how_often = str_repeating_how_often

            if str_repeating_up_to and str_repeating_up_to != '':
                new_event.int_series_endUNIX = Helper().INT__UNIX_from_date_and_time_STR(
                    str_repeating_up_to, request.POST.get('time', None))

        new_event.save()

        hosts = request.POST.get('hosts', None)
        if hosts:
            if hosts.startswith(','):
                hosts = hosts[1:]
            hosts = hosts.split(',')
            for host in hosts:
                new_event.many_hosts.add(Person.objects.by_url_discourse(host))

        # if loggedin user: share event to other platforms (Meetup, Discourse, etc.)
        if request.user.is_authenticated:
            new_event.create_discourse_event()
            new_event.create_meetup_event()

        # else (if event created via live website) inform via slack about new event and give community chance to delete it or confirm it
        elif 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == DOMAIN:
            Notify().send(
                'A website visitor created a new event via our website.\n' +
                'If no one deletes it within the next 24 hours, it will be automatically published and appears in our website search'+(', meetup group' if Secret('MEETUP.ACCESS_TOKEN').value else '')+(' and discourse' if Secret('DISCOURSE.API_KEY').exists == True else '')+'.\n' +
                '🚫-> Does this event already exist or is it spam? Open on the following event link and click "Delete event".\n' +
                '✅-> You have a user account for our website and want to publish the event directly? Open on the following event link and click "Approve event".\n' +
                'https://'+DOMAIN+'/'+new_event.str_slug
            )
        else:
            self.value = JsonResponse(
                {
                    'error': '--> Request not sent via hackerspace domain. Skipped notifying via Slack.'
                }
            )

        # if event is repeating, create upcoming instances
        new_event = new_event.create_upcoming_instances()

        # if user is signed in and event autoapproved - direct to event page, else show info
        self.value = JsonResponse(
            {
                'url_next': '/'+new_event.str_slug
            }
        )
