from django.db import models

from pyprintplus import Log


class PhotoSet(models.QuerySet):
    def count_overview(self):
        return {
            'total': self.count(),
            'Wiki': self.filter(str_source='Wiki').count(),
            'Twitter': self.filter(str_source='Twitter').count(),
            'Instagram': self.filter(str_source='Instagram').count(),
            'Flickr': self.filter(str_source='Flickr').count(),
        }

    def random(self, num_results=30):
        import random
        # get random numbers to show random results
        random_set = []
        maximum = self.count()-1
        if maximum > 0:
            while len(random_set) < num_results and len(random_set) != maximum:
                random_number = random.randint(0, maximum)
                while random_number in random_set:
                    random_number = random.randint(0, maximum)
                random_set.append(random_number)

        random_results = []
        for number in random_set:
            random_results.append(self.all()[number])

        return random_results

    def latest(self):
        return self.order_by('-int_UNIXtime_created')

    def oldest(self):
        return self.order_by('int_UNIXtime_created')

    def import_from_google_photos(self, test=False):
        from _apis.models import GooglePhotos
        Log().print('import_from_google_photos()')
        GooglePhotos(test=test).import_photos()

    def import_from_twitter(self, test=False):
        from _apis.models import Twitter
        Log().print('import_from_twitter()')
        Twitter(test=test).import_photos()

    def import_from_wiki(self, test=False):
        from _apis.models import MediaWiki
        Log().print('import_from_wiki()')
        MediaWiki(test=test).import_photos()

    def import_from_flickr(self, test=False):
        from _apis.models import Flickr
        Log().print('import_from_flickr()')
        Flickr(test=test).import_photos()

    def import_from_instagram(self, test=False):
        from _apis.models import Instagram
        Log().print('import_from_instagram()')
        Instagram(test=test).import_photos()


class Photo(models.Model):
    objects = PhotoSet.as_manager()
    text_description_en_US = models.TextField(
        blank=True, null=True, verbose_name='Description en-US')
    text_description_he_IL = models.TextField(
        blank=True, null=True, verbose_name='Description he-IL')
    url_image = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Image URL')
    url_post = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Post URL')
    str_source = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Source')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.url_image

    @property
    def str_relative_time(self):
        Log().print('photo.str_relative_time')
        import time
        from datetime import datetime

        timestamp = self.int_UNIXtime_created

        # in last 60 minutes
        if timestamp >= time.time()-(60*60):
            minutes_in_past = int((time.time()-timestamp)/60)
            Log().print('--> return STR')
            return str(minutes_in_past)+' minute'+('s' if minutes_in_past > 1 else '')+' ago'

        # in last 24 hours
        elif timestamp >= time.time()-(60*60*24):
            hours_in_past = int(((time.time()-timestamp)/60)/60)
            Log().print('--> return STR')
            return str(hours_in_past)+' hour'+('s' if hours_in_past > 1 else '')+' ago'

        # else if in last 6 days, return number of days ago
        elif timestamp >= time.time()-(60*60*24*6):
            days_in_past = int((((time.time()-timestamp)/60)/60)/24)
            Log().print('--> return STR')
            return str(days_in_past)+' day'+('s' if days_in_past > 1 else '')+' ago'

        # else date string
        else:
            Log().print('--> return STR')
            return datetime.utcfromtimestamp(timestamp).strftime('%b %d, %Y')
