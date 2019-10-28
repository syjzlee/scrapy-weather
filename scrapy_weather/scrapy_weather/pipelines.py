# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import datetime
import pymysql
from pprint import pprint
from twisted.enterprise import adbapi


class ScrapyWeatherPipeline(object):
    def process_item(self, item, spider):
        return item


class CityCodeJsonPipeline(object):
    def __init__(self):
        self.file = open('CityCode.json', 'wb')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()


class WeatherSqlPipeline(object) :
    """
    同步操作
    """
    def __init__(self) :
        # 建立连接
        self.conn = pymysql.connect('localhost', 'root', 'ljp310851649.', 'weather')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        for key in item:
            if not isinstance(item[key], str):
                item[key] = str(item[key])
        # sql语句
        insert_sql ="insert into weather(aq,aqi,aq_text,publish_time,city,code,province,alert,issuecontent,fmeans," \
                     "airpressure,feelst,humidity,icomfort,info,rain,rcomfort,temperature,winddirect,windpower,\
                      windspeed,days_1,days_2,days_3,days_4,days_5,days_6,days_7) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                     "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['aq'], item['aqi'], item['aq_text'], datetime.datetime.strptime(item['publish_time'], '%Y-%m-%d %H:%M'),
                                    item['city'], item['code'], item['province'], item['alert'], item['issuecontent'], item['fmeans'],
                                    item['airpressure'], item['feelst'], item['humidity'], item['icomfort'],
                                    item['info'], item['rain'], item['rcomfort'], item['temperature'], item['winddirect'],
                                    item['windpower'], item['windspeed'], item['days_1'], item['days_2'], item['days_3'],
                                    item['days_4'], item['days_5'], item['days_6'], item['days_7'] ))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()


# class WeatherSqlPipeline(object):
# """异步"""
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings) :  # 函数名固定，会被scrapy调用，直接可用settings的值
#         """
#         数据库建立连接
#         :param settings: 配置参数
#         :return: 实例化参数
#         """
#         adbparams = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             password=settings['MYSQL_PASSWORD'],
#             cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
#         )
#         # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
#         dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
#         # 返回实例化参数
#         return cls(dbpool)
#
#     def process_item(self, item, spider) :
#         """
#         使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
#         """
#         query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
#         # 添加异常处理
#         query.addCallback(self.handle_error)  # 处理异常
#
#     def do_insert(self, cursor, item) :
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
#         insert_sql = "insert into weather(aq,aqi,aq_text,publish_time,city,code,province,alert,issuecontent,fmeans," \
#                      "airpressure,feelst,humidity,icomfort,info,rain,rcomfort,temperature,winddirect,windpower,\
#                       windspeed,days_1,days_2,days_3,days_4,days_5,days_6,days_7) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
#                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(insert_sql, (item['aq'], item['aqi'], item['aq_text'], item['publish_time'], item['city'],
#                                     item['code'], item['province'], item['alert'], item['issuecontent'], item['fmeans'],
#                                     item['airpressure'], item['feelst'], item['humidity'], item['icomfort'],
#                                     item['info'], item['rain'], item['rcomfort'], item['temperature'], item['winddirect'],
#                                     item['windpower'], item['windspeed'], item['days_1'], item['days_2'], item['days_3'],
#                                     item['days_4'], item['days_5'], item['days_6'], item['days_7'] ))
#
#     def handle_error(self, failure):
#         if failure:
#             # 打印错误信息
#             print(failure)

