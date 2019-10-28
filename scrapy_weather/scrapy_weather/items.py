# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyWeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CityCodeItem(scrapy.Item):
    code = scrapy.Field()
    city_name = scrapy.Field()
    province = scrapy.Field()
    url = scrapy.Field()


class WeatherItem(scrapy.Item):
    aq = scrapy.Field()
    aqi = scrapy.Field()
    aq_text = scrapy.Field()
    publish_time = scrapy.Field()
    city = scrapy.Field()
    code = scrapy.Field()
    province = scrapy.Field()
    alert = scrapy.Field()  # 预警
    issuecontent = scrapy.Field()  # 预警及防护
    fmeans = scrapy.Field()  # 防护措施
    airpressure = scrapy.Field()  # 气压
    feelst = scrapy.Field()  # 体感温度
    humidity = scrapy.Field()  # 相对湿度
    icomfort = scrapy.Field()  # 舒适度 是个代码，好像没法用。 不知道代码字典。太原舒适度为凉爽，较舒适时候，它的值为-1
    info = scrapy.Field()  # 天气状况描述，多云 晴 下雨 雪等
    rain = scrapy.Field()  # 降水量  0位不下雨   9999和其他表示相同都为空没有值
    rcomfort = scrapy.Field()  # 太原舒适度为凉爽，较舒适时候，它的值为50
    temperature = scrapy.Field()  # 温度
    winddirect = scrapy.Field()  # 方向
    windpower = scrapy.Field() # 风力
    windspeed = scrapy.Field() # 速度 很多时候为空字符串""
    days_1 = scrapy.Field()
    days_2 = scrapy.Field()
    days_3 = scrapy.Field()
    days_4 = scrapy.Field()
    days_5 = scrapy.Field()
    days_6 = scrapy.Field()
    days_7 = scrapy.Field()

