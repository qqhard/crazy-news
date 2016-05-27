# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import jieba
import jieba.posseg as pseg

class MongoPipeline(object):

    def __init__(self):
        self.client = MongoClient()
        self.page = self.client.crazynews.page

    def process_item(self, item, spider):
        self.page.insert_one(dict(item))
        return item

class TextPipeline(object):
    def process_item(self, item, spider):
        soup = BeautifulSoup(item['text'])
        item['text'] = soup.get_text()
        return item

class SegPipeline(object):
    def process_item(self, item, spider):
        words = pseg.cut(item['text'])
        item['words'] = [(key.word,key.flag) for key in words]
        return item
