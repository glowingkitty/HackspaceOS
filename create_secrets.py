import json
import secrets

# template
SECRETS = {
    'DJANGO': {
        'SECRET_KEY': secrets.token_urlsafe(50),
        'ADMIN_URL': secrets.token_urlsafe(20),
    },
    'AWS': {
        'ACCESS_KEYID': None,
        'SECRET_ACCESS_KEY': None,
        'S3': {
            'BUCKET_NAME': None,
            'SERVER_AREA': None
        }
    },
    'DISCOURSE': {
        'API_KEY': None,
        'API_USERNAME': None,
    },
    'MEETUP': {
        'ACCESS_TOKEN': None,
        'CLIENT_ID': None,
        'CLIENT_SECRET': None
    },
    'SLACK': {
        'API_TOKEN': None
    }
}

print('Saving secrets.json ...')
with open('secrets.json', 'w') as outfile:
    json.dump(SECRETS, outfile, indent=4)

print('✅Saved secrets.json!')
