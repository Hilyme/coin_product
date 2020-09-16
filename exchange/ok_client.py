#!/usr/bin/python
# -*- coding: utf-8 -*-

from exchange.ok_api import OkAPI
from common.Client import Client
from common.Common import Common
from retrying import retry
import datetime
import time


class OkClient(Client):

    def __init__(self):
        super().__init__()
        self.exchange_name = 'ok'

        self.__api = OkAPI(self)
        self.__trade_side = {'1': Common.open_long, '2': Common.open_short, '3': Common.close_long,
                             '4': Common.close_short}
        self.__status = {'0': Common.status_open, '1': Common.status_part_filled, '2': Common.status_filled,
                         '3': Common.status_ordering, '4': Common.status_canceling, '-1': Common.status_canceled,
                         '-2': Common.status_failure}
        self.strategy = None
        self._f_balance = dict()
        self._ws_sub = dict()
        self._orders = dict()
        self._f_ws_sub = dict()
        self._last_kline = dict()

    def f_instrument_info(self):
        """
        参数名	参数类型	描述
        instrument_id	String	合约ID，如BTC-USD-180213,BTC-USDT-191227
        underlying	String	标的指数，如：BTC-USD
        base_currency	String	交易货币，如：BTC-USD中的BTC ,BTC-USDT中的BTC
        quote_currency	String	计价货币币种，如：BTC-USD中的USD ,BTC-USDT中的USDT
        settlement_currency	String	盈亏结算和保证金币种，如BTC
        contract_val	String	合约面值(美元)
        listing	String	上线日期
        delivery	String	交割日期
        tick_size	String	下单价格精度
        trade_increment	String	下单数量精度
        alias	String	本周 this_week
        次周 next_week
        季度 quarter
        次季度 bi_quarter
        is_inverse	String	true or false ,是否 币本位保证金合约
        contract_val_currency	String	合约面值计价币种 如 usd，btc，ltc，etc xrp eos
        """
        res = None
        result = []
        try:
            res = self.__api.f_instruments()
            for ins in res:
                amount_precision = int(ins['trade_increment'])
                price_precision = float(ins['tick_size'])
                ins_info = {
                    'exchange': self.exchange_name,
                    'symbol': ins['underlying'],
                    'instrument_id': ins['instrument_id'],
                    'amount_precision': amount_precision,
                    'price_precision': price_precision,
                    'contract_type': ins['alias']
                }
                result.append(ins_info)
        except Exception as e:
            print('f_instrument_info--异常--ok', e, res)
        return result

    @retry(stop_max_attempt_number=3)
    def f_trade(self, instrument_id, side, price, amount, client_oid=''):
        try:
            for k, v in self.__trade_side:
                if v == side:
                    side = k
                    break
            res = None
            num = 0
            while num < 3:
                res = self.__api.f_trade(instrument_id, side, price, amount, client_oid)
                if 'code' in res:
                    time.sleep(2)
                    if res['code'] == 32019:
                        num += 1
                        last, buy, sell = self.f_ticker(instrument_id)
                        price = last
                    else:
                        break
                else:
                    break
            print('f_trade-------res', res)
            order_id = res['client_oid']
            return order_id
        except Exception as e:
            time.sleep(1)
            raise Exception(e)

    def f_order_info(self, instrument_id, client_oid):
        try:
            res = self.__api.f_order_info(instrument_id, client_oid)
            print('f_order_info-------res', res)
            instrument_id = res['instrument_id']
            order_id = res['order_id']
            status = self.__status[res['state']]
            side = res['type']
            side = self.__trade_side[side]
            amount = int(res['size'])
            filled_amount = int(res['filled_qty'])
            fee = float(res['fee'])
            init_price = float(res['price'])
            price = float(res['price_avg'])
            client_oid = res['client_oid']
            data = {'instrument_id': instrument_id, 'order_id': order_id, 'status': status, 'side': side,
                    'amount': amount, 'filled_amount': filled_amount, 'price': price, 'init_price': init_price,
                    'fee': fee, 'client_oid': client_oid}
            return data
        except Exception as e:
            time.sleep(1)
            raise Exception(e)

    def f_cancel_order(self, instrument_id, order_id):
        try:
            res = self.__api.f_cancel_order(instrument_id, order_id)
            if not res['result']:
                raise Exception(res)
        except Exception as e:
            raise Exception(e)

    @retry(stop_max_attempt_number=3)
    def f_ticker(self, instrument_id):

        try:
            res = self.__api.f_ticker(instrument_id)
            last = float(res['last'])
            bid = float(res['best_bid'])
            ask = float(res['best_ask'])
            return last, bid, ask
        except Exception as e:
            time.sleep(1)
            raise Exception(e)

    def f_depth(self, instrument_id):

        try:
            res = self.__api.f_depth(instrument_id)
            data = {'bids': res['bids'], 'asks': res['asks']}
            return data
        except Exception as e:
            raise Exception(e)

    def f_kline(self, instrument_id, interval, number=300):
        try:
            if number <= 300:
                res = self.__api.f_kline(instrument_id, interval)
                res.reverse()
                return res
            else:
                result = list()
                end = datetime.datetime.utcnow().isoformat() + 'Z'
                flag = True
                while flag:
                    res = self.__api.f_kline(instrument_id, interval, end)
                    result.extend(res)
                    if len(result) >= number or len(res) < 300:
                        flag = False
                    else:
                        end = res[-1][0]
                        result.pop(-1)

                result.reverse()
                return result
        except Exception as e:
            raise Exception(e)

    def f_account(self, instrument_id):
        try:
            res = self.__api.f_account(instrument_id)
            contracts = res['contracts']
            contract = contracts[0]
            amount = float(contract['available_qty'])
            return amount
        except Exception as e:
            print('异常了-f_account', e)

    @retry(stop_max_attempt_number=3)
    def f_position(self, instrument_id):
        try:
            res = self.__api.f_position(instrument_id)
            res = res['holding']
            position = res[0]
            amount_l = int(position['long_avail_qty'])
            amount_s = int(position['short_avail_qty'])
            last = float(position['last'])
            data = {'long': amount_l, 'short': amount_s, 'last': last}
            return data
        except Exception as e:
            time.sleep(1)
            print('异常了-f_position', e)

    def ws_f_ticker(self, message):
        try:
            for i in message:
                instrument_id = i['instrument_id']
                data = {'instrument_id': instrument_id, 'last': i['last'], 'bid': i['best_bid'], 'ask': i['best_ask'],
                        'time': i['timestamp']}
                self.strategy.ws_ticker(self, data)
        except Exception as e:
            print('异常了-ws_f_ticker', e, message)

    def ws_f_kline(self, message):
        try:
            kline = message['table']
            l = len(kline) - 1
            interval = int(kline[14:l])
            message = message['data']
            for i in message:
                instrument_id = i['instrument_id']
                candle = i['candle']
                last_k = candle[0]

                data = {'exchange': self.exchange_name, 'instrument_id': instrument_id, 'interval': interval,
                        'time': last_k[0], 'open': float(last_k[1]), 'high': float(last_k[2]), 'low': float(last_k[3]),
                        'close': float(last_k[4])}
                self.strategy.ws_kline(self, data)

        except Exception as e:
            print('异常了-ws_f_kline', e, message)

    def ws_f_order(self, message):
        try:
            for i in message:
                instrument_id = i['instrument_id']
                order_id = i['order_id']
                status = self.__status[i['state']]
                side = i['type']
                side = self.__trade_side[side]
                amount = int(i['size'])
                filled_amount = int(i['filled_qty'])
                fee = float(i['fee'])
                init_price = float(i['price'])
                price = float(i['price_avg'])
                client_oid = i['client_oid']

                data = {'instrument_id': instrument_id, 'order_id': order_id, 'status': status, 'side': side,
                        'amount': amount, 'filled_amount': filled_amount, 'price': price, 'init_price': init_price,
                        'fee': fee, 'client_oid': client_oid}
                self._orders[instrument_id] = data
                self.strategy.ws_order(self, data)
        except Exception as e:
            print('异常了-ws_f_order', e, message)

    def ws_f_account(self, message):
        try:
            for i in message:
                for k, v in i.items():
                    contracts = v['contracts']
                    for avail in contracts:
                        self._f_balance[k] = float(avail['available_qty'])
                        # do something
            print('ws_f_account', self._f_balance)
        except Exception as e:
            print('异常了--ws_account', e, message)

    def ws_f_position(self, message):
        try:
            for i in message:
                instrument_id = i['instrument_id']
                data = {'instrument_id': instrument_id, 'long': int(i['long_avail_qty']),
                        'short': int(i['short_avail_qty']), 'last': float(i['last'])}
                self.strategy.ws_position(self, data)
        except Exception as e:
            print('异常了-ws_f_position', e, message)

    def get_instrument_id(self, instruments, symbol, contract_type):
        for instrument in instruments:
            if instrument['symbol'] == symbol and instrument['contract_type' == contract_type]:
                return instrument['instrument_id']

    def ws_f_sub(self, subs):
        instruments = self.f_instrument_info()
        for sub in subs:
            instrument_id = self.get_instrument_id(instruments, sub.symbol, sub.contract_type)
            sub.instrument_id = instrument_id
        self.__api.ws_sub(subs)

    def ws_f_unsub(self, unsubs):
        instruments = self.f_instrument_info()
        for unsub in unsubs:
            instrument_id = self.get_instrument_id(instruments, unsub.symbol, unsub.contract_type)
            unsub.instrument_id = instrument_id
        self.__api.ws_unsub(unsubs)


if __name__ == '__main__':
    client = OkClient()
    instrument_info = client.f_instrument_info()
    print(instrument_info)
