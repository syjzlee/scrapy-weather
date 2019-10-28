# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy_weather.items import CityCodeItem
from pprint import pprint

class GetCityCodeSpider(scrapy.Spider):
    name = 'get_city_code'
    allowed_domains = ['nmc.cn']
    start_urls = ['http://www.nmc.cn/f/rest/province']

    # 重写settings的内容，设置请求头
    custom_settings = {
        # 'LOG_LEVEL': "DEBUG",
        # 'LOG_FILE': 'get_city_code.txt',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,text/javascript,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
    }

    def parse(self, response):
        provinces = re.findall('forecast(.*?).html"', response.text)
        for province in provinces:
            url = response.url + province
            print(url)
            yield scrapy.Request(url, callback=self.parse_city)


    def parse_city(self, response):
        # citys = eval(response.text)
        citys = json.loads(response.text)
        for city in citys:
            print(city)
            item = CityCodeItem()
            item['code'] = city['code']
            item['city_name'] = city['city']
            item['province'] = city['province']
            item['url'] = city['url']
            yield item







