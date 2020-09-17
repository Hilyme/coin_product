from common.Common import Common
from common.log import log
from strategy.etf import Etf
from flask import Flask
import os

from strategy.test import Test

Test().start()

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(64)


if __name__ == '__main__':

    app.run(host=Common.server_host, port=Common.server_port, debug=False)

    pass

