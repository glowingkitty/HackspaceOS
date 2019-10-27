from django.db import models

from hackerspace.models.events import updateTime


class ConsensusItem(models.Model):
    str_name = models.CharField(max_length=250, blank=True, null=True)
    text_description = models.TextField(blank=True, null=True)

    boolean_meeting_1_passed = models.BooleanField(default=False)
    boolean_meeting_2_passed = models.BooleanField(default=False)

    one_created_by = models.ForeignKey(
        'Person', related_name="o_created_by", default=None, blank=True, null=True, on_delete=models.SET_NULL)

    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.str_name

    def save(self, *args, **kwargs):
        self = updateTime(self)
        super(ConsensusItem, self).save(*args, **kwargs)
