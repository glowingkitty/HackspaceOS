from django.db import models


class GuildeSet(models.QuerySet):
    def QUERYSET__by_name(self, name):
        if not name or name == '':
            return None
        return self.filter(str_name__icontains=name).first()

    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'guilde',
                'name': result.str_name,
                'url': '/'+result.str_slug,
                'menu_heading': 'menu_h_guildes'
            })
        return results_list


class Guilde(models.Model):
    objects = GuildeSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_wiki = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Wiki URL')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    many_members = models.ManyToManyField(
        'Person', related_name="m_members", blank=True, verbose_name='Members')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def events(self):
        from hackerspace.models import Event

        search_query = self.str_name.lower().split('guilde')[0]
        return Event.objects.QUERYSET__upcoming().filter(one_guilde=self)

    @property
    def str_menu_heading(self):
        return 'menu_h_guildes'

    def save(self, *args, **kwargs):
        import urllib.parse
        from hackerspace.models.events import RESULT__updateTime

        self = RESULT__updateTime(self)
        self.str_slug = urllib.parse.quote(
            'guilde/'+self.str_name.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and'))
        super(Guilde, self).save(*args, **kwargs)
