from bs4 import BeautifulSoup
import json
import os
import random
import requests
import sys
import time

from MacroDefine import (
    LOCAL_JSON_PATH, URL_ELSWORD, URL_GAMER, URL_PAGE, URL_TAIL, USER_AGENT
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

    # --------------- overwrite method -----------------#
    def load(self):
        self.__requestSoup(URL_ELSWORD)

        self.__getTotalPageNumber()
        self._askKeyword()
        self.__askPageRange()

        for i in range(self._pageStart, self._pageEnd + 1):
            url = URL_GAMER + URL_PAGE + str(i) + URL_TAIL
            self.__requestSoup(url)

            lsContent = self.__getContentList()
            lsFloor = self.__getFloorList()

            self._dicFloor2Content.update(dict(zip(lsFloor, lsContent)))
            self._uiProxy.printMessage('Page %d updated' % i)
            time.sleep(random.uniform(0.5, 2.0))

        self._uiProxy.printMessage('Update complete')

        dicResult = dict()
        if self._keyword:
            for floor, content in self._dicFloor2Content.items():
                if self._keyword in content:
                    dicResult[floor] = content

            if dicResult:
                self._uiProxy.printMessage(['Matched floors:', str(list(dicResult.keys()))])

        if self.__askWriteData():
            self.save(dicResult)

    def reset(self):
        self._numPage = 0
        self._pageStart = 1
        self._pageEnd = -1
        self._keyword = ''
        self._dicFloor2Content = dict()

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

            if dicResult:
                self._uiProxy.printMessage(['Matched floors:', str(list(dicResult.keys()))])

    def reset(self):
        self._keyword = ''
        self._dicFloor2Content = dict()
