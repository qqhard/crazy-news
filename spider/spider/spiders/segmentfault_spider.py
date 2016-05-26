import scrapy
from spider.items import MyItem
import re

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

    def parse_page(self, response):
        item = MyItem()
        item['title'] = response.xpath('//*[@id="articleTitle"]/a/text()').extract_first()
        item['url'] = response.url
        item['time'] = response.xpath('//a[@class=\'text-muted\']/text()').extract_first()
        item['text'] = response.xpath('//div[@class=\'article fmt article__content\']').extract_first()
        item['domain'] = 'segmentfault'
        yield item
