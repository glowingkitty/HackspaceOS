from django.db import models


class WishesSet(models.QuerySet):
    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'wish',
                'name': result.str_name_en_US,
                'url': '/'+result.str_slug,
                'menu_heading': 'menu_h_wishes'
            })
        return results_list


class Wish(models.Model):
    objects = WishesSet.as_manager()
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    one_person = models.ForeignKey(
        'Person', related_name="o_wishes_person", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Guilde')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name_en_US

    @property
    def str_menu_heading(self):
        return 'menu_h_wishes'

    def save(self, *args, **kwargs):
        from _database.models import Helper

        self = Helper().RESULT__updateTime(self)
        super(Wish, self).save(*args, **kwargs)
