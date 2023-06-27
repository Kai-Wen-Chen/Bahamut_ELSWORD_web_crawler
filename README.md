# 巴哈姆特場外艾爾之光討論串(第三串)爬蟲練習 (Bahamut_ELSWORD_web_crawler)

- ~~**目前這個爬蟲無法使用 因為巴哈現在要求使用者必須登入才能瀏覽場外休憩區 因此這個爬蟲會被擋**~~
- ~~**Currently, this crawler cannot work because the contents cannot be accessed unless user log in Bahamut**~~
- **2023.06.15更新: 加入巴哈姆特登入機制 使用者登入後便可使用**
- **2023.06.15 Update: Enable user login to Bahamut to make the crawler able to work**
- **執行檔仍是舊版不支援登入的版本 仍無法使用 待未來更新 (.exe still cannot support login feature and work properly, remain to be updated in the future)**

## 功能列表 (Feature list)

此爬蟲僅限場外艾爾之光第三串使用 可支援最新網站資料及本地資料搜尋

This web crawler only supports this [Bahamut website](https://forum.gamer.com.tw/C.php?page=1&bsn=60076&snA=5149433)
Able to support online and local data search


## 使用說明 (Usage)

### By Python

- **需求 (Requirement)**
  - **Python 3**, **selenium (webdriver)**, **BeautifulSoup**
  - if you have any missing module, please download by yourself (pip/apt/...)
- **Execute main.py**
  - By command line: ```python main.py``` (if you have **python-is-python3**) or ```python3 main.py```
  - By IDE: Run/Debug main.py

### By exe (Currently does not work)

- 目前exe尚未更新 無法使用

### 操作流程 (Operation steps)

選擇搜尋線上或是本地紀錄 (Choose to search online or local records)

#### 線上 (Online)
1. 輸入巴哈姆特帳密以登入 (**本爬蟲不會記錄任何帳密 只會傳送給巴哈登入系統**)
2. 詢問是否要限制搜尋的頁數範圍 (只搜尋特定頁數範圍內的樓層或是全樓層搜尋)
3. 詢問關鍵字(若無則直接抓下範圍內所有樓層)
4. 顯示出符合搜尋條件的**樓層編號和內文**
5. 可將此次的搜尋存在本地(文件資料夾) 下次可直接使用本地紀錄節省時間
-------------------------------------------------------------------------------------------------------
1. Log in Bahamut (**This program won't keep any account and password, only pass them to Bahamut login system**)
2. Ask user if need to restrict the page range to search (Search the floors within the page range only, or all floors)
3. Ask keyword to search (If no keyword, will search all contents in designated page range)
4. Show the **floor number and contents** of all matched floors
5. User can save the search result to local for the requirement of reviewing the result in the future

#### 本地 (Local)
1. 詢問關鍵字(若無則直接顯示所有樓層)
2. 顯示出符合的**樓層編號和內文**
-------------------------------------------------------------------------------------------------------
1. Ask keyword to search (If no keyword, will show all floors in the local record)
2. Show the **floor number and contents** of all matched floors

## TODO list (it is not guaranteed to implement with a certain schedule :p)

1. 更新執行檔 (Update .exe)
2. ~~顯示符合搜尋條件的**樓層內文** (Show the **contents** of matched floors)~~
3. 優化搜尋方法 (Optimize searching method)
4. 客製化想要爬蟲的討論串 (Customize the url to do web scraping)
