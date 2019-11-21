from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_MEETUP_GROUP

from django.core import serializers
from django.db import models


def getWeekday(number):
    days = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    return days[number]


def updateTime(result):
    import time

    # update time
    if not result.int_UNIXtime_created:
        result.int_UNIXtime_created = time.time()
    result.int_UNIXtime_updated = time.time()
    return result


def extractSpace(json_meetup_result):
    from hackerspace.models import Space
    from hackerspace.YOUR_HACKERSPACE import EVENTS_SPACES_OVERWRITE, EVENTS_SPACE_DEFAULT

    if 'how_to_find_us' in json_meetup_result:
        spaces = Space.objects.all()

        for space in spaces.iterator():
            if space.str_name.lower() in json_meetup_result['how_to_find_us'].lower():
                return space

    # else...
    for field in EVENTS_SPACES_OVERWRITE:
        if field in json_meetup_result['name']:
            return Space.objects.by_name(EVENTS_SPACES_OVERWRITE[field])
    else:
        return Space.objects.by_name(EVENTS_SPACE_DEFAULT)


def extractGuilde(json_meetup_result):
    from hackerspace.YOUR_HACKERSPACE import EVENTS_GUILDES_OVERWRITE
    from hackerspace.models import Guilde

    for str_keyword in EVENTS_GUILDES_OVERWRITE:
        if str_keyword in json_meetup_result['name']:
            return Guilde.objects.filter(str_name=EVENTS_GUILDES_OVERWRITE[str_keyword]).first()


def timezoneToOffset(timezone_name):
    from datetime import datetime
    import pytz

    return int(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()*1000)


def offsetToTimezone(offset_ms):
    from datetime import datetime
    import pytz

    now = datetime.now(pytz.utc)  # current time
    return [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
            if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]


def extractTimezone(json_meetup_result):
    from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_TIMEZONE_STRING

    if 'utc_offset' in json_meetup_result and json_meetup_result['utc_offset'] != timezoneToOffset(HACKERSPACE_TIMEZONE_STRING):
        return offsetToTimezone(json_meetup_result['utc_offset'])

    return HACKERSPACE_TIMEZONE_STRING


def createEvent(event):
    from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_NAME, HACKERSPACE_ADDRESS

    Event().create(json_content={
        'str_name': event['name'],
        'int_UNIXtime_event_start': round(event['time']/1000),
        'int_UNIXtime_event_end': round(event['time']/1000)+(event['duration']/1000),
        'int_minutes_duration': ((event['duration']/1000)/60),
        'url_featured_photo': event['featured_photo']['photo_link'] if 'featured_photo' in event else None,
        'text_description': event['description'],
        'str_location_name': event['venue']['name'] if event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_NAME,
        'str_location_street': event['venue']['address_1'] if event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['STREET'],
        'str_location_zip': event['venue']['zip'] if event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['ZIP'],
        'str_location_city': event['venue']['city'] if event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['CITY'],
        'str_location_countrycode': event['venue']['country'].upper() if event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['COUNTRYCODE'],
        'one_space': extractSpace(event),
        'one_guilde': extractGuilde(event),
        'str_series_id': event['series']['id'] if 'series' in event else None,
        'int_series_startUNIX': round(
            event['series']['start_date'] / 1000) if 'series' in event and 'start_date' in event['series'] else None,
        'int_series_endUNIX': round(
            event['series']['end_date'] / 1000) if 'series' in event and 'end_date' in event['series'] else None,
        'text_series_timing': 'weekly: '+str(event['series']['weekly']) if 'series' in event and 'weekly' in event['series'] else 'monthly: ' +
        str(event['series']['monthly']
            ) if 'series' in event and 'monthly' in event['series'] else None,
        'url_meetup_event': event['link'] if 'link' in event else None,
        'int_UNIXtime_created': event['created'],
        'int_UNIXtime_updated': event['updated'],
        'str_timezone': extractTimezone(event)
    }
    )


