from django.db import models
from log import log
from config import Config


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

    def import_all_from_wiki(self, WIKI_API_URL=Config('BASICS.WIKI.API_URL').value, test=False):
        import requests

        if not WIKI_API_URL:
            log('--> BASICS.WIKI.API_URL not found in config.json -> BASICS - Please add your WIKI_API_URL first.')
            return

        response_json = requests.get(WIKI_API_URL +
                                     '?action=query&list=categorymembers&cmtitle=Category:Meeting_Notes&cmlimit=500&format=json').json()

        all_wiki_pages = [
            x['title'] for x in response_json['query']['categorymembers'] if 'Meeting Notes 20' in x['title']]

        if test:
            all_wiki_pages = all_wiki_pages[:4]
        else:
            while 'continue' in response_json and 'cmcontinue' in response_json['continue']:
                response_json = requests.get(WIKI_API_URL +
                                             '?action=query&list=categorymembers&cmcontinue='+response_json['continue']['cmcontinue']+'&cmtitle=Category:Meeting_Notes&cmlimit=500&format=json').json()

                all_wiki_pages += [
                    x['title'] for x in response_json['query']['categorymembers'] if 'Meeting Notes 20' in x['title']]

        for meeting in all_wiki_pages:
            MeetingNote().import_from_wiki(meeting, WIKI_API_URL)

        print('Imported all meeting notes from wiki')

    def LIST__search_results(self):
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
        from datetime import datetime
        from config import Config

        local_timezone = pytz.timezone(
            Config('PHYSICAL_SPACE.TIMEZONE_STRING').value)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_created, local_timezone)
        return local_time.date()

    @property
    def str_menu_heading(self):
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

    def openMeetingNotes(self, riseuppad_meeting_path=Config('MEETINGS.RISEUPPAD_MEETING_PATH').value):
        import time
        from _apis.models import Scraper

        browser = Scraper('https://pad.riseup.net/p/' + riseuppad_meeting_path,
                          scraper_type='selenium', auto_close_selenium=False).selenium
        time.sleep(5)
        browser.switch_to.frame(browser.find_element_by_name("ace_outer"))
        browser.switch_to.frame(browser.find_element_by_name("ace_inner"))
        return browser

    def start(self,
              riseuppad_meeting_path=Config(
                  'MEETINGS.RISEUPPAD_MEETING_PATH').value,
              hackspace_name=Config('BASICS.NAME').value,
              timezone=Config('PHYSICAL_SPACE.TIMEZONE_STRING').value
              ):
        print('Starting...')
        import os
        import sys
        import time
        from datetime import datetime
        import pytz
        from config import Config
        from django.template.loader import get_template

        browser = self.openMeetingNotes(
            riseuppad_meeting_path=riseuppad_meeting_path)

        # copy template for new meeting into riseup pad
        meeting_template = get_template(os.path.join(
            sys.path[0], '_database/templates/meeting_notes.txt')).render({
                'MeetingNumber': MeetingNote.objects.count()+1,
                'HackspaceName': hackspace_name,
                'Date': str(
                    datetime.now(pytz.timezone(timezone)).date())
            })

        input_field = browser.find_element_by_id('innerdocbody')
        input_field.clear()
        input_field.send_keys(meeting_template)

        print('Done: https://pad.riseup.net/p/' + riseuppad_meeting_path)
        browser.close()

    def end(self, riseuppad_meeting_path=Config('MEETINGS.RISEUPPAD_MEETING_PATH').value):
        # save meeting notes
        browser = self.openMeetingNotes(
            riseuppad_meeting_path=riseuppad_meeting_path)
        self.text_notes = browser.find_element_by_id('innerdocbody').text
        self.save()
        browser.close()

        # to do: auto notify via slack
        print('Done: Ended & saved meeting')

    def STR__get_keywords(self):
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
        from config import Config

        try:
            # find main topics via heading in note template
            main_topics = re.findall('(?<==).*', open(os.path.join(
                sys.path[0], '_database/templates/meeting_notes__'+Config('BASICS.NAME').value+'.txt'), 'r').read())
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
        except:
            return ''

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
        if self.text_date:
            return self.text_date
        else:
            return 'New MeetingNote'

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
            sys.path[0], '_database/meeting_notes/'+self.text_date+'.txt'), 'r').read()
        self.updateCreatedBasedOnName()
        self.save()

    def import_from_wiki(self, page, wiki_api_url=Config('BASICS.WIKI.API_URL').value):
        import requests

        if not wiki_api_url:
            log('--> BASICS.WIKI.API_URL not found in config.json -> BASICS - Please add your WIKI_API_URL first.')
            return

        self.text_date = page.split('Notes ')[1].replace(' ', '-')

        # see if notes already exist, else, create
        if MeetingNote.objects.filter(text_date=self.text_date).exists() == False:
            # remove all links
            from bs4 import BeautifulSoup

            response_json = requests.get(
                wiki_api_url+'?action=parse&page='+page+'&format=json').json()['parse']
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
        from _database.models import Helper

        self = Helper().RESULT__updateTime(self)
        if not self.text_date:
            self.text_date = str(self.date)

        super(MeetingNote, self).save(*args, **kwargs)

        if not self.text_main_topics:
            self.text_main_topics = self.get_main_topics()

        if self.text_notes and not self.text_keywords:
            self.text_keywords = self.STR__get_keywords()
        else:
            self.start()

        super(MeetingNote, self).save(*args, **kwargs)
