from _setup.models import Config


class OpenStatus():
    def __init__(self, request):
        from datetime import datetime
        import calendar
        import pytz
        from _website.templatetags.translate import landingpage
        from _database.models import Event
        from _website.models import Request
        language = Request(request).language

        # if an event is happening - show space open. Else use opening hours defined by config.json
        if self.still_temporary and Config('PHYSICAL_SPACE.TEMPORARY_LANDINGPAGE_HEADER.OPENING_STATUS').value:
            translated_status = Config(
                'PHYSICAL_SPACE.TEMPORARY_LANDINGPAGE_HEADER.OPENING_STATUS').value
            color_indicator = 'grey'
        elif Event.objects.QUERYSET__now():
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
            self.value = '<div dir="rtl" align="right">'+translated_status + \
                '</div><div class="status_code_icon '+color_indicator+' rtl"></div>'
        else:
            self.value = '<div class="status_code_icon ' + \
                color_indicator+'"></div><div>'+translated_status+'</div>'

    @property
    def still_temporary(self):
        import datetime
        from dateutil.parser import parse
        # see if TEMPORARY_LANDINGPAGE_HEADER.UP_TO_DATE has already passed
        if not Config('PHYSICAL_SPACE.TEMPORARY_LANDINGPAGE_HEADER.UP_TO_DATE').value:
            return False
        up_to_date = parse(
            Config('PHYSICAL_SPACE.TEMPORARY_LANDINGPAGE_HEADER.UP_TO_DATE').value)
        now = datetime.datetime.now()
        return now <= up_to_date
