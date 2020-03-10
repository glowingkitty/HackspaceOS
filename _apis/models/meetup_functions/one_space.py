from _setup.models import Config


class MeetupOneSpace():
    def __init__(self, event):
        from _database.models import Space

        if 'how_to_find_us' in event:
            spaces = Space.objects.all()

            for space in spaces.iterator():
                if space.str_name_en_US.lower() in event['how_to_find_us'].lower():
                    self.value = space

        # else...
        EVENTS_SPACES_OVERWRITE = Config(
            'EVENTS.EVENTS_SPACES_OVERWRITE').value
        for field in EVENTS_SPACES_OVERWRITE:
            if field in event['name']:
                self.value = Space.objects.QUERYSET__by_name(
                    EVENTS_SPACES_OVERWRITE[field])
        else:
            self.value = Space.objects.QUERYSET__by_name(
                Config('EVENTS.EVENTS_SPACE_DEFAULT').value)
