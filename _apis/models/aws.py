import time
from _setup.models import Secret
from pyprintplus import Log
import boto3
from botocore.exceptions import NoCredentialsError


class Aws():
    def __init__(self,
                 access_key_id=Secret('AWS.ACCESS_KEYID').value,
                 secret_access_key=Secret('AWS.SECRET_ACCESS_KEY').value,
                 bucket_name=Secret('AWS.S3.BUCKET_NAME').value,
                 server_area=Secret('AWS.S3.SERVER_AREA').value,
                 show_log=True,
                 test=False):
        self.logs = ['self.__init__']
        self.test = test
        self.started = round(time.time())
        self.show_log = show_log
        self.setup_done = True if access_key_id and secret_access_key and bucket_name and server_area else False
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_name = bucket_name
        self.server_area = server_area

        if self.setup_done:
            self.s3_url = bucket_name+'.s3-' + server_area+'.amazonaws.com'
            self.session = boto3.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
            )
            self.s3_bucket = self.session.resource('s3').Bucket(bucket_name)
            self.s3_client = boto3.client('s3')

    @property
    def config(self):
        return Secret('AWS').value

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from pyprintplus import Log
        import json

        try:
            if not self.access_key_id or not self.secret_access_key or not self.bucket_name:
                Log().show_messages(
                    ['Let\'s setup AWS - so whenever a user creates a new event via your new website, the event image will be uploaded to AWS S3.'])

                Log().show_message(
                    'To upload photos to S3: Enter your AWS ACCESS_KEYID')
                self.access_key_id = None if self.test else input()
                if not self.access_key_id and not self.test:
                    raise KeyboardInterrupt

                Log().show_message(
                    'To upload photos to S3: Enter your AWS SECRET_ACCESS_KEY')
                self.secret_access_key = None if self.test else input()
                if not self.secret_access_key and not self.test:
                    raise KeyboardInterrupt

                Log().show_message(
                    'To upload photos to S3: Enter your S3 BUCKET_NAME')
                self.bucket_name = None if self.test else input()
                if not self.bucket_name and not self.test:
                    raise KeyboardInterrupt

                Log().show_message(
                    'To upload photos to S3: Enter your S3 SERVER_AREA')
                self.server_area = None if self.test else input()
                if not self.server_area and not self.test:
                    raise KeyboardInterrupt

                Log().show_message(
                    'To delete photos from S3: Did you configure the AWS CLI? (yes|no)')
                reply = 'yes' if self.test else input()
                if reply == 'no':
                    Log().show_messages([
                        'Install the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html',
                        'Configure your AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration'
                    ])

                with open('_setup/secrets.json') as json_config:
                    secrets = json.load(json_config)
                    secrets['AWS']['ACCESS_KEYID'] = self.access_key_id
                    secrets['AWS']['SECRET_ACCESS_KEY'] = self.secret_access_key
                    secrets['AWS']['S3']['BUCKET_NAME'] = self.bucket_name
                    secrets['AWS']['S3']['SERVER_AREA'] = self.server_area

                with open('_setup/secrets.json', 'w') as outfile:
                    json.dump(secrets, outfile, indent=4)

            Log().show_message('Aws setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    def upload(self, image):
        self.log('upload()')
        if not self.setup_done:
            self.log('-> ERROR: Secrets are missing. Complete setup first.')
            return None
        elif not image:
            self.log('-> ERROR: Image is needed')
            return None

        s3_object = self.s3_bucket.put_object(
            Key=image.name, Body=image, ACL='public-read')
        if s3_object:
            return 'https://'+self.s3_url+'/'+image.name
        else:
            return None

    def delete(self, file_name):
        self.log('delete()')
        if not self.setup_done:
            return False

        try:
            response = self.s3_client.delete_object(
                Bucket=self.bucket_name, Key=file_name)
            if response['ResponseMetadata']['HTTPStatusCode'] == 204:
                return True
            else:
                self.log('-> ERROR: Unexpected response: {}'.format(response))
                return False

        except NoCredentialsError:
            self.log(
                '-> ERROR: Credentials not found. Probably you havent setup the AWS CLI. To fix this: use "sudo apt install awscli", followed by "aws configure" or read more online: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration')
