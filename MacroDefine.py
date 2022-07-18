import os

from pathlib import Path

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

URL_GAMER = 'https://forum.gamer.com.tw/C.php?'
URL_PAGE = 'page='
URL_TAIL = '&bsn=60076&snA=5149433'
URL_ELSWORD = 'https://forum.gamer.com.tw/C.php?page=1&bsn=60076&snA=5149433'

LOCAL_JSON_PATH = os.path.join(Path.home(), 'Documents', 'bahamut.json')

QUESTION_CONTENT_SOURCE = 'Do you want to get current online data or local stored data?'
QUESTION_NEED_PAGE_RANGE = 'Do you want to set the page range of search? If select No, search all pages as default'
QUESTION_PAGE_START = 'Please enter the start page: '
QUESTION_PAGE_END = 'Please enter the end page: '
QUESTION_WRITE_DATA = 'Do you want to store the search result in your device?'
QUESTION_KEYWORD = 'Please enter the keyword you want to search (If no keyword, get all floors)'

INPUT_CONTENT_SOURCE = 'Press the related number to select, online(1) / local(2) / exit(3): '
INPUT_NEED_PAGE_RANGE = 'Press the related number to select, Yes(1) / No(2): '
INPUT_WRITE_DATA = 'Press the related number to select, Yes(1) / No(2): '
