from django.core import serializers
from django.db import models
from getConfig import get_config
from asci_art import show_message
from hackerspace.log import log

def INT__getWeekday(number):
    log('INT__getWeekday(number={})'.format(number))
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


def RESULT__updateTime(result):
    log('RESULT__updateTime(result={})'.format(result))
    import time

    # update time
    if not result.int_UNIXtime_created:
        result.int_UNIXtime_created = time.time()
    result.int_UNIXtime_updated = time.time()
    return result


def RESULT__extractSpace(json_meetup_result):
    log('RESULT__extractSpace(json_meetup_result)')
    from hackerspace.models import Space
    from getConfig import get_config

    if 'how_to_find_us' in json_meetup_result:
        spaces = Space.objects.all()

        for space in spaces.iterator():
            if space.str_name_en_US.lower() in json_meetup_result['how_to_find_us'].lower():
                return space

    # else...
    EVENTS_SPACES_OVERWRITE = get_config('EVENTS.EVENTS_SPACES_OVERWRITE')
    for field in EVENTS_SPACES_OVERWRITE:
        if field in json_meetup_result['name']:
            return Space.objects.QUERYSET__by_name(EVENTS_SPACES_OVERWRITE[field])
    else:
        return Space.objects.QUERYSET__by_name(get_config('EVENTS.EVENTS_SPACE_DEFAULT'))


def RESULT__extractGuilde(json_meetup_result):
    log('RESULT__extractGuilde(json_meetup_result)')
    from hackerspace.models import Guilde
    from getConfig import get_config

    EVENTS_GUILDES_OVERWRITE = get_config('EVENTS.EVENTS_GUILDES_OVERWRITE')

    for str_keyword in EVENTS_GUILDES_OVERWRITE:
        if str_keyword in json_meetup_result['name']:
            log('--> {} found in result.name'.format(str_keyword))
            log('--> return guilde')
            return Guilde.objects.filter(str_name_en_US=EVENTS_GUILDES_OVERWRITE[str_keyword]).first()
    else:
        log('--> return None')
        return None


def INT__timezoneToOffset(timezone_name):
    log('INT__timezoneToOffset(timezone_name={})'.format(timezone_name))
    from datetime import datetime
    import pytz

    log('--> return INT')
    return int(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()*1000)


def LIST__offsetToTimezone(offset_ms):
    log('LIST__offsetToTimezone(offset_ms={})'.format(offset_ms))
    from datetime import datetime
    import pytz

    now = datetime.now(pytz.utc)  # current time
    log('--> return LIST')
    return [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
            if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]


def STR__extractTimezone(json_meetup_result):
    log('STR__extractTimezone(json_meetup_result)')
    from getConfig import get_config
    TIMEZONE_STRING = get_config('PHYSICAL_SPACE.TIMEZONE_STRING')

    if 'utc_offset' in json_meetup_result and json_meetup_result['utc_offset'] != INT__timezoneToOffset(TIMEZONE_STRING):
        return LIST__offsetToTimezone(json_meetup_result['utc_offset'])

    log('--> return STR')
    return TIMEZONE_STRING

def get_lat_lon_and_location(str_location):
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    from getConfig import get_config

    geolocator = Nominatim(user_agent=get_config('BASICS.NAME').lower())
    str_location = str_location.replace('\n',', ')
    float_lat = None
    float_lon = None
    while float_lat==None and len(str_location)>0:
        try:
            location = geolocator.geocode(str_location)

            float_lat, float_lon = location.latitude, location.longitude
        except GeocoderTimedOut:
            print('GeocoderTimedOut! This might be solved by turning off your VPN.')
            break
        except:
            str_location=','.join(str_location.split(',')[:-1])
    
    return str_location, float_lat, float_lon

def STR__get_timezone_from_lat_lon(lat,lon):
    import requests
    url="https://api.teleport.org/api/locations/"+str(lat)+","+str(lon)+"/?embed=location:nearest-cities/location:nearest-city/"
    response = requests.get(url).json()
    try:
        return response['_embedded']['location:nearest-cities'][0]['_embedded']['location:nearest-city']['_links']['city:timezone']['name']
    except:
        return None

