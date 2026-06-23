"""Assignment - Week 3 Python"""

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# Task 1
# Parse hotel data from internet and save hotels.csv / districts.csv
# (從網路抓取旅館資料，產生 hotels.csv 和 districts.csv)
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

import csv                                                                    # 匯入 csv，負責輸出 hotels.csv 和 districts.csv
import json                                                                   # 匯入 json，負責解析飯店 JSON 資料
import re                                                                     # 匯入 re，負責從地址抓出行政區
from pathlib import Path                                                       # 匯入 Path，負責取得目前檔案資料夾
from urllib.request import Request, urlopen                                    # 匯入 Request/urlopen，負責下載飯店資料


TASK1_BASE_DIR = Path(__file__).resolve().parent                               # 取得目前 Python 檔案所在資料夾

HOTELS_CH_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"  # 設定中文飯店資料網址

HOTELS_EN_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"  # 設定英文飯店資料網址


def task1_fetch_text(url: str) -> str:                                         # 定義下載文字內容的函式
    request = Request(                                                          # 建立 Request 物件 用 Request() 把網址包裝成比較像正常瀏覽器發出的網路請求。
        url,                                                                    # 放入要下載的網址
        headers={                                                               # 設定 HTTP headers
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"  # 設定 User-Agent，模擬一般瀏覽器
        },                                                                      # headers 設定結束
    )                                                                           # Request 建立結束

    with urlopen(request, timeout=20) as response:                              # 開啟網址並設定最多等待 20 秒
        return response.read().decode("utf-8")                                  # 讀取回應內容並轉成 UTF-8 字串


def task1_fetch_json(url: str) -> dict:                                        # 定義下載 JSON 的函式
    return json.loads(task1_fetch_text(url))                                    # 先下載文字，再用 json.loads 轉成字典


def task1_clean_phone(phone: str) -> str:                                      # 定義清理電話格式的函式
    return re.sub(r"\s+", "", phone or "")                                      # 移除電話中的空白，方便中英文資料配對


def task1_extract_district(address: str) -> str:                               # 定義從地址取出行政區的函式
    match = re.search(r"臺北市\s*([^市縣]{1,4}區)", address)                    # 在地址中尋找臺北市後面的某某區
    return match.group(1) if match else ""                                      # 找到就回傳行政區，找不到就回傳空字串


