import math, time
from common.Common import Common
from strategy.strategy import Strategy
import numpy as np
import talib

MA1 = 5
MA2 = 200


class Test(Strategy):

    def __init__(self):
        super().__init__()

    def start(self):
        super().start()

        for i in self.manage.exchanges.values():

            i.d_ws_sub(self,['BTC_USDT'],{Common.ws_ticker:''})

        return

        exchange = self.manage.exchanges['OkClient']
        self.test8(exchange, 'BTC','USDT')

        return

        res = DB.find(Common.db_analyze)

        for i in res:
            print(i['coin'], i['fund'])
            exchange = self.manage.exchanges[i['exchange']]
            self.test7(exchange, i['coin'], i['fund'])
            time.sleep(1)

        # 测试一下，10%止损，如果涨回止损价重新买入

    def ws_kline(self, exchange, ws_data, kline=None):
        print(11,ws_data)

    def ws_ticker(self,exchange,ws_data):

        print(exchange.className,ws_data)

    def test8(self, exchange, coin, fund):

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        #periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.01
        stop_profit = 0.01

        for period in periods:

            kline = exchange.kline(coin, fund, period, 2000)

            aaa = [4, 6, 8, 10, 12, 15, 16, 20, 30, 50, 60, 90, 120]

            for aa in aaa:

                k = []
                init_money = 10000
                money = 10000
                buy_price = None
                sell_price = None
                stop_price = None
                amount = None
                item_num = 0
                last_price = None
                side = 'buy'
                trend = None

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])
                    price = close

                    if ii < aa:
                        k.append(price)
                        continue

                    k_max = max(k)
                    k_min = min(k)
                    if price > k_max:
                        trend = 'buy'
                    elif price < k_min:
                        trend = 'sell'
                    else:
                        trend = None

                    k.append(price)
                    k.pop(0)

                    if side == 'buy':

                        if trend == 'buy':
                            side = 'sell'
                            buy_price = price
                            last_price = price
                            stop_price = buy_price * (1 - stop_loss)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                            # print('trend=buy时 money：', money, ii,i,'buy_price：',buy_price)

                    elif side == 'sell':

                        if price < stop_price:

                            last_money = money

                            money = amount * price
                            money = (1 - fee) * money

                            side = ''

                            rate = '{:.4%}'.format((money - last_money) / last_money)
                            # print('trend=sell时 times：', item_num, 'last_money：', last_money, 'money：', money, 'rate: ', rate, ii, i, 'buy_price：', buy_price, 'close：', close)

                        else:

                            if price > last_price:

                                last_price = price
                                s_p = (1 - stop_profit) * last_price

                                if s_p > buy_price:
                                    stop_price = s_p

                    elif side == '':

                        if price >= stop_price:

                            side = 'sell'
                            buy_price = price
                            last_price = price
                            stop_price = buy_price * (1 - stop_loss)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                if side == 'sell':
                    money = amount * price
                    money = (1 - fee) * money

                rate = '{:.4%}'.format((money - init_money) / init_money)
                print('period：', period,'k:',aa, '         times：', item_num, '          money：', money, 'rate: ', rate,len(kline))
            print('')
            print('')
            print('')
            time.sleep(1)

    def test7(self, exchange, coin, fund):

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]


        #periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.01
        stop_profit = 0.01

        for period in periods:

            kline = exchange.kline(coin, fund, period, 2000)

            aaa = [4, 6, 8, 10, 12, 15, 16, 20, 30, 50, 60, 90, 120]

            for aa in aaa:

                k = []
                init_money = 10000
                money = 10000
                buy_price = None
                sell_price = None
                stop_price = None
                amount = None
                item_num = 0
                last_price = None
                side = 'buy'
                trend = None

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])
                    price = close

                    if ii < aa:
                        k.append(price)
                        continue

                    k_max = max(k)
                    k_min = min(k)
                    if price > k_max:
                        trend = 'buy'
                    elif price < k_min:
                        trend = 'sell'
                    else:
                        trend = None

                    k.append(price)
                    k.pop(0)

                    if side == 'buy':

                        if trend == 'buy':
                            side = 'sell'

                            buy_price = price
                            last_price = price
                            stop_price = buy_price * (1 - stop_loss)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                            # print('trend=buy时 money：', money, ii,i,'buy_price：',buy_price)

                    elif side == 'sell':

                        if price < stop_price:

                            last_money = money

                            money = amount * price
                            money = (1 - fee) * money

                            side = 'buy'

                            rate = '{:.4%}'.format((money - last_money) / last_money)
                            # print('trend=sell时 times：', item_num, 'last_money：', last_money, 'money：', money, 'rate: ', rate, ii, i, 'buy_price：', buy_price, 'close：', close)

                        else:

                            if price > last_price:

                                last_price = price
                                s_p = (1 - stop_profit) * last_price

                                if s_p > buy_price:
                                    stop_price = s_p

                if side == 'sell':
                    money = amount * price
                    money = (1 - fee) * money

                rate = '{:.4%}'.format((money - init_money) / init_money)
                print('period：', period,'k:',aa, '         times：', item_num, '          money：', money, 'rate: ', rate,len(kline))
            print('')
            print('')
            print('')
            time.sleep(1)

    def test6(self, exchange, coin, fund):

        #反马丁格尔策略

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        #periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001

        for period in periods:

            kline = exchange.kline(coin, fund, period, 2000)
            #kline = exchange.f_kline('ETH-USD-190628',period,3000)

            init_money = 10000
            money = 10000
            amount = 0
            item_num = 0
            aa = [5,10,20,30,50,100,200]

            for aaa in aa:

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])
                    price = close

                    if ii == 0:
                        money = init_money / 2
                        amount = money / price
                        continue

                    nnn = ii % aaa
                    if nnn != 0:
                        continue

                    mm = amount * price

                    if mm > money:
                        m3 = (mm + money) / 2
                        m4 = mm - m3
                        a1 = m4 / price
                        amount = amount - a1
                        money = money + m4

                        item_num += 1

                        #print('>',item_num,money,amount * price)

                    elif mm < money:

                        m3 = (mm + money) / 2
                        m4 = money - m3
                        al = m4 / price
                        amount = amount + al
                        money = money - m4

                        item_num += 1

                        #print('<', item_num, money, amount * price)

                money = amount * price + money
                rate = '{:.4%}'.format((money - init_money) / init_money)
                print('period：', period,'aaa：',aaa, '         times：', item_num, '          amount：', money, 'rate: ', rate,len(kline))
                print('')
                print('')
                print('')
                time.sleep(1)


    def test5(self, exchange, coin, fund):

        #动态平衡策略

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        #periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001

        for period in periods:

            kline = exchange.kline(coin, fund, period, 2000)
            #kline = exchange.f_kline('ETH-USD-190927',period,3000)

            init_money = 10000
            money = 10000
            amount = 0
            item_num = 0
            aa = [5,10,20,30,50,100,200]

            for aaa in aa:

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])
                    price = close

                    if ii == 0:
                        money = init_money / 2
                        amount = money / price
                        continue

                    nnn = ii % aaa
                    if nnn != 0:
                        continue

                    mm = amount * price

                    if mm > money:
                        m3 = (mm + money) / 2
                        m4 = mm - m3
                        a1 = m4 / price
                        amount = amount - a1
                        money = money + m4

                        item_num += 1

                        #print('>',item_num,money,amount * price)

                    elif mm < money:

                        m3 = (mm + money) / 2
                        m4 = money - m3
                        al = m4 / price
                        amount = amount + al
                        money = money - m4

                        item_num += 1

                        #print('<', item_num, money, amount * price)

                money = amount * price + money
                rate = '{:.4%}'.format((money - init_money) / init_money)
                print('period：', period,'aaa：',aaa, '         times：', item_num, '          amount：', money, 'rate: ', rate,len(kline))
                print('')
                print('')
                print('')
                time.sleep(1)

    def test4(self, exchange, coin, fund):

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.003
        stop_profit = stop_loss

        for period in periods:

            #kline = exchange.kline(coin, fund, period, 2000)
            kline = exchange.f_kline('ETH-USD-190628',period,3000)
            l = len(kline) - 1000
            kline = kline[l:]

            aaa = [6]

            for aa in aaa:

                bb = int(aa / 2)
                print('aa', aa, bb)

                k = []
                k_stop = []

                init_money = 30000
                money = 30000
                balance = 30000
                buy_price = None
                sell_price = None
                stop_price = None
                amount = 0
                item_num = 0
                last_price = None
                side = 'buy'

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])

                    if ii < aa - 1:
                        k.append(close)
                        continue

                    trend = ''
                    k.append(close)
                    if len(k) > aa:
                        k.pop(0)

                    left = True
                    right = True
                    last_v = k[0]
                    cc = k[1:bb]
                    for dd in cc:
                        if dd > last_v:
                            last_v = dd
                        else:
                            left = False
                            break

                    last_v = k[bb]
                    cc = k[bb+1:]
                    for dd in cc:
                        if dd < last_v:
                            last_v = dd
                        else:
                            right = False
                            break

                    if left and right:
                        trend = 'sell'

                    left = True
                    right = True
                    last_v = k[0]
                    cc = k[1:bb]
                    for dd in cc:
                        if dd < last_v:
                            last_v = dd
                        else:
                            left = False
                            break

                    last_v = k[bb]
                    cc = k[bb + 1:]
                    for dd in cc:
                        if dd > last_v:
                            last_v = dd
                        else:
                            right = False
                            break

                    if left and right:
                        trend = 'buy'

                    if side == 'buy':

                        if trend == 'buy':
                            side = 'sell'

                            money = int(balance / 3)
                            balance = balance - money

                            buy_price = close
                            last_price = close
                            stop_price = buy_price * (1 - stop_loss)
                            low_profit_price = buy_price * (stop_loss * 3 + 1)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                            print('trend=buy时 money：', money, ii,i,'buy_price：',buy_price)


                    elif side == 'sell':

                        if close < stop_price or trend == 'sell':

                            last_money = money

                            money = amount * close

                            money = (1 - fee) * money

                            balance = balance + money

                            side = 'buy'

                            rate = '{:.4%}'.format((money - last_money) / last_money)

                            print('trend=sell时 times：', item_num, 'last_money：', last_money, 'money：', money, 'rate: ', rate, ii, i, 'buy_price：', buy_price, 'close：', close)


                        else:

                            if close > last_price:

                                last_price = close

                                s_p = (1 - stop_profit) * last_price

                                if last_price > low_profit_price:
                                    stop_price = s_p

                if side == 'sell':
                    money = amount * close
                    money = money + balance
                else:
                    money = balance

                rate = '{:.4%}'.format((money - init_money) / init_money)
                print('period：', period, '         times：', item_num, '          amount：', money, 'rate: ', rate,
                      len(kline))
            print('')
            print('')
            print('')
            time.sleep(1)

    def test3(self, exchange, coin, fund):


        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        periods = [Common.kline_1m]
        fee = 0.0003
        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.003
        stop_profit = stop_loss

        for period in periods:

            kline = exchange.kline(coin,fund, period,2000)
            #kline = exchange.f_kline('ETH-USD-190628',period,2000)

            aaa = [4,6,8,10,12,15,16,20,30,50,60,90,120]

            for aa in aaa:

                bb = int(aa / 2)
                print('aa',aa,bb)

                k = []
                k_stop = []

                init_money = 30000
                money = 30000
                balance = 30000
                buy_price = None
                sell_price = None
                stop_price = None
                amount = None
                item_num = 0
                last_price = None
                side = 'buy'

                for ii, i in enumerate(kline):

                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])

                    if ii < aa:
                        k.append(close)
                        continue

                    trend = ''
                    k.append(close)


                    k_max = max(k)
                    index = k.index(k_max)
                    if index == bb:
                        left = True
                        right = True
                        last_v = k[0]
                        cc = k[1:bb+1]
                        for dd in cc:
                            if dd > last_v:
                                last_v = dd
                            else:
                                left = False
                                break

                        last_v = k_max
                        cc = k[bb+1:]
                        for dd in cc:
                            if dd < last_v:
                                last_v = dd
                            else:
                                right = False
                                break

                        if left and right:
                            trend = 'sell'

                    k_min = min(k)
                    index = k.index(k_min)
                    if index == bb:
                        left = True
                        right = True
                        last_v = k[0]
                        cc = k[1:bb + 1]
                        for dd in cc:
                            if dd < last_v:
                                last_v = dd
                            else:
                                left = False
                                break

                        last_v = k_min
                        cc = k[bb + 1:]
                        for dd in cc:
                            if dd > last_v:
                                last_v = dd
                            else:
                                right = False
                                break

                        if left and right:
                            trend = 'buy'

                    k.pop(0)

                    if side == 'buy':

                        if trend == 'buy':

                            side = 'sell'

                            money = int(balance / 3)
                            balance = balance - money

                            buy_price = close
                            last_price = close
                            stop_price = buy_price * (1 - stop_loss)
                            low_profit_price = buy_price * (stop_loss * 3 + 1)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                            #print('trend=buy时 money：', money, ii,i,'buy_price：',buy_price)

                    elif side == 'sell':

                        if close < stop_price or trend=='sell':

                            last_money = money
                            money = amount * close
                            money = (1 - fee) * money
                            balance = balance + money

                            side = 'buy'

                            rate = '{:.4%}'.format((money - last_money) / last_money)
                            #print('trend=sell时 times：', item_num, 'last_money：', last_money, 'money：', money, 'rate: ', rate, ii, i, 'buy_price：', buy_price, 'close：', close)

                        else:

                            if close > last_price:

                                last_price = close
                                s_p = (1 - stop_profit) * last_price

                                if last_price > low_profit_price:
                                    stop_price = s_p



                    '''
                    if trend == 'sell':

                            last_money = money
                            money = amount * close
                            money = (1 - fee) * money
                            balance = balance + money

                            side = 'buy'

                            rate = '{:.4%}'.format((money - last_money) / last_money)
                            print('trend=sell时 times：', item_num, 'last_money：', last_money,'money：',money, 'rate: ', rate, ii,i,'buy_price：',buy_price,'close：',close)

   
                            

                        elif trend == '':
                            c_m = amount * close
                            c_m = (1 - fee) * c_m
                            rate = '{:.4%}'.format((c_m - money) / money)
                            #print( 'trend=空时 money：', money,'c_m：',c_m, 'rate: ', rate,ii,i,'buy_price：',buy_price,'close：',close)
                            
                    '''

                if side == 'sell':
                    money = amount * close
                    money = money + balance
                else:
                    money = balance

                rate = '{:.4%}'.format((money - init_money) / init_money)
                print( 'period：', period, '         times：', item_num, '          amount：',money,'rate: ',rate,len(kline))
            print('')
            print('')
            print('')
            time.sleep(1)

    def ws_kline_test(self, exchange, coin, fund, data):

        k = list()
        for i in data:
            k.append(float(i['close']))

        kline = np.array(k)

        print('ws_kline', kline)

        last, buy, sell = exchange.get_ticker(coin, fund)
        pair = '{}_{}'.format(coin, fund)

        ma_1 = talib.MA(kline, MA1)
        ma_2 = talib.MA(kline, MA2)



        print('MA1：', MA1, ma_1, 'MA2：', MA2, ma_2)

        if pair in self.__exchangeData.keys():

            exist_data = self.__exchangeData[pair]

            if ma_1[-1] > ma_2[-1]:
                if not exist_data['trade_state'] and exist_data['side'] == Common.trade_side_buy:

                    if exist_data['status'] == Common.status_open:
                        self.cancelOrder(exchange, coin, fund, exist_data['order_id'])

                    exist_data['auto_trade'] = True
                    self.buy(exchange, coin, fund, buy)

            elif ma_1[-1] < ma_2[-1]:
                if not exist_data['trade_state'] and exist_data['side'] == Common.trade_side_sell:

                    if exist_data['status'] == Common.status_open:
                        self.cancelOrder(exchange, coin, fund, exist_data['order_id'])

                    exist_data['auto_trade'] = True
                    self.sell(exchange, coin, fund, sell)
        else:
            if ma_1[-1] > ma_2[-1]:
                self.buy(exchange, coin, fund, buy)
            elif ma_1[-1] < ma_2[-1]:
                self.sell(exchange, coin, fund, sell)

    def test(self, exchange, coin, fund):

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]
        #periods = [Common.kline_30m]
        num_list = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 25, 30, 45, 50, 60, 70, 80, 90, 100, 110,
                    120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310,
                    320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510,
                    520, 530, 540, 550, 560, 570, 580, 590, 600]
        # num_list = [20]
        fee = 0.0015
        k5_value = 5

        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.04
        stop_profit = 0.04

        for period in periods:

            kline = exchange.kline(coin, fund, period)
            #kline = kline[:192]
            kline.reverse()

            trends = ['long','short']

            for trend in trends:

                money = 10000
                borrow_money = 0
                side = 'buy' if trend == 'long' else 'sell'
                buy_price = None
                sell_price = None
                stop_price = None
                amount = None
                item_num = 0
                price = 1
                last_price = None

                for index, i in enumerate(kline):

                    price = float(i[4])
                    high = float(i[2])
                    low = float(i[3])

                    if trend == 'long':
                        if side == 'buy':
                            side = 'sell'
                            buy_price = price
                            last_price = buy_price
                            stop_price = buy_price * (1 - stop_loss)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                        else:
                            if price > stop_price:

                                if price > last_price:

                                    last_price = price
                                    s_p = (1 - stop_profit) * price
                                    if s_p > buy_price:
                                        stop_price = s_p
                            else:

                                price = stop_price
                                money = amount * price
                                money = (1 - fee) * money

                                trend = 'short'
                                side = 'buy'
                                sell_price = price
                                last_price = sell_price
                                stop_price = sell_price * (1 + stop_loss)
                                borrow_money = money
                                amount = borrow_money / sell_price
                                amount = (1 - fee) * amount
                                item_num += 1
                    else:
                        if side == 'buy':

                            if price < stop_price:

                                if price < last_price:
                                    last_price = price
                                    s_p = (1 + stop_profit) * price
                                    if s_p < sell_price:
                                        stop_price = s_p
                            else:

                                price = stop_price
                                sell_money = amount * price
                                sell_money = (1 - fee) * sell_money
                                money = money + sell_money - borrow_money

                                trend = 'long'
                                side = 'sell'
                                buy_price = price
                                last_price = buy_price
                                stop_price = buy_price * (1 - stop_loss)
                                amount = money / buy_price
                                amount = (1 - fee) * amount
                                item_num += 1

                        else:

                            side = 'buy'
                            sell_price = price
                            last_price = sell_price
                            stop_price = sell_price * (1 + stop_loss)
                            borrow_money = money
                            amount = borrow_money / sell_price
                            amount = (1 - fee) * amount
                            item_num += 1

                if side == 'buy':
                    money = amount * price + money - borrow_money
                else:
                    money = amount * price

                print('趋势：',trend,'      周期：', period,'         总交易次数：',item_num,'          最后计算金额：',amount * price)

        """
            for num in num_list:

                data = np.empty([0, 0])
                data_h = np.empty([0, 0])
                data_l = np.empty([0, 0])
                side = 'sell'
                amount = 0
                money = 100
                buy_money = money
                sell_money = 0

                item_num = 0

                # a = {'coin':coin,'fund':fund,'money':money}
                # lever_id = DB.insert_one(Common.db_lever,a)
                # lever_exchange_id = None

                for index, i in enumerate(kline):

                    # data = np.append(data, [[float(i['open']), float(i['high']), float(i['low']), float(i['close'])]], axis=0)

                    close = float(i['close'])
                    high = float(i['high'])
                    low = float(i['low'])

                    data = np.append(data, close)
                    data_h = np.append(data, high)
                    data_l = np.append(data, low)

                    # if len(data) > num: data = np.delete(data, 0)

                    if index > num:

                        # u,m,l = talib.BBANDS(data,timeperiod=num, nbdevup=2, nbdevdn=2, matype=0)
                        # m,a,c = talib.MACD(data,fastperiod=12, slowperiod=26, signalperiod=9)

                        k5 = talib._ta_lib.MA(data, timeperiod=k5_value)
                        k10 = talib._ta_lib.MA(data, timeperiod=num)
                        k5 = Common.pricePrecision(k5[-1], price_precision)
                        k10 = Common.pricePrecision(k10[-1], price_precision)

                        sar = talib._ta_lib.SAR(data_h, data_l)
                        sar = Common.pricePrecision(sar[-1], price_precision)

                        if close > sar and k5 > k10:

                            if side == 'sell':
                                '''
                                print('买')
                                print(index)

                                print(i)

                                print(close)
                                print(k5)
                                print(k10)
                                print(sar)
                                '''

                                side = 'buy'
                                price = Common.pricePrecision(close, price_precision)
                                amount = buy_money / price
                                amount = Common.amountPrecision((1 - fee) * amount, amount_precision)

                                # lever_exchange = {'lever_id':lever_id,'side':side,'buy_price':price,'buy_money':buy_money,'buy_amount':amount}
                                # lever_exchange_id = DB.insert_one(Common.db_lever_exchange,lever_exchange)

                                item_num += 1

                        elif close < sar and k5 < k10:

                            if side == 'buy':
                                '''
                                print('卖')

                                print(index)

                                print(i)

                                print(close)
                                print(k5)
                                print(k10)
                                print(sar)
                                '''

                                side = 'sell'
                                price = Common.pricePrecision(close, price_precision)
                                sell_money = amount * price
                                sell_money = Common.pricePrecision((1 - fee) * sell_money, price_precision)

                                rate = '{}%'.format(round((sell_money - buy_money) / buy_money * 100, 4))

                                buy_money = sell_money

                                # query = {'_id': lever_exchange_id}
                                # value = {'side':side,'sell_price':price,'sell_money':sell_money,'rate':rate}
                                # DB.update(Common.db_lever_exchange, query, value)

                if side == 'buy':
                    price = close
                    sell_money = price * amount

                print('{}日线---金额：{},---------交易了{}次'.format(num, sell_money, item_num), k5_value, len(data))
                
        """

    def test2(self, exchange, coin, fund):

        periods = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m,
                   Common.kline_1h, Common.kline_2h]

        periods = [Common.kline_5m]
        fee = 0.0015
        amount_precision = 0.001
        price_precision = 0.0001
        stop_loss = 0.04
        stop_profit = 0.04

        for period in periods:

            kline = exchange.kline(coin, fund, period)
            kline.reverse()

            trends = ['long', 'short']
            k = []

            for trend in trends:

                money = 10000
                borrow_money = 0
                side = 'buy' if trend == 'long' else 'sell'
                buy_price = None
                sell_price = None
                stop_price = None
                amount = None
                item_num = 0
                price = 1
                last_price = None
                k.clear()

                for index, i in enumerate(kline):

                    price = float(i[4])
                    high = float(i[2])
                    low = float(i[3])

                    if trend == 'long':
                        if side == 'buy':
                            side = 'sell'
                            buy_price = price
                            stop_price = buy_price * (1 - stop_loss)
                            amount = money / buy_price
                            amount = (1 - fee) * amount
                            item_num += 1

                        else:

                            r = (price - last_price) / last_price
                            r = round(r * 100, 4)

                            if price > stop_price:

                                if price > last_price:

                                    last_price = price
                                    s_p = (1 - stop_profit) * price
                                    if s_p > buy_price:
                                        stop_price = s_p
                            else:

                                price = stop_price
                                money = amount * price
                                money = (1 - fee) * money

                                trend = 'short'
                                side = 'buy'
                                sell_price = price
                                stop_price = sell_price * (1 + stop_loss)
                                borrow_money = money
                                amount = borrow_money / sell_price
                                amount = (1 - fee) * amount
                                item_num += 1
                    else:
                        if side == 'buy':

                            if price < stop_price:

                                if price < last_price:
                                    s_p = (1 + stop_profit) * price
                                    if s_p < sell_price:
                                        stop_price = s_p
                            else:

                                price = stop_price
                                sell_money = amount * price
                                sell_money = (1 - fee) * sell_money
                                money = money + sell_money - borrow_money

                                trend = 'long'
                                side = 'sell'
                                buy_price = price
                                stop_price = buy_price * (1 - stop_loss)
                                amount = money / buy_price
                                amount = (1 - fee) * amount
                                item_num += 1

                        else:

                            side = 'buy'
                            sell_price = price
                            stop_price = sell_price * (1 + stop_loss)
                            borrow_money = money
                            amount = borrow_money / sell_price
                            amount = (1 - fee) * amount
                            item_num += 1
                    last_price = price
                if side == 'buy':
                    money = amount * price + money - borrow_money
                else:
                    money = amount * price

                print('趋势：', trend, '      周期：', period, '         总交易次数：', item_num, '          最后计算金额：',
                      amount * price)

    def test1(self, exchange, coin, fund):

        kline = exchange.kline(coin, fund, Common.kline_5m)
        kline.reverse()

        c = list()
        h = list()
        l = list()

        last_c = None
        aa = list()

        for index, i in enumerate(kline):
            close = float(i[4])
            c.append(close)
            high = float(i[2])
            h.append(high)
            low = float(i[3])
            l.append(low)

            #rate = '{}%'.format(round((price - buy_price) / buy_price * 100, 4))
            #rateh = '{}%'.format(round((high - buy_price) / buy_price * 100, 4))
            #ratel = '{}%'.format(round((low - buy_price) / buy_price * 100, 4))

            #print(rate, rateh, ratel)

            if last_c:

                r = (close - last_c) / last_c
                r = round(r * 100, 4)
                aa.append(r)


            last_c = close
        r_h = '{}%'.format(max(aa))
        r_l = '{}%'.format(min(aa))
        print(r_h,r_l)
        #a = max(l)
        #i = l.index(a)
       # print(a,i,kline[i])


    def inspectMarket(self, exchange, coin, fund):

        try:
            last, buy, sell = exchange.ticker(coin, fund)

            t = [Common.kline_1m, Common.kline_3m, Common.kline_5m, Common.kline_15m, Common.kline_30m, Common.kline_1h,
                 Common.kline_2h, Common.kline_4h]
            tt = ['1分钟', '3分钟', '5分钟', '15分钟', '30分钟', '1小时', '2小时', '4小时']

            percents = list()
            p1 = list()
            p2 = list()
            p3 = list()

            for index, item in enumerate(t):

                percents.clear()
                p1.clear()
                p2.clear()
                p3.clear()

                p1_max_num = 0
                p1_min_num = 0
                p1_num = 0

                p2_max_num = 0
                p2_min_num = 0
                p2_num = 0

                kline = exchange.kline(coin, fund, item)
                # print(len(kline),kline)

                for i in kline:

                    high = float(i['high'])
                    low = float(i['low'])
                    open = float(i['open'])
                    close = float(i['close'])

                    percent = round((high - low) / open, 4) * 100
                    percents.append(percent)

                    percent = round((high - open) / open, 4) * 100
                    p1.append(percent)

                    if high > open:
                        p1_max_num += 1
                    elif high < open:
                        p1_min_num += 1
                    else:
                        p1_num += 1

                    percent = round((low - open) / open, 4) * 100
                    p2.append(percent)

                    percent = round((close - open) / open, 4) * 100
                    p3.append(percent)

                    if close > open:
                        p2_max_num += 1
                    elif close < open:
                        p2_min_num += 1
                    else:
                        p2_num += 1

                print(tt[index])
                print('平均波动：{}%'.format(math.fsum(percents) / len(kline)))
                print('最大波动：{}%'.format(max(percents)))
                print('最小波动：{}%'.format(min(percents)))

                print('相比开盘价涨幅数量：{}'.format(p1_max_num))
                print('相比开盘价平均涨幅：{}%'.format(math.fsum(p1) / len(kline)))
                print('相比开盘价最大涨幅：{}%'.format(max(p1)))
                print('相比开盘价最小涨幅：{}%'.format(min(p1)))

                print('相比开盘价涨幅数量：{}'.format(p1_min_num))
                print('相比开盘价平均跌幅：{}%'.format(math.fsum(p2) / len(kline)))
                print('相比开盘价最大跌幅：{}%'.format(min(p2)))
                print('相比开盘价最小跌幅：{}%'.format(max(p2)))

                print('相比开盘价涨跌幅为0数量：{}'.format(p1_num))

                print('相比开盘价-收盘价--涨幅数量：{}'.format(p2_max_num))
                print('相比开盘价-收盘价--跌幅数量：{}'.format(p2_min_num))
                print('相比开盘价-收盘价--相等数量：{}'.format(p2_num))
                print('相比开盘价-收盘价--平均幅度：{}%'.format(math.fsum(p3) / len(kline)))
                print('相比开盘价-收盘价--最大幅度：{}%'.format(min(p3)))
                print('相比开盘价-收盘价--最小幅度：{}%'.format(max(p3)))

                print('')
                print('')

                time.sleep(5)

        except Exception as e:
            self.errorPrint('executeStrategy', exchange, e)

    def trend(self, exchange, coin, fund, price, trend):

        try:
            borrow_coin = fund if trend == Common.trend_long else coin
            data = exchange.leverAccount(coin, fund)

            borrow_avail = data['borrow_avail']
            borrow_avail_num = float(borrow_avail[borrow_coin]['available'])

            balance = data['balance']
            balance_num = float(balance[borrow_coin]['available'])
            print('可借：', borrow_coin, borrow_avail_num)
            print('当前账户可以用', balance_num)

            return

            order = {'trend': trend}

            if trend == Common.trend_long:
                money = borrow_avail + avail
                amount = Common.amountPrecision(money / price, coin)
                self.buy(exchange, coin, fund, price, amount, order)

            else:

                amount = Common.amountPrecision(borrow_avail + avail, coin)
                self.sell(exchange, coin, fund, price, amount, order)

        except Exception as e:

            self.errorPrint('trend', exchange, e)

    def errorPrint(self, func, exchange, e):

        print('异常了---%s--%s' % (func, exchange.className), e)
