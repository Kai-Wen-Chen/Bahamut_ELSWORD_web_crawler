import os

from pathlib import Path

USER_AGENT2 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

URL_GAMER = 'https://forum.gamer.com.tw/C.php?'
URL_PAGE = 'page='
URL_TAIL = '&bsn=60076&snA=5149433'
URL_ELSWORD = 'https://forum.gamer.com.tw/C.php?page=1&bsn=60076&snA=5149433'
URL_LOGIN = 'https://user.gamer.com.tw/login.php'

LOCAL_JSON_PATH = os.path.join(Path.home(), 'Documents', 'bahamut.json')

QUESTION_CONTENT_SOURCE = 'Do you want to get current online data or local stored data?'
QUESTION_NEED_PAGE_RANGE = 'Do you want to set the page range of search? If select No, search all pages as default'
QUESTION_PAGE_START = 'Please enter the start page: '
QUESTION_PAGE_END = 'Please enter the end page: '
QUESTION_WRITE_DATA = 'Do you want to store the search result in your device?'
QUESTION_KEYWORD = 'Please enter the keyword you want to search (If no keyword, get all floors)'
QUSETION_SHOW_MORE_RESULT = 'Do you want to show the next 10 results?'

INPUT_CONTENT_SOURCE = 'Press the related number to select, online(1) / local(2) / exit(3): '
INPUT_USER_ID = 'Please input your Bahamut user id (account), input nothing will end this program: '
INPUT_USER_PASSWORD = 'Please input your Bahamut password, input nothing will end this program: '
INPUT_NEED_PAGE_RANGE = 'Press the related number to select, Yes(1) / No(2): '
INPUT_WRITE_DATA = 'Press the related number to select, Yes(1) / No(2): '
INPUT_NEED_SHOW_MORE_RESULT = 'Press the related number to select, Yes(1) / no(2): '
