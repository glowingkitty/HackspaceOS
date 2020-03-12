from django.test import TestCase
from _apis.models import Telegram
from _setup.models import Config
from random import randint


class TelegramTestCase(TestCase):
    def test_message(self):
        if Telegram().setup_done:
            messages = Config('UNITTESTS.TELEGRAM_TEST_MESSAGES').value
            selected_message = randint(0, len(messages)-1)
            response = Telegram().message(messages[selected_message])
            self.assertEqual(response, True)