class EventSet(models.QuerySet):
    def next_meeting(self):
        import time

        return self.filter(str_name='Noisebridge General Meeting', int_UNIXtime_event_start__gt=time.time()).order_by('int_UNIXtime_event_start').first()

    def in_timeframe(self, from_UNIX_time, to_UNIX_time, str_space_name=None):
        from django.db.models import Q
        from hackerspace.models import Space
        if str_space_name:
            space = Space.objects.by_name(str_space_name)
            if space:
                self = self.filter(one_space=space)
        return self.filter(
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
        )

    def overlapping_events(self, new_event_UNIX_time, new_event_duration_minutes, space):
        import pytz
        from datetime import datetime, timedelta
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_TIMEZONE_STRING

        local_time = datetime.fromtimestamp(
            new_event_UNIX_time, pytz.timezone(HACKERSPACE_TIMEZONE_STRING))

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

        queryset_overlapping_events = Event.objects.in_timeframe(
            new_event_UNIX_time, new_event_UNIX_time+(new_event_duration_minutes*60), space)

        # get values needed to show events in correct position
        list_overlapping_events = []
        for event in queryset_overlapping_events:
            minutes_distance = ((
                event.int_UNIXtime_event_start - times[0]['int_UNIX_time'])/60)+60

            list_overlapping_events.append({
                'str_name': event.str_name,
                'str_slug': event.str_slug,
                'int_percent_top_distance': str(round((minutes_distance/(len(times)*60))*100))+'%',
                'int_percent_height': str(round(event.int_minutes_duration/(len(times)*60)*100))+'%'
            })

        your_event_minutes_distance = (
            (new_event_UNIX_time - times[0]['int_UNIX_time'])/60)+60
        return {
            'times': times,
            'your_event': {
                'int_percent_top_distance': str(round((your_event_minutes_distance/(len(times)*60))*100))+'%',
                'int_percent_height': str(round(new_event_duration_minutes/(len(times)*60)*100))+'%'
            },
            'overlapping_events': list_overlapping_events
        }

    def in_space(self, one_space=None, str_space=None):
        if one_space:
            return self.filter(one_space=one_space)
        elif str_space:
            return self.filter(one_space__str_name=str_space)
        else:
            return []

    def by_host(self, one_host=None, str_host=None):
        if one_host:
            return self.filter(many_hosts=one_host)
        elif str_host:
            return self.filter(many_hosts__str_name__contains=str_host)
        else:
            return []

    def by_guilde(self, one_guilde=None, str_guilde=None):
        if one_guilde:
            return self.filter(one_guilde=one_guilde)
        elif str_guilde:
            return self.filter(one_guilde__str_name__contains=str_guilde)
        else:
            return []

    def as_list(self):
        for event in self.all():
            print(event)

    def upcoming(self):
        import time

        return self.filter(int_UNIXtime_event_end__gt=time.time()).order_by('int_UNIXtime_event_start')

    def in_minutes(self, minutes, name_only=False):
        import pytz
        from datetime import datetime, timedelta
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_TIMEZONE_STRING

        date_in_x_minutes = datetime.now(pytz.timezone(
            HACKERSPACE_TIMEZONE_STRING))+timedelta(minutes=minutes)
        events_in_x_minutes = []
        self = self.upcoming()[:3]
        for event in self.all():
            event_start_date = event.datetime_start

            if event_start_date.date() == date_in_x_minutes.date() \
                    and event_start_date.hour == date_in_x_minutes.hour \
                    and event_start_date.minute == date_in_x_minutes.minute:
                events_in_x_minutes.append(event)

        if name_only == True:
            return [x.str_name.replace('&', 'and').replace('@', 'at').replace('|', '').replace('#', 'sharp') for x in events_in_x_minutes]

        return events_in_x_minutes

    def search_results(self):
        results_list = []
        added = []
        results = self.all()
        for result in results:
            if not result.str_name in added:
                relative_time = result.str_relative_time
                results_list.append({
                    'icon': 'event',
                    'name': result.str_name+'<br>=> '+(relative_time if relative_time else str(result.datetime_start.date())),
                    'url': '/'+result.str_slug,
                    'menu_heading': 'menu_h_events'
                })
                added.append(result.str_name)
        return results_list

    def announce(self):
        self.announce_via_marry()
        self.announce_via_flaschentaschen()

    def announce_via_flaschentaschen(self):
        for event in self.all()[:3]:
            event.announce_via_flaschentaschen()

    def announce_via_marry(self):
        for event in self.all()[:3]:
            event.announce_via_marry()

    def pull_from_meetup(self, slug=HACKERSPACE_MEETUP_GROUP):
        import requests
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_NAME

        json_our_group = requests.get('https://api.meetup.com/'+slug+'/events',
                                      params={
                                          'fields': [
                                              'featured_photo',
                                              'series',
                                              'simple_html_description',
                                              'rsvp_sample',
                                              'description_images',
                                          ],
                                          'photo-host': 'public'
                                      }).json()

        print('Saving '+str(len(json_our_group)) +
              ' events from our hackerspace group')

        for event in json_our_group:
            if slug == HACKERSPACE_MEETUP_GROUP or HACKERSPACE_NAME in event['name']:
                createEvent(event)

        print('Done! Saved '+str(len(json_our_group)) + ' events from Meetup')

    def pull_from_wiki(self):
        # TODO
        return []


