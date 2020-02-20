from django.test import TestCase
from _database.models import Wish


class WishesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Wish(str_name_en_US='I wish people would clean up after themself.').save()
        Wish(str_name_en_US='I wish we would have a high end gaming pc.').save()

    def test_LIST__search_results(self):
        self.assertTrue(len(Wish.objects.LIST__search_results()) > 0)
