
import json
from asci_art import show_messages, set_secret, show_message
import requests

later_then_config = 'Guess later then... Open your config.json at any time to make changes.'

# local copy of functions in events.py - otherwise Django would have to be loaded without config - what causes errors


def get_lat_lon_and_location(str_location):
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut

    geolocator = Nominatim(user_agent='hackerspace_template_creator')
    str_location = str_location.replace('\n', ', ')
    float_lat = None
    float_lon = None
    while float_lat == None and len(str_location) > 0:
        try:
            location = geolocator.geocode(str_location)

            float_lat, float_lon = location.latitude, location.longitude
        except GeocoderTimedOut:
            print('GeocoderTimedOut! This might be solved by turning off your VPN.')
            break
        except:
            str_location = ','.join(str_location.split(',')[:-1])

    return str_location, float_lat, float_lon


def STR__get_timezone_from_lat_lon(lat, lon):
    import requests
    url = "https://api.teleport.org/api/locations/" + \
        str(lat)+","+str(lon) + \
        "/?embed=location:nearest-cities/location:nearest-city/"
    response = requests.get(url).json()
    try:
        return response['_embedded']['location:nearest-cities'][0]['_embedded']['location:nearest-city']['_links']['city:timezone']['name']
    except:
        return None


# template
file_path = 'hackerspace/Website/templates/config_template.json'
with open(file_path) as json_file:
    CONFIG = json.load(json_file)

show_messages([
    'Let\'s setup your website!'
])

# ask questions for setup
CONFIG = set_secret(CONFIG, later_then_config,
                    'First: What is the name of your hackerspace?', 'BASICS', 'NAME')

if CONFIG['BASICS']['NAME']:
    show_message(
        'Ok, great! Give me a seconds, so I can try to setup your RISEUPPAD_MEETING_PATH, and MEETUP_GROUP as well...')

    # if hackerspace name saved, also save other config defaults based on name
    CONFIG['MEETINGS']['RISEUPPAD_MEETING_PATH'] = CONFIG['BASICS']['NAME'].lower() + \
        '-meetings'
    if requests.get('https://www.meetup.com/'+CONFIG['BASICS']['NAME'].lower()).status_code == 200:
        CONFIG['EVENTS']['MEETUP_GROUP'] = CONFIG['BASICS']['NAME'].lower()

CONFIG = set_secret(CONFIG, later_then_config,
                    'Ok, great. And in what city is your hackerspace? (Just the city name itself)', 'PHYSICAL_SPACE', 'ADDRESS', 'CITY')
if CONFIG['PHYSICAL_SPACE']['ADDRESS']['CITY']:
    CONFIG['BASICS']['HACKERSPACE_IS_SENTENCES'][0] = CONFIG['BASICS']['HACKERSPACE_IS_SENTENCES'][0].replace(
        '{{ CITY }}', CONFIG['PHYSICAL_SPACE']['ADDRESS']['CITY'])


CONFIG = set_secret(CONFIG, later_then_config,
                    'Enter your hackerspace street & house number.', 'PHYSICAL_SPACE', 'ADDRESS', 'STREET')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Enter your hackerspace ZIP code.', 'PHYSICAL_SPACE', 'ADDRESS', 'ZIP')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Enter your hackerspace state. (California for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'STATE')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Enter your hackerspace country code (US or DE for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'COUNTRYCODE')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Anything else people have to know to find your hackerspace?', 'PHYSICAL_SPACE', 'ADDRESS', 'HOW_TO_FIND_US')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Please enter the URL of your embedded map, to show people where your hackerspace is. My suggestion: go to https://www.google.com/maps - select your hackerspace, press the "Share" button -> "Embed a map" and enter here the "scr" URL of the iframe code.', 'BASICS', 'EMBEDDED_MAP_URL')

# save lat/lon based on address
if CONFIG['PHYSICAL_SPACE']['ADDRESS']['STREET'] and CONFIG['PHYSICAL_SPACE']['ADDRESS']['CITY']:
    show_message(
        'Ok, great! Give me a seconds, so I can try to find and save the matching LAT_LON and TIMEZONE_STRING as well...')
    location, lat, lon = get_lat_lon_and_location(
        CONFIG['PHYSICAL_SPACE']['ADDRESS']['STREET']+', ' +
        CONFIG['PHYSICAL_SPACE']['ADDRESS']['CITY'] +
        (', '+CONFIG['PHYSICAL_SPACE']['ADDRESS']['STATE'] if CONFIG['PHYSICAL_SPACE']['ADDRESS']['STATE'] else '') +
        (', '+CONFIG['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE']
            if CONFIG['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE'] else '')
    )
    if lat != None:
        CONFIG['PHYSICAL_SPACE']['LAT_LON'] = [lat, lon]

        # also save timezone string based on lat/lon
        CONFIG['PHYSICAL_SPACE']['TIMEZONE_STRING'] = STR__get_timezone_from_lat_lon(
            lat, lon)
        show_message('It worked!')

CONFIG = set_secret(CONFIG, later_then_config,
                    'What #hashtag do people use when they talk online about your hackerspace on Twitter or Instagram? (Example: #noisebridge)', 'SOCIAL', 'HASHTAG')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Do you have a donation page, where people can donate money online? If yes, please enter the url. (or press Enter to skip)', 'BASICS', 'DONATION_URLs', 'MONEY')
CONFIG = set_secret(CONFIG, later_then_config,
                    'Where is your hackerspace GIT repo hosted? So others can suggest changes to your code. (please enter the full URL)', 'WEBSITE', 'WEBSITE_GIT')
CONFIG = set_secret(CONFIG, later_then_config,
                    'What domain will you use for your new hackerspace website? (Just the domain. Example: "noisebridge.net")', 'WEBSITE', 'DOMAIN')
# try to auto find the wiki api url, else ask for it
show_message('One second...')
if CONFIG['WEBSITE']['DOMAIN'] and requests.get('https://'+CONFIG['WEBSITE']['DOMAIN']+'/api.php').status_code == 200:
    CONFIG['BASICS']['WIKI']['API_URL'] = 'https://' + \
        CONFIG['WEBSITE']['DOMAIN']+'/api.php'
else:
    CONFIG = set_secret(CONFIG, later_then_config,
                        'Do you have a wiki? What is the API URL?', 'BASICS', 'WIKI', 'API_URL')
CONFIG = set_secret(CONFIG, later_then_config,
                    'And the last question: What should be your website\'s primary color (for buttons for example). Recommended: a color in your hackerspace logo?', 'CSS', 'PRIMARY_COLOR')

with open('config.json', 'w') as outfile:
    json.dump(CONFIG, outfile, indent=4)

show_messages([
    '✅ Yeahh we are done! I saved your config in the config.json file in the main directory. So you can easily change them any time.',
])
