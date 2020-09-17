from common.Common import Common
from exchange.SubConfig import SubConfig
from exchange.ok_client import OkClient
from strategy.strategy import Strategy
import numpy as np
import talib


class Test(Strategy):

    def __init__(self):
        super().__init__()
        self.exchanges = []
        ok = OkClient()
        ok.strategy = self
        self.exchanges.append(ok)
        self.sub_symbol = ['BTC-USD', 'XRP-USD']
        self.sub_contract_type = ['this_week', 'next_week']
        self.sub_frequency = [Common.frequency_1min, Common.frequency_tick]

    def start(self):
        super().start()
        subs = []
        for i in self.exchanges:
            for symbol in self.sub_symbol:
                for contract_type in self.sub_contract_type:
                    for frequency in self.sub_frequency:
                        sub = SubConfig(symbol, contract_type, frequency)
                        subs.append(sub)
            i.ws_f_sub(subs)
        return

    def ws_ticker(self, exchange, ws_data):
        print("--------------------", self, "ws_ticker------------------")
        print(type(exchange), ws_data)

    def ws_kline(self, exchange, ws_data, kline=None):
        print("===================", self, "ws_kline====================")
        instrument_id = ws_data['instrument_id']
        frequency = ws_data['interval']
        bob = ws_data['time']
        open = ws_data['open']
        high = ws_data['high']
        low = ws_data['low']
        close = ws_data['close']
        vol = ws_data['vol']
        print("instrument_id = ", instrument_id)
        print("frequency = ", frequency)
        print("bob = ", bob)
        print("open = ", open)
        print("high = ", high)
        print("low = ", low)
        print("close = ", close)
        print("vol = ", vol)
