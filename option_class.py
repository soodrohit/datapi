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

from typing import List
from typing import Any
from dataclasses import dataclass
import traceback
import sys


@dataclass
class Ask:
    price: float
    quantity: int

    @staticmethod
    def from_dict(obj: Any) -> 'Ask':
        _price = float(obj.get("price"))
        _quantity = int(obj.get("quantity"))
        return Ask(_price, _quantity)


@dataclass
class Bid:
    price: float
    quantity: int

    @staticmethod
    def from_dict(obj: Any) -> 'Bid':
        _price = float(obj.get("price"))
        _quantity = int(obj.get("quantity"))
        return Bid(_price, _quantity)


@dataclass
class Carry:
    bestBuy: float
    bestSell: float
    lastPrice: float

    @staticmethod
    def from_dict(obj: Any) -> 'Carry':
        _bestBuy = float(obj.get("bestBuy"))
        _bestSell = float(obj.get("bestSell"))
        _lastPrice = float(obj.get("lastPrice"))
        return Carry(_bestBuy, _bestSell, _lastPrice)


@dataclass
class Price:
    bestBuy: float
    bestSell: float
    lastPrice: float

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        _bestBuy = float(obj.get("bestBuy"))
        _bestSell = float(obj.get("bestSell"))
        _lastPrice = float(obj.get("lastPrice"))
        return Price(_bestBuy, _bestSell, _lastPrice)


@dataclass
class CarryOfCost:
    price: Price
    carry: Carry

    @staticmethod
    def from_dict(obj: Any) -> 'CarryOfCost':
        _price = Price.from_dict(obj.get("price"))
        _carry = Carry.from_dict(obj.get("carry"))
        return CarryOfCost(_price, _carry)


@dataclass
class Info:
    symbol: str
    companyName: str
    industry: str
    activeSeries: List[str]
    debtSeries: List[object]
    tempSuspendedSeries: List[str]
    isFNOSec: bool
    isCASec: bool
    isSLBSec: bool
    isDebtSec: bool
    isSuspended: bool
    isETFSec: bool
    isDelisted: bool
    isin: str

    @staticmethod
    def from_dict(obj: Any) -> 'Info':
        _symbol = str(obj.get("symbol"))
        _companyName = str(obj.get("companyName"))
        _industry = str(obj.get("industry"))
        if obj.get("activeSeries") is not None:
            _activeSeries = [y for y in obj.get("activeSeries")]
        else:
            _activeSeries = []
        if obj.get("debtSeries") is not None:
            _debtSeries = [y for y in obj.get("debtSeries")]
        else:
            _debtSeries = []
        if obj.get("tempSuspendedSeries") is not None:
            _tempSuspendedSeries = [y for y in obj.get("tempSuspendedSeries")]
        else:
            _tempSuspendedSeries = []
        _isFNOSec = str(obj.get("isFNOSec"))
        _isCASec = str(obj.get("isCASec"))
        _isSLBSec = str(obj.get("isSLBSec"))
        _isDebtSec = str(obj.get("isDebtSec"))
        _isSuspended = str(obj.get("isSuspended"))
        _isETFSec = str(obj.get("isETFSec"))
        _isDelisted = str(obj.get("isDelisted"))
        _isin = str(obj.get("isin"))
        return Info(_symbol, _companyName, _industry, _activeSeries, _debtSeries, _tempSuspendedSeries, _isFNOSec, _isCASec, _isSLBSec, _isDebtSec, _isSuspended, _isETFSec, _isDelisted, _isin)


@dataclass
class TradeInfo:
    tradedVolume: int
    value: float
    vmap: float
    premiumTurnover: float
    openInterest: int
    changeinOpenInterest: int
    pchangeinOpenInterest: float
    marketLot: int

    @staticmethod
    def from_dict(obj: Any) -> 'TradeInfo':
        _tradedVolume = int(obj.get("tradedVolume"))
        _value = float(obj.get("value"))
        _vmap = float(obj.get("vmap"))
        _premiumTurnover = float(obj.get("premiumTurnover"))
        _openInterest = int(obj.get("openInterest"))
        _changeinOpenInterest = int(obj.get("changeinOpenInterest"))
        _pchangeinOpenInterest = float(obj.get("pchangeinOpenInterest"))
        _marketLot = int(obj.get("marketLot"))
        return TradeInfo(_tradedVolume, _value, _vmap, _premiumTurnover, _openInterest, _changeinOpenInterest, _pchangeinOpenInterest, _marketLot)


