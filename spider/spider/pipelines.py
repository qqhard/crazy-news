# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MongoPipeline(object):

    def __init__(self):
        self.client = MongoClient()
        self.page = self.client.crazynews.page

    def process_item(self, item, spider):
        self.page.insert_one(dict(item))
        return item

class TimePipeline(object):

    def __init__(self):
        self.router = {
            'csdn':self._csdn
        }

    def _default(self, item):
        return item

    def _csdn(self, item):
        timeStr = item['time'].strip()
        timeStruct = time.strptime(timeStr,'%Y-%m-%d %H:%M')
        item['time'] = time.mktime(timeStruct)
        return item

    def process_item(self, item, spider):
        handle = self.router.get(item['domain'],self._default)
        return handle(item)
