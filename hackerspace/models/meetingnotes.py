from django.db import models


def startChrome(headless, url):
    import os
    import sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    if headless == True:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    browser_path = os.path.join(
        sys.path[0], 'hackerspace/website/selenium/chromedriver_'+sys.platform)
    browser = webdriver.Chrome(
        chrome_options=options, executable_path=browser_path)
    browser.get(url)
    return browser


def openMeetingNotes():
    import time
    from hackerspace.YOUR_HACKERSPACE import RISEUPPAD_MEETING_PATH

    browser = startChrome(
        headless=True, url='https://pad.riseup.net/p/'+RISEUPPAD_MEETING_PATH)
    time.sleep(5)
    browser.switch_to_frame(0)
    browser.switch_to_frame(0)
    return browser


class MeetingNoteSet(models.QuerySet):
    def remove_empty_notes(self):
        self.filter(text_notes__isnull=True).delete()
        print('Deleted all empty notes')

    def current(self):
        return self.filter(text_notes__isnull=True).order_by('-int_UNIXtime_created').first()

    def past(self, older_then=None):
        if older_then:
            self = self.filter(
                text_notes__isnull=False,
                int_UNIXtime_created__lt=older_then.int_UNIXtime_created)
        return self.filter(text_notes__isnull=False).order_by('-int_UNIXtime_created')

    def import_all_from_wiki(self):
        import requests
        from hackerspace.YOUR_HACKERSPACE import WIKI_API_URL

        response_json = requests.get(WIKI_API_URL +
                                     '?action=query&list=categorymembers&cmtitle=Category:Meeting_Notes&cmlimit=500&format=json').json()

        all_wiki_pages = [
            x['title'] for x in response_json['query']['categorymembers'] if 'Meeting Notes 20' in x['title']]

        while 'continue' in response_json and 'cmcontinue' in response_json['continue']:
            response_json = requests.get(WIKI_API_URL +
                                         '?action=query&list=categorymembers&cmcontinue='+response_json['continue']['cmcontinue']+'&cmtitle=Category:Meeting_Notes&cmlimit=500&format=json').json()

            all_wiki_pages += [
                x['title'] for x in response_json['query']['categorymembers'] if 'Meeting Notes 20' in x['title']]

        for meeting in all_wiki_pages:
            MeetingNote().import_from_wiki(meeting)

        print('Imported all meeting notes from wiki')

    def search_results(self):
        results_list = []
        results = self.all()
        for result in results:
            results_list.append({
                'icon': 'meetingnote',
                'name': 'Meeting notes - '+str(result),
                'url': '/meeting/'+result.text_date,
                'menu_heading': 'menu_h_meetings'
            })
        return results_list


