import urllib.parse

from django.db import models

from hackerspace.APIs.discourse import get_category_posts
from hackerspace.models.events import updateTime
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCOURSE_URL
from datetime import datetime

from django.db.models import Q


class ConsensusSet(models.QuerySet):
    def search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'consensus',
                'name': result.str_name,
                'url': result.url_discourse
            })
        return results_list

    def pull_from_discourse(self):
        print('pull_from_discourse()')
        from hackerspace.models import Person
        from dateutil import parser

        consensus_items = get_category_posts(
            category='consensus-items', all_pages=True)
        print('process {} consensus-items'.format(len(consensus_items)))
        for consensus_item in consensus_items:
            if consensus_item['title'] != 'About the Consensus Items category':
                Consensus().create(json_content={
                    'str_name': consensus_item['title'],
                    'url_discourse': HACKERSPACE_DISCOURSE_URL + 't/'+consensus_item['slug'],
                    'text_description': consensus_item['excerpt'],
                    'int_UNIXtime_created': round(datetime.timestamp(parser.parse(consensus_item['created_at']))),
                    'one_creator': Person.objects.get_discourse_creator(consensus_item['slug']),
                }
                )

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
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    one_creator = models.ForeignKey(
        'Person', related_name="o_consensus_creator", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Creator')
    str_status = models.CharField(
        max_length=250, default='new', choices=STATUS_CHOICES, verbose_name='Status')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def menu_heading(self):
        return 'menu_h_consensus'

    def create(self, json_content):
        try:
            obj = Consensus.objects.get(
                str_name=json_content['str_name']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj = updateTime(obj)
            obj.save()
            print('Updated "'+obj.str_name+'"')
        except Consensus.DoesNotExist:
            obj = Consensus(**json_content)
            obj = updateTime(obj)
            obj.save()
            print('Created "'+obj.str_name+'"')

    def save(self, *args, **kwargs):
        self = updateTime(self)
        super(Consensus, self).save(*args, **kwargs)
