import json
import secrets
from asci_art import show_messages, set_secrets

later_then_secrets = 'Guess later then... Open your secrets.json at any time to make changes.'

# template
file_path = 'hackerspace/Website/templates/secrets_template.json'
with open(file_path) as json_file:
    SECRETS = json.load(json_file)

SECRETS['DJANGO']['SECRET_KEY'] = secrets.token_urlsafe(50)
SECRETS['DJANGO']['ADMIN_URL'] = secrets.token_urlsafe(20),

show_messages([
    'Welcome to your new hackerspace website! Let\'s setup the website.',
    'The first step: your secrets (API keys, etc.)',
    'Starting with: AWS (needed to enable users to upload event images when they create a new event via your new website)'
])

SECRETS = set_secrets(SECRETS, later_then_secrets, 'AWS')

show_messages([
    'Does your hackerspace use Discourse? It\'s a great forum software used by many hackerspaces & other communities.',
    'Let\'s setup your Discourse secrets, so we can automatically post new user generated events from your website to your Discourse page.',
])

SECRETS = set_secrets(SECRETS, later_then_secrets, 'Discourse')


show_messages([
    'Does your hackerspace have a Meetup group? Meetup.com is super useful to make more people aware of your events!',
    'Let\'s setup your Meetup secrets, so we can automatically post new user generated events from your website to your Meetup group.',
])

SECRETS = set_secrets(SECRETS, later_then_secrets, 'Meetup')


show_messages([
    'Does your hackerspace use Slack? Slack is both useful for chats within the community - but also for notifications from automated scripts.',
    'Let\'s setup your Slack API_TOKEN, so we can automatically inform you if a visitor created an event. So people in your community have the chance to reject the event and prevent it from automatically getting posted.',
])

SECRETS = set_secrets(SECRETS, later_then_secrets, 'Slack')

with open('secrets.json', 'w') as outfile:
    json.dump(SECRETS, outfile, indent=4)

show_messages([
    '✅ Yeahh we are done! I saved your secrets in the secrets.json file in the main directory. So you can easily change them any time.',
])
