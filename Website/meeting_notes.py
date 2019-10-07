import os
import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def startChrome(headless, url):
    options = Options()
    if headless == True:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    if 'Website' in sys.path[0]:
        browser_path = os.path.join(
            sys.path[0], 'Selenium/chromedriver_'+sys.platform)
    else:
        browser_path = os.path.join(
            sys.path[0], 'Website/Selenium/chromedriver_'+sys.platform)
    browser = webdriver.Chrome(
        chrome_options=options, executable_path=browser_path)
    browser.get(url)
    return browser


def openMeetingNotes():
    browser = startChrome(
        headless=True, url='https://pad.riseup.net/p/nbmeeting')
    time.sleep(5)
    browser.switch_to_frame(0)
    browser.switch_to_frame(0)
    return browser


def getMeetingNotes():
    browser = openMeetingNotes()
    return browser.find_element_by_id('innerdocbody').text


def endMeeting():
    # save meeting notes
    notes = getMeetingNotes()
    notes_file = open('MeetingNotes/'+str(datetime.now().date())+'.txt', 'w')
    notes_file.write(notes)
    notes_file.close()


def startMeeting():
    print('Starting...')
    browser = openMeetingNotes()

    input_field = browser.find_element_by_id('innerdocbody')
    input_field.clear()

    # copy template for new meeting into riseup pad
    meeting_template = open('MeetingNotes/Template.txt', 'r').read()
    for line in reversed(meeting_template.split('\n')):
        input_field.send_keys(Keys.RETURN)
        input_field.send_keys(line.replace(
            '{{ Date }}', str(datetime.now().date())))
    print('Done: https://pad.riseup.net/p/nbmeeting')


# endMeeting()
