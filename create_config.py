import json
import secrets

# Init a config.py file with a random Djanog secret, Admin URL and placeholders for API keys

# template
SECRETS = {
    'DJANGO_SECRET_KEY': secrets.token_urlsafe(50),
    'ADMIN_URL': secrets.token_urlsafe(20),
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

print('Saving config.json ...')
with open('config.json', 'w') as outfile:
    json.dump(SECRETS, outfile, indent=4)

print('✅Saved config.json!')
