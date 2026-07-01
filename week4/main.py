"""Assignment - Week 4 FastAPI application."""

import csv                                                                          # 匯入 csv，備援讀取 Week 3 產生的 hotels.csv
import json                                                                         # 匯入 json，解析遠端旅館資料 JSON
import re                                                                           # 匯入 re，用正規表示式清理電話字串
from pathlib import Path                                                            # 匯入 Path，處理資料夾與檔案路徑
from typing import Optional                                               # 匯入 Optional，讓 Python 3.9 可以表示可能是 None 的型別
from urllib.request import Request as UrlRequest, urlopen                         # 匯入 UrlRequest 和 urlopen，抓取遠端旅館資料

from fastapi import FastAPI, Form, Request                                  # 匯入 FastAPI、Form、Request，建立網站與接收表單資料
from fastapi.responses import RedirectResponse                                    # 匯入 RedirectResponse，處理重新導向
from fastapi.staticfiles import StaticFiles                            # 匯入 StaticFiles，讓瀏覽器可以讀取 CSS 和 JavaScript 檔案
from fastapi.templating import Jinja2Templates                                      # 匯入 Jinja2Templates，渲染 HTML template
from starlette.middleware.sessions import SessionMiddleware                          # 匯入 SessionMiddleware，管理登入狀態


BASE_DIR = Path(__file__).resolve().parent                                           # 取得 main.py 所在資料夾，也就是 week4_pages
HOTEL_CSV_PATH = BASE_DIR / "hotels.csv"                                             # 設定本資料夾 hotels.csv 備援路徑
HOTELS_CH_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch" # 設定 Week 3 中文旅館資料 URL
HOTELS_EN_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en" # 設定 Week 3 英文旅館資料 URL
CORRECT_EMAIL = "abc@abc.com"                                                       # 設定 PDF 指定的正確登入信箱
CORRECT_PASSWORD = "abc"                                                            # 設定 PDF 指定的正確登入密碼


app = FastAPI()                                                                      # 建立 FastAPI 應用程式物件
app.add_middleware(SessionMiddleware, secret_key="week4-assignment-secret-key")      # 加入 SessionMiddleware，讓 request.session 可以記錄登入狀態
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")      # 設定 /static 網址路徑，讓瀏覽器可以讀取 static 資料夾中的 CSS 和 JavaScript
templates = Jinja2Templates(directory=BASE_DIR / "templates")                        # 設定 Jinja2 templates 資料夾位置


def fetch_text(url: str) -> str:                                                     # 輔助函式：從指定 URL 抓取文字內容
    request = UrlRequest(url, headers={"User-Agent": "Mozilla/5.0"})                  # 建立 URL request，附上 User-Agent 模擬瀏覽器
    with urlopen(request, timeout=8) as response:                                    # 開啟網址並設定最多等待 8 秒
        return response.read().decode("utf-8")                                       # 讀取回應內容並轉成 UTF-8 字串


def fetch_json(url: str) -> dict:                                                    # 輔助函式：從指定 URL 抓取 JSON 資料
    return json.loads(fetch_text(url))                                                # 先抓文字，再用 json.loads 轉成 Python 字典


def clean_phone(phone: str) -> str:                                                   # 輔助函式：清理電話格式，方便中英文資料配對
    return re.sub(r"\s+", "", phone or "")                                            # 移除所有空白，若 phone 是 None 則當空字串處理


def load_hotels_from_urls() -> list[dict[str, str]]:                                  # 輔助函式：依照 PDF/Week 3 URL 載入旅館資料
    chinese_hotels = fetch_json(HOTELS_CH_URL)["list"]                                # 抓取中文旅館資料並取出 list
    english_hotels = fetch_json(HOTELS_EN_URL)["list"]                                # 抓取英文旅館資料並取出 list
    english_by_phone = {clean_phone(hotel.get("tel", "")): hotel for hotel in english_hotels} # 建立電話對英文資料的查找字典
    hotels = []                                                                       # 建立整理後的旅館資料清單
    for index, hotel in enumerate(chinese_hotels, start=1):                           # 逐一處理中文旅館資料，並從 1 開始建立 ID
        phone = hotel.get("電話或手機號碼", "")                                       # 取得中文資料中的電話欄位
        english_hotel = english_by_phone.get(clean_phone(phone), {})                  # 用清理後電話找對應英文旅館資料
        hotels.append({"id": index, "chinese_name": hotel.get("旅宿名稱", ""), "english_name": english_hotel.get("hotel name", ""), "phone": phone})                                                         # 加入整理後旅館資料
    return hotels                                                                     # 回傳整理完成的旅館資料清單


