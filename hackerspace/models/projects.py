from django.db import models


class ProjectSet(models.QuerySet):
    def LIST__search_results(self):
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
        from hackerspace.APIs.discourse import get_category_posts
        from datetime import datetime
        from dateutil import parser
        from getKey import STR__get_key
        from asci_art import show_message
        import time
        import requests

        DISCOURSE_URL = STR__get_key('DISCOURSE.DISCOURSE_URL')
        if DISCOURSE_URL:
            show_message(
                '✅ Found DISCOURSE.DISCOURSE_URL - start importing projects from Discourse.')
            time.sleep(2)

            if requests.get(DISCOURSE_URL+'/c/projects').status_code == 200:
                projects = get_category_posts(
                    category='projects', all_pages=True)
                print('LOG: --> process {} projects'.format(len(projects)))
                for project in projects:
                    if project['title'] != 'About the Projects category':
                        Project().create(json_content={
                            'str_name': project['title'],
                            'url_featured_photo': project['image_url'] if project['image_url'] and '/uploads' in project['image_url'] else None,
                            'url_discourse': STR__get_key('DISCOURSE.DISCOURSE_URL') + 't/'+project['slug'],
                            'text_description': project['excerpt'],
                            'one_creator': Person.objects.get_discourse_creator(project['slug']),
                            'int_UNIXtime_created': round(datetime.timestamp(parser.parse(project['created_at'])))
                        }
                        )
            else:
                show_message(
                    'WARNING: Can\'t find the "projects" category on your Discourse. Skipped importing Consensus Items from Discourse.')
                time.sleep(4)
        else:
            show_message(
                'WARNING: Can\'t find the DISCOURSE.DISCOURSE_URL in your secrets.json. Will skip Discourse for now.')
            time.sleep(4)


class Project(models.Model):
    objects = ProjectSet.as_manager()
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
    def str_menu_heading(self):
        return 'menu_h_projects'

    def create(self, json_content):
        try:
            obj = Project.objects.get(
                url_discourse=json_content['url_discourse']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj.save()
            print('Updated "'+obj.str_name+'"')
        except Project.DoesNotExist:
            obj = Project(**json_content)
            obj.save()
            print('Created "'+obj.str_name+'"')

    def save(self, *args, **kwargs):
        from hackerspace.models.events import RESULT__updateTime
        import urllib.parse

        self = RESULT__updateTime(self)
        super(Project, self).save(*args, **kwargs)
