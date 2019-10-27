from django.db import models

from hackerspace.models.events import updateTime


def getKeywords(description):
    keywords = ''
    # to do
    return keywords


class MeetingNote(models.Model):
    text_notes = models.TextField(blank=True, null=True)

    many_consensus_items = models.ManyToManyField(
        'ConsensusItem', related_name="m_consensus_items", blank=True)

    text_keywords = models.TextField(blank=True, null=True)
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    @property
    def date(self):
        local_timezone = pytz.timezone(HACKERSPACE_TIMEZONE_STRING)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_created, local_timezone)
        return local_time.date()

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        self = updateTime(self)
        self.text_keywords = getKeywords(self.text_notes)
        super(MeetingNote, self).save(*args, **kwargs)
