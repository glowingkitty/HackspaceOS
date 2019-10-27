import time
from datetime import datetime, timedelta

import pytz
from django.db import models

from hackerspace.YOUR_HACKERSPACE import (HACKERSPACE_ADDRESS,
                                          HACKERSPACE_NAME,
                                          HACKERSPACE_TIMEZONE_STRING)


def updateTime(result):
    # update time
    if not result.int_UNIXtime_created:
        result.int_UNIXtime_created = time.time()
    result.int_UNIXtime_updated = time.time()
    return result


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

    str_repeating = models.CharField(max_length=30,
                                     choices=REPEATING_CHOICES,
                                     default=NOT)
    date_repeating_end = models.DateTimeField(
        'date_repeating_end', blank=True, null=True)
    one_original_event = models.ForeignKey(
        'Event', default=None, on_delete=models.CASCADE, null=True)

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

    def save(self, *args, **kwargs):
        self = updateTime(self)
        super(Event, self).save(*args, **kwargs)
