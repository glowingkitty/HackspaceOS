# Init a config.py file with a random Djanog secret, Admin URL and placeholders for API keys

import json
import secrets

# template
SECRETS = {
    'DJANGO_SECRET_KEY': '{{ DJANGO_SECRET_KEY }}',
    'ADMIN_URL': '{{ ADMIN_URL }}',
    'AWS_ACCESS_KEYID': None,
    'AWS_SECRET_ACCESS_KEY': None,
    'DISCOURSE_API_KEY': None,
    'DISCOURSE_API_USERNAME': None,
    'MEETUP': {
        'ACCESS_TOKEN': None,
        'CLIENT_ID': None,
        'CLIENT_SECRET': None
    },
    'SLACK': {
        'API_TOKEN': None
    }
}

print('Generating DJANGO_SECRET_KEY ...')
SECRETS['DJANGO_SECRET_KEY'] = secrets.token_urlsafe(50)

print('Generating ADMIN_URL ...')
SECRETS['ADMIN_URL'] = secrets.token_urlsafe(20)

print('Saving config.json ...')
with open('config.json', 'w') as outfile:
    json.dump(SECRETS, outfile, indent=4)

print('✅Setup complete!')
print('Test your local server by running "python manage.py runserver 0.0.0.0:8000"')
