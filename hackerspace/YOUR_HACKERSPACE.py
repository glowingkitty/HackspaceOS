import calendar

"""
Welcome to the new website of your local hackerspace. Powered by you! (and everyone who contributed to our git repo)
"""

HACKERSPACE_NAME = 'Noisebridge'

# The following sentences are used on the landingpage header, to describe your hackerspace.
HACKERSPACE_IS_SENTENCES = [
    'is a <a class="highlight_text_red" target="_blank" href="https://en.wikipedia.org/wiki/Hackerspace">hackerspace</a> in San Francisco',
    'is a community',
    'is a maker & learning space',
    'is a <a class="highlight_text_red" target="_blank" href="https://www.noisebridge.net/wiki/Do-ocracy">do-ocracy</a>',
    'is what you make out of it'
]

HACKERSPACE_ADDRESS = {
    'STREET': '2169 Mission St',
    'ZIP': '94110',
    'CITY': 'San Francisco',
    'STATE': 'CA',
    'COUNTRYCODE': 'US',
    'EXTRA_INFO': '(entrence left next to the supermarket)'
}

# list your social network channels (name in small letters please and check that the CSS classes exist in footer.css)
# Recommended: max 5 (only show the most relevant networks)
HACKERSPACE_SOCIAL_NETWORKS = [
    {'name': 'GitHub', 'url': 'https://github.com/noisebridge'},
    {'name': 'Patreon', 'url': 'https://patreon.com/Noisebridge'},
    {'name': 'YouTube', 'url': 'https://www.youtube.com/user/noisebridge'},
    {'name': 'Instagram', 'url': 'https://www.instagram.com/noisebridgehackerspace/'},
    {'name': 'Facebook', 'url': 'https://www.facebook.com/noisebridge'},
    {'name': 'Twitter', 'url': 'https://www.twitter.com/noisebridge'},
    {'name': 'Twitch', 'url': 'https://www.twitch.tv/noisebridge'},
    {'name': 'Mailinglists', 'url': 'https://lists.noisebridge.net/listinfo'},
    {'name': 'Flickr', 'url': 'https://www.flickr.com/groups/noisebridge'},
    {'name': 'Foursquare',
        'url': 'https://foursquare.com/v/noisebridge/4a8b745ff964a5207e0c20e3'},
    {'name': 'Meetup', 'url': 'https://www.meetup.com/noisebridge/'},
    {'name': 'IRC', 'url': 'irc://chat.freenode.net/#noisebridge'},
    {'name': 'Blog', 'url': 'https://blog.noisebridge.net/'},
]

HACKERSPACE_TIMEZONE_STRING = 'America/Los_Angeles'

# https://pad.riseup.net/p/{{PATH}}
RISEUPPAD_MEETING_PATH = 'nbmeeting'
DOMAIN = 'noisebridge.net'

WEBSITE_GIT = 'https://github.com/marcoEDU/HackerspaceTemplatePackage/tree/master/hackerspace'
WEBSITE_GIT_PROVIDER = 'GitHub'
EDIT_CONTENT_LINK = 'https://app.slack.com/client/T027UKEC9/C02A1V2PY'
EDIT_CONTENT_INFO = 'ask on the #rack channel in Slack for access to the website database'

# https://www.meetup.com/{{HACKERSPACE_MEETUP_GROUP}}/
HACKERSPACE_MEETUP_GROUP = 'noisebridge'
EXTRA_MEETUP_GROUPS = ['Free-Code-Camp-SF', 'StartupSchool-SF']

# how do you want to call people coming to your hackerspace?
HACKERSPACE_PEOPLE_NAME = 'Noisebutts'

HACKERSPACE_DISCOURSE_URL = 'https://discuss.noisebridge.info/'
HACKERSPACE_INTERNAL_COMMUNICATION_PLATFORMS = [
    {'name': 'Discuss', 'url': HACKERSPACE_DISCOURSE_URL},
]

WIKI_API_URL = 'https://www.noisebridge.net/api.php'

# if your hackerspace has official opening hours, define them here as a json
HACKERSPACE_OPENING_HOURS_SUMMARY = 'Mon-Sun, 11AM -  10PM'
HACKERSPACE_OPENING_HOURS = {}
days_num = 0
while days_num < 7:
    HACKERSPACE_OPENING_HOURS[calendar.day_name[days_num]] = [
        # (24 hour clock) example: 11:00 to 22:00
        # enter the hours & minutes when the status starts to change to a new status
        # HH, MM, Status, ColorIndicator
        (0, 0, 'Probably open', 'grey'),
        (2, 0, 'Probably closed', 'orange'),
        (9, 0, 'Probably open', 'grey'),
        (11, 0, 'Open now', 'green'),
        (22, 0, 'Probably open', 'grey')
    ]
    days_num += 1

HACKERSPACE_IS_OPEN_BASED_ON_OPENING_HOURS = True
# If you don't want the "Open now" info on the landingpage be
# dependend on the opening hours, use the following line to call a function to see if the space is open (return True) or closed (return False)
HACKERSPACE_IS_OPEN_CUSTOM_CHECK = None

DONATION_URLs = {
    'MONEY': 'https://donate.noisebridge.net/',
    'HARDWARE': 'https://www.noisebridge.net/Donations',
    'ORGANIZE_EVENT': 'https://www.meetup.com/noisebridge/',
    'VOLUNTEER': 'https://www.meetup.com/noisebridge/',
}

EMBEDDED_MAP_URL = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3154.178154041456!2d-122.42143928490898!3d37.762420679761654!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x808f7e23baa2b1df%3A0x81b913a252fb8d04!2sNoisebridge!5e0!3m2!1sen!2sus!4v1572324947963!5m2!1sen!2sus'

IMPORTANT_URLS = {
    'AUTO_CREATE_NEW_MEETING': WEBSITE_GIT,
    'END_MEETING': WEBSITE_GIT+'/models/meetingnotes.py#L132',
    'MEETING_TEMPLATE': WEBSITE_GIT+'/Website/templates/meeting_notes.txt'
}

SAYHELLO = 'Greetings by the person at the computer next to the entrance. Hello fellow ' + \
    HACKERSPACE_PEOPLE_NAME+'. Be excellent to each other and have an excellent day'

EVENTS_SPACE_DEFAULT = 'Hackatorium'
EVENTS_SPACES_OVERWRITE = {
    'Whiteboarding & Algorithms Workshop': 'Church',
    'Noisebridge Python Class': 'Church',
    'Gamebridge Unityversity': 'Church',
    'Queer Game Developers Meetup': 'Church',
    'Laser Cutter Safety Training': 'SparkleForge',
}

# overwrite event hosts with their Discuss user names!
EVENTS_HOSTS_OVERWRITE = {
    'Free Code Camp': ['tymeart'],
    'Noisebridge Sewing Project Night': ['tymeart'],
    'Laser Cutter Safety Training': ['ruthgrace'],
    'Noisebridge Extended Tour': ['pyconaut'],
    'Whiteboarding & Algorithms Workshop - Weekend Edition': ['Bernice'],
    'Circuit Hacking Mondays': ['spacegreens'],
    'BUIDL Night': ['kinnard'],
    'Startup School SF Meetup': ['kinnard'],
    'Gamebridge Unityversity C# Unity Game Dev - Art And Etcetera': ['Bernice', 'Mark'],
    'Gamebridge Unityversity Unity C# Game Development': ['Mark'],
    'Noisebridge Python Class': ['Jared'],
}
