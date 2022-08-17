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

from importlib.metadata import metadata
import os
import traceback
import sys
from os import path
import datetime
from shutil import register_unpack_format
from zoneinfo import ZoneInfo
from numpy import double
import pytz
import json
from option_class import *


# Current time in IST
IST = pytz.timezone('Asia/Kolkata')
# Data Store Path
data_directory = "data"
# Test Data Store Path
if os.environ["DEBUG"]=="True":
    data_directory = "data/test"


def save_data(symbol, stock_quote_data):
    save_file_path = get_data_folder(symbol)
    stock_data_json = json.loads(stock_quote_data)
    root = Root.from_dict(stock_data_json)
    # Group by expiry, calls and puts
    for optionExpiryDate in root.expiryDates:
        all_calls = filter(lambda x : x.metadata.expiryDate==optionExpiryDate 
                                and x.metadata.optionType=="Call"
                                and (x.metadata.instrumentType=="Stock Options" 
                                        or x.metadata.instrumentType=="Index Options"), root.stocks)
        all_puts = filter(lambda x : x.metadata.expiryDate==optionExpiryDate 
                                and x.metadata.optionType=="Put"
                                and (x.metadata.instrumentType=="Stock Options" 
                                        or x.metadata.instrumentType=="Index Options"), root.stocks)
        try:
            write_all_data(all_calls, all_puts, symbol, root.opt_timestamp)
        except:
            traceback.print_exception(*sys.exc_info())
        finally:
            continue
    with open(save_file_path, mode="w") as f:
        f.write(stock_quote_data)
    print(f"Saved quote for {symbol} at {save_file_path}")
        # for optionStrikePrice in root.strikePrices:
        #     try:
        #         calls = filter(lambda x : x.metadata.expiryDate==optionExpiryDate 
        #                         and x.metadata.strikePrice==optionStrikePrice 
        #                         and x.metadata.optionType=="Call"
        #                         and x.metadata.instrumentType=="Stock Options", root.stocks)
        #         call_strike_data = list(calls)[0]
        #         call_expiry_path = get_expiry_path(symbol, optionExpiryDate, call_strike_data.metadata.identifier)
        #         write_strike_data(call_expiry_path, call_strike_data.metadata, call_strike_data.marketDeptOrderBook,
        #                             root.underlyingValue, root.opt_timestamp)
        #     except:
        #         msg = f'Error with CE {optionExpiryDate} {optionStrikePrice} \n'
        #         print(msg)
        #         traceback.print_exception(*sys.exc_info())
        #     try:
        #         puts = filter(lambda x : x.metadata.expiryDate==optionExpiryDate 
        #                         and x.metadata.strikePrice==optionStrikePrice 
        #                         and x.metadata.optionType=="Put"
        #                         and x.metadata.instrumentType=="Stock Options", root.stocks)
        #         put_strike_data = list(puts)[0]
        #         put_expiry_path = get_expiry_path(symbol, optionExpiryDate, put_strike_data.metadata.identifier)
        #         write_strike_data(put_expiry_path, put_strike_data.metadata, put_strike_data.marketDeptOrderBook,
        #                             root.underlyingValue, root.opt_timestamp)
        #     except:
        #         msg = f'Error with PE {optionExpiryDate} {optionStrikePrice} \n'
        #         print(msg)
        #         traceback.print_exception(*sys.exc_info())
        #     finally:
        #         continue


def write_all_data(all_calls: filter, all_puts: filter, symbol: str, opt_timestamp: str) -> None:
    for call_strike in all_calls:
        try:
            call_expiry_path = get_expiry_path(symbol, call_strike.metadata.expiryDate, call_strike.metadata.identifier)
            write_strike_data(call_expiry_path, call_strike.metadata, 
                                call_strike.marketDeptOrderBook, call_strike.underlyingValue, opt_timestamp)
        except:
                traceback.print_exception(*sys.exc_info())
                msg = f'Error with CE {call_strike.metadata.expiryDate} {call_strike.metadata.strikePrice} \n'
                print(msg)
        finally:
            continue
    for put_strike in all_puts:
        try:
            put_expiry_path = get_expiry_path(symbol, put_strike.metadata.expiryDate, put_strike.metadata.identifier)
            write_strike_data(put_expiry_path, put_strike.metadata, 
                                put_strike.marketDeptOrderBook, put_strike.underlyingValue, opt_timestamp)
        except:
                traceback.print_exception(*sys.exc_info())
                msg = f'Error with PE {put_strike.metadata.expiryDate} {put_strike.metadata.strikePrice} \n'
                print(msg)
        finally:
            continue


