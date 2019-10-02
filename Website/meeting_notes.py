from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import sys
import os
import time
from datetime import datetime


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


def getMeetingNotes():
    browser = startChrome(
        headless=True, url='https://pad.riseup.net/p/nbmeeting')
    time.sleep(5)
    browser.switch_to_frame(0)
    browser.switch_to_frame(0)
    return browser.find_element_by_id('innerdocbody').text


def saveMeetingNotes():
    notes = getMeetingNotes()
    notes_file = open('MeetingNotes/'+str(datetime.now().date())+'.txt', 'w')
    notes_file.write(notes)
    notes_file.close()


saveMeetingNotes()
