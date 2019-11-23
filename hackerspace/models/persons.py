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

    def pull_from_discourse(self):
        from hackerspace.APIs.discourse import get_users
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCOURSE_URL

        print('pull_from_discourse()')
        users = get_users()
        print('process {} users'.format(len(users)))
        for user in users:
            Person().create(json_content={
                'str_name': user['user']['name'] if user['user']['name'] and user['user']['name'] != '' else user['user']['username'],
                'url_featured_photo': HACKERSPACE_DISCOURSE_URL + user['user']['avatar_template'].replace('{size}', '240'),
                'url_discourse': HACKERSPACE_DISCOURSE_URL + 'u/'+user['user']['username'],
                'text_description': user['user']['title'] if user['user']['title'] != '' else None
            })

    def by_name(self, name):
        from django.db.models import Q
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCOURSE_URL
        return self.filter(Q(url_discourse=HACKERSPACE_DISCOURSE_URL + 'u/'+name) | Q(str_name__icontains=name)).first()


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
        return Event.objects.by_host(one_host=self)

    def save(self, *args, **kwargs):
        from hackerspace.models.events import updateTime
        self = updateTime(self)
        super(Person, self).save(*args, **kwargs)
