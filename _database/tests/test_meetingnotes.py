from django.test import TestCase
from _database.models import MeetingNote


class MeetingNotesTestCase(TestCase):
    def test_LIST__search_results(self):
        MeetingNote.objects.import_all_from_wiki(
            WIKI_API_URL='https://www.noisebridge.net/api.php', test=True)
        self.assertTrue(len(MeetingNote.objects.LIST__search_results()) > 0)

    def test_start_and_meeting_end(self):
        MeetingNote().start('hackspace-os-test')
        MeetingNote().end('hackspace-os-test')
