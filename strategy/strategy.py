class Strategy:

    def __init__(self):
        pass

    def start(self):
        pass

    def ws_kline(self, exchange, ws_data, kline=None):
        pass

    def ws_ticker(self, exchange, ws_data):
        pass

    def ws_depth(self, exchange, ws_data):
        pass

    def ws_order(self, exchange, ws_data):
        pass

    def ws_account(self, exchange, message):
        pass

    def ws_leverAccount(self, exchange, message):
        pass

    def refresh(self):
        pass

    def tickers(self):
        pass

    def buy(self, exchange, coin, fund, price, amount, exist_data):
        pass

    def sell(self, exchange, coin, fund, price, amount, exist_data):
        pass

    def cancelOrder(self, exchange, coin, fund, order_id):
        pass

    def __del__(self):
        pass
