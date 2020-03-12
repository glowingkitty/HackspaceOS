from django.db import models


class MachineSet(models.QuerySet):
    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'machine',
                'name': result.str_name_en_US,
                'url': '/'+result.str_slug,
                'menu_heading': 'menu_h_machines'
            })
        return results_list


class Machine(models.Model):
    objects = MachineSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_machine_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
    one_space = models.ForeignKey(
        'Space', related_name="o_machine_space", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Space')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_wiki = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Wiki URL')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name_en_US

    @property
    def events(self):
        from _database.models import Event

        return Event.objects.QUERYSET__in_space(one_space=self)

    @property
    def str_menu_heading(self):
        return 'menu_h_machines'

    def save(self, *args, **kwargs):
        from _database.models import Helper
        import urllib.parse
        self = Helper().RESULT__updateTime(self)
        self.str_slug = urllib.parse.quote(
            'machine/'+self.str_name_en_US.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and'))
        super(Machine, self).save(*args, **kwargs)