class MeetingNote(models.Model):
    objects = MeetingNoteSet.as_manager()
    text_date = models.TextField(blank=True, null=True)
    text_notes = models.TextField(blank=True, null=True)

    text_main_topics = models.TextField(blank=True, null=True)

    many_consensus_items = models.ManyToManyField(
        'Consensus', related_name="m_consensus_items", blank=True)

    text_keywords = models.TextField(blank=True, null=True)
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    @property
    def date(self):
        import pytz
        from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_TIMEZONE_STRING
        from datetime import datetime

        local_timezone = pytz.timezone(HACKERSPACE_TIMEZONE_STRING)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_created, local_timezone)
        return local_time.date()

    @property
    def menu_heading(self):
        return 'menu_h_meetings'

    @property
    def list_main_topics(self):
        return self.text_main_topics.split(',') if self.text_main_topics else None

    @property
    def running_since(self):
        import time

        # reduce 30 seconds, considering time it takes to create notes
        seconds_ago = time.time()-self.int_UNIXtime_created-30
        minutes = round(seconds_ago/60)
        hours = round(minutes/60) if minutes > 60 else 0
        if minutes > 60:
            minutes = minutes-(hours*60)
        return '{}h {}min'.format(hours, minutes)

    def start(self):
        print('Starting...')
        import os
        import sys
        import time
        from datetime import datetime
        import pytz
        from selenium.webdriver.common.keys import Keys
        from hackerspace.YOUR_HACKERSPACE import (
            HACKERSPACE_TIMEZONE_STRING, RISEUPPAD_MEETING_PATH)

        browser = openMeetingNotes()

        input_field = browser.find_element_by_id('innerdocbody')
        input_field.clear()

        # copy template for new meeting into riseup pad
        meeting_template = open(os.path.join(
            sys.path[0], 'hackerspace/website/templates/meeting_notes.txt'), 'r').read()
        for line in reversed(meeting_template.split('\n')):
            input_field.send_keys(Keys.RETURN)
            line = line.replace('{{ Date }}', str(
                datetime.now(pytz.timezone(HACKERSPACE_TIMEZONE_STRING)).date()))
            line = line.replace('{{ MeetingNumber }}', str(
                MeetingNote.objects.count()+1))
            time.sleep(0.3)
            input_field.send_keys(line)
        print('Done: https://pad.riseup.net/p/'+RISEUPPAD_MEETING_PATH)

    def end(self):
        # save meeting notes
        browser = openMeetingNotes()
        self.text_notes = browser.find_element_by_id('innerdocbody').text
        self.save()

        # to do: auto notify via slack
        print('Done: Ended & saved meeting')

    def get_keywords(self):
        import re

        keywords = re.findall('#(\w+)', self.text_notes)
        keywords = [
            x.replace('#', '')
            .replace('_', ' ')
            for x in keywords if
            x != 'summary'
        ]
        filtered = []
        for keyword in keywords:
            if keyword not in filtered:
                filtered.append(keyword)

        return ','.join(filtered)

    def get_main_topics(self):
        import os
        import sys
        import re

        # find main topics via heading in note template
        main_topics = re.findall('(?<==).*', open(os.path.join(
            sys.path[0], 'hackerspace/website/templates/meeting_notes.txt'), 'r').read())
        main_topics = [
            x.replace('==', '')
            .replace('= ', '')
            .replace(' =', '')
            .replace('=', '')
            .replace('[[', '')
            .replace(']]', '')
            .strip()
            for x in main_topics if
            x != ''
            and 'Meeting Summary' not in x
            and 'End of Meeting' not in x
            and 'Discussion Item' not in x
        ]

        return ','.join(main_topics)

    def add_keyword(self, keyword):
        if self.text_keywords and keyword != '':
            self.text_keywords += ','+keyword
        else:
            self.text_keywords = keyword
        super(MeetingNote, self).save()
        print('Saved keyword - '+keyword)

    def remove_keyword(self, keyword):
        if self.text_keywords and keyword != '':
            self.text_keywords = self.text_keywords.replace(
                ','+keyword, '').replace(keyword+',', '')
            super(MeetingNote, self).save()
            print('Removed keyword - '+keyword)

    def __str__(self):
        return self.text_date

    def updateCreatedBasedOnName(self):
        import time
        from datetime import datetime

        try:
            self.int_UNIXtime_created = int(time.mktime(
                datetime.strptime(self.text_date, "%Y-%m-%d").timetuple()))
            super(MeetingNote, self).save()
        except:
            print('Failed for '+self.text_date)

    def import_from_local(self):
        import os
        import sys

        self.text_notes = open(os.path.join(
            sys.path[0], 'hackerspace/meeting_notes/'+self.text_date+'.txt'), 'r').read()
        self.updateCreatedBasedOnName()
        self.save()

    def import_from_wiki(self, page):
        import requests
        from hackerspace.YOUR_HACKERSPACE import WIKI_API_URL

        self.text_date = page.split('Notes ')[1].replace(' ', '-')

        # see if notes already exist, else, create
        if MeetingNote.objects.filter(text_date=self.text_date).exists() == False:
            # remove all links
            from bs4 import BeautifulSoup
            response_json = requests.get(
                WIKI_API_URL+'?action=parse&page='+page+'&format=json').json()['parse']
            soup = BeautifulSoup(str(response_json['text']).replace(
                "{\'*\': \'", "").replace("'}", "").replace("\\n", "").replace("\\\'", "\'"), 'html.parser')
            for a in soup.findAll('a'):
                del a['href']
            self.text_notes = str(soup)
            self.updateCreatedBasedOnName()

            self.save()
            print('Imported from wiki - '+self.text_date)
        else:
            print('Skipped - Already exists. '+self.text_date)

    def save(self, *args, **kwargs):
        from hackerspace.models.events import updateTime

        self = updateTime(self)
        if not self.text_date:
            self.text_date = str(self.date)

        super(MeetingNote, self).save(*args, **kwargs)

        if not self.text_main_topics:
            self.text_main_topics = self.get_main_topics()

        if self.text_notes and not self.text_keywords:
            self.text_keywords = self.get_keywords()
        else:
            self.start()

        super(MeetingNote, self).save(*args, **kwargs)