def load_hotels_from_csv() -> list[dict[str, str]]:                            # 輔助函式：遠端失敗時從本資料夾 CSV 備援載入旅館資料
    hotels = []                                                                       # 建立整理後的旅館資料清單
    with open(HOTEL_CSV_PATH, newline="", encoding="utf-8") as file:                  # 開啟 week4 資料夾中的 hotels.csv
        reader = csv.reader(file)                                                     # 建立 CSV reader
        for index, row in enumerate(reader, start=1):                                 # 逐列讀取 CSV，並從 1 開始建立 ID
            if len(row) < 5:                                                          # 如果欄位數不足，代表資料不完整
                continue                                                              # 跳過這筆不完整資料
            hotels.append({"id": index, "chinese_name": row[0], "english_name": row[1], "phone": row[4]}) # 加入 CSV 旅館資料
    return hotels                                                                     # 回傳整理完成的旅館資料清單


def load_hotels() -> list[dict[str, str]]:                                            # 輔助函式：統一取得旅館資料，先遠端再備援
    try:                                                                              # 嘗試使用 Week 3 遠端 URL
        return load_hotels_from_urls()                                                # 遠端成功時回傳 URL 資料
    except Exception:                                                                 # 遠端失敗時，例如網路不通
        return load_hotels_from_csv()                                                 # 改用本資料夾 CSV 備援資料


HOTELS_CACHE: Optional[list[dict[str, str]]] = None                                   # 建立旅館資料快取，預設還沒有載入


def get_hotels() -> list[dict[str, str]]:                                             # 輔助函式：取得旅館資料並使用快取避免重複載入
    global HOTELS_CACHE                                                               # 宣告要使用全域 HOTELS_CACHE
    if HOTELS_CACHE is None:                                                          # 如果目前還沒有載入旅館資料
        HOTELS_CACHE = load_hotels()                                                  # 載入旅館資料並存入快取
    return HOTELS_CACHE                                                               # 回傳快取中的旅館資料


@app.get("/")                                                                         # 設定 GET / 首頁路由
async def home(request: Request):                                              # Task 1 Home Page 主函式：顯示首頁登入與旅館查詢表單
    return templates.TemplateResponse("index.html", {"request": request})             # 回傳首頁 template


@app.post("/login")                                                                   # 設定 POST /login 登入驗證路由
async def login(request: Request, email: str = Form(default=""), password: str = Form(default="")): # Task 2 Verification + Task 3 Session 主函式：登入驗證並設定 session
    email = email.strip()                                                             # 移除 email 前後空白
    password = password.strip()                                                       # 移除 password 前後空白
    if email == "" or password == "":                                                 # 如果信箱或密碼是空字串
        request.session["LOGGED_IN"] = False                                          # 將登入狀態設為 False
        return RedirectResponse("/ohoh?msg=請輸入信箱和密碼", status_code=303)          # 導向錯誤頁並帶入空欄位訊息
    if email == CORRECT_EMAIL and password == CORRECT_PASSWORD:                       # 如果帳號密碼符合 PDF 指定值
        request.session["LOGGED_IN"] = True                                           # 將登入狀態設為 True
        return RedirectResponse("/member", status_code=303)                           # 導向會員頁
    request.session["LOGGED_IN"] = False                                              # 如果帳密錯誤，將登入狀態設為 False
    return RedirectResponse("/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)             # 導向錯誤頁並帶入帳密錯誤訊息


@app.get("/member")                                                                   # 設定 GET /member 會員頁路由
async def member(request: Request):                          # Task 3 User State Management 主函式：會員頁檢查 session 登入狀態
    if request.session.get("LOGGED_IN") is not True:                                  # 如果 session 中不是已登入狀態
        return RedirectResponse("/", status_code=303)                                 # 強制導回首頁
    return templates.TemplateResponse("member.html", {"request": request})            # 已登入時回傳會員頁 template


@app.get("/logout")                                                                   # 設定 GET /logout 登出路由
async def logout(request: Request):                                             # Task 3 Logout 主函式：登出並清除登入狀態
    request.session["LOGGED_IN"] = False                                              # 將登入狀態設為 False
    return RedirectResponse("/", status_code=303)                                     # 登出後導回首頁


@app.get("/ohoh")                                                                     # 設定 GET /ohoh 錯誤頁路由
async def error(request: Request, msg: str = ""):                        # Task 2 Error Page 主函式：接收 query string 的 msg
    return templates.TemplateResponse("error.html", {"request": request, "message": msg}) # 回傳錯誤頁並顯示 message


@app.get("/hotel/{hotel_id}")                                                         # 設定 GET /hotel/{hotel_id} 旅館頁路由
async def hotel(request: Request, hotel_id: int):                   # Task 4 Path Parameter 主函式：接收 path parameter hotel_id
    hotel_data = None                                                                 # 預設查不到旅館資料
    hotels = get_hotels()                                                             # 取得旅館資料清單
    if hotel_id > 0 and hotel_id <= len(hotels):                                      # 如果 hotel_id 是正整數且在資料範圍內
        hotel_data = hotels[hotel_id - 1]                                    # 取得對應旅館，因為 list index 從 0 開始所以要 -1
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel_id": hotel_id, "hotel": hotel_data}) # 回傳旅館頁 template
