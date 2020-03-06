from _setup.asci_art import show_message


class SetupNewLatLonTimezone():
    def __init__(self, config):
        self.config = config

        # save lat/lon based on address
        if self.config['PHYSICAL_SPACE']['ADDRESS']['STREET'] and self.config['PHYSICAL_SPACE']['ADDRESS']['CITY']:
            show_message(
                'Ok, great! Give me a seconds, so I can try to find and save the matching LAT_LON and TIMEZONE_STRING as well...')
            location, lat, lon = self.get_lat_lon_and_location(
                self.config['PHYSICAL_SPACE']['ADDRESS']['STREET']+', ' +
                self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'] +
                (', '+self.config['PHYSICAL_SPACE']['ADDRESS']['STATE'] if self.config['PHYSICAL_SPACE']['ADDRESS']['STATE'] else '') +
                (', '+self.config['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE']
                    if self.config['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE'] else '')
            )
            if lat != None:
                self.config['PHYSICAL_SPACE']['LAT_LON'] = [lat, lon]

                # also save timezone string based on lat/lon
                self.config['PHYSICAL_SPACE']['TIMEZONE_STRING'] = self.STR__get_timezone_from_lat_lon(
                    lat, lon)
                show_message('It worked!')

    def get_lat_lon_and_location(self, str_location):
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

    def STR__get_timezone_from_lat_lon(self, lat, lon):
        import requests
        url = "https://api.teleport.org/api/locations/" + \
            str(lat)+","+str(lon) + \
            "/?embed=location:nearest-cities/location:nearest-city/"
        response = requests.get(url).json()
        try:
            return response['_embedded']['location:nearest-cities'][0]['_embedded']['location:nearest-city']['_links']['city:timezone']['name']
        except:
            return None
