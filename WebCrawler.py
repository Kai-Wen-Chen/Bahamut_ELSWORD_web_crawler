import abc
import json
import os.path
import sys

import requests

from bs4 import BeautifulSoup
from ContentContainer import OnlineContentContainer, LocalContentContainer
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


class MyWebCrawler(WebCrawler, BaseException):
    def __init__(self):
        WebCrawler.__init__(self)
        self._soup = None
        self._uiProxy = MyUIProxy()
        self._onlineContentContainer = None
        self._localContentContainer = None

    def start(self):
        while True:
            self.__reset()
            mode = self.__askContentSource()
            if mode == 'online':
                self.getOnlineContent()
            else:
                self.getLocalContent()

    def getOnlineContent(self):
        if not self._onlineContentContainer:
            self._onlineContentContainer = OnlineContentContainer()
        self._onlineContentContainer.load()

    def getLocalContent(self):
        if not self._localContentContainer:
            self._localContentContainer = LocalContentContainer()
        self._localContentContainer.load()

    # --------------- private method -----------------#
    def __askContentSource(self):
        ans = self._uiProxy.askContentSource()

        if ans == 3:
            sys.exit(0)

        return 'online' if ans == 1 else 'local'

    def __reset(self):
        if self._onlineContentContainer:
            self._onlineContentContainer.reset()
        if self._localContentContainer:
            self._localContentContainer.reset()
