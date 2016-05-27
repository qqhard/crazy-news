# -*- coding: utf-8 -*-
import scrapy
from spider.items import MyItem
import re
import time

class CsdnSpider(scrapy.spiders.Spider):
    name = "csdn"
    allowed_domains = ["blog.csdn.net"]

    def __init__(self):
        base_urls = [
            "http://blog.csdn.net/index.html"
        ]
        start_urls = []
        for base_url in base_urls:
            for j in range(5):
                start_urls.append(base_url+"?page="+str(j+1))
        self.start_urls = start_urls

    def parse(self, response):
        urls = response.xpath('//div[@class="blog_list"]/h1/a//@href').extract()
        for url in urls:
            if url.startswith("http://") == False:
                continue
            request = scrapy.Request(url,callback=self.parse_page)
            yield request

    def _parse_time(self, timeStr):
        timeStr = timeStr.strip()
        timeStruct = time.strptime(timeStr,'%Y-%m-%d %H:%M')
        return time.mktime(timeStruct)

    def parse_page(self, response):
        item = MyItem()
        item['title'] = response.xpath('//span[@class="link_title"]/a/text()').extract_first()
        item['url'] = response.url
        item['time'] = self._parse_time(response.xpath('//span[@class="link_postdate"]/text()').extract_first())
        item['text'] = response.xpath('//*[@id="article_content"]').extract_first()
        item['domain'] = 'csdn'
        yield item
