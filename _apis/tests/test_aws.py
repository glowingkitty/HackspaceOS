from django.test import TestCase
from _apis.models import Aws


class AwsTestCase(TestCase):
    def test_s3_upload_and_delete(self):
        if Aws().setup_done:
            with open('README.md', 'rb') as f:
                file_url = Aws().upload(f)
                self.assertTrue(type(file_url) == str)
                Aws().delete('README.md')
