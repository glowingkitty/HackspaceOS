from django.db import models

from hackerspace.models import Event
from hackerspace.models.events import updateTime
import urllib.parse


class SpaceSet(models.QuerySet):
    def search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'space',
                'name': result.str_name,
                'url': '/'+result.str_slug
            })
        return results_list


class Space(models.Model):
    objects = SpaceSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name = models.CharField(max_length=250, blank=True, null=True)
    url_featured_photo = models.URLField(max_length=200, blank=True, null=True)
    text_description = models.TextField(blank=True, null=True)
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def events(self):
        return Event.objects.in_space(one_space=self)

    @property
    def menu_heading(self):
        return 'menu_h_spaces'

    def save(self, *args, **kwargs):
        self = updateTime(self)
        self.str_slug = urllib.parse.quote(
            'space/'+self.str_name.lower().replace(' ', '-'))
        super(Space, self).save(*args, **kwargs)
