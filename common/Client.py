#!/usr/bin/python
# -*- coding: utf-8 -*-


class Client(object):

    def __init__(self):
        # print('%s-----函数---%s' % (str(self), sys._getframe().f_code.co_name))
        pass

    def loadData(self, data):
        pass

    def get_balance(self, coin, amount=0):
        pass

    def get_l_balance(self, coin, fund, balance_coin):
        pass

    def get_ticker(self, coin, fund):
        pass

    def ws_sub(self, strategy, coin, fund, subs):
        pass

    def ws_unsub(self, strategy, coin, fund, subs):
        pass

    def ticker(self, pair):
        pass

    def coin_pair(self):
        pass

    def ws_ticker(self, message):
        pass

    def ws_account(self, message):
        pass

    def ws_l_account(self, message):
        pass

    def account(self, coin):
        pass

    def buy(self, coin, fund, price, amount):
        pass

    def sell(self, coin, fund, price, amount):
        pass

    def order(self, coin, fund, orderid):
        pass

    def ws_order(self, message):
        pass

    def ws_trade(self, message):
        pass

    def orders(self, coin, fund, status):
        pass

    def kline(self, coin, fund, interval, start, end):
        pass

    def ws_kline(self, message):
        pass

    def cancelOrder(self, coin, fund, orderid):
        pass

    def l_accounts(self):
        pass

    def l_account(self, coin, fund):
        pass

    def l_buy(self, coin, fund, price, amount):
        pass

    def l_sell(self, coin, fund, price, amount):
        pass

    def l_order(self, coin, fund, orderid):
        pass

    def l_cancelOrder(self, coin, fund, orderid):
        pass

    def l_borrow(self, coin, fund, borrow_coin, amount):
        pass

    def l_borrowed(self, coin, fund, status=0):
        pass

    def l_repay(self, coin, fund, repay_coin):
        pass

    def l_availability(self, coin, fund):
        pass

    def ws_depth(self, message):
        pass

    def ws_f_ticker(self, message):
        pass

    def ws_f_kline(self, message):
        pass

    def ws_f_order(self, message):
        pass

    def ws_f_account(self, message):
        pass

    def ws_f_position(self, message):
        pass

    def __del__(self):
        pass
        # print('%s-----函数---%s' % (str(self), sys._getframe().f_code.co_name))
