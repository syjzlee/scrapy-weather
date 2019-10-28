# scrapy-weather-
使用scrapy爬取想要的城市的天气，并将结果存入数据库中。


# 进入到日志文件的目录中，直接执行以下命令即可：
'''
python timer.py
'''


在CityCode.json 文件中有城市的相关信息，包括URL，code等。查询你想要爬取的城市url，然后将该URL添加到
scrapy_weather\scrapy_weather\spiders\city_weather.py中的start_urls列表即可。
