# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class SpiderPipeline(object):

    def __init__(self):
        self.client = MongoClient()
        self.page = self.client.crazynews.page

    def process_item(self, item, spider):
        self.page.insert_one(dict(item))
        return item
