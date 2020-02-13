from django.db import models


class SpaceSet(models.QuerySet):
    def QUERYSET__by_name(self, name):
        if not name or name == '':
            return None
        return self.filter(str_name_en_US__icontains=name).first()

    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'space',
                'name': result.str_name_en_US,
                'url': '/'+result.str_slug,
                'menu_heading': 'menu_h_spaces'
            })
        return results_list


class Space(models.Model):
    objects = SpaceSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    image_featured_photo = models.ImageField(upload_to ='spaces_images',blank=True, null=True, verbose_name='Photo')
    url_wiki = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Wiki URL')
    one_guilde = models.ForeignKey(
        'Guilde', related_name="o_spaces_guilde", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
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
        return Event.objects.QUERYSET__upcoming().QUERYSET__in_space(one_space=self)

    @property
    def machines(self):
        from _database.models import Machine

        return Machine.objects.filter(one_space=self)

    @property
    def str_menu_heading(self):
        return 'menu_h_spaces'

    def save(self, *args, **kwargs):
        from _database.models.events import RESULT__updateTime
        import urllib.parse

        self = RESULT__updateTime(self)
        self.str_slug = urllib.parse.quote(
            'space/'+self.str_name_en_US.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and'))
        super(Space, self).save(*args, **kwargs)
