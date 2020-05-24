from django.db import models
from pyprintplus import Log
from _setup.models import Secret


class PersonSet(models.QuerySet):
    def get_discourse_creator(self, slug):
        from _apis.models import Discourse
        from django.db.models import Q

        print('get_discourse_creator()')
        try:
            details = Discourse().get_post_details(slug)
            return self.filter(Q(str_name_en_US=details['name']) | Q(str_name_en_US=details['username'])).first()
        except:
            return None

    def by_url_discourse(self, url):
        return self.filter(url_discourse=url).first()

    def import_from_discourse(self, DISCOURSE_URL=Secret('DISCOURSE.DISCOURSE_URL').value):
        from _apis.models import Discourse
        import time
        import requests
        from pyprintplus import Log

        if DISCOURSE_URL:
            Log().show_message(
                '✅ Found DISCOURSE.DISCOURSE_URL - start importing persons from Discourse.')
            time.sleep(2)

            if requests.get(DISCOURSE_URL).status_code == 200:
                users = Discourse(url=DISCOURSE_URL).get_users()
                Log().print('--> process {} users'.format(len(users)))
                for user in users:
                    Person().create(json_content={
                        'str_name_en_US': user['user']['name'] if user['user']['name'] and user['user']['name'] != '' else user['user']['username'],
                        'url_featured_photo': DISCOURSE_URL + user['user']['avatar_template'].replace('{size}', '240'),
                        'url_discourse': DISCOURSE_URL + 'u/'+user['user']['username'],
                        'text_description_en_US': user['user']['title'] if user['user']['title'] != '' else None
                    })
            else:
                Log().show_message(
                    'WARNING: I can\'t access your Discourse page. Is the URL correct? Will skip Discourse for now.')
                time.sleep(4)
        else:
            Log().show_message(
                'WARNING: Can\'t find the DISCOURSE.DISCOURSE_URL in your secrets.json. Will skip Discourse for now.')
            time.sleep(4)

    def QUERYSET__by_name(self, name):
        if not name or name == '':
            return None
        from django.db.models import Q
        from _setup.models import Secret

        return self.filter(Q(url_discourse=Secret('DISCOURSE.DISCOURSE_URL').value + 'u/'+name) | Q(str_name_en_US__icontains=name)).first()


class Person(models.Model):
    objects = PersonSet.as_manager()
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
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name_en_US

    @property
    def str_name_shortened(self):
        if not ' ' in self.str_name_en_US:
            return self.str_name_en_US
        return self.str_name_en_US.split(' ')[0]+' '+self.str_name_en_US.split(' ')[1][:1]

    def create(self, json_content):
        try:
            obj = Person.objects.get(
                url_discourse=json_content['url_discourse']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj.save()
            print('Updated "'+obj.str_name_en_US+'"')
        except Person.DoesNotExist:
            obj = Person(**json_content)
            obj.save()
            print('Created "'+obj.str_name_en_US+'"')

    @property
    def events(self):
        from _database.models import Event
        return Event.objects.QUERYSET__by_host(one_host=self)

    def save(self, *args, **kwargs):
        from _database.models import Helper
        self = Helper().RESULT__updateTime(self)
        super(Person, self).save(*args, **kwargs)