def task1_write_hotel_csv_files() -> None:                                     # 主函式：Task 1，負責產生飯店相關 CSV
    chinese_hotels = task1_fetch_json(HOTELS_CH_URL)["list"]                   # 下載中文飯店資料，取出 list 陣列
    english_hotels = task1_fetch_json(HOTELS_EN_URL)["list"]                   # 下載英文飯店資料，取出 list 陣列

    english_by_phone = {                                                       # 建立用電話查英文飯店資料的字典
        task1_clean_phone(hotel.get("tel", "")): hotel                         # key 是清理後電話，value 是英文飯店資料
        for hotel in english_hotels                                             # 逐一讀取每一筆英文飯店資料
    }                                                                           # 英文飯店電話對照表建立結束

    hotel_rows = []                                                             # 建立 hotels.csv 要寫入的資料列清單
    district_totals = {}                                                        # 建立 districts.csv 的行政區統計字典

    for hotel in chinese_hotels:                                                # 逐一處理每一筆中文飯店資料
        phone = task1_clean_phone(hotel.get("電話或手機號碼", ""))              # 取出並清理中文資料的電話
        english_hotel = english_by_phone.get(phone, {})                         # 用電話找對應的英文飯店資料
        chinese_address = hotel.get("地址", "")                                 # 取出中文地址
        room_count = int(hotel.get("房間數", "0") or 0)                         # 取出房間數並轉成整數

        hotel_rows.append(                                                      # 將合併後的一筆飯店資料加入清單
            [                                                                   # 建立一列 CSV 欄位
                hotel.get("旅宿名稱", ""),                                      # 欄位 1，中文名稱
                english_hotel.get("hotel name", ""),                            # 欄位 2，英文名稱
                chinese_address,                                                # 欄位 3，中文地址
                english_hotel.get("address", ""),                               # 欄位 4，英文地址
                hotel.get("電話或手機號碼", ""),                                # 欄位 5，電話
                room_count,                                                     # 欄位 6，房間數
            ]                                                                   # 一列 CSV 欄位結束
        )                                                                       # 加入 hotels.csv 資料列結束

        district = task1_extract_district(chinese_address)                      # 從中文地址取出行政區

        if district:                                                            # 如果有成功取得行政區才做統計
            district_totals.setdefault(district, {"hotels": 0, "rooms": 0})      # 如果行政區不存在就建立初始值
            district_totals[district]["hotels"] += 1                            # 該行政區旅館數加 1
            district_totals[district]["rooms"] += room_count                    # 該行政區房間數加上目前飯店房間數

    with open(TASK1_BASE_DIR / "hotels.csv", "w", newline="", encoding="utf-8") as file:  # 開啟 hotels.csv 準備寫入
        writer = csv.writer(file)                                               # 建立 CSV writer
        writer.writerows(hotel_rows)                                            # 一次寫入所有飯店資料列

    district_rows = [                                                           # 建立 districts.csv 要寫入的資料列
        [district, totals["hotels"], totals["rooms"]]                           # 每列包含行政區、旅館數、房間數
        for district, totals in sorted(district_totals.items())                  # 依行政區名稱排序後逐一輸出
    ]                                                                           # districts.csv 資料列建立結束

    with open(TASK1_BASE_DIR / "districts.csv", "w", newline="", encoding="utf-8") as file:  # 開啟 districts.csv 準備寫入
        writer = csv.writer(file)                                               # 建立 CSV writer
        writer.writerows(district_rows)                                         # 一次寫入所有行政區統計列


task1_write_hotel_csv_files()                                                   # 執行 Task 1，產生 hotels.csv 和 districts.csv
print("Created hotels.csv, districts.csv")                                      # 印出 Task 1 完成訊息


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# Task 2
# Parse PTT Steam article data and save articles.csv
# (使用 BeautifulSoup 解析 PTT Steam 文章資料，產生 articles.csv)
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

import csv                                                                    # 匯入 csv，負責輸出 articles.csv
from pathlib import Path                                                       # 匯入 Path，負責取得目前檔案資料夾
from urllib.parse import urljoin                                               # 匯入 urljoin，負責組合 PTT 文章網址
from urllib.request import Request, urlopen                                    # 匯入 Request/urlopen，負責下載 PTT HTML

from bs4 import BeautifulSoup                                                  # 匯入 BeautifulSoup，負責解析 HTML 程式碼


TASK2_BASE_DIR = Path(__file__).resolve().parent                               # 取得目前 Python 檔案所在資料夾
PTT_BASE_URL = "https://www.ptt.cc"                                            # 設定 PTT 網站主網址
PTT_STEAM_URL = "https://www.ptt.cc/bbs/Steam/index.html"                     # 設定 PTT Steam 看板最新列表頁


def task2_fetch_text(url: str) -> str:                                         # 定義下載 PTT HTML 的函式
    request = Request(                                                          # 建立 Request 物件
        url,                                                                    # 放入要下載的網址
        headers={                                                               # 設定 HTTP headers
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"  # 設定 User-Agent，模擬一般瀏覽器
        },                                                                      # headers 設定結束
    )                                                                           # Request 建立結束

    with urlopen(request, timeout=20) as response:                              # 開啟網址並設定最多等待 20 秒
        return response.read().decode("utf-8")                                  # 讀取回應內容並轉成 UTF-8 字串


def task2_parse_like_count(text: str) -> int:                                  # 定義推文數轉換函式
    text = text.strip()                                                         # 去掉推文數前後空白

    if text == "爆":                                                            # 如果推文數顯示爆
        return 100                                                              # 依一般作法轉成 100

    if text.startswith("X"):                                                    # 如果推文數是負評 X 開頭
        return -10                                                              # 依一般作法轉成 -10

    if text == "":                                                              # 如果推文數是空白
        return 0                                                                # 空白代表 0

    return int(text) if text.isdigit() else 0                                   # 數字就轉整數，其他狀況回傳 0


