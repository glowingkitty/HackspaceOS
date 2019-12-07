from django.db import models


class PersonSet(models.QuerySet):
    def get_discourse_creator(self, slug):
        from hackerspace.APIs.discourse import get_post_details
        from django.db.models import Q

        print('get_discourse_creator()')
        try:
            details = get_post_details(slug)
            return self.filter(Q(str_name=details['name']) | Q(str_name=details['username'])).first()
        except:
            return None

    def by_url_discourse(self, url):
        return self.filter(url_discourse=url).first()

    def import_from_discourse(self):
        from hackerspace.APIs.discourse import get_users
        from getKey import STR__get_key
        import time
        import requests
        from asci_art import show_message

        DISCOURSE_URL = STR__get_key('DISCOURSE.DISCOURSE_URL')
        if DISCOURSE_URL:
            show_message(
                '✅ Found DISCOURSE.DISCOURSE_URL - start importing persons from Discourse.')
            time.sleep(2)

            if requests.get(DISCOURSE_URL).status_code == 200:
                users = get_users()
                print('LOG: --> process {} users'.format(len(users)))
                for user in users:
                    Person().create(json_content={
                        'str_name': user['user']['name'] if user['user']['name'] and user['user']['name'] != '' else user['user']['username'],
                        'url_featured_photo': DISCOURSE_URL + user['user']['avatar_template'].replace('{size}', '240'),
                        'url_discourse': DISCOURSE_URL + 'u/'+user['user']['username'],
                        'text_description': user['user']['title'] if user['user']['title'] != '' else None
                    })
            else:
                show_message(
                    'WARNING: I can\'t access your Discourse page. Is the URL correct? Will skip Discourse for now.')
                time.sleep(4)
        else:
            show_message(
                'WARNING: Can\'t find the DISCOURSE.DISCOURSE_URL in your secrets.json. Will skip Discourse for now.')
            time.sleep(4)

    def QUERYSET__by_name(self, name):
        if not name or name == '':
            return None
        from django.db.models import Q
        from getKey import STR__get_key

        return self.filter(Q(url_discourse=STR__get_key('DISCOURSE.DISCOURSE_URL') + 'u/'+name) | Q(str_name__icontains=name)).first()


class Person(models.Model):
    objects = PersonSet.as_manager()
    str_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Name')
    url_featured_photo = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Photo URL')
    url_discourse = models.URLField(
        max_length=200, blank=True, null=True, verbose_name='Discourse URL')
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    @property
    def str_name_shortened(self):
        if not ' ' in self.str_name:
            return self.str_name
        return self.str_name.split(' ')[0]+' '+self.str_name.split(' ')[1][:1]

    def create(self, json_content):
        try:
            obj = Person.objects.get(
                url_discourse=json_content['url_discourse']
            )
            for key, value in json_content.items():
                setattr(obj, key, value)
            obj.save()
            print('Updated "'+obj.str_name+'"')
        except Person.DoesNotExist:
            obj = Person(**json_content)
            obj.save()
            print('Created "'+obj.str_name+'"')

    @property
    def events(self):
        from hackerspace.models import Event
        return Event.objects.QUERYSET__by_host(one_host=self)

    def save(self, *args, **kwargs):
        from hackerspace.models.events import RESULT__updateTime
        self = RESULT__updateTime(self)
        super(Person, self).save(*args, **kwargs)
