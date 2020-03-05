from _setup.log import log


class Helper():
    def RESULT__updateTime(self, result):
        log('RESULT__updateTime(result={})'.format(result))
        import time

        # update time
        if not result.int_UNIXtime_created:
            result.int_UNIXtime_created = time.time()
        result.int_UNIXtime_updated = time.time()
        return result

    def JSON_RESPONSE_more_results(self, request, template_path, queryset):
        log('JSON_RESPONSE_more_results(request, template_path, queryset)')
        from django.http import JsonResponse
        from django.template.loader import get_template

        # see if request comes from a guilde/space page, then show guilde/space events, not all events
        if request.GET.get('origin', None):
            if 'guilde/' in request.GET.get('origin', None):
                queryset = queryset.filter(
                    one_guilde__str_slug=request.GET.get('origin', None)[1:])
            elif 'space/' in request.GET.get('origin', None):
                queryset = queryset.filter(
                    one_space__str_slug=request.GET.get('origin', None)[1:])

        start_from = int(request.GET.get('from', None))
        upt_to = int(start_from+10)

        log('--> return JsonResponse')
        return JsonResponse({
            'html': get_template('components/body/'+template_path).render({
                'all_results': queryset[start_from:upt_to],
                'specific_selector': request.GET.get('specific_selector', None)
            }),
            'continue_from': upt_to,
            'more_results': True if queryset.count() > upt_to else False
        })

    def JSON_RESPONSE_more_photos(self, request):
        log('JSON_RESPONSE_more_photos(request)')
        from django.http import JsonResponse
        from django.template.loader import get_template
        from _database.models import Photo

        start_from = int(request.GET.get('from', None))
        upt_to = int(start_from+30)

        # get photos: latest, oldest or random
        if request.GET.get('type', None) == 'latest':
            queryset = Photo.objects.latest()
        elif request.GET.get('type', None) == 'oldest':
            queryset = Photo.objects.oldest()
        elif request.GET.get('type', None) == 'random':
            queryset = Photo.objects.random()

        log('--> return JsonResponse')
        return JsonResponse({
            'html': get_template('components/body/photos_list.html').render({
                'photos': queryset[start_from:upt_to] if request.GET.get('type', None) != 'random' else queryset,
            }),
            'continue_from': upt_to,
            'more_results': True if request.GET.get('type', None) == 'random' or queryset.count() > upt_to else False
        })

    def DATETIME__from_date_and_time_STR(self, str__date, str__time):
        import pytz
        from datetime import datetime
        from _setup.config import Config

        TIMEZONE_STRING = Config('PHYSICAL_SPACE.TIMEZONE_STRING').value
        if 'AM' in str__time or 'PM' in str__time:
            datetime_input = pytz.timezone(TIMEZONE_STRING).localize(
                datetime.strptime(str(str__date+' '+str__time.replace(' ', '')), "%Y-%m-%d %I:%M%p"))
        else:
            datetime_input = pytz.timezone(TIMEZONE_STRING).localize(
                datetime.strptime(str(str__date+' '+str__time.replace(' ', '')), "%Y-%m-%d %H:%M"))
        log('--> return DATETIME')
        return datetime_input

    def INT__UNIX_from_date_and_time_STR(self, str__date, str__time):
        log('INT__UNIX_from_date_and_time_STR(str__date={},str__time={})'.format(
            str__date, str__time))
        from datetime import datetime

        log('--> get datetime from string')
        datetime_input = DATETIME__from_date_and_time_STR(str__date, str__time)

        log('--> datetime to UNIX time')
        int_timestamp = round(datetime.timestamp(datetime_input))

        log('--> return INT')
        return int_timestamp

    def INT__duration_minutes(self, str_duration):
        hours = int(str_duration.split(':')[0])
        minutes = int(str_duration.split(':')[1])
        log('--> return INT')
        return (hours*60)+minutes
