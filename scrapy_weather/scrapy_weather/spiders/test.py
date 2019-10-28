# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy_weather.items import WeatherItem
#
#
# class TianqiNanjingSpider(scrapy.Spider):
#     name = 'test'
#     allowed_domains = ['www.nmc.cn']
#     start_urls = ['http://www.itcast.cn/channel/teacher.shtml', 'http://www.nmc.cn/publish/forecast/AJS/nanjing1.html']
#     # url2 = ('http://www.itcast.cn/channel/teacher.shtml', 'http://www.nmc.cn/publish/forecast/AJS/nanjing1.html')
#
#     # def start_requests(self):
#     #     """重新初始化start_urls"""
#     #     for url in self.url2:
#     #         yield self.make_requests_from_url(url)
#
#     def parse(self, response):
#         print('*'*100)
#         print(response.url)
#         with open("tianqi_nanjing.html", "a", encoding='utf-8') as f :
#             f.write(response.url + '\n')