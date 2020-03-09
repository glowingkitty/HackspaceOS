from _setup.config import Config


class MeetupSTRlocation():
    def __init__(self, event):
        HACKERSPACE_NAME = Config('BASICS.NAME').value
        HACKERSPACE_ADDRESS = Config('PHYSICAL_SPACE.ADDRESS').value
        str_location_name = event['venue']['name'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_NAME
        str_location_street = event['venue']['address_1'] if 'venue' in event and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['STREET']
        str_location_zip = event['venue']['zip'] if 'venue' in event and 'zip' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['ZIP']
        str_location_city = event['venue']['city'] if 'venue' in event and 'city' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['CITY']
        str_location_countrycode = event['venue']['country'].upper() if 'venue' in event and 'country' in event['venue'] and event['venue']['name'] and event[
            'venue']['name'] != HACKERSPACE_NAME else HACKERSPACE_ADDRESS['COUNTRYCODE']
        self.value = str_location_name+'\n'+str_location_street+'\n' + \
            str_location_zip+', '+str_location_city+', '+str_location_countrycode