def createEvent(event):
    log('createEvent(event)')
    from getConfig import get_config
    HACKERSPACE_NAME = get_config('BASICS.NAME')
    HACKERSPACE_ADDRESS = get_config('PHYSICAL_SPACE.ADDRESS')
    str_location_name = event['venue']['name'] if event['venue']['name'] and event[
        'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_NAME
    str_location_street = event['venue']['address_1'] if event['venue']['name'] and event[
        'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['STREET']
    str_location_zip = event['venue']['zip'] if event['venue']['name'] and event[
        'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['ZIP']
    str_location_city = event['venue']['city'] if event['venue']['name'] and event[
        'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['CITY']
    str_location_countrycode = event['venue']['country'].upper() if event['venue']['name'] and event[
        'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['COUNTRYCODE']

    Event().create(json_content={
        'str_name_en_US': event['name'],
        'int_UNIXtime_event_start': round(event['time']/1000),
        'int_UNIXtime_event_end': round(event['time']/1000)+(event['duration']/1000),
        'int_minutes_duration': ((event['duration']/1000)/60),
        'url_featured_photo': event['featured_photo']['photo_link'] if 'featured_photo' in event else None,
        'text_description_en_US': event['description'],
        'str_location': str_location_name+'\n'+str_location_street+'\n'+str_location_zip+', '+str_location_city+', '+str_location_countrycode,
        'one_space': RESULT__extractSpace(event),
        'one_guilde': RESULT__extractGuilde(event),
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
        'str_timezone': STR__extractTimezone(event)
    }
    )


class EventSet(models.QuerySet):
    def QUERYSET__next_meeting(self):
        log('Event.objects.QUERYSET__next_meeting(self)')
        import time

        log('--> return QUERYSET')
        return self.filter(str_name_en_US='Noisebridge General Meeting', int_UNIXtime_event_start__gt=time.time()).order_by('int_UNIXtime_event_start').first()

    def QUERYSET__in_timeframe(self, from_UNIX_time, to_UNIX_time, str_space_name=None):
        log('Event.objects.QUERYSET__in_timeframe(self, from_UNIX_time={}, to_UNIX_time={}, str_space_name={})'.format(from_UNIX_time,to_UNIX_time,str_space_name))
        from django.db.models import Q
        from hackerspace.models import Space
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
        log('Event.objects.JSON__overlapping_events(self, new_event_UNIX_time={}, new_event_duration_minutes={}, space={})'.format(new_event_UNIX_time, new_event_duration_minutes, space))
        import pytz
        from datetime import datetime, timedelta
        from getConfig import get_config

        local_time = datetime.fromtimestamp(
            new_event_UNIX_time, pytz.timezone(get_config('PHYSICAL_SPACE.TIMEZONE_STRING')))

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
        log('Event.objects.QUERYSET__in_space(self, one_space={}, str_space={})'.format(one_space, str_space))
        if one_space:
            log('--> return QUERYSET')
            return self.filter(one_space=one_space)
        elif str_space:
            log('--> return QUERYSET')
            return self.filter(one_space__str_name_en_US=str_space)
        else:
            return []

    def QUERYSET__by_host(self, one_host=None, str_host=None):
        log('Event.objects.QUERYSET__by_host(self, one_host={}, str_host={})'.format(one_host, str_host))
        if one_host:
            log('--> return QUERYSET')
            return self.filter(many_hosts=one_host)
        elif str_host:
            log('--> return QUERYSET')
            return self.filter(many_hosts__str_name_en_US__contains=str_host)
        else:
            return []

    def QUERYSET__by_guilde(self, one_guilde=None, str_guilde=None):
        log('Event.objects.QUERYSET__by_guilde(self, one_guilde={}, str_guilde={})'.format(one_guilde, str_guilde))
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

    def QUERYSET__upcoming(self,boolean_approved=False):
        log('Event.objects.QUERYSET__upcoming(self,boolean_approved={})'.format(boolean_approved))
        import time

        log('--> return QUERYSET')
        return self.filter(int_UNIXtime_event_end__gt=time.time()).exclude(boolean_approved=boolean_approved).order_by('int_UNIXtime_event_start')

    def LIST__in_minutes(self, minutes, name_only=False):
        log('Event.objects.LIST__in_minutes(self,minutes={},name_only={})'.format(minutes, name_only))
        import pytz
        from datetime import datetime, timedelta
        from getConfig import get_config

        date_in_x_minutes = datetime.now(pytz.timezone(
            get_config('PHYSICAL_SPACE.TIMEZONE_STRING')))+timedelta(minutes=minutes)
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
                'num_events':len(events),
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

    def import_from_meetup(self, slug=get_config('EVENTS.MEETUP_GROUP')):
        log('Event.objects.import_from_meetup(self,slug={})'.format(slug))
        import requests
        from getConfig import get_config
        import time

        if slug:
            show_message(
                '✅ Start importing existing events from "'+slug+'" on Meetup.')
            time.sleep(2)

            if requests.get('https://meetup.com/'+slug).status_code == 200:
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

                log('--> Saving '+str(len(json_our_group)) +
                    ' events from our hackerspace group')

                for event in json_our_group:
                    if slug == get_config('EVENTS.MEETUP_GROUP') or get_config('BASICS.NAME') in event['name']:
                        createEvent(event)

                log('--> Done! Saved '+str(len(json_our_group)) + ' events from Meetup')

            else:
                show_message(
                    'WARNING: I can\'t access the Meetup group. Is the URL correct? Will skip the Meetup group for now.')
                time.sleep(4)
        else:
            show_message(
                'WARNING: Can\'t find the Meetup group in your config.json. Will skip the Meetup group for now.')
            time.sleep(4)

class Event(models.Model):
    from getConfig import get_config

    HACKERSPACE_ADDRESS = get_config('PHYSICAL_SPACE.ADDRESS')
    LAT_LON = get_config('PHYSICAL_SPACE.LAT_LON')
    CROWD_SIZE = get_config('EVENTS.CROWD_SIZE')
    
    ADDRESS_STRING = get_config('BASICS.NAME')+'<br>' + \
        (HACKERSPACE_ADDRESS['STREET'] if HACKERSPACE_ADDRESS['STREET'] else '')+'<br' + \
        (HACKERSPACE_ADDRESS['ZIP'] if HACKERSPACE_ADDRESS['ZIP'] else '')+(', '+HACKERSPACE_ADDRESS['CITY'] if HACKERSPACE_ADDRESS['CITY'] else '') + \
        (', '+HACKERSPACE_ADDRESS['STATE'] if HACKERSPACE_ADDRESS['STATE'] else '')+(', '+HACKERSPACE_ADDRESS['COUNTRYCODE'] if HACKERSPACE_ADDRESS['COUNTRYCODE'] else '')
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EVENT_CROWD_SIZE = (
        (SMALL, CROWD_SIZE['SMALL']),
        (MEDIUM, CROWD_SIZE['MEDIUM']),
        (LARGE, CROWD_SIZE['LARGE']),
    )

    WEEKLY = 'weekly'
    BIWEEKLY = 'biweekly'
    MONTHLY = 'monthly'
    REPEAT_HOW_OFTEN = (
        (WEEKLY, 'weekly'),
        (BIWEEKLY, 'biweekly'),
        (MONTHLY, 'monthly'),
    )

    objects = EventSet.as_manager()
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    str_slug = models.CharField(max_length=250, unique=True, blank=True, null=True)
    boolean_approved = models.BooleanField(default=True)
    int_UNIXtime_event_start = models.IntegerField(
        blank=True, null=True, verbose_name='Event start (UNIX time)')
    int_minutes_duration = models.IntegerField(
        default=60, verbose_name='Duration in minutes')
    int_UNIXtime_event_end = models.IntegerField(
        blank=True, null=True, verbose_name='Event end (UNIX time)')

    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    image_featured_photo = models.ImageField(upload_to ='event_images',blank=True, null=True, verbose_name='Photo')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')

    str_location = models.CharField(
        max_length=250, default=ADDRESS_STRING, verbose_name='Location')
    float_lat = models.FloatField(default=LAT_LON[0], blank=True, null=True,verbose_name='Lat')
    float_lon = models.FloatField(default=LAT_LON[1], blank=True, null=True,verbose_name='Lon')

    one_space = models.ForeignKey(
        'Space', related_name="o_space", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Space')
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
    many_hosts = models.ManyToManyField(
        'Person', related_name="m_persons", blank=True, verbose_name='Hosts')

    boolean_looking_for_volunteers = models.BooleanField(default=False)

    str_series_id = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Series ID')
    int_series_startUNIX = models.IntegerField(
        blank=True, null=True, verbose_name='Series Start (UNIX time)')
    int_series_endUNIX = models.IntegerField(
        blank=True, null=True, verbose_name='Series End (UNIX time)')
    str_series_repeat_how_often = models.CharField(
        max_length=50, choices=REPEAT_HOW_OFTEN, blank=True, null=True, verbose_name='Series How often repeating?')
    text_series_timing = models.TextField(
        blank=True, null=True)  # json saved as text

    str_crowd_size = models.CharField(
        max_length=250, choices=EVENT_CROWD_SIZE, default=SMALL, verbose_name='Expected crowd size')
    str_welcomer = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='(for large events) Who welcomes people at the door?')

    url_meetup_event = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Meetup URL')
    url_discourse_event = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='discourse URL')
    url_discourse_wish = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='discourse wish URL')

    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)
    str_timezone = models.CharField(
        max_length=100, default=get_config('PHYSICAL_SPACE.TIMEZONE_STRING'), blank=True, null=True, verbose_name='Timezone')

    def __str__(self):
        if not self.datetime_range:
            return self.str_name_en_US
        return self.str_name_en_US+' | '+self.datetime_range

    def RESULT__next_event(self):
        log('event.RESULT__next_event()')
        log('--> return QUERYSET')
        return Event.objects.QUERYSET__upcoming().filter(str_name_en_US=self.str_name_en_US).exclude(str_slug=self.str_slug).first()

    # TODO: figure out based on what (keywords?) similar events should be filtered
    def similar_events(self):
        log('event.similar_events()')
        log('--> return None')
        return None

    @property
    def str_menu_heading(self):
        log('event.str_menu_heading')
        log('--> return STR')
        return 'menu_h_events'

    @property
    def str_series(self):
        log('event.str_series')
        import json

        if not self.text_series_timing:
            return None

        text_series_timing = self.text_series_timing.replace(
            'weekly: ', '"weekly": ').replace('monthly: ', '"monthly": ').replace("'", '"')
        json_series_timing = json.loads('{'+text_series_timing+'}')
        if 'weekly' in json_series_timing:
            weekday_num = json_series_timing['weekly']['days_of_week'][0]
            log('--> return STR')
            return 'every '+(json_series_timing['weekly']['interval']+'nd' if json_series_timing['weekly']['interval'] > 1 else '')+INT__getWeekday(weekday_num)

        if 'monthly' in json_series_timing:
            log('--> return STR')
            return 'every month'
    
    @property
    def json_data(self):
        return {
                'str_name_en_US':self.str_name_en_US,
                'url_hackerspace_event':'https://'+get_config('WEBSITE.DOMAIN')+'/'+self.str_slug,
                'datetime_start':str(self.datetime_start),
                'datetime_end':str(self.datetime_end),
                'str_timezone':self.str_timezone,
                'int_UNIXtime_event_start':self.int_UNIXtime_event_start,
                'int_minutes_duration':self.int_minutes_duration,
                'int_UNIXtime_event_end':self.int_UNIXtime_event_end,
                'url_featured_photo':self.url_featured_photo,
                'text_description_en_US':self.text_description_en_US,
                'str_location':self.str_location,
                'float_lat':self.float_lat,
                'float_lon':self.float_lon,
                'str_space':self.one_space.str_name_en_US if self.one_space else None,
                'str_guilde':self.one_guilde.str_name_en_US if self.one_guilde else None,
                'list_hosts':[x.str_name_shortened for x in self.many_hosts.all()],
                'int_series_startUNIX':self.int_series_startUNIX,
                'int_series_endUNIX':self.int_series_endUNIX,
                'str_series_repeat_how_often':self.str_series_repeat_how_often,
                'str_crowd_size':self.str_crowd_size,
                'str_welcomer':self.str_welcomer,
                'url_meetup_event':self.url_meetup_event,
                'url_discourse_event':self.url_discourse_event,
                'url_discourse_wish':self.url_discourse_wish,
                'int_UNIXtime_created':self.int_UNIXtime_created,
                'int_UNIXtime_updated':self.int_UNIXtime_updated,
            }

    @property
    def str_relative_time(self):
        log('event.str_relative_time')
        import time

        timestamp = self.int_UNIXtime_event_start

        # if date within next 5 minutes
        if timestamp < time.time() and self.int_UNIXtime_event_end > time.time():
            log('--> return STR')
            return 'Now'

        # in next 60 minutes
        elif timestamp <= time.time()+(60*60):
            minutes_in_future = int((timestamp - time.time())/60)
            log('--> return STR')
            return 'in '+str(minutes_in_future)+' minute'+('s' if minutes_in_future > 1 else '')

        # in next 12 hours
        elif timestamp <= time.time()+(60*60*12):
            hours_in_future = int(((timestamp - time.time())/60)/60)
            log('--> return STR')
            return 'in '+str(hours_in_future)+' hour'+('s' if hours_in_future > 1 else '')

        # else if in next 6 days, return name of day
        elif timestamp <= time.time()+(60*60*24*6):
            name_of_weekday = self.datetime_start.strftime("%A")
            log('--> return STR')
            return name_of_weekday

        else:
            log('--> return None')
            return None

    @property
    def str_relative_publish_time(self):
        import time

        int_UNIX_published_in = self.int_UNIXtime_created+(24*60*60)

        # in next 60 minutes
        if int_UNIX_published_in <= time.time()+(60*60):
            minutes_in_future = int((int_UNIX_published_in - time.time())/60)
            log('--> return STR')
            return 'in '+str(minutes_in_future)+' minute'+('s' if minutes_in_future > 1 else '')

        # in next 24 hours
        elif int_UNIX_published_in <= time.time()+(24*60*60):
            hours_in_future = int(((int_UNIX_published_in - time.time())/60)/60)
            log('--> return STR')
            return 'in '+str(hours_in_future)+' hour'+('s' if hours_in_future > 1 else '')

    @property
    def datetime_start(self):
        log('event.datetime_start')
        import pytz
        from datetime import datetime

        if not self.int_UNIXtime_event_start:
            log('--> return None')
            return None
        local_timezone = pytz.timezone(self.str_timezone)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_event_start, local_timezone)
        log('--> return DATETIME')
        return local_time

    @property
    def datetime_end(self):
        log('event.datetime_end')
        from datetime import timedelta

        if not self.datetime_start:
            log('--> return None')
            return None

        log('--> return DATETIME')
        return self.datetime_start+timedelta(minutes=self.int_minutes_duration)

    @property
    def datetime_range(self):
        log('event.datetime_range')
        if not (self.datetime_start and self.datetime_end):
            log('--> return None')
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
        log('--> return STR')
        return month+' '+day_num+' | '+start_time+(' - ' + end_time if self.int_minutes_duration < (24*60) else ' | '+str(round(self.int_minutes_duration/60/24))+' days')

    def publish(self):
        log('event.publish()')
        self.boolean_approved=True
        super(Event, self).save()

        self.create_discourse_event()
        # self.create_meetup_event()


    def create_upcoming_instances(self):
        log('event.create_upcoming_instances()')
        import time
        if not self.str_series_repeat_how_often:
            log('--> return')
            return self
        
        log('--> Define days_increase')
        if self.str_series_repeat_how_often=='weekly':
            days_increase = 7

        elif self.str_series_repeat_how_often=='biweekly':
            days_increase = 14
        
        elif self.str_series_repeat_how_often=='monthly':
            days_increase = 30
        
        log('--> Define start & end time of while statement')
        original_pk = self.pk
        original_slug = self.str_slug
        original_event_start = self.int_UNIXtime_event_start
        original_event_end = self.int_UNIXtime_event_end

        int_UNIX_time = self.int_series_startUNIX+(days_increase*24*60*60)
        int_UNIX_end = time.time()+(2*30*24*60*60)

        self.int_UNIXtime_event_start += (days_increase*24*60*60)
        self.int_UNIXtime_event_end += (days_increase*24*60*60)
        hosts = self.many_hosts.all()

        if self.int_series_endUNIX and self.int_series_endUNIX < int_UNIX_end:
            int_UNIX_end = self.int_series_endUNIX

        while int_UNIX_time < int_UNIX_end:
            log('--> Create event on UNIX time '+str(int_UNIX_time))
            self.pk = None
            self.str_slug = None
            self.save()

            log('--> Add many hosts for new instance')
            for host in hosts:
                self.many_hosts.add(host)

            int_UNIX_time+=(days_increase*24*60*60)
            self.int_UNIXtime_event_start += (days_increase*24*60*60)
            self.int_UNIXtime_event_end += (days_increase*24*60*60)
        

        log('--> Back to original values of first event')
        self.pk = original_pk
        self.str_slug = original_slug
        self.int_UNIXtime_event_start = original_event_start
        self.int_UNIXtime_event_end = original_event_end
        return self

    def create_discourse_event(self):
        log('event.create_discourse_event()')
        from hackerspace.APIs.discourse import create_post
        from django.template.loader import get_template

        self.url_discourse_event = create_post(
            str(self),
            get_template('components/discourse/event_post.html').render({
                'result': self
            }),
            get_config('EVENTS.DISCOURSE_EVENTS_CATEGORY'))
        super(Event, self).save()
        log('--> return event')
        return self

    def delete_discourse_event(self):
        log('event.delete_discourse_event()')
        from hackerspace.APIs.discourse import delete_post
        if self.url_discourse_event:
            deleted = delete_post(self.url_discourse_event)
            if deleted==True:
                self.url_discourse_event=None
            super(Event, self).save()
        log('--> return event')
        return self

    def delete_discourse_wish(self):
        log('event.delete_discourse_wish()')
        from hackerspace.APIs.discourse import delete_post
        if self.url_discourse_wish:
            deleted = delete_post(self.url_discourse_wish)
            if deleted==True:
                self.url_discourse_wish=None
            super(Event, self).save()
        log('--> return event')
        return self

    def delete_photo(self):
        log('event.delete_photo()')
        import boto3
        from getKey import STR__get_key
        # if url_featured_photo - delete on AWS
        if self.url_featured_photo:
            session = boto3.Session(
                        aws_access_key_id=STR__get_key('AWS.ACCESS_KEYID'),
                        aws_secret_access_key=STR__get_key('AWS.SECRET_ACCESS_KEY'),
                    )
            s3 = session.resource('s3')
            s3.delete_object(Bucket=STR__get_key('AWS.S3.BUCKET_NAME'), Key=self.url_featured_photo.split('amazonaws.com/')[1])
            self.url_featured_photo = None
            super(Event, self).save()
            return self
            
        # else delete in local folder
        elif self.image_featured_photo:
            print('TODO...')


    def delete(self):
        log('event.delete()')
        # delete discourse posts
        self.delete_discourse_wish()
        self.delete_discourse_event()

        # delete uploaded photo
        self.delete_photo()

        # delete in database
        super(Event, self).delete()
    
    def create_meetup_event(self):
        # API Doc: https://www.meetup.com/meetup_api/docs/:urlname/events/#create
        log('event.create_meetup_event()')
        import requests
        from getKey import STR__get_key
        from getConfig import get_config

        if not STR__get_key('MEETUP.ACCESS_TOKEN'):
            log('--> No MEETUP.ACCESS_TOKEN')
            log('--> return None')
            return None

        response = requests.post('https://api.meetup.com/'+get_config('EVENTS.MEETUP_GROUP')+'/events',
            params={
                'access_token': STR__get_key('MEETUP.ACCESS_TOKEN'),
                'sign': True,
                'announce': False,
                'publish_status':'draft',
                'description': self.text_description_en_US,
                'duration':self.int_minutes_duration*60*1000,
                'event_hosts':None,# TODO figure out meetup user IDs and how to add them here
                'fee':{
                    'accepts':None, # TODO add option for paid events later
                    'amount':None,
                    'currency':None,
                    'refund_policy':None
                },
                'guest_limit':2, # from 0 to 2
                'how_to_find_us':get_config('PHYSICAL_SPACE.ADDRESS')['HOW_TO_FIND_US'],
                'lat':self.float_lat,
                'lon':self.float_lon,
                'name':self.str_name_en_US,
                'self_rsvp':False,
                'time': self.int_UNIXtime_event_start,
                'venue_id':None, #TODO figure out how to get venue id
                'venue_visibility':None #TODO
            })
        
        #TODO returns 400 response - scope_error: Insufficient oauth scope
        if response.status_code==200:
            self.url_meetup_event = response.json()['link']
            self.save()
            log('--> return event')
            return self
        else:
            log('--> '+str(response.status_code)+' response: '+str(response.json()))


    def save(self, *args, **kwargs):
        try:
            log('event.save()')
            import urllib.parse
            from hackerspace.models.events import RESULT__updateTime
            from hackerspace.models import Space, Person
            import bleach
            from getConfig import get_config

            log('--> clean from scripts')
            if self.str_name_en_US:
                self.str_name_en_US = bleach.clean(self.str_name_en_US)
            if self.text_description_en_US:
                if not self.url_meetup_event:
                    self.text_description_en_US = bleach.clean(self.text_description_en_US)
            if self.text_description_he_IL:
                self.text_description_he_IL = bleach.clean(self.text_description_he_IL)
            if self.str_location:
                self.str_location = bleach.clean(self.str_location)
            if self.str_series_repeat_how_often:
                self.str_series_repeat_how_often = bleach.clean(self.str_series_repeat_how_often)
            if self.text_series_timing:
                self.text_series_timing = bleach.clean(self.text_series_timing)
            if self.str_crowd_size:
                self.str_crowd_size = bleach.clean(self.str_crowd_size)
            if self.str_welcomer:
                self.str_welcomer = bleach.clean(self.str_welcomer)
            if self.str_timezone:
                self.str_timezone = bleach.clean(self.str_timezone)

            self = RESULT__updateTime(self)
            if not self.str_slug:
                self.str_slug = urllib.parse.quote(
                    'event/'+(str(self.datetime_start.date())+'-' if self.datetime_start else '')+self.str_name_en_US.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and').replace('(', '').replace(')', ''))
                counter=0
                while Event.objects.filter(str_slug=self.str_slug).exists()==True:
                    counter+=1
                    self.str_slug = urllib.parse.quote(
                    'event/'+(str(self.datetime_start.date())+'-' if self.datetime_start else '')+self.str_name_en_US.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and').replace('(', '').replace(')', '')+str(counter))

            log('--> Save lat/lon if not exist yet')
            if not self.float_lat:
                self.str_location, self.float_lat, self.float_lon = get_lat_lon_and_location(self.str_location)

            super(Event, self).save(*args, **kwargs)

            log('--> Save hosts')
            if not self.many_hosts.exists():
                EVENTS_HOSTS_OVERWRITE = get_config('EVENTS.EVENTS_HOSTS_OVERWRITE')
                # search in predefined event hosts in YOURHACKERSPACE
                for event_name in EVENTS_HOSTS_OVERWRITE:
                    if event_name in self.str_name_en_US:
                        for host_name in EVENTS_HOSTS_OVERWRITE[event_name]:
                            host = Person.objects.QUERYSET__by_name(host_name)
                            if host:
                                self.many_hosts.add(host)
        except:
            log('--> ERROR: coudlnt save event - '+str(self))



    def create(self, json_content):
        log('event.create(json_content)')
        try:
            obj = Event.objects.get(
                str_name_en_US=json_content['str_name_en_US'],
                int_UNIXtime_event_start=json_content['int_UNIXtime_event_start']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            super(Event, obj).save()
            log('--> Updated "'+obj.str_name_en_US+' | ' + obj.datetime_range+'"')

        except Event.DoesNotExist:
            obj = Event(**json_content)
            obj.save()
            log('--> Created "'+obj.str_name_en_US+' | ' + obj.datetime_range+'"')

    # Noisebridge specific
    def announce_via_marry(self):
        log('event.announce_via_marry()')
        import time
        from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.marry import speak

        start_time = self.str_relative_time if self.int_UNIXtime_event_start < time.time(
        )+(60*60) else self.datetime_start.strftime('%I %p')
        if start_time == 'Now':
            speak(str(self.str_name_en_US)+' is happening now', None)
        else:
            speak(str(self.str_name_en_US)+' starts at '+start_time, None)

    def announce_via_flaschentaschen(self):
        log('event.announce_via_flaschentaschen()')
        from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.flaschentaschen import showText
        showText(self)
