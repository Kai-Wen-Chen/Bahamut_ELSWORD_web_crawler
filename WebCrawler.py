import abc
import json
import os.path
import random
import sys

import requests
import time

from bs4 import BeautifulSoup
from MacroDefine import (
    USER_AGENT, URL_GAMER, URL_PAGE, URL_TAIL, URL_ELSWORD, LOCAL_JSON_PATH
)
from UIProxy import MyUIProxy


class WebCrawler(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def getOnlineContent(self):
        return NotImplemented

    @abc.abstractmethod
    def _request(self, url):
        return NotImplemented


class MyWebCrawler(WebCrawler, BaseException):
    def __init__(self):
        WebCrawler.__init__(self)
        self._soup = None
        self._uiProxy = MyUIProxy()
        self._numPage = 0
        self._mode = 'online'
        self._pageStart = 1
        self._pageEnd = -1
        self._keyword = ''
        self._dicFloor2Content = dict()

    def start(self):
        self.__reset()
        self.__askContentSource()
        if self._mode == 'online':
            self.getOnlineContent()
        else:
            self.getLocalContent()

    def getOnlineContent(self):
        self.__requestSoup(URL_ELSWORD)

        self.__getTotalPageNumber()
        self.__askKeyword()
        self.__askPageRange()

        for i in range(self._pageStart, self._pageEnd + 1):
            url = URL_GAMER + URL_PAGE + str(i) + URL_TAIL
            self.__requestSoup(url)

            lsContent = self.__getContentList()
            lsFloor = self.__getFloorList()

            self._dicFloor2Content.update(dict(zip(lsFloor, lsContent)))
            self._uiProxy.printMessage('Page %d updated' % i)
            time.sleep(random.uniform(1.0, 3.0))

        self._uiProxy.printMessage('Update complete')

        dicResult = dict()
        if self._keyword:
            for floor, content in self._dicFloor2Content.items():
                if self._keyword in content:
                    dicResult[floor] = content

            if dicResult:
                self._uiProxy.printMessage(['Matched floors:', str(list(dicResult.keys()))])

        if self.__askWriteData():
            self.__writeData(dicResult)

    def getLocalContent(self):
        if not os.path.exists(LOCAL_JSON_PATH) or not os.path.isfile(LOCAL_JSON_PATH):
            self._uiProxy.printMessage(['The local file doesn\'t exist', 'End program'])
            sys.exit(1)

        with open(LOCAL_JSON_PATH, 'r', encoding='utf-8') as f:
            self._dicFloor2Content = json.load(f)

        self._uiProxy.printMessage('Update complete')

        self.__askKeyword()

        dicResult = dict()
        if self._keyword:
            for floor, content in self._dicFloor2Content.items():
                if self._keyword in content:
                    dicResult[floor] = content

            if dicResult:
                self._uiProxy.printMessage(['Matched floors:', str(list(dicResult.keys()))])

        if self.__askWriteData():
            self.__writeData(dicResult)

    # --------------- protected method -----------------#
    def _request(self, url):
        headers = {
            'User-Agent': USER_AGENT
        }

        try:
            request = requests.get(url, headers=headers)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self._uiProxy.printMessage('Timeout, end program')
            sys.exit(1)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            self._uiProxy.printMessage('Weird URL, end program')
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            # catastrophic error.
            self._uiProxy.printMessage('Request failed, end program')
            sys.exit(1)

        return request

    # --------------- private method -----------------#
    def __askContentSource(self):
        ans = self._uiProxy.askContentSource()

        if ans == 3:
            sys.exit(0)

        self._mode = 'online' if ans == 1 else 'local'

    def __askKeyword(self):
        self._keyword = self._uiProxy.askKeyWord()

    def __askPageRange(self):
        self._pageStart, self._pageEnd = self._uiProxy.askPageRange(self._numPage)
        if self._pageEnd == -1:
            self._pageEnd = self._numPage

    def __askWriteData(self):
        return self._uiProxy.askWriteData()

    def __requestSoup(self, url):
        request = self._request(url)
        if not request:
            return None

        self._soup = BeautifulSoup(request.text, 'html.parser')

    def __getTotalPageNumber(self):
        pgBtn = self._soup.select_one('p.BH-pagebtnA')
        self._numPage = int(pgBtn.contents[-1].text)

    def __getContentList(self):
        contents = self._soup.select('.c-article__content')
        lsContent = []

        for i in range(len(contents)):
            lsContent.append(contents[i].text.strip())

        return lsContent

    def __getFloorList(self):
        postHeaders = self._soup.select('.c-post__header__author')
        lsFloor = []

        for i in range(len(postHeaders)):
            lsFloor.append(postHeaders[i].select_one('a.floor').get('data-floor'))

        return lsFloor

    def __writeData(self, data):
        import json
        try:
            with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
                if data:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                else:
                    json.dump(self._dicFloor2Content, f, ensure_ascii=False, indent=4)
            self._uiProxy.printMessage('Result stored')
        except EnvironmentError:
            self._uiProxy.printMessage('Something wrong, maybe the disk is full')

    def __reset(self):
        self._numPage = 0
        self._mode = 'online'
        self._pageStart = 1
        self._pageEnd = -1
        self._keyword = ''
        self._dicFloor2Content = dict()
