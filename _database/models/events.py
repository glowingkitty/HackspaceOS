from django.core import serializers
from django.db import models
from _setup.models import Config
from _setup.models import Log
from _setup.models import Log


class Event(models.Model):
    from _setup.models import Config
    from _database.models.event_set import EventSet

    HACKERSPACE_ADDRESS = Config('PHYSICAL_SPACE.ADDRESS').value
    LAT_LON = Config('PHYSICAL_SPACE.LAT_LON').value
    CROWD_SIZE = Config('EVENTS.CROWD_SIZE').value

    ADDRESS_STRING = Config('BASICS.NAME').value+'<br>' + \
        (HACKERSPACE_ADDRESS['STREET'] if HACKERSPACE_ADDRESS['STREET'] else '')+'<br' + \
        (HACKERSPACE_ADDRESS['ZIP'] if HACKERSPACE_ADDRESS['ZIP'] else '')+(', '+HACKERSPACE_ADDRESS['CITY'] if HACKERSPACE_ADDRESS['CITY'] else '') + \
        (', '+HACKERSPACE_ADDRESS['STATE'] if HACKERSPACE_ADDRESS['STATE'] else '')+(
            ', '+HACKERSPACE_ADDRESS['COUNTRYCODE'] if HACKERSPACE_ADDRESS['COUNTRYCODE'] else '')
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
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    str_slug = models.CharField(
        max_length=250, unique=True, blank=True, null=True)
    boolean_approved = models.BooleanField(default=True)
    int_UNIXtime_event_start = models.IntegerField(
        blank=True, null=True, verbose_name='Event start (UNIX time)')
    int_minutes_duration = models.IntegerField(
        default=60, verbose_name='Duration in minutes')
    int_UNIXtime_event_end = models.IntegerField(
        blank=True, null=True, verbose_name='Event end (UNIX time)')

    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    image_featured_photo = models.ImageField(
        upload_to='event_images', blank=True, null=True, verbose_name='Photo')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')

    boolean_online_meetup = models.BooleanField(default=False)
    str_location = models.CharField(
        max_length=250, default=ADDRESS_STRING, verbose_name='Location')
    float_lat = models.FloatField(
        default=LAT_LON[0], blank=True, null=True, verbose_name='Lat')
    float_lon = models.FloatField(
        default=LAT_LON[1], blank=True, null=True, verbose_name='Lon')

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

    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)
    str_timezone = models.CharField(
        max_length=100, default=Config('PHYSICAL_SPACE.TIMEZONE_STRING').value, blank=True, null=True, verbose_name='Timezone')

    def __str__(self):
        if not self.datetime_range:
            return self.str_name_en_US
        return self.str_name_en_US+' | '+self.datetime_range

    def INT__getWeekday(self, number):
        Log().print('INT__getWeekday(number={})'.format(number))
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

    def RESULT__extractSpace(self, json_meetup_result):
        Log().print('RESULT__extractSpace(json_meetup_result)')
        from _database.models import Space
        from _setup.models import Config

        if 'how_to_find_us' in json_meetup_result:
            spaces = Space.objects.all()

            for space in spaces.iterator():
                if space.str_name_en_US.lower() in json_meetup_result['how_to_find_us'].lower():
                    return space

        # else...
        EVENTS_SPACES_OVERWRITE = Config(
            'EVENTS.EVENTS_SPACES_OVERWRITE').value
        for field in EVENTS_SPACES_OVERWRITE:
            if field in json_meetup_result['name']:
                return Space.objects.QUERYSET__by_name(EVENTS_SPACES_OVERWRITE[field])
        else:
            return Space.objects.QUERYSET__by_name(Config('EVENTS.EVENTS_SPACE_DEFAULT').value)

    def RESULT__extractGuilde(self, json_meetup_result):
        Log().print('RESULT__extractGuilde(json_meetup_result)')
        from _database.models import Guilde
        from _setup.models import Config

        EVENTS_GUILDES_OVERWRITE = Config(
            'EVENTS.EVENTS_GUILDES_OVERWRITE').value

        for str_keyword in EVENTS_GUILDES_OVERWRITE:
            if str_keyword in json_meetup_result['name']:
                Log().print('--> {} found in result.name'.format(str_keyword))
                Log().print('--> return guilde')
                return Guilde.objects.filter(str_name_en_US=EVENTS_GUILDES_OVERWRITE[str_keyword]).first()
        else:
            Log().print('--> return None')
            return None

    def INT__timezoneToOffset(self, timezone_name):
        Log().print('INT__timezoneToOffset(timezone_name={})'.format(timezone_name))
        from datetime import datetime
        import pytz

        Log().print('--> return INT')
        return int(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()*1000)

    def LIST__offsetToTimezone(self, offset_ms):
        Log().print('LIST__offsetToTimezone(offset_ms={})'.format(offset_ms))
        from datetime import datetime
        import pytz

        now = datetime.now(pytz.utc)  # current time
        Log().print('--> return LIST')
        return [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
                if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]

    def STR__extractTimezone(self, json_meetup_result):
        Log().print('STR__extractTimezone(json_meetup_result)')
        from _setup.models import Config
        TIMEZONE_STRING = Config('PHYSICAL_SPACE.TIMEZONE_STRING').value

        if 'utc_offset' in json_meetup_result and json_meetup_result['utc_offset'] != self.INT__timezoneToOffset(TIMEZONE_STRING):
            return self.LIST__offsetToTimezone(json_meetup_result['utc_offset'])

        Log().print('--> return STR')
        return TIMEZONE_STRING

    def get_lat_lon_and_location(self, str_location):
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut
        from _setup.models import Config

        geolocator = Nominatim(user_agent=Config('BASICS.NAME').value.lower())
        str_location = str_location.replace('\n', ', ')
        float_lat = None
        float_lon = None
        while float_lat == None and len(str_location) > 0:
            try:
                location = geolocator.geocode(str_location)

                float_lat, float_lon = location.latitude, location.longitude
            except GeocoderTimedOut:
                print('GeocoderTimedOut! This might be solved by turning off your VPN.')
                break
            except:
                str_location = ','.join(str_location.split(',')[:-1])

        return str_location, float_lat, float_lon

    def createEvent(self, event):
        Log().print('createEvent(event)')
        from _setup.models import Config
        from dateutil.parser import parse
        from datetime import datetime

        HACKERSPACE_NAME = Config('BASICS.NAME').value
        HACKERSPACE_ADDRESS = Config('PHYSICAL_SPACE.ADDRESS').value
        str_location_name = event['venue']['name'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_NAME
        str_location_street = event['venue']['address_1'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['STREET']
        str_location_zip = event['venue']['zip'] if 'venue' in event and 'zip' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['ZIP']
        str_location_city = event['venue']['city'] if 'venue' in event and 'city' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['CITY']
        str_location_countrycode = event['venue']['country'].upper() if 'venue' in event and 'country' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['COUNTRYCODE']

        Event().create(json_content={
            'str_name_en_US': event['name'] if 'name' in event else event['title'],
            'int_UNIXtime_event_start': round(event['time']/1000) if 'time' in event else parse(event['event']['start']).timestamp(),
            'int_UNIXtime_event_end': round(event['time']/1000)+(event['duration']/1000) if 'time' in event else parse(event['event']['end']).timestamp() if 'end' in event['event'] else parse(event['event']['start']).timestamp()+(120*60),
            'int_minutes_duration': ((event['duration']/1000)/60) if 'duration' in event else round(
                (parse(event['event']['end']).timestamp() - parse(event['event']['start']).timestamp())/1000) if 'end' in event['event'] else 120,
            'url_featured_photo': event['featured_photo']['photo_link'] if 'featured_photo' in event else event['image_url'] if 'image_url' in event and event['image_url'] else None,
            'text_description_en_US': event['description'],
            'str_location': str_location_name+'\n'+str_location_street+'\n'+str_location_zip+', '+str_location_city+', '+str_location_countrycode,
            'one_space': self.RESULT__extractSpace(event),
            'one_guilde': self.RESULT__extractGuilde(event),
            'str_series_id': event['series']['id'] if 'series' in event else None,
            'int_series_startUNIX': round(
                event['series']['start_date'] / 1000) if 'series' in event and 'start_date' in event['series'] else None,
            'int_series_endUNIX': round(
                event['series']['end_date'] / 1000) if 'series' in event and 'end_date' in event['series'] else None,
            'text_series_timing': 'weekly: '+str(event['series']['weekly']) if 'series' in event and 'weekly' in event['series'] else 'monthly: ' +
            str(event['series']['monthly']
                ) if 'series' in event and 'monthly' in event['series'] else None,
            'url_meetup_event': event['link'] if 'link' in event else None,
            'int_UNIXtime_created': event['created'] if 'created' in event else parse(event['created_at']).timestamp(),
            'int_UNIXtime_updated': event['updated'] if 'updated' in event else parse(event['last_posted_at']).timestamp(),
            'str_timezone': self.STR__extractTimezone(event)
        }
        )

    def RESULT__next_event(self):
        Log().print('event.RESULT__next_event()')
        Log().print('--> return QUERYSET')
        return Event.objects.QUERYSET__upcoming().filter(str_name_en_US=self.str_name_en_US, str_series_repeat_how_often=self.str_series_repeat_how_often).exclude(str_slug=self.str_slug).first()

    @property
    def str_menu_heading(self):
        return 'menu_h_events'

    @property
    def series(self):
        return Event.objects.filter(str_name_en_US=self.str_name_en_US, str_series_repeat_how_often=self.str_series_repeat_how_often).order_by('int_UNIXtime_event_start')

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
            return 'every '+(json_series_timing['weekly']['interval']+'nd' if json_series_timing['weekly']['interval'] > 1 else '')+self.INT__getWeekday(weekday_num)

        if 'monthly' in json_series_timing:
            return 'every month'

    @property
    def json_data(self):
        return {
            'str_name_en_US': self.str_name_en_US,
            'url_hackerspace_event': 'https://'+Config('WEBSITE.DOMAIN').value+'/'+self.str_slug,
            'datetime_start': str(self.datetime_start),
            'datetime_end': str(self.datetime_end),
            'str_timezone': self.str_timezone,
            'int_UNIXtime_event_start': self.int_UNIXtime_event_start,
            'int_minutes_duration': self.int_minutes_duration,
            'int_UNIXtime_event_end': self.int_UNIXtime_event_end,
            'url_featured_photo': self.url_featured_photo,
            'text_description_en_US': self.text_description_en_US,
            'str_location': self.str_location,
            'float_lat': self.float_lat,
            'float_lon': self.float_lon,
            'str_space': self.one_space.str_name_en_US if self.one_space else None,
            'str_guilde': self.one_guilde.str_name_en_US if self.one_guilde else None,
            'list_hosts': [x.str_name_shortened for x in self.many_hosts.all()],
            'int_series_startUNIX': self.int_series_startUNIX,
            'int_series_endUNIX': self.int_series_endUNIX,
            'str_series_repeat_how_often': self.str_series_repeat_how_often,
            'str_crowd_size': self.str_crowd_size,
            'str_welcomer': self.str_welcomer,
            'url_meetup_event': self.url_meetup_event,
            'url_discourse_event': self.url_discourse_event,
            'int_UNIXtime_created': self.int_UNIXtime_created,
            'int_UNIXtime_updated': self.int_UNIXtime_updated,
        }

    @property
    def str_relative_time(self):
        import time

        if not self.int_UNIXtime_event_start:
            return None

        timestamp = self.int_UNIXtime_event_start

        # show if event is over
        if self.int_UNIXtime_event_end < time.time():
            return 'Ended'

        # if date within next 5 minutes
        elif timestamp < time.time() and self.int_UNIXtime_event_end > time.time():
            return 'Now'

        # in next 60 minutes
        elif timestamp <= time.time()+(60*60):
            minutes_in_future = int((timestamp - time.time())/60)
            return 'in '+str(minutes_in_future)+' minute'+('s' if minutes_in_future > 1 else '')

        # in next 12 hours
        elif timestamp <= time.time()+(60*60*12):
            hours_in_future = int(((timestamp - time.time())/60)/60)
            return 'in '+str(hours_in_future)+' hour'+('s' if hours_in_future > 1 else '')

        # else if in next 6 days, return name of day
        elif timestamp <= time.time()+(60*60*24*6):
            name_of_weekday = self.datetime_start.strftime("%A")
            return name_of_weekday

        else:
            return None

    @property
    def videocall_now(self):
        if self.boolean_online_meetup and self.str_relative_time == 'Now':
            return True
        else:
            return False

    @property
    def str_relative_publish_time(self):
        import time

        int_UNIX_published_in = self.int_UNIXtime_created+(24*60*60)

        # in next 60 minutes
        if int_UNIX_published_in <= time.time()+(60*60):
            minutes_in_future = int((int_UNIX_published_in - time.time())/60)
            return 'in '+str(minutes_in_future)+' minute'+('s' if minutes_in_future > 1 else '')

        # in next 24 hours
        elif int_UNIX_published_in <= time.time()+(24*60*60):
            hours_in_future = int(
                ((int_UNIX_published_in - time.time())/60)/60)
            return 'in '+str(hours_in_future)+' hour'+('s' if hours_in_future > 1 else '')

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
    def time_range(self):
        if not (self.datetime_start and self.datetime_end):
            return None

        start_time = self.datetime_start.strftime(
            '%I:%M %p') if self.datetime_start.minute > 0 else self.datetime_start.strftime('%I %p')
        if self.datetime_start.strftime('%p') == self.datetime_end.strftime('%p'):
            start_time = start_time[:-3]
        end_time = self.datetime_end.strftime(
            '%I:%M %p') if self.datetime_end.minute > 0 else self.datetime_end.strftime('%I %p')

        # remove zeros to shorten text
        if start_time.startswith('0'):
            start_time = start_time[1:]
        if end_time.startswith('0'):
            end_time = end_time[1:]

        # if runtime > 24 hours, show num of days instead
        return '⏰'+start_time+(' - ' + end_time if self.int_minutes_duration < (24*60) else ' | '+str(round(self.int_minutes_duration/60/24))+' days')

    @property
    def time_range_text(self):
        return self.time_range.replace('⏰', '')

    @property
    def datetime_range(self):
        if not (self.datetime_start and self.datetime_end):
            return None

        month = self.datetime_start.strftime('%b')
        day_num = str(self.datetime_start.day)

        # if runtime > 24 hours, show num of days instead
        return '🗓'+month+' '+day_num+' | '+self.time_range

    @property
    def datetime_range_text(self):
        return self.datetime_range.replace('⏰', '').replace('🗓', '')

    @property
    def repeating(self):
        import calendar

        if not self.str_series_repeat_how_often:
            return False

        if self.str_series_repeat_how_often == 'weekly':
            day_of_week = calendar.day_name[self.datetime_start.weekday()]
            how_often = 'Every '+day_of_week

        elif self.str_series_repeat_how_often == 'biweekly':
            day_of_week = calendar.day_name[self.datetime_start.weekday()]
            how_often = 'Every 2nd '+day_of_week

        elif self.str_series_repeat_how_often == 'monthly':
            date_of_month = self.datetime_start.day
            if date_of_month == 1:
                date_of_month = str(date_of_month)+'st'
            elif date_of_month == 2:
                date_of_month = str(date_of_month)+'nd'
            elif date_of_month == 3:
                date_of_month = str(date_of_month)+'rd'
            else:
                date_of_month = str(date_of_month)+'th'
            how_often = 'Every month on the '+date_of_month
        return how_often

    def save_social_media_image(self):
        Log().print('event.save_social_media_image()')
        import time
        import asyncio
        from pyppeteer import launch

        filename = 'social_image'+str(time.time())+'.png'

        async def main():
            browser = await launch(headless=True, ignoreHTTPSErrors=True, args=['--no-sandbox'])
            page = await browser.newPage()
            await page.emulate({'viewport': {'width': 500, 'height': 500}})
            await page.goto('https://'+Config('WEBSITE.DOMAIN').value+'/'+self.str_slug+'/banner')
            await page.screenshot({'path': filename})
            await browser.close()

        asyncio.get_event_loop().run_until_complete(main())

        return filename

    def publish(self):
        Log().print('event.publish()')
        self.boolean_approved = True
        super(Event, self).save()

        self.create_discourse_event()
        # self.create_meetup_event()

    def create_upcoming_instances(self):
        Log().print('event.create_upcoming_instances()')
        import time
        if not self.str_series_repeat_how_often:
            Log().print('--> return')
            return self

        Log().print('--> Define days_increase')
        if self.str_series_repeat_how_often == 'weekly':
            days_increase = 7

        elif self.str_series_repeat_how_often == 'biweekly':
            days_increase = 14

        elif self.str_series_repeat_how_often == 'monthly':
            days_increase = 30

        Log().print('--> Define start & end time of while statement')
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
            Log().print('--> Create event on UNIX time '+str(int_UNIX_time))
            self.pk = None
            self.str_slug = None
            self.save()

            Log().print('--> Add many hosts for new instance')
            for host in hosts:
                self.many_hosts.add(host)

            int_UNIX_time += (days_increase*24*60*60)
            self.int_UNIXtime_event_start += (days_increase*24*60*60)
            self.int_UNIXtime_event_end += (days_increase*24*60*60)

        Log().print('--> Back to original values of first event')
        self.pk = original_pk
        self.str_slug = original_slug
        self.int_UNIXtime_event_start = original_event_start
        self.int_UNIXtime_event_end = original_event_end
        return self

    def create_discourse_event(self):
        Log().print('event.create_discourse_event()')
        from _apis.models import create_post
        from django.template.loader import get_template

        if self.str_series_repeat_how_often:
            name = (self.repeating + ' | '+self.time_range_text +
                    ' | '+self.str_name_en_US)
        else:
            name = self.datetime_range_text+' | '+self.str_name_en_US

        self.url_discourse_event = create_post(
            name,
            get_template('components/discourse/event_post.html').render({
                'result': self
            }),
            Config('EVENTS.DISCOURSE_EVENTS_CATEGORY').value)
        super(Event, self).save()
        Log().print('--> return event')
        return self

    def delete_discourse_event(self):
        Log().print('event.delete_discourse_event()')
        from _apis.models import delete_post
        if self.url_discourse_event:
            deleted = delete_post(self.url_discourse_event)
            if deleted == True:
                self.url_discourse_event = None
            super(Event, self).save()
        Log().print('--> return event')
        return self

    def delete_photo(self):
        Log().print('event.delete_photo()')
        from _apis.models import Aws
        # if url_featured_photo - delete on AWS
        if self.url_featured_photo and 'amazonaws.com' in self.url_featured_photo:
            success = Aws().delete(
                self.url_featured_photo.split('amazonaws.com/')[1])
            if success:
                self.url_featured_photo = None
                super(Event, self).save()
                return self
            else:
                return self

        # else delete in local folder
        elif self.image_featured_photo:
            self.image_featured_photo.delete(save=True)
            return self

    def delete(self):
        Log().print('event.delete()')
        # delete discourse posts
        self.delete_discourse_event()

        # delete uploaded photo
        self.delete_photo()

        super(Event, self).delete()
        Log().print('--> Deleted')

    def delete_series(self):
        Log().print('event.delete_series()')
        # delete in database
        if self.str_series_repeat_how_often:
            # if series, delete all in series
            Event.objects.filter(str_name_en_US=self.str_name_en_US,
                                 str_series_repeat_how_often=self.str_series_repeat_how_often).delete()
            Log().print('--> Deleted')
        else:
            Log().print('--> Not a series. Skipped deleting.')

    def create_meetup_event(self):
        from _apis.models import Meetup
        returned_event = Meetup().create(self)
        if returned_event:
            self = returned_event
        return self

    def save(self, *args, **kwargs):
        # try:
        Log().print('event.save()')
        import urllib.parse
        from _database.models import Helper, Space, Person
        import bleach
        from _setup.models import Config
        import re

        Log().print('--> clean from scripts')
        if self.str_name_en_US:
            self.str_name_en_US = bleach.clean(self.str_name_en_US)
        if self.text_description_en_US:
            if not self.url_meetup_event:
                self.text_description_en_US = bleach.clean(
                    self.text_description_en_US)
        if self.text_description_he_IL:
            self.text_description_he_IL = bleach.clean(
                self.text_description_he_IL)
        if self.str_location:
            self.str_location = bleach.clean(
                self.str_location).replace('&lt;br&gt;', '<br>')
        if self.str_series_repeat_how_often:
            self.str_series_repeat_how_often = bleach.clean(
                self.str_series_repeat_how_often)
        if self.text_series_timing:
            self.text_series_timing = bleach.clean(self.text_series_timing)
        if self.str_crowd_size:
            self.str_crowd_size = bleach.clean(self.str_crowd_size)
        if self.str_welcomer:
            self.str_welcomer = bleach.clean(self.str_welcomer)
        if self.str_timezone:
            self.str_timezone = bleach.clean(self.str_timezone)

        self = Helper().RESULT__updateTime(self)
        if not self.str_slug:
            self.str_slug = 'event/'+(str(self.datetime_start.date(
            ))+'-' if self.datetime_start else '')+re.sub('[\W_]+', '', self.str_name_en_US.lower())
            counter = 0
            while Event.objects.filter(str_slug=self.str_slug).exists() == True:
                counter += 1
                self.str_slug = 'event/'+(str(self.datetime_start.date())+'-' if self.datetime_start else '')+re.sub(
                    '[\W_]+', '', self.str_name_en_US.lower())+str(counter)

        Log().print('--> Save lat/lon if not exist yet')
        if not self.float_lat:
            self.str_location, self.float_lat, self.float_lon = get_lat_lon_and_location(
                self.str_location)

        super(Event, self).save(*args, **kwargs)

        Log().print('--> Save hosts')
        if not self.many_hosts.exists():
            EVENTS_HOSTS_OVERWRITE = Config(
                'EVENTS.EVENTS_HOSTS_OVERWRITE').value
            # search in predefined event hosts in YOURHACKERSPACE
            for event_name in EVENTS_HOSTS_OVERWRITE:
                if event_name in self.str_name_en_US:
                    for host_name in EVENTS_HOSTS_OVERWRITE[event_name]:
                        host = Person.objects.QUERYSET__by_name(host_name)
                        if host:
                            self.many_hosts.add(host)
        # except:
        #     Log().print('--> ERROR: coudlnt save event - '+str(self))

    def create(self, json_content):
        Log().print('event.create(json_content)')
        try:
            obj = Event.objects.get(
                str_name_en_US=json_content['str_name_en_US'],
                int_UNIXtime_event_start=json_content['int_UNIXtime_event_start']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            super(Event, obj).save()
            Log().print('--> Updated "'+obj.str_name_en_US +
                        ' | ' + obj.datetime_range+'"')

        except Event.DoesNotExist:
            obj = Event(**json_content)
            obj.save()
            Log().print('--> Created "'+obj.str_name_en_US +
                        ' | ' + obj.datetime_range+'"')

    # Noisebridge specific
    def announce_via_marry(self):
        Log().print('event.announce_via_marry()')
        import time
        from _apis.models import MarrySpeak

        start_time = self.str_relative_time if self.int_UNIXtime_event_start < time.time(
        )+(60*60) else self.datetime_start.strftime('%I %p')
        if start_time == 'Now':
            MarrySpeak().speak(str(self.str_name_en_US)+' is happening now', None)
        else:
            MarrySpeak().speak(str(self.str_name_en_US)+' starts at '+start_time, None)

    def announce_via_flaschentaschen(self):
        Log().print('event.announce_via_flaschentaschen()')
        from _apis.models import Flaschentaschen
        Flaschentaschen().showText(self)
