from django.db import models


class MachineSet(models.QuerySet):
    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'machine',
                'name': result.str_name,
                'url': '/'+result.str_slug,
                'menu_heading': 'menu_h_machines'
            })
        return results_list


class Machine(models.Model):
    objects = MachineSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_machine_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
    one_space = models.ForeignKey(
        'Space', related_name="o_machine_space", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Space')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_wiki = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Wiki URL')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def events(self):
        from hackerspace.models import Event

        return Event.objects.QUERYSET__in_space(one_space=self)

    @property
    def str_menu_heading(self):
        return 'menu_h_machines'

    def save(self, *args, **kwargs):
        from hackerspace.models.events import RESULT__updateTime
        import urllib.parse
        self = RESULT__updateTime(self)
        self.str_slug = urllib.parse.quote(
            'machine/'+self.str_name.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and'))
        super(Machine, self).save(*args, **kwargs)
