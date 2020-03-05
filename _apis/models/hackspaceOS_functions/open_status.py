class OpenStatus():
    def __init__(self, request):
        from django.http import JsonResponse
        from datetime import datetime
        import calendar
        import pytz
        from _setup.config import Config
        from _website.templatetags.translate import landingpage
        from _database.models import Event
        from _website.models import Request
        language = Request(request).language

        # if an event is happening - show space open. Else use opening hours defined by config.json
        if Event.objects.QUERYSET__now():
            translated_status = landingpage('Open now', language)
            color_indicator = 'green'
        else:
            timezone = pytz.timezone(Config(
                'PHYSICAL_SPACE.TIMEZONE_STRING').value)
            today_weekday = calendar.day_name[datetime.now(timezone).weekday()]
            now_hour = datetime.now(timezone).hour
            now_minute = datetime.now(timezone).minute
            status = 'Unknown'

            for status_change in Config('PHYSICAL_SPACE.OPENING_HOURS').value[today_weekday]:
                if now_hour >= status_change[0] and now_minute >= status_change[1]:
                    status = status_change[2]
                    translated_status = landingpage(status, language)
                    color_indicator = status_change[3]
                else:
                    break
        if language == 'hebrew':
            self.value = JsonResponse(
                {'html': '<div dir="rtl" align="right">'+translated_status +
                 '</div><div class="status_code_icon '+color_indicator+' rtl"></div>'})
        else:
            self.value = JsonResponse(
                {'html': '<div class="status_code_icon '+color_indicator+'"></div><div>'+translated_status+'</div>'})
