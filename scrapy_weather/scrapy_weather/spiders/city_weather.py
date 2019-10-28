# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy_weather.items import WeatherItem
from pprint import pprint





def search_id(url):
    with open('./CityCode.json', 'r', encoding='utf-8')as f :
        for line in f.readlines():
            dic = json.loads(line, encoding='utf-8')
            if dic['url'] in url:
                return dic['code']
        return None


class CityWeatherSpider(scrapy.Spider):
    name = 'city_weather'
    allowed_domains = ['www.nmc.cn']
    start_urls = ['http://www.nmc.cn/publish/forecast/AJS/nanjing1.html', # 南京
                  'http://www.nmc.cn/publish/forecast/ASN/xian.html',  # 西安
                  'http://www.nmc.cn/publish/forecast/ASX/wutaishan.html', # 五台山
                  'http://www.nmc.cn/publish/forecast/ASX/fanzhi.html', # 繁峙
                  'http://www.nmc.cn/publish/forecast/AAH/xuancheng.html']   # 宣城
    # start_urls = ['http://www.nmc.cn/f/rest/aqi/54503?_={0:.0f}'.format(time.time()*1000)]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
    }

    def parse(self, response):
        item = WeatherItem()

        # days = response.xpath('//*[@id="forecast"]//div[@class="today"]//tbody')
        days = response.xpath('//*[@id="forecast"]//div[@class="detail"]')
        for i in range(len(days)):
            day = dict()
            day['date'] = days[i].xpath('./div[2]/div[1]/text()').extract_first().strip()
            day['day_info'] = days[i].xpath('./div[1]/table/tbody/tr[3]/td[1]/text()').extract_first()
            day['night_info'] = days[i].xpath('./div[1]/table/tbody/tr[3]/td[2]/text()').extract_first()
            day['day_temp'] = days[i].xpath('./div[1]/table/tbody/tr[4]/td[1]/text()').extract_first()
            day['night_temp'] = days[i].xpath('./div[1]/table/tbody/tr[4]/td[2]/text()').extract_first()
            day['day_winddirect'] = days[i].xpath('./div[1]/table/tbody/tr[5]/td[1]/text()').extract_first()
            day['night_winddirect'] = days[i].xpath('./div[1]/table/tbody/tr[5]/td[2]/text()').extract_first()
            day['day_power'] = days[i].xpath('./div[1]/table/tbody/tr[6]/td[1]/text()').extract_first()
            day['night_power'] = days[i].xpath('./div[1]/table/tbody/tr[6]/td[2]/text()').extract_first()
            item['days_' + str(i+1)] = day


        # aqi_url = 'http://www.nmc.cn/f/rest/aqi/58238?_={0:.0f}'.format(time.time()*1000)
        aqi_url = 'http://www.nmc.cn/f/rest/aqi/{0}?_={1:.0f}'.format(search_id(response.url), time.time()*1000)
        yield scrapy.Request(aqi_url, meta={'item': item}, callback=self.parse_aqi)

    def parse_aqi(self, response):
        item = response.meta['item']

        res_aq = json.loads(response.text)
        item['aq'] = res_aq['aq']
        item['aqi'] = res_aq['aqi']
        item['aq_text'] = res_aq['text']

        print(response.url + '*'*100)
        real_url = response.url.replace('aqi', 'real').split('=')[0] + '={0:.0f}'.format(time.time() * 1000)
        yield scrapy.Request(real_url, meta={'item': item}, callback=self.parse_real)

    def parse_real(self, response):
        item = response.meta['item']

        res_real = json.loads(response.text)
        item['publish_time'] = res_real['publish_time']
        item['city'] = res_real['station']['city']
        item['code'] = res_real['station']['code']
        item['province'] = res_real['station']['province']
        item['alert'] = res_real['warn']['alert']
        item['issuecontent'] = res_real['warn']['issuecontent']
        item['fmeans'] = res_real['warn']['fmeans']
        item['airpressure'] = res_real['weather']['airpressure']
        item['feelst'] = res_real['weather']['feelst']
        item['humidity'] = res_real['weather']['humidity']
        item['icomfort'] = res_real['weather']['icomfort']
        item['info'] = res_real['weather']['info']
        item['rain'] = res_real['weather']['rain']
        item['rcomfort'] = res_real['weather']['rcomfort']
        item['temperature'] = res_real['weather']['temperature']
        item['winddirect'] = res_real['wind']['direct']
        item['windpower'] = res_real['wind']['power']
        item['windspeed'] = res_real['wind']['speed']

        print(response.url + '*'*100)
        pprint(item)
        # yield scrapy.Request(url, meta={'item': item}, callback=self.parse_forecast)
        yield item
