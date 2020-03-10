from _setup.models import Log
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from _setup.models import Secret


class Scraper():
    def __init__(self,
                 url=None,
                 show_log=True,
                 scraper_type='bs4',
                 scroll_down=False,
                 user_agent='desktop',
                 auto_close_selenium=True,
                 selenium_remote_webdriver=Secret('REMOTE_WEBDRIVER_IP').value):
        self.logs = ['self.__init__']
        self.show_log = show_log
        self.started = round(time.time())
        self.type = scraper_type
        self.page = None
        self.scroll_down = scroll_down
        self.selenium = None
        self.auto_close_selenium = auto_close_selenium
        self.selenium_remote_webdriver = selenium_remote_webdriver
        if user_agent == 'mobile':
            self.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'
        else:
            self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

        if self.type == 'bs4':
            self.help = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
        elif self.type == 'selenium':
            self.help = 'https://selenium-python.readthedocs.io'
        else:
            self.help = None

        if url:
            self.get_page(url)

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def get_page(self, url):
        self.log('get_page()')

        if self.type == 'bs4':
            self.log('-> load page via bs4')
            self.page = BeautifulSoup(
                get(url, headers={'User-Agent': self.user_agent}).text, 'html.parser')
        elif self.type == 'selenium':
            self.log('-> load page via selenium')

            firefox_options = webdriver.FirefoxOptions()
            profile = webdriver.FirefoxProfile()
            profile.set_preference(
                "general.useragent.override", self.user_agent)
            # if remote webdriver defined, use remote - else local
            if self.selenium_remote_webdriver:
                self.selenium = webdriver.Remote(
                    command_executor=self.selenium_remote_webdriver+'/wd/hub',
                    options=firefox_options,
                    browser_profile=profile
                )
            else:
                options = Options()
                options.headless = True
                self.selenium = webdriver.Firefox(
                    firefox_profile=profile,
                    options=options,
                    executable_path='geckodriver'
                )

            self.selenium.get(url)

            if self.scroll_down:
                counter = 0
                body = self.selenium.find_element_by_css_selector('body')
                while counter < self.scroll_down:
                    self.log('-> scrolling down...')
                    body.send_keys(Keys.PAGE_DOWN)
                    counter += 1

            page = self.selenium.page_source
            if self.auto_close_selenium:
                self.selenium.close()
            self.page = BeautifulSoup(page, 'html.parser')
            self.type = 'bs4'

        return self.page

    def select(self, selector, by='class'):
        self.log('select()')

        if not self.page:
            self.log('-> ERROR: page is missing')
            return None

        if not selector:
            self.log('-> ERROR: selector is missing')
            return None

        self.log('-> check for sub-selectors')
        if ' | ' in selector:
            sub_selectors = selector.split(' | ')
            selector = sub_selectors[0]
            sub_selectors = sub_selectors[1:]
        else:
            sub_selectors = None

        if by == 'class':
            if self.type == 'bs4':
                self.log('-> select class with bs4')
                selected = self.page.find_all(class_=selector)

        elif by == 'tag':
            if self.type == 'bs4':
                self.log('-> select tag with bs4')
                selected = self.page.find_all(selector)

        elif by == 'id':
            if self.type == 'bs4':
                self.log('-> select id with bs4')
                selected = self.page.find(id=selector)

        elif by == 'select':
            if self.type == 'bs4':
                self.log('-> select id with bs4')
                selected = self.page.select(selector)

        else:
            self.log('-> ERROR: by doesnt match available options')

        if sub_selectors:
            self.log('-> apply sub selector')
            for selector in sub_selectors:
                if selected == None:
                    return None

                if selector == '0':
                    selected = selected[0]
                elif selector == '1':
                    selected = selected[1]
                elif selector == '1:':
                    selected = selected[1:]
                elif selector == 'text':
                    if type(selected) == list:
                        selected = [x.text.replace(
                            '\n', '').strip() for x in selected]
                    else:
                        selected = selected.text.replace('\n', '').strip()

                elif selector == 'a':
                    selected = selected.a
                elif selector == 'span':
                    selected = selected.span
                elif selector == 'int':
                    selected = selected.text

                    if type(selected) == str:
                        selected = selected.replace(',', '').replace('.', '')

                    if ' ' in selected:
                        selected = selected.split(' ')[0]
                    if 'K' in selected:
                        selected = float(selected.split('K')[0])*1000
                    elif 'M' in selected:
                        selected = float(selected.split('M')[0])*1000000

                    selected = int(selected)
                else:
                    selected = selected.get(selector)

        return selected
