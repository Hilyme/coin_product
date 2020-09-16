# -*- coding:utf-8 -*-

"""
@author:    tz_zs
"""
import json
import threading
import zlib

import websocket
from websocket import WebSocketApp

try:
    import thread
except ImportError:
    import _thread as thread
import time


class Test(object):
    def __init__(self):
        super(Test, self).__init__()
        # self.url = "ws://echo.websocket.org/"
        self.url = "wss://real.okex.com:8443/ws/v3"
        # self.url = "wss://real.okex.com:10440/ws/v1"
        self.ws = None

    def inflate(self, data):
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated

    def on_message(self, message):
        print("####### on_message #######")
        data = json.loads(self.inflate(message))
        print(self)
        print(data)
        msg = message.decode('utf-8')
        print("----", msg, "-----")

    def on_error(self, error):
        print("####### on_error #######")
        print(self)
        print(error)

    def on_close(self):
        print("####### on_close #######")
        print(self)
        print("####### closed #######")

    def on_open(self):
        print("on_open")

        def run(*args):
            w_s = []
            w_s.append('{}/{}:{}'.format('futures', 'ticker', 'XRP-USD-200925'))
            w_s.append('{}/{}:{}'.format('futures', 'candle60s', 'XRP-USD-200925'))
            self.ws.send(json.dumps({'op': 'subscribe', 'args': w_s}))
            # for i in range(3):
            #     time.sleep(1)
            #     # self.ws.send("Hello %d" % i)
            # time.sleep(1)
            # self.ws.close()
            # print("thread terminating...")

        thread.start_new_thread(run, ())

    def start(self):
        print("----------start start...-------------")
        self.ws = WebSocketApp(self.url,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=20)
        print("--------------start end...--------------")


if __name__ == '__main__':
    print("--------------main start...--------------")
    t = threading.Thread(target=Test().start)
    t.start()
    print("--------------main end...----------------")

"""
<__main__.Test object at 0x7fb4e855cb70>
####### on_message #######
<__main__.Test object at 0x7fb4e855cb70>
Hello 0
####### on_message #######
<__main__.Test object at 0x7fb4e855cb70>
Hello 1
####### on_message #######
<__main__.Test object at 0x7fb4e855cb70>
Hello 2
thread terminating...
####### on_close #######
<__main__.Test object at 0x7fb4e855cb70>
####### closed #######
"""
