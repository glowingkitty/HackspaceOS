import time
from datetime import datetime, timedelta

import pytz
import requests
from django.db import models
from django.core import serializers

from hackerspace.YOUR_HACKERSPACE import (HACKERSPACE_ADDRESS,
                                          HACKERSPACE_NAME,
                                          HACKERSPACE_TIMEZONE_STRING)


def updateTime(result):
    # update time
    if not result.int_UNIXtime_created:
        result.int_UNIXtime_created = time.time()
    result.int_UNIXtime_updated = time.time()
    return result


def extractSpace(json_meetup_result):
    if not 'how_to_find_us' in json_meetup_result:
        from hackerspace.models import Space
        spaces = Space.objects.all()

        for space in spaces.iterator():
            if space.str_name.lower() in json_meetup_result['how_to_find_us'].lower():
                return space

    return None


def timezoneToOffset(timezone_name):
    return int(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds()*1000)


def offsetToTimezone(offset_ms):
    now = datetime.now(pytz.utc)  # current time
    return [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
            if now.astimezone(tz).utcoffset().total_seconds()*1000 == offset_ms][0]


def extractTimezone(json_meetup_result):
    if 'utc_offset' in json_meetup_result and json_meetup_result['utc_offset'] != timezoneToOffset(HACKERSPACE_TIMEZONE_STRING):
        return offsetToTimezone(json_meetup_result['utc_offset'])

    return HACKERSPACE_TIMEZONE_STRING


class EventSet(models.QuerySet):
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
        return self.filter(int_UNIXtime_event_end__gt=time.time())

    def pull_from_meetup(self):
        upcoming_start = datetime.today()\
            .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        upcoming_end = (datetime.today() + timedelta(days=30))\
            .replace(hour=0, minute=0, second=0, microsecond=0)\
            .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        meetup_api_fields = 'name,venue,description,local_date,local_time,duration'
        json_response = requests.get('https://api.meetup.com/noisebridge/events',
                                     params={
                                         'fields': ['series', 'simple_html_description', 'rsvp_sample'],
                                         'photo-host': 'public'
                                     }).json()

        print('Saving '+str(len(json_response))+' events')

        for event in json_response:
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

    print('Done! Saved ')


class Event(models.Model):
    NOT = 'Not repeating'
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Bi-weekly'
    MONTHLY = 'Monthly'
    REPEATING_CHOICES = (
        (NOT, 'Not repeating'),
        (WEEKLY, 'Weekly'),
        (BIWEEKLY, 'Bi-weekly'),
        (MONTHLY, 'Monthly')
    )

    objects = EventSet.as_manager()
    str_name = models.CharField(max_length=250, blank=True, null=True)
    int_UNIXtime_event_start = models.IntegerField(blank=True, null=True)
    int_minutes_duration = models.IntegerField(default=60)
    int_UNIXtime_event_end = models.IntegerField(blank=True, null=True)

    url_featured_photo = models.URLField(max_length=200, blank=True, null=True)
    text_description = models.TextField(blank=True, null=True)

    str_location_name = models.CharField(
        max_length=250, default=HACKERSPACE_NAME)
    str_location_street = models.CharField(
        max_length=250, default=HACKERSPACE_ADDRESS['STREET'])
    str_location_zip = models.CharField(
        max_length=10, default=HACKERSPACE_ADDRESS['ZIP'])
    str_location_city = models.CharField(
        max_length=50, default=HACKERSPACE_ADDRESS['CITY'])
    str_location_countrycode = models.CharField(
        max_length=50, default=HACKERSPACE_ADDRESS['COUNTRYCODE'])

    one_space = models.ForeignKey(
        'Space', related_name="o_space", default=None, blank=True, null=True, on_delete=models.SET_NULL)
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL)
    many_hosts = models.ManyToManyField(
        'Person', related_name="m_persons", blank=True)

    str_series_id = models.CharField(max_length=250, blank=True, null=True)
    int_series_startUNIX = models.IntegerField(blank=True, null=True)
    int_series_endUNIX = models.IntegerField(blank=True, null=True)
    text_series_timing = models.TextField(
        blank=True, null=True)  # json saved as text

    url_meetup_event = models.URLField(max_length=250, blank=True, null=True)
    url_discuss_event = models.URLField(max_length=250, blank=True, null=True)
    url_slack_event = models.URLField(max_length=250, blank=True, null=True)

    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)
    str_timezone = models.CharField(
        max_length=100, default=HACKERSPACE_TIMEZONE_STRING, blank=True, null=True)

    def __str__(self):
        return self.str_name+' | '+str(self.datetime_start)

    @property
    def datetime_start(self):
        if not self.int_UNIXtime_event_start:
            return 'No start time'
        local_timezone = pytz.timezone(self.str_timezone)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_event_start, local_timezone)
        return local_time

    @property
    def datetime_end(self):
        return self.datetime_start+timedelta(minutes=self.int_minutes_duration)

    @property
    def str_location(self):
        return self.str_location_name+'\n'+self.str_location_street+'\n'+self.str_location_zip+'\n'+self.str_location_city+'\n'+self.str_location_countrycode

    def create(self, json_content):
        try:
            obj = Event.objects.get(
                str_name=json_content['str_name'],
                int_UNIXtime_event_start=json_content['int_UNIXtime_event_start']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj = updateTime(obj)
            obj.save()
            print('Updated "'+json_content['str_name']+' | ' +
                  str(json_content['int_UNIXtime_event_start'])+'"')
        except Event.DoesNotExist:
            obj = Event(**json_content)
            obj = updateTime(obj)
            obj.save()
            print('Created "'+json_content['str_name']+' | ' +
                  str(json_content['int_UNIXtime_event_start'])+'"')
