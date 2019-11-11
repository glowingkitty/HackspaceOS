import urllib.parse

from django.db import models

from hackerspace.APIs.discourse import get_category_posts
from hackerspace.models.events import updateTime
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCOURSE_URL
from datetime import datetime
from dateutil import parser


class ProjectSet(models.QuerySet):
    def search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'project',
                'name': result.str_name,
                'url': result.url_discourse
            })
        return results_list

    def latest(self):
        return self.order_by('-int_UNIXtime_created')

    def pull_from_discourse(self):
        print('pull_from_discourse()')
        from hackerspace.models import Person

        projects = get_category_posts(category='projects', all_pages=True)
        print('process {} projects'.format(len(projects)))
        for project in projects:
            if project['title'] != 'About the Projects category':
                Project().create(json_content={
                    'str_name': project['title'],
                    'url_featured_photo': project['image_url'] if project['image_url'] and '/uploads' in project['image_url'] else None,
                    'url_discourse': HACKERSPACE_DISCOURSE_URL + 't/'+project['slug'],
                    'text_description': project['excerpt'],
                    'one_creator': Person.objects.get_discourse_creator(project['slug']),
                    'int_UNIXtime_created': round(datetime.timestamp(parser.parse(project['created_at'])))
                }
                )


class Project(models.Model):
    objects = ProjectSet.as_manager()
    str_slug = models.CharField(max_length=250, blank=True, null=True)
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    one_creator = models.ForeignKey(
        'Person', related_name="o_project_creator", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Creator')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def menu_heading(self):
        return 'menu_h_projects'

    def create(self, json_content):
        try:
            obj = Project.objects.get(
                url_discourse=json_content['url_discourse']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj = updateTime(obj)
            obj.save()
            print('Updated "'+obj.str_name+'"')
        except Project.DoesNotExist:
            obj = Project(**json_content)
            obj = updateTime(obj)
            obj.save()
            print('Created "'+obj.str_name+'"')

    def save(self, *args, **kwargs):
        self = updateTime(self)
        self.str_slug = urllib.parse.quote(
            'project/'+self.str_name.lower().replace(' ', '-').replace('/', '').replace('@', 'at').replace('&', 'and').replace('(', '').replace(')', ''))
        super(Project, self).save(*args, **kwargs)