@dataclass
class OtherInfo:
    settlementPrice: float
    dailyvolatility: float
    annualisedVolatility: float
    impliedVolatility: float
    clientWisePositionLimits: int
    marketWidePositionLimits: int

    @staticmethod
    def from_dict(obj: Any) -> 'OtherInfo':
        _settlementPrice = float(obj.get("settlementPrice"))
        _dailyvolatility = float(obj.get("dailyvolatility"))
        _annualisedVolatility = float(obj.get("annualisedVolatility"))
        _impliedVolatility = float(obj.get("impliedVolatility"))
        _clientWisePositionLimits = int(obj.get("clientWisePositionLimits"))
        _marketWidePositionLimits = int(obj.get("marketWidePositionLimits"))
        return OtherInfo(_settlementPrice, _dailyvolatility, _annualisedVolatility, _impliedVolatility, _clientWisePositionLimits, _marketWidePositionLimits)


@dataclass
class MarketDeptOrderBook:
    totalBuyQuantity: int
    totalSellQuantity: int
    bid: List[Bid]
    ask: List[Ask]
    carryOfCost: CarryOfCost
    tradeInfo: TradeInfo
    otherInfo: OtherInfo

    @staticmethod
    def from_dict(obj: Any) -> 'MarketDeptOrderBook':
        _totalBuyQuantity = int(obj.get("totalBuyQuantity"))
        _totalSellQuantity = int(obj.get("totalSellQuantity"))
        _bid = [Bid.from_dict(y) for y in obj.get("bid")]
        _ask = [Ask.from_dict(y) for y in obj.get("ask")]
        _carryOfCost = CarryOfCost.from_dict(obj.get("carryOfCost"))
        _tradeInfo = TradeInfo.from_dict(obj.get("tradeInfo"))
        _otherInfo = OtherInfo.from_dict(obj.get("otherInfo"))
        return MarketDeptOrderBook(_totalBuyQuantity, _totalSellQuantity, _bid, _ask, _carryOfCost, _tradeInfo, _otherInfo)


@dataclass
class Metadata:
    instrumentType: str
    expiryDate: str
    optionType: str
    strikePrice: int
    identifier: str
    openPrice: float
    highPrice: float
    lowPrice: float
    closePrice: int
    prevClose: float
    lastPrice: float
    change: float
    pChange: float
    numberOfContractsTraded: int
    totalTurnover: float

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        _instrumentType = str(obj.get("instrumentType"))
        _expiryDate = str(obj.get("expiryDate"))
        _optionType = str(obj.get("optionType"))
        _strikePrice = int(obj.get("strikePrice"))
        _identifier = str(obj.get("identifier"))
        _openPrice = float(obj.get("openPrice"))
        _highPrice = float(obj.get("highPrice"))
        _lowPrice = float(obj.get("lowPrice"))
        _closePrice = int(obj.get("closePrice"))
        _prevClose = float(obj.get("prevClose"))
        _lastPrice = float(obj.get("lastPrice"))
        _change = float(obj.get("change"))
        _pChange = float(obj.get("pChange"))
        _numberOfContractsTraded = int(obj.get("numberOfContractsTraded"))
        _totalTurnover = float(obj.get("totalTurnover"))
        return Metadata(_instrumentType, _expiryDate, _optionType, _strikePrice, _identifier, _openPrice, _highPrice, _lowPrice, _closePrice, _prevClose, _lastPrice, _change, _pChange, _numberOfContractsTraded, _totalTurnover)


@dataclass
class Stock:
    metadata: Metadata
    underlyingValue: float
    volumeFreezeQuantity: int
    marketDeptOrderBook: MarketDeptOrderBook

    @staticmethod
    def from_dict(obj: Any) -> 'Stock':
        _metadata = Metadata.from_dict(obj.get("metadata"))
        _underlyingValue = float(obj.get("underlyingValue"))
        _volumeFreezeQuantity = int(obj.get("volumeFreezeQuantity"))
        _marketDeptOrderBook = MarketDeptOrderBook.from_dict(obj.get("marketDeptOrderBook"))
        return Stock(_metadata, _underlyingValue, _volumeFreezeQuantity, _marketDeptOrderBook)


@dataclass
class Root:
    info: Info
    underlyingValue: float
    vfq: int
    fut_timestamp: str
    opt_timestamp: str
    stocks: List[Stock]
    strikePrices: List[int]
    expiryDates: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        try:
            _info = Info.from_dict(obj.get("info"))
            _underlyingValue = float(obj.get("underlyingValue"))
            _vfq = int(obj.get("vfq"))
            _fut_timestamp = str(obj.get("fut_timestamp"))
            _opt_timestamp = str(obj.get("opt_timestamp"))
            _stocks = [Stock.from_dict(y) for y in obj.get("stocks")]
            noDupes=[]
            [noDupes.append(i) for i in obj.get("strikePrices") if not noDupes.count(i)]
            _strikePrices = noDupes
            _strikePrices.remove(0)
            noDupes=[]
            [noDupes.append(i) for i in obj.get("expiryDates") if not noDupes.count(i)]
            _expiryDates = noDupes
            return Root(_info, _underlyingValue, _vfq, _fut_timestamp, _opt_timestamp, _stocks, _strikePrices, _expiryDates)
        except:
            traceback.print_exception(*sys.exc_info())

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
