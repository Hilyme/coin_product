from common.Common import Common
import asyncio,threading,time,logging,sys
from datetime import datetime

ETF_AMOUNT = 1050


class Etf:

    def __init__(self):

        self._exchange = HbClient()
        self._etf_coins = dict()
        self._swap = None
        self._exchange_data = []
        self._open = []
        self._etf_config = {}
        self._thread = None
        self._etf_rate_in = -10
        self._etf_rate_out = 10

    def start(self):

        res = self._exchange.etf_config()
        p = ['HB10_USDT']
        self._etf_config['HB10_USDT'] = {'count':1}
        unit = res['unit_price']
        for i in unit:
            pair = i['coin'] + '_USDT'
            p.append(pair)
            self._etf_config[pair] = {'count': i['amount']}

        query = {'exchange': 'HbClient', 'pair': {'$in': p}}
        res = DB.find(Common.db_coin_pair, query)
        for i in res:
            self._etf_config[i['pair']].update({'amount_precision':i['amount_precision'],'price_precision':i['price_precision'],'min_amount':i['min_amount']})

        self._exchange.d_ws_sub(self,p,{Common.ws_order:'',Common.ws_depth:''})

    def ws_depth(self,exchange,ws_data):

        pair = ws_data['pair']
        buy = ws_data['buy']
        sell = ws_data['sell']
        config = self._etf_config[pair]
        count = config['count'] * ETF_AMOUNT

        num = 0
        for i in sell:
            if num >= count:
                buy_price = i[0]
                break
            num += i[1]

        num = 0
        for i in buy:
            if num >= count:
                sell_price = i[0]
                break
            num += i[1]

        buy_money = count * buy_price
        sell_money = count * sell_price

        if len(self._etf_coins) < 11:
            if pair not in self._etf_coins:
                self._etf_coins[pair] = {'coin': pair.split('_')[0], 'amount': 0, 'buy_price': buy_price,'sell_price':sell_price,
                                         'count': config['count'], 'buy_money': buy_money,'sell_money':sell_money,
                                         'amount_precision': config['amount_precision'],
                                         'price_precision': config['price_precision'],
                                         'min_amount': config['min_amount']}

            return

        data = self._etf_coins[pair]
        data.update({'buy_money': buy_money,'sell_money':sell_money})

        if self._swap:
            return

        bm = 0
        hb10_bm = 0
        sm = 0
        hb10_sm = 0
        for k, v in self._etf_coins.items():

            if k == 'HB10_USDT':
                hb10_bm = v['buy_money']
                hb10_sm = v['sell_money']
            else:
                bm += v['buy_money']
                sm += v['sell_money']

        in_rate = hb10_sm / bm - 1
        out_rate = hb10_bm / sm - 1

        if in_rate > self._etf_rate_in:
            logging.info(f'in---{hb10_sm}----{bm}---=={in_rate}')

            self._etf_rate_in = in_rate
        elif out_rate < self._etf_rate_out:
            logging.info(f'out---{hb10_bm}----{sm}---=={out_rate}')

            self._etf_rate_out = out_rate

        if in_rate > 0.0082:

            self._swap = 'in'
            self._exchange.d_ws_close()

            tasks = []
            for k, v in self._etf_coins.items():
                if k != 'HB10_USDT':
                    amount = v['count'] * ETF_AMOUNT
                    amount = amount / 0.997
                    amount = Utility.precison_value(v['amount_precision'], amount)
                    amount = amount + Utility.precision(v['amount_precision'])
                    amount = Utility.precison_value(v['amount_precision'], amount)

                    price = v['buy_price']
                    price = Utility.precison_value(v['price_precision'], price)

                    tasks.append({'coin': v['coin'], 'price': price, 'amount': amount})

            self.async_task(self.buy, tasks)

        elif out_rate < -0.0092:

            self._swap = 'out'
            self._exchange.d_ws_close()

            v = self._etf_coins['HB10_USDT']
            amount = ETF_AMOUNT / 0.996
            amount = Utility.precison_value(v['amount_precision'], amount)
            amount = amount + Utility.precision(v['amount_precision'])
            amount = Utility.precison_value(v['amount_precision'], amount)

            price = v['buy_price']
            price = Utility.precison_value(v['price_precision'], price)

            self.buy({'coin': 'HB10', 'price': price, 'amount': amount})

            # Utility.email_analyze(text)

    def ws_trade(self,exchange,ws_data):

        try:
            pair = ws_data['pair']
            price = ws_data['price']

            if len(self._etf_coins) < 11:

                if pair not in self._etf_coins:
                    config = self._etf_config[pair]
                    money = config['count'] * ETF_AMOUNT * price
                    self._etf_coins[pair] = {'coin': pair.split('_')[0],'amount': 0, 'price': price, 'count': config['count'], 'money': money,'amount_precision': config['amount_precision'],'price_precision': config['price_precision'],'min_amount':config['min_amount']}

                return

            data = self._etf_coins[pair]
            money = data['count'] * ETF_AMOUNT * price
            data.update({'money': money})

            if self._swap:
                return

            money = 0
            m10 = 0

            for k,v in self._etf_coins.items():

                if k == 'HB10_USDT':
                    m10 = v['money']
                else:
                    money += v['money']

            rate = m10 / money - 1
            if rate > self._etf_rate_in:
                logging.info(f'in---{m10}----{money}---=={rate}')
                self._etf_rate_in = rate
            elif rate < self._etf_rate_out:
                logging.info(f'out---{m10}----{money}---=={rate}')
                self._etf_rate_out = rate

            if rate > 0.0082:

                self._swap = 'in'
                self._exchange.d_ws_close()

                tasks = []
                for k, v in self._etf_coins.items():
                    if k != 'HB10_USDT':
                        amount = v['count'] * ETF_AMOUNT
                        amount = amount / 0.997
                        amount = Utility.precison_value(v['amount_precision'], amount)
                        amount = amount + Utility.precision(v['amount_precision'])
                        amount = Utility.precison_value(v['amount_precision'], amount)

                        price = v['price']
                        price = Utility.precison_value(v['price_precision'], price)

                        tasks.append({'coin': v['coin'], 'price': price, 'amount': amount})

                self.async_task(self.buy, tasks)

            elif rate < -0.0092:

                self._swap = 'out'
                self._exchange.d_ws_close()

                v = self._etf_coins['HB10_USDT']
                amount = ETF_AMOUNT / 0.996
                amount = Utility.precison_value(v['amount_precision'], amount)
                amount = amount + Utility.precision(v['amount_precision'])
                amount = Utility.precison_value(v['amount_precision'], amount)

                price = v['price']
                price = Utility.precison_value(v['price_precision'], price)

                self.buy({'coin': 'HB10', 'price': price, 'amount': amount})

                #Utility.email_analyze(text)

        except Exception as e:
            logging.error(f'{sys._getframe().f_code.co_name}---{e}')

    def ws_order(self,exchange,ws_data):

        logging.info(f'{sys._getframe().f_code.co_name}---{ws_data}')

        pair = ws_data['pair']

        if pair not in self._etf_coins:
            return

        if ws_data['status'] == Common.status_open:

            data = {'pair':pair,'order_id': ws_data['order_id'], 'money': ws_data['money'], 'amount': ws_data['amount'], 'unfee_amount': ws_data['unfee_amount'],'side':ws_data['side'],'price':ws_data['price']}
            self._open.append(data)
            self.open_order()

        elif ws_data['status'] == Common.status_filled:

            for i in self._open:
                if i['pair'] == pair:
                    self._open.remove(i)
                    break

            if self._swap == 'in':

                self._exchange_data.append({'pair': pair, 'money': ws_data['money']})

                if len(self._exchange_data) == 10:

                    logging.debug(333333333333333333333)
                    #Utility.email_analyze('333333333333333333333')

                    self._swap = 'swap_in'
                    self.swap_in(ETF_AMOUNT)

                    v = self._etf_coins['HB10_USDT']
                    #price = v['price']
                    price = v['sell_price']
                    price = Utility.precison_value(v['price_precision'], price)

                    self.sell({'coin': 'HB10', 'price': price, 'amount': ETF_AMOUNT})

            elif self._swap == 'swap_in':

                logging.debug(f'4444444444444444444444,{self._exchange_data}')

                #Utility.email_analyze('4444444444444444444444')

                money = 0
                for i in self._exchange_data:
                    money += i['money']

                profit_money = ws_data['money'] - money
                rate = '{:.2%}'.format(profit_money / money)

                data = {'swap':'in','coins':self._exchange_data,'coins_money':money,'hb10_money':ws_data['money'],'profit_money':profit_money,'rate':rate,'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                DB.insert_one(Common.db_etf, data)

                self._exchange_data.clear()
                self._etf_coins.clear()
                self._swap = None

                self._exchange.d_ws_resub

                # t = threading.Timer(300, self._exchange.d_ws_resub)
                # t.start()

            elif self._swap == 'out':

                logging.debug(555555555555555)
                #Utility.email_analyze('555555555555555')

                self._swap = 'swap_out'
                amount = int(ETF_AMOUNT / 0.996 * 0.998)
                self.swap_out(amount)
                self._hb10_money = ws_data['money']

                time.sleep(0.1)
                tasks = []
                for k, v in self._etf_coins.items():
                    if k != 'HB10_USDT':
                        amount = v['count'] * ETF_AMOUNT
                        amount = Utility.precison_value(v['amount_precision'], amount)

                        price = v['sell_price']
                        price = Utility.precison_value(v['price_precision'], price)

                        tasks.append({'coin': v['coin'], 'price': price, 'amount': amount})

                self.async_task(self.sell, tasks)

            elif self._swap == 'swap_out':

                logging.debug(66666666666666)

                #Utility.email_analyze('66666666666666')

                self._exchange_data.append({'pair': pair, 'money': ws_data['money']})

                if len(self._exchange_data) == 10:

                    money = 0
                    for i in self._exchange_data:
                        money += i['money']

                    profit_money = money - self._hb10_money
                    rate = '{:.2%}'.format(profit_money / self._hb10_money)

                    data = {'swap': 'out', 'coins': self._exchange_data, 'coins_money': money,'hb10_money': self._hb10_money,'profit_money':profit_money, 'rate': rate,'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    DB.insert_one(Common.db_etf, data)

                    self._exchange_data.clear()
                    self._etf_coins.clear()
                    self._swap = None

                    self._exchange.d_ws_resub

                    # t = threading.Timer(300, self._exchange.d_ws_resub)
                    # t.start()

        elif ws_data['status'] == Common.status_part_filled:

            flag = True
            for i in self._open:
                if i['pair'] == pair:
                    i.update({'unfee_amount': ws_data['unfee_amount']})
                    flag = False
                    break

            if flag:
                data = {'pair': pair, 'order_id': ws_data['order_id'], 'money': ws_data['money'],'amount': ws_data['amount'], 'unfee_amount': ws_data['unfee_amount'], 'side': ws_data['side'],'price': ws_data['price']}
                self._open.append(data)
                self.open_order()

        elif ws_data['status'] == Common.status_canceled or ws_data['status'] == Common.status_part_canceled:
            for i in self._open:
                if i['pair'] == pair:
                    self._open.remove(i)
                    break

    def ws_account(self,exchange,ws_data):

        logging.info(ws_data)

    def buy(self,data):
        logging.info(f'etf_buy---{data}')
        try:
            self._exchange.buy(data['coin'],'USDT', data['price'], data['amount'])
        except Exception as e:
            logging.error(f'{sys._getframe().f_code.co_name}---{e}')

    def sell(self, data):
        logging.info(f'etf_sell---{data}')
        try:
            self._exchange.sell(data['coin'], 'USDT', data['price'], data['amount'])
        except Exception as e:
            logging.error(f'{sys._getframe().f_code.co_name}---{e}')

    def swap_in(self, amount):
        try:
            self._exchange.swap_in(amount)
        except Exception as e:
            logging.error(f'{sys._getframe().f_code.co_name}---{e}')

    def swap_out(self, amount):
        try:
            self._exchange.swap_out(amount)
        except Exception as e:
            logging.error(f'{sys._getframe().f_code.co_name}---{e}')

    def async_task(self,func,execute_data):

        async def execute(data):
            await loop.run_in_executor(None, func, data)

        tasks = []

        for i in execute_data:
            tasks.append(execute(i))

        loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def open_order(self):

        def execute(event):

            event.wait(60)

            while len(self._open) > 0:

                for i in self._open:

                    pair = i['pair']
                    etf_coin = self._etf_coins[pair]
                    min_amount = etf_coin['min_amount']
                    amount = i['amount'] - i['unfee_amount']
                    amount = Utility.precison_value(etf_coin['amount_precision'], amount)

                    if amount >= min_amount:

                        coin,fund = pair.split('_')
                        res = self._exchange.depth(coin, fund)

                        if i['side'] == Common.trade_side_buy:
                            # price = res['buy'][9][0]
                            # if price > i['price']:
                            #     self._exchange.cancelOrder(coin, fund, i['order_id'])
                            #     event.wait(0.3)
                            #     price = res['buy'][4][0]
                            #     self.buy({'coin': coin, 'price': price, 'amount': amount})

                            self._exchange.cancelOrder(coin, fund, i['order_id'])
                            event.wait(0.3)
                            price = res['sell'][1][0]
                            self.buy({'coin': coin, 'price': price, 'amount': amount})

                        else:
                            # price = res['sell'][9][0]
                            # if price < i['price']:
                            #     self._exchange.cancelOrder(coin, fund, i['order_id'])
                            #     event.wait(0.3)
                            #     price = res['sell'][4][0]
                            #     self.sell({'coin': coin, 'price': price, 'amount': amount})

                            self._exchange.cancelOrder(coin, fund, i['order_id'])
                            event.wait(0.3)
                            price = res['buy'][1][0]
                            self.sell({'coin': coin, 'price': price, 'amount': amount})

                if len(self._open) > 0:
                    event.wait(60)

            self._thread = None

        if not self._thread:

            event = threading.Event()
            self._thread = threading.Thread(target=execute,args=(event,))
            self._thread.setDaemon(True)
            self._thread.start()