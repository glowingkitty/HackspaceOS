import urllib.parse

from django.db import models

from _apis.models import Discourse
from datetime import datetime

from django.db.models import Q


class ConsensusSet(models.QuerySet):
    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'consensus',
                'name': result.str_name_en_US,
                'url': result.url_discourse
            })
        return results_list

    def import_from_discourse(self):
        print('import_from_discourse()')
        from _database.models import Person
        from _apis.models import Discourse
        from dateutil import parser
        from _setup.models import Secret
        import time
        import requests
        from pyprintplus import Log

        DISCOURSE_URL = Secret('DISCOURSE.DISCOURSE_URL').value
        if DISCOURSE_URL:
            Log().show_message(
                '✅ Found DISCOURSE.DISCOURSE_URL - start importing Consensus Items from Discourse.')
            time.sleep(2)

            if requests.get(DISCOURSE_URL+'/c/consensus-items').status_code == 200:
                consensus_items = Discourse().get_category_posts(
                    category='consensus-items', all_pages=True)
                print('process {} consensus-items'.format(len(consensus_items)))
                for consensus_item in consensus_items:
                    if consensus_item['title'] != 'About the Consensus Items category':
                        Consensus().create(json_content={
                            'str_name_en_US': consensus_item['title'],
                            'url_discourse': Secret('DISCOURSE.DISCOURSE_URL').value + 't/'+consensus_item['slug'],
                            'text_description_en_US': consensus_item['excerpt'],
                            'int_UNIXtime_created': round(datetime.timestamp(parser.parse(consensus_item['created_at']))),
                            'one_creator': Person.objects.get_discourse_creator(consensus_item['slug']),
                        }
                        )
            else:
                Log().show_message(
                    'WARNING: Can\'t find the "consensus-items" category on your Discourse. Skipped importing Consensus Items from Discourse.')
                time.sleep(4)
        else:
            Log().show_message(
                'WARNING: Can\'t find the DISCOURSE.DISCOURSE_URL in your secrets.json. Will skip Discourse for now.')
            time.sleep(4)

    def latest(self):
        return self.order_by('-int_UNIXtime_created')

    def current(self):
        return self.filter(Q(str_status='new') | Q(str_status='passed_1')).latest()

    def archived(self):
        return self.filter(Q(str_status='approved') | Q(str_status='rejected') | Q(str_status='archived')).latest()


STATUS_CHOICES = (
    ('new', 'New'),
    ('passed_1', 'Meeting 1 passed'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('archived', 'Archived'),
)


class Consensus(models.Model):
    objects = ConsensusSet.as_manager()
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    one_creator = models.ForeignKey(
        'Person', related_name="o_consensus_creator", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Creator')
    str_status = models.CharField(
        max_length=250, default='new', choices=STATUS_CHOICES, verbose_name='Status')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name_en_US

    @property
    def str_menu_heading(self):
        return 'menu_h_consensus'

    def create(self, json_content):
        from _database.models import Helper
        try:
            obj = Consensus.objects.get(
                str_name_en_US=json_content['str_name_en_US']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj = Helper().RESULT__updateTime(obj)
            obj.save()
            print('Updated "'+obj.str_name_en_US+'"')
        except Consensus.DoesNotExist:
            obj = Consensus(**json_content)
            obj = Helper().RESULT__updateTime(obj)
            obj.save()
            print('Created "'+obj.str_name_en_US+'"')

    def save(self, *args, **kwargs):
        from _database.models import Helper
        self = Helper().RESULT__updateTime(self)
        super(Consensus, self).save(*args, **kwargs)
