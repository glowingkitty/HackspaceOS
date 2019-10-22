import calendar
import pytz

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
    'COUNTRYCODE': 'US'
}

# if your hackerspace has official opening hours, define them here as a json
HACKERSPACE_TIMEZONE = pytz.timezone('America/Los_Angeles')
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
