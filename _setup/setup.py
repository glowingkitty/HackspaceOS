
from _setup.asci_art import show_message, show_messages
import requests
from _apis.models import *


def get_template(which):
    import json
    file_path = '_database/templates/'+which+'_template.json'
    with open(file_path) as json_file:
        template = json.load(json_file)
    return template


def create_folder(folder_path):
    import os

    # You should change 'test' to your preferred folder.
    MYDIR = (folder_path)
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)


def copy_file_to_backup(file_path, folder_name):
    try:
        from shutil import copyfile
        copyfile(file_path, 'setup_backup/' +
                 folder_name+'/'+file_path.split('/')[-1])
    except:
        pass


def copy_file_from_backup(file_path, folder_name):
    try:
        from shutil import copyfile
        copyfile('setup_backup/' +
                 folder_name+'/'+file_path.split('/')[-1], file_path)
    except:
        pass


def get_size(file_path):
    import os
    return str(round(os.path.getsize(file_path)/1000000, 1))+' MB'


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


class Setup():
    def __init__(self, name=None):
        self.name = name
        self.backup_files = [
            'config.json',
            'secrets.json',
            'db.sqlite3',
            '_website/static/images/logo.svg',
            '_website/static/images/header_logo.jpg',
            '_website/static/images/header_banner.jpg',
            '_website/static/images/favicons/favicon.ico',
            '_website/static/images/favicons/favicon-32x32.png',
            '_website/static/images/favicons/favicon-16x16.png',
            '_website/static/images/favicons/apple-touch-icon.png',
        ]
        self.config = get_template('config')
        self.secrets = get_template('secrets')

    @property
    def boolean_files_exist(self):
        from os import path
        for file_path in self.backup_files:
            file_exist = path.exists(file_path)
            if file_exist == True:
                return file_exist
        else:
            return False

    def _menu(self):
        import os
        options = ['Create a new website']
        options_string = '1 - Create a new website'
        counter = 1

        # build options string

        # if any file in self.backup_files exist, show "export setup" and "delete current setup"
        if self.boolean_files_exist == True:
            counter += 1
            new_option = 'Export current setup'
            options.append(new_option)
            options_string += ', '+str(counter)+' - '+new_option

            counter += 1
            new_option = 'Delete current setup'
            options.append(new_option)
            options_string += ', '+str(counter)+' - '+new_option

        # if any folders in "backup" folder, show "import backup"
        folders = os.listdir()
        folder_options = ''
        backups_counter = 1
        for file_name in folders:
            if 'setup_backup__' in file_name:
                backups_counter += 1

        if backups_counter > 1:
            counter += 1
            new_option = 'Import backup'
            options.append(new_option)
            options_string += ', '+str(counter)+' - '+new_option

        # if only "Create a new website" as an option, auto proceed with that
        if counter == 1:
            self._new()
        else:
            show_message(
                'Welcome! How can I help you? (enter a number) '+options_string)
            selection_processedd = False
            while selection_processedd == False:
                # try:
                selection = input()
                selector_number = int(selection)-1
                if options[selector_number] == 'Create a new website':
                    self._new()
                    selection_processedd = True
                elif options[selector_number] == 'Export current setup':
                    self._export()
                    selection_processedd = True
                elif options[selector_number] == 'Delete current setup':
                    self._delete()
                    selection_processedd = True
                elif options[selector_number] == 'Import backup':
                    self._import()
                    selection_processedd = True
                else:
                    show_message(
                        'ERROR: That option doesn\'t exist. How can I help you? (enter a number) '+options_string)
                # except KeyboardInterrupt:
                #     exit()
                # except:
                #     show_message(
                #         'ERROR: That option doesn\'t exist. How can I help you? (enter a number) '+options_string)

    def _new(self):
        import secrets
        import json
        from _setup.asci_art import show_messages, set_secret, set_secrets, show_message
        from googletrans import Translator
        translator = Translator()

        show_messages([
            'Let\'s setup your new hackerspace website!'
        ])

        # then setup config.json
        later_then_config = 'Guess later then... Open your config.json at any time to make changes.'

        show_message('First: What is the name of your hackerspace?')
        self.name = input()
        if self.name:
            self.config['BASICS']['NAME'] = self.name
            show_message(
                'Ok, great! Give me a seconds, so I can try to setup your RISEUPPAD_MEETING_PATH, and MEETUP_GROUP as well...')

            # if hackerspace name saved, also save other config defaults based on name
            self.config['MEETINGS']['RISEUPPAD_MEETING_PATH'] = self.name.lower() + \
                '-meetings'

        self.config = set_secret(self.config, later_then_config,
                                 'Ok, great. And in what city is your hackerspace? (Just the city name itself)', 'PHYSICAL_SPACE', 'ADDRESS', 'CITY')
        if self.config['PHYSICAL_SPACE']['ADDRESS']['CITY']:
            self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['english'][0] = self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['english'][0].replace(
                '{{ CITY }}', self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'])
            self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['hebrew'][0] = self.config['BASICS']['HACKERSPACE_IS_SENTENCES']['hebrew'][0].replace(
                '{{ CITY }}', translator.translate(
                    text=self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'],
                    dest='he').text)

        self.config = set_secret(self.config, later_then_config,
                                 'Enter your hackerspace street & house number.', 'PHYSICAL_SPACE', 'ADDRESS', 'STREET')
        self.config = set_secret(self.config, later_then_config,
                                 'Enter your hackerspace ZIP code.', 'PHYSICAL_SPACE', 'ADDRESS', 'ZIP')
        self.config = set_secret(self.config, later_then_config,
                                 'Enter your hackerspace state. (California for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'STATE')
        self.config = set_secret(self.config, later_then_config,
                                 'Enter your hackerspace country code (US or DE for example)', 'PHYSICAL_SPACE', 'ADDRESS', 'COUNTRYCODE')
        self.config = set_secret(self.config, later_then_config,
                                 'Anything else people have to know to find your hackerspace?', 'PHYSICAL_SPACE', 'ADDRESS', 'HOW_TO_FIND_US__english')
        self.config = set_secret(self.config, later_then_config,
                                 'Please enter the URL of your embedded map, to show people where your hackerspace is. My suggestion: go to https://www.google.com/maps - select your hackerspace, press the "Share" button -> "Embed a map" and enter here the "scr" URL of the iframe code.', 'BASICS', 'EMBEDDED_MAP_URL')

        # save lat/lon based on address
        if self.config['PHYSICAL_SPACE']['ADDRESS']['STREET'] and self.config['PHYSICAL_SPACE']['ADDRESS']['CITY']:
            show_message(
                'Ok, great! Give me a seconds, so I can try to find and save the matching LAT_LON and TIMEZONE_STRING as well...')
            location, lat, lon = get_lat_lon_and_location(
                self.config['PHYSICAL_SPACE']['ADDRESS']['STREET']+', ' +
                self.config['PHYSICAL_SPACE']['ADDRESS']['CITY'] +
                (', '+self.config['PHYSICAL_SPACE']['ADDRESS']['STATE'] if self.config['PHYSICAL_SPACE']['ADDRESS']['STATE'] else '') +
                (', '+self.config['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE']
                    if self.config['PHYSICAL_SPACE']['ADDRESS']['COUNTRYCODE'] else '')
            )
            if lat != None:
                self.config['PHYSICAL_SPACE']['LAT_LON'] = [lat, lon]

                # also save timezone string based on lat/lon
                self.config['PHYSICAL_SPACE']['TIMEZONE_STRING'] = STR__get_timezone_from_lat_lon(
                    lat, lon)
                show_message('It worked!')

        self.config = set_secret(self.config, later_then_config,
                                 'What #hashtag do people use when they talk online about your hackerspace on Twitter or Instagram? (Example: #noisebridge)', 'SOCIAL', 'HASHTAG')
        self.config = set_secret(self.config, later_then_config,
                                 'Do you have a donation page, where people can donate money online? If yes, please enter the url. (or press Enter to skip)', 'BASICS', 'DONATION_URLs', 'MONEY')
        self.config = set_secret(self.config, later_then_config,
                                 'Where is your hackerspace GIT repo hosted? So others can suggest changes to your code. (please enter the full URL)', 'WEBSITE', 'WEBSITE_GIT')
        self.config = set_secret(self.config, later_then_config,
                                 'What domain will you use for your new hackerspace website? (Just the domain. Example: "noisebridge.net")', 'WEBSITE', 'DOMAIN')

        show_message('One second...')
        # auto generate the event footer for discourse and meetup
        if self.config['WEBSITE']['DOMAIN'] and self.config['BASICS']['NAME']:
            self.config['EVENTS']['DISCOURSE_AND_MEETUP_EVENT_FOOTER_HTML'] =\
                '<br>------------------<br>'\
                '<br>'+self.config['BASICS']['NAME']+' is funded by YOUR donations. '\
                'So if you want to support '+self.config['BASICS']['NAME']+' - donations are always welcomed - '\
                'money, hardware or time (by organizing or volunteering an event). '\
                'Visit https://' + \
                self.config['WEBSITE']['DOMAIN']+' for more details.'

        self.config = set_secret(self.config, later_then_config,
                                 'And the last question: What should be your website\'s primary color (for buttons for example). Recommended: a color in your hackerspace logo?', 'CSS', 'PRIMARY_COLOR')

        # then setup secrets.json
        later_then_secrets = 'Guess later then... Open your secrets.json at any time to make changes.'

        self.secrets['DJANGO']['SECRET_KEY'] = secrets.token_urlsafe(50)
        self.secrets['DJANGO']['ADMIN_URL'] = secrets.token_urlsafe(20)

        with open('config.json', 'w') as outfile:
            json.dump(self.config, outfile, indent=4)

        with open('secrets.json', 'w') as outfile:
            json.dump(self.secrets, outfile, indent=4)

        show_messages([
            'Awesome! Let\'s complete the setup by saving your secrets (API keys, etc.)'
        ])

        apis = (Search, Meetup, Notify, Flickr, GooglePhotos, Instagram, Aws)
        for api in apis:
            if not api().setup_done:
                api().setup()

        show_messages([
            '✅ Yeahh we are done! I saved your config.json and secrets.json files in the main directory. So you can easily change them any time.',
        ])

    def _export(self):
        if self.name:
            folder_name = self.name
        else:
            show_messages([
                'Hello! It seems you want to export your current settings? (your config.json, secrets.json and important images)'
            ])

            show_message(
                'If that\'s the case, enter now a name for the exported folder. (or press Enter to exit)')

            folder_name = input()

        if not folder_name:
            show_message('Ok, got it. Maybe another time.')
            exit()
        else:
            from zipfile import ZipFile, ZIP_DEFLATED

            # copy files into folder
            with ZipFile('setup_backup__'+folder_name+'.zip', 'w', ZIP_DEFLATED) as zip:
                # writing each file one by one
                for file in self.backup_files:
                    try:
                        zip.write(file)
                    except:
                        pass

                show_message('✅Done! Exported "'+folder_name +
                             '" ('+get_size('setup_backup__'+folder_name+'.zip')+')')

    def _import(self):
        import os

        folders = os.listdir()
        folder_options = ''
        counter = 1
        backups = []
        for file_name in folders:
            if 'setup_backup__' in file_name:
                backups.append(file_name)
                if counter > 1:
                    folder_options += ', '
                folder_options += str(counter)+' - ' + \
                    file_name.split('setup_backup__')[1].split('.zip')[0]
                counter += 1

        if counter == 1:
            show_message('No backups found.')
        else:
            show_message(
                'Which setup would you like to import? '+folder_options)
            selected_folder = input()

            # test if folder exist
            try:
                from zipfile import ZipFile

                selected_num = int(selected_folder)-1
                folder_name = backups[selected_num]

                # first delete existing files
                for file_path in self.backup_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)

                # copy files into folder
                with ZipFile(folder_name, 'r') as zip:
                    # extracting all the files
                    zip.extractall()

                show_message('✅Done! Imported "'+folder_name.split('setup_backup__')
                             [1].split('.zip')[0] + '" ('+get_size(folder_name)+')')

            except:
                show_message(
                    'ERROR: The folder doesnt exist. Please enter a correct number.')

    def _delete(self):
        import os
        show_message(
            'WARNING: Are you sure you want to delete your current setup? This will delete the config.json, secrets.json and your logos & favicons. Enter "delete" to delete the current setup.')
        confirm = input()
        if confirm == 'delete':
            for file_path in self.backup_files:
                if os.path.exists(file_path):
                    os.remove(file_path)

            show_message('✅Done! I deleted the current setup.')

        else:
            show_message('Ok. I won\'t delete anything.')


Setup()._menu()
