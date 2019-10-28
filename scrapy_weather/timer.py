# encoding: utf-8
# 定时爬取,半小时爬取一次.


import time
import datetime
import os
import logging



logger = logging.getLogger()
logger.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s %(levelname)s ====>>%(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S')

base_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(base_dir, 'log.txt')
fh = logging.FileHandler(file_path, encoding='utf-8')
fh.setFormatter(format)
logger.addHandler(fh)


while True:
    now = datetime.datetime.now()
    date_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M')
    print('The spider city_weather:\t' +date_time)
    print(os.path.realpath(__file__))
    logger.info('The spider city_weather:\t' +date_time)
    os.system("scrapy crawl city_weather")
    time.sleep(60*5)   # 更新时间5分钟
