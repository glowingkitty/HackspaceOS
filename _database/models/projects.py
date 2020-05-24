from django.db import models
from pyprintplus import Log
from _setup.models import Secret


class ProjectSet(models.QuerySet):
    def LIST__search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'project',
                'name': result.str_name_en_US,
                'url': result.url_discourse
            })
        return results_list

    def latest(self):
        return self.order_by('-int_UNIXtime_created')

    def import_from_discourse(self, DISCOURSE_URL=Secret('DISCOURSE.DISCOURSE_URL').value):
        print('import_from_discourse()')
        from _database.models import Person
        from _apis.models import Discourse
        from datetime import datetime
        from dateutil import parser
        from pyprintplus import Log
        import time
        import requests

        if DISCOURSE_URL:
            Log().show_message(
                '✅ Found DISCOURSE.DISCOURSE_URL - start importing projects from Discourse.')
            time.sleep(2)

            if requests.get(DISCOURSE_URL+'/c/projects').status_code == 200:
                projects = Discourse().get_category_posts(
                    category='projects', all_pages=True)
                Log().print('--> process {} projects'.format(len(projects)))
                for project in projects:
                    if project['title'] != 'About the Projects category':
                        Project().create(json_content={
                            'str_name_en_US': project['title'],
                            'url_featured_photo': project['image_url'] if project['image_url'] and '/uploads' in project['image_url'] else None,
                            'url_discourse': Secret('DISCOURSE.DISCOURSE_URL').value + 't/'+project['slug'],
                            'text_description_en_US': project['excerpt'] if 'excerpt' in project else None,
                            'one_creator': Person.objects.get_discourse_creator(project['slug']),
                            'int_UNIXtime_created': round(datetime.timestamp(parser.parse(project['created_at'])))
                        }
                        )
            else:
                Log().show_message(
                    'WARNING: Can\'t find the "projects" category on your Discourse. Skipped importing Consensus Items from Discourse.')
                time.sleep(4)
        else:
            Log().show_message(
                'WARNING: Can\'t find the DISCOURSE.DISCOURSE_URL in your secrets.json. Will skip Discourse for now.')
            time.sleep(4)


class Project(models.Model):
    objects = ProjectSet.as_manager()
    str_name_en_US = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name en-US')
    str_name_he_IL = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name he-IL')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')
    one_creator = models.ForeignKey(
        'Person', related_name="o_project_creator", default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Creator')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name_en_US

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
            print('Updated "'+obj.str_name_en_US+'"')
        except Project.DoesNotExist:
            obj = Project(**json_content)
            obj.save()
            print('Created "'+obj.str_name_en_US+'"')

    def save(self, *args, **kwargs):
        from _database.models import Helper
        import urllib.parse
        from googletrans import Translator
        translator = Translator()

        if self.str_name_en_US:
            self.str_name_en_US = translator.translate(
                self.str_name_en_US, 'en').text
            if not self.str_name_he_IL:
                self.str_name_he_IL = translator.translate(
                    self.str_name_en_US, 'he').text

        self = Helper().RESULT__updateTime(self)
        super(Project, self).save(*args, **kwargs)