def task2_parse_publish_time(article_url: str) -> str:                         # 定義抓取文章發文時間的函式
    article_html = task2_fetch_text(article_url)                                # 下載文章頁 HTML
    soup = BeautifulSoup(article_html, "html.parser")                           # 使用 BeautifulSoup 解析文章 HTML
    meta_tags = soup.select("span.article-meta-tag")                            # 找出文章頁上方的作者、標題、時間標籤

    for tag in meta_tags:                                                       # 逐一檢查每一個 meta 標籤
        if tag.get_text(strip=True) == "時間":                                  # 如果標籤文字是時間
            value = tag.find_next_sibling("span", class_="article-meta-value")  # 取得旁邊的時間值
            return value.get_text(strip=True) if value else ""                  # 找到時間就回傳，找不到就回傳空字串

    return ""                                                                   # 如果整頁沒有時間資料，就回傳空字串


def task2_parse_article_rows_from_page(page_url: str):                         # 定義解析單一列表頁的函式
    html = task2_fetch_text(page_url)                                           # 下載 PTT 列表頁 HTML
    soup = BeautifulSoup(html, "html.parser")                                   # 使用 BeautifulSoup 解析列表頁 HTML
    article_rows = []                                                           # 建立目前列表頁的文章資料列清單

    for entry in soup.select("div.r-ent"):                                      # 逐一讀取列表頁上的文章區塊
        title_link = entry.select_one("div.title a")                            # 找出文章標題連結

        if title_link is None:                                                  # 如果沒有標題連結
            continue                                                            # 代表文章被刪除，直接跳過

        title = title_link.get_text(strip=True)                                 # 取得文章標題文字
        like_text = entry.select_one("div.nrec").get_text(strip=True)           # 取得推文數文字
        article_url = urljoin(PTT_BASE_URL, title_link["href"])                 # 將相對文章網址轉成完整網址
        publish_time = task2_parse_publish_time(article_url)                    # 進入文章頁取得完整發文時間
        like_count = task2_parse_like_count(like_text)                          # 將推文數文字轉成數字

        article_rows.append([title, like_count, publish_time])                  # 加入 articles.csv 的一筆資料

    previous_link = ""                                                          # 建立上一頁網址，預設為空字串

    for link in soup.select("div.btn-group-paging a"):                          # 逐一檢查分頁按鈕
        if "上頁" in link.get_text():                                           # 如果按鈕文字包含上頁
            previous_link = urljoin(PTT_BASE_URL, link["href"])                 # 組合成完整上一頁網址
            break                                                               # 找到上一頁後就停止迴圈

    return article_rows, previous_link                                          # 回傳文章資料列與下一輪要抓的上一頁網址


def task2_write_articles_csv_file() -> None:                                   # 主函式：Task 2，負責產生 PTT 文章 CSV
    rows = []                                                                   # 建立 articles.csv 的全部資料列清單
    page_url = PTT_STEAM_URL                                                    # 從 Steam 看板最新頁開始

    for _ in range(3):                                                          # 依作業要求抓前三個列表頁
        page_rows, page_url = task2_parse_article_rows_from_page(page_url)      # 解析目前頁面並取得上一頁網址
        rows.extend(page_rows)                                                  # 將目前頁面的文章資料加入總清單

    with open(TASK2_BASE_DIR / "articles.csv", "w", newline="", encoding="utf-8") as file:  # 開啟 articles.csv 準備寫入
        writer = csv.writer(file)                                               # 建立 CSV writer
        writer.writerows(rows)                                                  # 寫入所有文章資料列


task2_write_articles_csv_file()                                                 # 執行 Task 2，產生 articles.csv
print("Created articles.csv")                                                   # 印出 Task 2 完成訊息