def write_strike_data(path: str, metadata: Metadata, marketDeptOrderBook: MarketDeptOrderBook, 
                        underlyingValue: float, quote_timestamp: str) -> None:
     with open(path, mode="a") as f:
        try:
            f.write(','.join([  quote_timestamp, 
                                str(underlyingValue),
                                str(metadata.openPrice),
                                str(metadata.highPrice),
                                str(metadata.lowPrice),
                                str(metadata.closePrice),
                                str(metadata.lastPrice),
                                str(metadata.change),
                                str(metadata.pChange),
                                str(metadata.numberOfContractsTraded),
                                str(marketDeptOrderBook.totalBuyQuantity),
                                str(marketDeptOrderBook.totalSellQuantity),
                                str(marketDeptOrderBook.tradeInfo.vmap),
                                str(marketDeptOrderBook.tradeInfo.openInterest),
                                str(marketDeptOrderBook.tradeInfo.changeinOpenInterest),
                                str(marketDeptOrderBook.tradeInfo.pchangeinOpenInterest),
                                str(marketDeptOrderBook.otherInfo.dailyvolatility),
                                str(marketDeptOrderBook.otherInfo.impliedVolatility),
                                str("\n")
                                ]
                            )
                    )
        except:
            traceback.print_exception(*sys.exc_info())


def get_expiry_path(symbol, optionExpiryDate, expiryIdentifier):
    if os.path.exists(os.path.abspath(path.join(os.curdir, data_directory,symbol,optionExpiryDate,expiryIdentifier))):
        datastorepath = os.path.abspath(path.join(os.curdir, data_directory,symbol,optionExpiryDate,expiryIdentifier))
        return datastorepath
    datastorepath = os.path.abspath(path.join(os.curdir, data_directory))
    if not os.path.exists(os.path.join(datastorepath, symbol)):
        os.mkdir(os.path.join(datastorepath, symbol))
    datastorepath = os.path.abspath(os.path.join(datastorepath, symbol))
    if not os.path.exists(os.path.join(datastorepath, optionExpiryDate)):
        os.mkdir(os.path.join(datastorepath, optionExpiryDate))
    datastorepath = os.path.abspath(path.join(datastorepath, optionExpiryDate, expiryIdentifier))
    if not os.path.exists(datastorepath):
        with open(datastorepath, mode="w") as f:
            f.write(','.join([ "quote_timestamp", 
                                "underlyingValue",
                                "openPrice",
                                "highPrice",
                                "lowPrice",
                                "closePrice",
                                "lastPrice",
                                "change",
                                "pChange",
                                "numberOfContractsTraded",
                                "totalBuyQuantity",
                                "totalSellQuantity",
                                "tradeInfo.vmap",
                                "openInterest",
                                "changeinOpenInterest",
                                "pchangeinOpenInterest",
                                "dailyvolatility",
                                "impliedVolatility",
                                str("\n")
                                ]
                            )
                        )
    return datastorepath


def get_data_folder(symbol):
    datastorepath = os.path.abspath(path.join(os.curdir, data_directory))
    if not os.path.exists(os.path.join(datastorepath, symbol)):
        os.mkdir(os.path.join(datastorepath, symbol))
    datastorepath = os.path.abspath(path.join(datastorepath, symbol))
    datepath = datetime.datetime.now(IST).today().date().isoformat()
    if not os.path.exists(os.path.join(datastorepath, datepath)):
        os.mkdir(os.path.join(datastorepath, datepath))
    datastorepath = os.path.abspath(path.join(datastorepath, datepath))
    timepath = datetime.datetime.now(IST).strftime('%H%M%S%f')
    datastorepath =  os.path.abspath(path.join(datastorepath, timepath))
    return datastorepath
