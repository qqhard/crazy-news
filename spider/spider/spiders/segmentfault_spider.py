# -*- coding: utf-8 -*-
import scrapy
from spider.items import MyItem
import re
import time
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

class SegmentfaultSpider(scrapy.spiders.Spider):
    name = "segmentfault"
    allowed_domains = ["segmentfault.com"]

    def __init__(self):
        base_urls = [
            "https://segmentfault.com/blogs",
            "https://segmentfault.com/blogs/newest",
            "https://segmentfault.com/blogs/hottest",
        ]
        start_urls = []
        for base_url in base_urls:
            for j in range(5):
                start_urls.append(base_url+"?page="+str(j+1))
        self.start_urls = start_urls

    def parse(self, response):
        url = response.url
        if url.startswith("https://segmentfault.com/blogs"):
            urls = response.xpath("//h2[@class=\"title\"]/a/@href").extract()
            for url in urls:
                request = scrapy.Request("https://segmentfault.com"+url,callback=self.parse_page)
                yield request

    def _page_time(self, timeStr):
        now_time = time.time()
        ret_time = 0
        if u'小时' in timeStr:
            ret_time = now_time - int(re.findall(u'(\d+)\s*小时',timeStr)[0]) * 3600
        elif u'分钟' in timeStr:
            ret_time = now_time - int(re.findall(u'(\d+)\s*分钟',timeStr)[0]) * 60
        elif u'天' in timeStr:
            ret_time = now_time - int(re.findall(u'(\d+)\s*天',timeStr)[0]) * 86400
        else:
            monthAndDay = re.findall(u'(\d+)月(\d+)日',timeStr)[0]
            now = datetime.datetime.now()
            publish_time = datetime.datetime(now.year,int(monthAndDay[0]),int(monthAndDay[1]))
            ret_time = time.mktime(publish_time.timetuple())
        return ret_time

    def parse_page(self, response):
        item = MyItem()
        item['title'] = response.xpath('//*[@id="articleTitle"]/a/text()').extract_first()
        item['url'] = response.url
        timeStr = response.xpath('//a[@class=\'text-muted\']/text()').extract_first()
        item['time'] = self._page_time(timeStr)
        item['text'] = response.xpath('//div[@class=\'article fmt article__content\']').extract_first()
        item['domain'] = 'segmentfault'
        yield item
