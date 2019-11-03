import os
import sys
import time
from datetime import datetime

import pytz
import requests
from django.db import models
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from hackerspace.models.events import updateTime
from hackerspace.YOUR_HACKERSPACE import (HACKERSPACE_TIMEZONE_STRING,
                                          RISEUPPAD_MEETING_PATH, WIKI_API_URL)


def startChrome(headless, url):
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
    browser = startChrome(
        headless=True, url='https://pad.riseup.net/p/'+RISEUPPAD_MEETING_PATH)
    time.sleep(5)
    browser.switch_to_frame(0)
    browser.switch_to_frame(0)
    return browser


class MeetingNoteSet(models.QuerySet):
    def current(self):
        return self.filter(text_notes__isnull=True).order_by('-int_UNIXtime_created').first()

    def past(self):
        return self.all().order_by('-int_UNIXtime_created')

    def import_all_from_wiki(self):
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
                'name': str(result),
                'url': '/meeting/'+result.text_date
            })
        return results_list


class MeetingNote(models.Model):
    objects = MeetingNoteSet.as_manager()
    text_date = models.TextField(blank=True, null=True)
    text_notes = models.TextField(blank=True, null=True)

    many_consensus_items = models.ManyToManyField(
        'ConsensusItem', related_name="m_consensus_items", blank=True)

    text_keywords = models.TextField(blank=True, null=True)
    int_UNIXtime_created = models.IntegerField(blank=True, null=True)
    int_UNIXtime_updated = models.IntegerField(blank=True, null=True)

    @property
    def date(self):
        local_timezone = pytz.timezone(HACKERSPACE_TIMEZONE_STRING)
        local_time = datetime.fromtimestamp(
            self.int_UNIXtime_created, local_timezone)
        return local_time.date()

    def start(self):
        print('Starting...')
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
        self.text_date = browser.find_element_by_id('innerdocbody').text
        self.save()

        # to do: auto notify via slack
        print('Done: Ended & saved meeting')

    def getKeywords(self):
        keywords = ''
        # to do
        return keywords

    def __str__(self):
        return self.text_date

    def import_from_local(self):
        self.text_notes = open(os.path.join(
            sys.path[0], 'hackerspace/meeting_notes/'+self.text_date+'.txt'), 'r').read()
        self.save()

    def import_from_wiki(self, page):
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

            self.save()
            print('Imported from wiki - '+self.text_date)
        else:
            print('Skipped - Already exists. '+self.text_date)

    def save(self, *args, **kwargs):
        self = updateTime(self)
        if not self.text_date:
            self.text_date = str(self.date)

        if self.text_notes:
            self.text_keywords = self.getKeywords()
        else:
            self.start()
        super(MeetingNote, self).save(*args, **kwargs)
