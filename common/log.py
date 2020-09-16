import sys,os
from datetime import datetime
import logging


def log():

    date = datetime.now()
    path = f'{sys.path[0]}/log/{date.year}-{date.month}-{date.day}.log'
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    fmt = '%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(funcName)s：\n %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=fmt,filename=path,filemode='w',datefmt='%a, %d %b %Y %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


log()