class Event(models.Model):
    from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_NAME, HACKERSPACE_ADDRESS, HACKERSPACE_TIMEZONE_STRING

    objects = EventSet.as_manager()
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    int_UNIXtime_event_start = models.IntegerField(
        blank=True, null=True, verbose_name='Event start (UNIX time)')
    int_minutes_duration = models.IntegerField(
        default=60, verbose_name='Duration in minutes')
    int_UNIXtime_event_end = models.IntegerField(
        blank=True, null=True, verbose_name='Event end (UNIX time)')

    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')

    str_location_name = models.CharField(
        max_length=250, default=HACKERSPACE_NAME, verbose_name='Location Name')
    str_location_street = models.CharField(
        max_length=250, default=HACKERSPACE_ADDRESS['STREET'], verbose_name='Location Street')
    str_location_zip = models.CharField(
        max_length=10, default=HACKERSPACE_ADDRESS['ZIP'], verbose_name='Location ZIP')
    str_location_city = models.CharField(
        max_length=50, default=HACKERSPACE_ADDRESS['CITY'], verbose_name='Location City')
    str_location_countrycode = models.CharField(
        max_length=50, default=HACKERSPACE_ADDRESS['COUNTRYCODE'], verbose_name='Location Country Code')

    one_space = models.ForeignKey(
        'Space', related_name="o_space", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Space')
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
    many_hosts = models.ManyToManyField(
        'Person', related_name="m_persons", blank=True, verbose_name='Hosts')

    str_series_id = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Series ID')
    int_series_startUNIX = models.IntegerField(
        blank=True, null=True, verbose_name='Series Start (UNIX time)')
    int_series_endUNIX = models.IntegerField(
        blank=True, null=True, verbose_name='Series End (UNIX time)')
    text_series_timing = models.TextField(
        blank=True, null=True)  # json saved as text

    url_meetup_event = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Meetup URL')
    url_discourse_event = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='discourse URL')
    url_discourse_wish = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='discourse wish URL')
    url_slack_event = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Slack URL')

    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)
    str_timezone = models.CharField(
        max_length=100, default=HACKERSPACE_TIMEZONE_STRING, blank=True, null=True, verbose_name='Timezone')

    def __str__(self):
        if not self.datetime_range:
            return self.str_name
        return self.str_name+' | '+self.datetime_range

    def next_event(self):
        return Event.objects.upcoming().filter(str_name=self.str_name).exclude(str_slug=self.str_slug).first()

    # TODO: figure out based on what (keywords?) similar events should be filtered
    def similar_events(self):
        return None

    @property
    def menu_heading(self):
        return 'menu_h_events'

    @property
    def str_series(self):
        import json

        if not self.text_series_timing:
            return None

        text_series_timing = self.text_series_timing.replace(
            'weekly: ', '"weekly": ').replace('monthly: ', '"monthly": ').replace("'", '"')
        json_series_timing = json.loads('{'+text_series_timing+'}')
        if 'weekly' in json_series_timing:
            weekday_num = json_series_timing['weekly']['days_of_week'][0]
            return 'every '+(json_series_timing['weekly']['interval']+'nd' if json_series_timing['weekly']['interval'] > 1 else '')+getWeekday(weekday_num)

        if 'monthly' in json_series_timing:
            return 'every month'

    @property
    def str_relative_time(self):
        import time

        timestamp = self.int_UNIXtime_event_start

        # if date within next 5 minutes
        if timestamp < time.time() and self.int_UNIXtime_event_end > time.time():
            return 'Now'

        # in next 60 minutes
        elif timestamp < time.time()+(60*60):
            minutes_in_future = int((timestamp - time.time())/60)
            return 'in '+str(minutes_in_future)+' minute'+('s' if minutes_in_future > 1 else '')

        # in next 12 hours
        elif timestamp < time.time()+(60*60*12):
            hours_in_future = int(((timestamp - time.time())/60)/60)
            return 'in '+str(hours_in_future)+' hour'+('s' if hours_in_future > 1 else '')

        # else if in next 6 days, return name of day
        elif timestamp < time.time()+(60*60*24*6):
            name_of_weekday = self.datetime_start.strftime("%A")
            return name_of_weekday

        else:
            return None

    @property
    def datetime_start(self):
        import pytz
        from datetime import datetime

        if not self.int_UNIXtime_event_start:
            return None
        local_timezone = pytz.timezone(self.str_timezone)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_event_start, local_timezone)
        return local_time

    @property
    def datetime_end(self):
        from datetime import timedelta

        if not self.datetime_start:
            return None
        return self.datetime_start+timedelta(minutes=self.int_minutes_duration)

    @property
    def datetime_range(self):
        if not (self.datetime_start and self.datetime_end):
            return None

        datetime_start = self.datetime_start
        datetime_end = self.datetime_end

        month = datetime_start.strftime('%b')
        day_num = str(datetime_start.day)
        start_time = datetime_start.strftime(
            '%I:%M %p') if datetime_start.minute > 0 else datetime_start.strftime('%I %p')
        if datetime_start.strftime('%p') == datetime_end.strftime('%p'):
            start_time = start_time[:-3]
        end_time = datetime_end.strftime(
            '%I:%M %p') if datetime_end.minute > 0 else datetime_end.strftime('%I %p')

        # remove zeros to shorten text
        if start_time.startswith('0'):
            start_time = start_time[1:]
        if end_time.startswith('0'):
            end_time = end_time[1:]

        # if runtime > 24 hours, show num of days instead
        return month+' '+day_num+' | '+start_time+(' - ' + end_time if self.int_minutes_duration < (24*60) else ' | '+str(round(self.int_minutes_duration/60/24))+' days')

    @property
    def str_location(self):
        return self.str_location_name+'\n'+self.str_location_street+'\n'+self.str_location_zip+'\n'+self.str_location_city+'\n'+self.str_location_countrycode

    def save(self, *args, **kwargs):
        print('LOG: Event.save')
        import urllib.parse
        from hackerspace.models.events import updateTime
        from hackerspace.models import Space, Person
        from hackerspace.YOUR_HACKERSPACE import EVENTS_HOSTS_OVERWRITE

        self = updateTime(self)
        self.str_slug = urllib.parse.quote(
            'event/'+(str(self.datetime_start.date())+'-' if self.datetime_start else '')+self.str_name.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and').replace('(', '').replace(')', ''))

        super(Event, self).save(*args, **kwargs)

        print('LOG: --> Save hosts')
        if not self.many_hosts.exists():
            # search in predefined event hosts in YOURHACKERSPACE
            for event_name in EVENTS_HOSTS_OVERWRITE:
                if event_name in self.str_name:
                    for host_name in EVENTS_HOSTS_OVERWRITE[event_name]:
                        host = Person.objects.by_name(host_name)
                        if host:
                            self.many_hosts.add(host)

    def create(self, json_content):
        try:
            obj = Event.objects.get(
                str_name=json_content['str_name'],
                int_UNIXtime_event_start=json_content['int_UNIXtime_event_start']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj.save()
            print('Updated "'+obj.str_name+' | ' + obj.datetime_range+'"')
        except Event.DoesNotExist:
            obj = Event(**json_content)
            obj.save()
            print('Created "'+obj.str_name+' | ' + obj.datetime_range+'"')

    # Noisebridge specific
    def announce_via_marry(self):
        import time
        from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.marry import speak

        start_time = self.str_relative_time if self.int_UNIXtime_event_start < time.time(
        )+(60*60) else self.datetime_start.strftime('%I %p')
        if start_time == 'Now':
            speak(str(self.str_name)+' is happening now', None)
        else:
            speak(str(self.str_name)+' starts at '+start_time, None)

    def announce_via_flaschentaschen(self):
        from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.flaschentaschen import showText
        showText(self)
