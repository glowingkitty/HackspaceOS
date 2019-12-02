from django.db import models


def boolean_is_image(image_url):
    image_url = image_url.lower()

    if image_url.endswith('.jpg') or image_url.endswith('.png'):
        return True
    else:
        return False


class PhotoSet(models.QuerySet):
    def import_from_twitter(self):
        print('LOG: import_from_twitter()')
        # TODO

    def import_from_wiki(self):
        # API documentation: https://www.mediawiki.org/wiki/API:Allimages
        print('LOG: import_from_wiki()')
        from hackerspace.YOUR_HACKERSPACE import WIKI_API_URL
        import requests
        from dateutil.parser import parse
        from datetime import datetime

        parameter = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'list': 'allimages',
            'aisort': 'timestamp',
            'aidir': 'descending',
            'ailimit': '500',
            'aiminsize': '50000',  # minimum 50kb size, to filter out small logos/icons
            'aiprop': 'timestamp|canonicaltitle|url'
        }
        response_json = requests.get(WIKI_API_URL, params=parameter).json()

        for photo in response_json['query']['allimages']:
            if boolean_is_image(photo['url']) == True:
                if Photo.objects.filter(url_image=photo['url']).exists() == False:
                    Photo(
                        text_description=photo['canonicaltitle'] if 'canonicaltitle' in photo else None,
                        url_image=photo['url'],
                        str_source='Wiki',
                        int_UNIXtime_created=round(
                            datetime.timestamp(parse(photo['timestamp']))),
                    ).save()
                    print('LOG: New photo saved')

        while 'continue' in response_json and 'aicontinue' in response_json['continue']:
            response_json = requests.get(
                WIKI_API_URL, params={**parameter, **{'aicontinue': response_json['continue']['aicontinue']}}).json()

            for photo in response_json['query']['allimages']:
                if boolean_is_image(photo['url']) == True:
                    if Photo.objects.filter(url_image=photo['url']).exists() == False:
                        Photo(
                            text_description=photo['canonicaltitle'] if 'canonicaltitle' in photo else None,
                            url_image=photo['url'],
                            str_source='Wiki',
                            int_UNIXtime_created=round(
                                datetime.timestamp(parse(photo['timestamp']))),
                        ).save()
                        print('LOG: New photo saved')

        print('LOG: Complete! All photos processed! Now {} photos'.format(
            Photo.objects.count()))

    def import_from_instagram(self):
        print('LOG: import_from_instagram()')
        # TODO

    def import_from_flickr(self):
        print('LOG: import_from_flickr()')
        # TODO


class Photo(models.Model):
    objects = PhotoSet.as_manager()
    text_description = models.TextField(
        blank=True, null=True, verbose_name='Description')
    url_image = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Image URL')
    str_source = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Source')
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.text_description
