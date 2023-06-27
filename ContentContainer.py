from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import os
import random
import sys
import time
import traceback

from MacroDefine import (
    LOCAL_JSON_PATH, URL_ELSWORD, URL_GAMER, URL_PAGE, URL_TAIL, USER_AGENT, URL_LOGIN
)
from UIProxy import MyUIProxy


class ContentContainer(object):
    def __init__(self):
        self._uiProxy = MyUIProxy()
        self._keyword = ''
        self._dicFloor2Content = dict()

    def load(self):
        return NotImplemented

    def save(self, data=None):
        if not data:
            data = self._dicFloor2Content
        try:
            with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self._uiProxy.printMessage('Result stored in %s' % LOCAL_JSON_PATH)
        except EnvironmentError:
            self._uiProxy.printMessage('EnvironmentError')

    def reset(self):
        return NotImplemented

    def _askKeyword(self):
        self._keyword = self._uiProxy.askKeyWord()


class OnlineContentContainer(ContentContainer):
    def __init__(self):
        ContentContainer.__init__(self)
        self._numPage = 0
        self._pageStart = 1
        self._pageEnd = -1
        self._driver = None

    # --------------- overwrite method -----------------#
    def load(self):
        self.__initWebDriver()
        self.__loginBahamut()
        # Currently, it's not enable to customize the directed url, will remain a future feature
        self.__redirectToURL(URL_ELSWORD)

        self._uiProxy.printMessage('Success to access url %s' % URL_ELSWORD)

        self.__getTotalPageNumber()
        self._askKeyword()
        self.__askPageRange()
        
        for i in range(self._pageStart, self._pageEnd + 1):
            self._uiProxy.printMessage('Update page %d ...' % i)
            url = URL_GAMER + URL_PAGE + str(i) + URL_TAIL
            self.__request(url)

            lsContent = self.__getContentList()
            lsFloor = self.__getFloorList()

            self._dicFloor2Content.update(dict(zip(lsFloor, lsContent)))
            self._uiProxy.printMessage('Page %d updated' % i)
            time.sleep(random.uniform(0.5, 1.0))
        
        self._uiProxy.printMessage('Update complete')

        dicResult = dict()
        if self._keyword:
            for floor, content in self._dicFloor2Content.items():
                if self._keyword in content:
                    dicResult[floor] = content
        else:
            for floor, content in self._dicFloor2Content.items():
                dicResult[floor] = content

        if dicResult:
            self._uiProxy.showContents(dicResult)

        if self.__askWriteData():
            self.save(dicResult)

    def reset(self):
        self._numPage = 0
        self._pageStart = 1
        self._pageEnd = -1
        self._keyword = ''
        self._dicFloor2Content = dict()
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    # --------------- private method -----------------#
    def __request(self, url):
        try:
            self._driver.get(url)
        except:
            traceback.print_exc()
            self._uiProxy.printMessage('Exception occurred, end program')
            sys.exit(0)

    def __askPageRange(self):
        self._pageStart, self._pageEnd = self._uiProxy.askPageRange(self._numPage)
        if self._pageEnd == -1:
            self._pageEnd = self._numPage

    def __askWriteData(self):
        return self._uiProxy.askWriteData()

    def __initWebDriver(self):        
        self._uiProxy.printMessage('Init webcrawler...')
        if self._driver is not None:
            self._driver.close()
            self._driver = None

        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('--headless')
        options.add_argument(f'--user-agent={USER_AGENT}')
        options.add_argument('--no-sandbox')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        self._driver = webdriver.Chrome(options=options)
        self._driver.get(URL_LOGIN)
        
    def __loginBahamut(self):
        def loginAccountInfo():
            userIdInputBox = self._driver.find_element(By.NAME, 'userid')
            passwordInputBox = self._driver.find_element(By.NAME, 'password')
            
            userId = self._uiProxy.askUserId()
            if not userId:
                sys.exit(0)
            
            password = self._uiProxy.askUserPassword()
            if not password:
                sys.exit(0)

            self._uiProxy.printMessage('Logging...')
            for c in userId:
                t = random.random()
                time.sleep(t)
                userIdInputBox.send_keys(c)

            for c in password:
                t = random.random()
                time.sleep(t)
                passwordInputBox.send_keys(c)

            loginBtn = self._driver.find_element(By.ID, 'btn-login')
            loginBtn.click()
        
        self._driver.refresh()
        loginAccountInfo()
        try:
            self._uiProxy.printMessage('Checking login status...')
            WebDriverWait(self._driver, 3).until(EC.url_to_be('https://www.gamer.com.tw/'))
        except TimeoutException:
            self._uiProxy.printMessage('Login failed or timeout, please retry')
            self.__loginBahamut()

        self._uiProxy.printMessage('Login success')

    def __redirectToURL(self, url=URL_ELSWORD):
        self._driver.get(url)
        try:
            self._uiProxy.printMessage('Redirecting to %s' % url)
            WebDriverWait(self._driver, 3).until(EC.url_to_be(url))
        except TimeoutException:
            self._uiProxy.printMessage('Redirecting to %s timout, end program' % url)
            sys.exit(0)

    def __getTotalPageNumber(self):
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        pgBtn = soup.find(class_='BH-pagebtnA')
        self._numPage = int(pgBtn.contents[-1].text)

    def __getContentList(self):
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        contents = soup.select('.c-article__content')
        lsContent = []

        for i in range(len(contents)):
            lsContent.append(contents[i].text.strip())

        return lsContent

    def __getFloorList(self):
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        postHeaders = soup.select('.c-post__header__author')
        lsFloor = []

        for i in range(len(postHeaders)):
            lsFloor.append(postHeaders[i].select_one('a.floor').get('data-floor'))

        return lsFloor


class LocalContentContainer(ContentContainer):
    def __init__(self):
        ContentContainer.__init__(self)

    # --------------- overwrite method -----------------#
    def load(self):
        if not os.path.exists(LOCAL_JSON_PATH) or not os.path.isfile(LOCAL_JSON_PATH):
            self._uiProxy.printMessage(['The local file doesn\'t exist', 'End program'])
            sys.exit(1)

        with open(LOCAL_JSON_PATH, 'r', encoding='utf-8') as f:
            self._dicFloor2Content = json.load(f)

        self._uiProxy.printMessage('Update complete')

        self._askKeyword()

        dicResult = dict()
        if self._keyword:
            for floor, content in self._dicFloor2Content.items():
                if self._keyword in content:
                    dicResult[floor] = content
        else:
            for floor, content in self._dicFloor2Content.items():
                dicResult[floor] = content

        if dicResult:
            self._uiProxy.showContents(dicResult)

    def reset(self):
        self._keyword = ''
        self._dicFloor2Content = dict()
