# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from module import dbModule

class RedbookPipeline(object):
    def __init__(self):
        self.db_class = dbModule.Database()

    def process_item(self, item, spider):
        # create record if doesn't exist.
        query ={
            "site" : item['book_site'],
            "isbn" : item['book_isbn'],
            "category" : item['book_cat'],
            "title" : item['book_title'],
            "price" : item['book_price'],
            "author" : item['book_author'],
            "publish" : item['book_publish'],
            "publish_date" : item['book_publish_date'],
            "img" : item['book_img'],
            "url" : item['book_url'],
            "crawled_time" : item['crawl_time']
        }
        self.db_class.insert(query)
        return item
    def close_spider(self, spider):
        self.db_class.dbclose()