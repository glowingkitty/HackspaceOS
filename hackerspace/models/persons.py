from django.db import models

from hackerspace.models import Event
from hackerspace.models.events import updateTime


class Person(models.Model):
    str_name = models.CharField(max_length=250, blank=True, null=True)
    url_featured_photo = models.URLField(max_length=200, blank=True, null=True)
    text_description = models.TextField(blank=True, null=True)
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def events(self):
        return Event.objects.by_host(one_host=self)

    def save(self, *args, **kwargs):
        self = updateTime(self)
        super(Person, self).save(*args, **kwargs)
