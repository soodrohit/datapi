# Copyright 2022 Rohit Sood

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import asyncio
import datetime
import os
import urllib
from datetime import date
from os import path, symlink
from typing import Dict, Any, List
from flask import request_started
import requests
from zoneinfo import ZoneInfo
from data_management import save_data, get_data_folder
import pytz
import threading
import concurrent.futures
import sys
import time


next_job_interval_in_seconds = 60
# Current time in IST
IST = pytz.timezone('Asia/Kolkata')


async def start_collector():
    is_market_open = get_market_open_state()
    headers: dict[str, str] = {}
    cookies: dict[str, str] = {}
    stock_list = getstocklist()
    test_mode = False
    # Debug Option
    if os.environ["DEBUG"]=="True":
        is_market_open = True
        test_mode = True
        print("starting quote crawler in test mode...")
    else:
        print("starting quote crawler...")
    while is_market_open:
        # loop through the stock list in groups of 8 threads
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # Start the load operations and mark each future with its stock symbol
            # fetch_quote_symbols = { executor.map(fetch_quote, stock): stock for stock in stock_list }
            fetch_quote_symbols = {executor.submit(fetch_quote, stock): stock for stock in stock_list}
        for quote_symbol in concurrent.futures.as_completed(fetch_quote_symbols):
            symbol = fetch_quote_symbols[quote_symbol]
            print("thread done for ", symbol)
        
        # threads = list()
        # for index in range(len(stock_list)):
        #     symbol=stock_list[index]
        #     print("Create and start thread ", symbol)
        #     x = threading.Thread(target=fetch_quote, args=(symbol,))
        #     threads.append(x)
        #     x.start()
        # for index, thread in enumerate(threads):
        #     symbol=stock_list[index]
        #     thread.join()
        #     print("thread done for ", symbol)
        print(f"Total time {round(time.time() - start, 2)}s")
        is_market_open = get_market_open_state()
        if is_market_open is not True:
            # reset the headers, cookies
            headers = {}
            cookies = {}
            print("Market closed!")
            if test_mode:
                # exits the program
                asyncio.get_running_loop().stop()
            while is_market_open is not True:
                await asyncio.sleep(next_job_interval_in_seconds)
                is_market_open = get_market_open_state()
        await asyncio.sleep(next_job_interval_in_seconds)
        print("starting next cycle of quote crawler...")


def fetch_quote(symbol):
    pTimer = time.time()
    headers: dict[str, str] = {}
    cookies: dict[str, str] = {}
    if cookies == {}:
        headers = getstaticheader(urllib.parse.quote(symbol))
        cookies = getfreshcookie()
    else:
        headers = getstaticheader(urllib.parse.quote(symbol))
    print(f"Getting quote for {symbol} ...")
    stock_quote = get_stock_data(symbol, headers, cookies)
    quoteFetched = time.time()
    save_data(symbol, stock_quote)
    print(f"{symbol} \n\tQuote Response in {round(quoteFetched - pTimer, 2)}s \n\tQuote Saved to disk in {round(time.time() - quoteFetched, 2)}s")

def get_market_open_state():
    # trading time between 9:15 AM - 3:30 PM (IST)
    # not a weekend
    # not a declared holiday
    now_india = datetime.datetime.now(IST)

    open_time = datetime.time(hour=9, minute=15, second=0, microsecond=0, tzinfo=ZoneInfo("Asia/Calcutta"))
    close_time = datetime.time(hour=15, minute=29, second=0, microsecond=0, tzinfo=ZoneInfo("Asia/Calcutta"))
    if now_india.weekday() == 5 or now_india.weekday() == 6:
        return False
    if not open_time <= now_india.time() <= close_time:
        return False
    market_holiday_list = get_market_holidays()
    if now_india.date() in market_holiday_list:
        return False
    return True


def get_market_holidays():
    holiday_list: list[date] = []
    with open(os.path.abspath("market_holidays.txt")) as f:
        for index, line in enumerate(f):
            holiday_list.append(datetime.datetime.strptime(str.strip(line.split('#')[1]), '%d-%b-%Y').date())
    return holiday_list


def getcustomcookie(symbol, headers):
    with open(os.path.abspath("nsecookie.txt")) as f:
        for index, line in enumerate(f):
            headers[str.strip(line.split('#')[0])] = str.strip(line.split('#')[1]).replace("$$symbol$$", symbol)
    return headers


def getstaticheader(symbol=''):
    if len(symbol) == 0:
        headers = {
            'authority': 'www.nseindia.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nseindia.com/',
            'accept-language': 'en-US,en;q=0.9'
        }
    else:
        headers = {
            'authority': 'www.nseindia.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://www.nseindia.com/get-quotes/derivatives?symbol={symbol}',
            'accept-language': 'en-US,en;q=0.9'
        }
    return headers


def get_stock_data(symbol, headers, cookies):
    url = f"https://www.nseindia.com/api/quote-derivative?symbol={urllib.parse.quote(symbol)}"
    try:
        response = requests.request("GET", url, headers=headers, cookies=cookies)
        stock_quote_data = response.text
        return stock_quote_data
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def getcookie(symbol):
    cookie_value = ''
    with open(os.path.abspath("nsecookie.txt")) as f:
        for index, line in enumerate(f):
            cookie_value = str.strip(line.split('#')[1]).replace("$$symbol$$", symbol)
    return cookie_value


def getheaders():
    headerdict = {}
    with open(os.path.abspath("nseheaders.txt")) as f:
        for index, line in enumerate(f):
            headerdict[line.split(':')[0]] = str.strip(line.split(':')[1])
            # print("Line {}: {}".format(index, line.strip()))
    return headerdict


def getfreshcookie():
    response = requests.request("GET", "https://www.nseindia.com/", headers=getstaticheader())
    return response.cookies


def getstocklist():
    stock_list = []
    stock_list_file = "stock_list.txt"
    if os.environ["DEBUG"]=="True":
        stock_list_file = "stock_list_debug.txt"
    with open(os.path.abspath(stock_list_file)) as f:
        for index, line in enumerate(f):
            stock_list.append(str.strip(line))
    return stock_list