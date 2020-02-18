from log import log
from django.db import models
from config import Config


class EventSet(models.QuerySet):
    def QUERYSET__next_meeting(self):
        log('Event.objects.QUERYSET__next_meeting(self)')
        import time

        log('--> return QUERYSET')
        return self.filter(str_name_en_US__icontains='General Meeting', int_UNIXtime_event_start__gt=time.time()).order_by('int_UNIXtime_event_start').first()

    def QUERYSET__now(self):
        log('Event.objects.QUERYSET__now(self)')
        import time

        log('--> return QUERYSET')
        return self.filter(int_UNIXtime_event_end__gt=time.time(), int_UNIXtime_event_start__lte=time.time(), boolean_approved=True).order_by('int_UNIXtime_event_start')

    def QUERYSET__in_timeframe(self, from_UNIX_time, to_UNIX_time, str_space_name=None):
        log('Event.objects.QUERYSET__in_timeframe(self, from_UNIX_time={}, to_UNIX_time={}, str_space_name={})'.format(
            from_UNIX_time, to_UNIX_time, str_space_name))
        from django.db.models import Q
        from _database.models import Space
        if str_space_name:
            space = Space.objects.QUERYSET__by_name(str_space_name)
            if space:
                self = self.filter(one_space=space)

        output = self.filter(
            # get events that start after from_UNIX_time and end before to_UNIX_time
            (
                Q(int_UNIXtime_event_start__gte=from_UNIX_time) &
                Q(int_UNIXtime_event_start__lte=to_UNIX_time)
            )
            # get events that end after from_UNIX_time and before to_UNIX_time
            | (
                Q(int_UNIXtime_event_end__gte=from_UNIX_time) &
                Q(int_UNIXtime_event_end__lte=to_UNIX_time)
            )
            # get events that start before from_UNIX_time and end after to_UNIX_time
            | (
                Q(int_UNIXtime_event_start__lte=from_UNIX_time) &
                Q(int_UNIXtime_event_end__gte=to_UNIX_time)
            )
        ).exclude(
            Q(int_UNIXtime_event_start__gte=to_UNIX_time) |
            Q(int_UNIXtime_event_end__lte=from_UNIX_time)
        ).exclude(
            boolean_approved=False
        )
        log('--> return QUERYSET ({} results)'.format(output.count()))
        return output

    def JSON__overlapping_events(self, new_event_UNIX_time, new_event_duration_minutes, space):
        log('Event.objects.JSON__overlapping_events(self, new_event_UNIX_time={}, new_event_duration_minutes={}, space={})'.format(
            new_event_UNIX_time, new_event_duration_minutes, space))
        import pytz
        from datetime import datetime, timedelta
        from config import Config
        from _database.models import Event

        local_time = datetime.fromtimestamp(
            new_event_UNIX_time, pytz.timezone(Config('PHYSICAL_SPACE.TIMEZONE_STRING').value))

        hours_before = 1
        hours_event_duration = round(new_event_duration_minutes/60)
        hours_after = 1

        times = []

        counter = 0
        while counter < hours_before:
            counter += 1
            times.insert(0, {
                'int_UNIX_time': round(new_event_UNIX_time-(counter*60)),
                'str_readable': str((local_time+timedelta(hours=-counter)).strftime('%I:%M %p'))
            })

        counter = 0
        while counter < hours_event_duration:
            times.append({
                'int_UNIX_time': round(new_event_UNIX_time+(counter*60)),
                'str_readable': str((local_time+timedelta(hours=counter)).strftime('%I:%M %p'))
            })
            counter += 1

        while (counter-hours_event_duration) < hours_after:
            times.append({
                'int_UNIX_time': round(new_event_UNIX_time+(counter*60)),
                'str_readable': str((local_time+timedelta(hours=counter)).strftime('%I:%M %p'))
            })
            counter += 1

        for time in times:
            time['int_percent_height'] = str(100/len(times))+'%'

        queryset_overlapping_events = Event.objects.QUERYSET__in_timeframe(
            new_event_UNIX_time, new_event_UNIX_time+(new_event_duration_minutes*60), space)

        # get values needed to show events in correct position
        list_overlapping_events = []
        for event in queryset_overlapping_events:
            minutes_distance = ((
                event.int_UNIXtime_event_start - times[0]['int_UNIX_time'])/60)+60

            list_overlapping_events.append({
                'str_name_en_US': event.str_name_en_US,
                'str_slug': event.str_slug,
                'int_percent_top_distance': str(round((minutes_distance/(len(times)*60))*100))+'%',
                'int_percent_height': str(round(event.int_minutes_duration/(len(times)*60)*100))+'%'
            })

        your_event_minutes_distance = (
            (new_event_UNIX_time - times[0]['int_UNIX_time'])/60)+60
        log('--> return JSON ({} overlapping events)'.format(len(list_overlapping_events)))
        return {
            'times': times,
            'your_event': {
                'int_percent_top_distance': str(round((your_event_minutes_distance/(len(times)*60))*100))+'%',
                'int_percent_height': str(round(new_event_duration_minutes/(len(times)*60)*100))+'%'
            },
            'overlapping_events': list_overlapping_events
        }

    def QUERYSET__in_space(self, one_space=None, str_space=None):
        log('Event.objects.QUERYSET__in_space(self, one_space={}, str_space={})'.format(
            one_space, str_space))
        if one_space:
            log('--> return QUERYSET')
            return self.filter(one_space=one_space)
        elif str_space:
            log('--> return QUERYSET')
            return self.filter(one_space__str_name_en_US=str_space)
        else:
            return []

    def QUERYSET__by_host(self, one_host=None, str_host=None):
        log('Event.objects.QUERYSET__by_host(self, one_host={}, str_host={})'.format(
            one_host, str_host))
        if one_host:
            log('--> return QUERYSET')
            return self.filter(many_hosts=one_host)
        elif str_host:
            log('--> return QUERYSET')
            return self.filter(many_hosts__str_name_en_US__contains=str_host)
        else:
            return []

    def QUERYSET__by_guilde(self, one_guilde=None, str_guilde=None):
        log('Event.objects.QUERYSET__by_guilde(self, one_guilde={}, str_guilde={})'.format(
            one_guilde, str_guilde))
        if one_guilde:
            log('--> return QUERYSET')
            return self.filter(one_guilde=one_guilde)
        elif str_guilde:
            log('--> return QUERYSET')
            return self.filter(one_guilde__str_name_en_US__contains=str_guilde)
        else:
            return []

    def as_list(self):
        log('Event.objects.as_list(self)')
        for event in self.all():
            print(event)

    def publish(self):
        log('Event.objects.publish(self)')
        for event in self.all():
            event.publish()

    def QUERYSET__not_approved(self):
        log('Event.objects.QUERYSET__not_approved(self)')
        log('--> return QUERYSET')
        return self.filter(boolean_approved=False)

    def QUERYSET__older_then_24h(self):
        import time
        log('Event.objects.QUERYSET__older_then_24h(self)')
        log('--> return QUERYSET')
        return self.filter(int_UNIXtime_created__lte=time.time()-(24*60*60))

    def QUERYSET__upcoming(self, boolean_approved=False):
        log('Event.objects.QUERYSET__upcoming(self,boolean_approved={})'.format(
            boolean_approved))
        import time

        log('--> return QUERYSET')
        return self.filter(int_UNIXtime_event_end__gt=time.time()).exclude(boolean_approved=boolean_approved).order_by('int_UNIXtime_event_start')

    def LIST__in_minutes(self, minutes, name_only=False):
        log('Event.objects.LIST__in_minutes(self,minutes={},name_only={})'.format(
            minutes, name_only))
        import pytz
        from datetime import datetime, timedelta
        from config import Config

        date_in_x_minutes = datetime.now(pytz.timezone(
            Config('PHYSICAL_SPACE.TIMEZONE_STRING').value))+timedelta(minutes=minutes)
        events_in_x_minutes = []
        self = self.QUERYSET__upcoming()[:3]
        for event in self.all():
            event_start_date = event.datetime_start

            if event_start_date.date() == date_in_x_minutes.date() \
                    and event_start_date.hour == date_in_x_minutes.hour \
                    and event_start_date.minute == date_in_x_minutes.minute:
                events_in_x_minutes.append(event)

        if name_only == True:
            log('--> return LIST')
            return [x.str_name_en_US.replace('&', 'and').replace('@', 'at').replace('|', '').replace('#', 'sharp') for x in events_in_x_minutes]

        log('--> return LIST')
        return events_in_x_minutes

    def LIST__search_results(self):
        log('Event.objects.LIST__search_results(self)')
        results_list = []
        added = []
        results = self.all()
        for result in results:
            if not result.str_name_en_US in added:
                relative_time = result.str_relative_time
                results_list.append({
                    'icon': 'event',
                    'name': result.str_name_en_US+'<br>=> '+(relative_time if relative_time else str(result.datetime_start.date())),
                    'url': '/'+result.str_slug,
                    'menu_heading': 'menu_h_events'
                })
                added.append(result.str_name_en_US)
        log('--> return LIST')
        return results_list

    def RESPONSE__JSON(self):
        from django.http import JsonResponse
        events = []
        for event in self.all():
            events.append(event.json_data)
        return JsonResponse(
            {
                'num_events': len(events),
                'events': events
            }
        )

    def announce(self):
        log('Event.objects.announce(self)')
        self.announce_via_marry()
        self.announce_via_flaschentaschen()

    def announce_via_flaschentaschen(self):
        log('Event.objects.announce_via_flaschentaschen(self)')
        for event in self.all()[:3]:
            event.announce_via_flaschentaschen()

    def announce_via_marry(self):
        log('Event.objects.announce_via_marry(self)')
        for event in self.all()[:3]:
            event.announce_via_marry()

    def import_from_discourse(self):
        log('Event.objects.import_from_discourse(self)')
        from _apis.models import Discourse
        from dateutil.parser import parse
        from datetime import datetime
        from django.db.models import Q
        from _database.models import Event

        events = Discourse().get_category_posts('events', True)
        now = datetime.now()
        for event in events:
            if 'event' in event:
                date_start = parse(event['event']['start'])
                if date_start.year >= now.year and date_start.month >= now.month and date_start.day >= now.day:
                    if Event.objects.filter(Q(str_name_en_US=event['title']) | Q(str_name_he_IL=event['title'])).exists() == False:
                        event['description'] = Discourse().get_post_details(event['slug'])[
                            'cooked']
                        self.createEvent(event)

    def update_field(self, fieldname, content):
        from _database.models import Event

        if fieldname == 'str_name_en_US':
            for entry in self.all():
                entry.str_name_en_US = content
                super(Event, entry).save()
        elif fieldname == 'str_name_he_IL':
            for entry in self.all():
                entry.str_name_en_US = content
                super(Event, entry).save()
        elif fieldname == 'text_description_en_US':
            for entry in self.all():
                entry.text_description_en_US = content
                super(Event, entry).save()
        elif fieldname == 'text_description_he_IL':
            for entry in self.all():
                entry.text_description_he_IL = content
                super(Event, entry).save()

    def import_from_meetup(self, slug=Config('EVENTS.MEETUP_GROUP').value):
        from _database.models import Event
        from _apis.models import Meetup
        events = Meetup(slug).events
        for event in events:
            Event().create(json_content=event)
