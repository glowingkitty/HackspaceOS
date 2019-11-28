import calendar

HACKERSPACE_ADDRESS = {
    'STREET': '2169 Mission St',
    'ZIP': '94110',
    'CITY': 'San Francisco',
    'STATE': 'CA',
    'COUNTRYCODE': 'US',
    'EXTRA_INFO': '(entrence left next to the supermarket)'
}

ADDRESS_STRING = 'Noisebridge<br>' + \
    HACKERSPACE_ADDRESS['STREET']+'<br' + \
    HACKERSPACE_ADDRESS['ZIP']+', '+HACKERSPACE_ADDRESS['CITY'] + \
    ', '+HACKERSPACE_ADDRESS['STATE']+', '+HACKERSPACE_ADDRESS['COUNTRYCODE']

HOW_TO_FIND_US = 'Entrence next to the supermarket, all the way up.'

LAT_LON = (37.762389, -122.4191587)

HACKERSPACE_TIMEZONE_STRING = 'America/Los_Angeles'


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

# how do you want to call people coming to your hackerspace?
HACKERSPACE_PEOPLE_NAME = 'Noisebutts'
