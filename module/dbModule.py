# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py

import pymongo
import json
from bson import json_util
from flask import Flask, render_template, request, url_for, jsonify
from jinja2 import UndefinedError
import re

class Database():

    def __init__(self):
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn.get_database("RedBook")             # db선택
        self.collection = self.db.get_collection("booklist")    # 테이블 선택

    def dbclose(self):
        self.conn.close()

    def insert(self, query):
        self.collection.insert(query)

    def execute(self, query):
        self.cursor.execute(query)

    def executeOne(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row

    def recentCrawledBook(self):
        rows = self.collection.find().sort('crawled_time', pymongo.DESCENDING).limit(6)
        results = list(rows)
        self.dbclose()
        return json.dumps(results, default=json_util.default, ensure_ascii=False)


    def find(self, keyword):
        print(keyword)
        rows = list(
            self.collection.aggregate([
                {'$sort':{"site":pymongo.DESCENDING, "crawled_time":pymongo.DESCENDING, "price":pymongo.ASCENDING}},
                {'$match': {'title': {'$regex': keyword} } },
                {'$group':
                            {
                                '_id': {'isbn':'$isbn', 'site':'$site'},
                                'books': {
                                    '$push':
                                    {
                                        'title': '$title',
                                        'category' : '$category',
                                        'price' : '$price',
                                        'author' : '$author',
                                        'publish' : '$publish',
                                        'publish_date' : '$publish_date',
                                        'img' : '$img',
                                        'url' : '$url',
                                        'crawled_time' : '$crawled_time'
                                    }
                                }
                            }
                        },
                        {'$group':
                            {
                                '_id': {'isbn': '$_id.isbn'},
                                'bookList': { '$push' : {'site' : '$_id.site', 'books' : '$books'}}
                            }
                        }
                    ])
                )
        print('rows 실행')
        results = list(rows)
        self.dbclose()
        return json.dumps(results, default=json_util.default, ensure_ascii=False)

    def find_ajax(self, keyword, page):
        start = int(page) * 5
        end = 5
        print(keyword)
        rows = list(
            self.collection.aggregate([
                {'$sort':{"site":pymongo.DESCENDING, "crawled_time":pymongo.DESCENDING, "price":pymongo.ASCENDING}},
                {'$match': {'title': {'$regex': keyword} } },
                {'$group':
                    {
                        '_id': {'isbn':'$isbn', 'site':'$site'},
                        'books': {
                            '$push':
                            {
                                'title': '$title',
                                'category' : '$category',
                                'price' : '$price',
                                'author' : '$author',
                                'publish' : '$publish',
                                'publish_date' : '$publish_date',
                                'img' : '$img',
                                'url' : '$url',
                                'crawled_time' : '$crawled_time'
                            }
                        }
                    }
                },
                {'$group':
                    {
                        '_id': {'isbn': '$_id.isbn'},
                        'bookList': { '$push' : {'site' : '$_id.site', 'books' : '$books'}}
                    }
                },
                {'$sort':{"bookList.books.publish_date":pymongo.DESCENDING}},
                {'$skip': start},
                {'$limit': end}
            ])
        )
        print('rows 실행')
        results = list(rows)
        self.dbclose()
        return json.dumps(results, default=json_util.default, ensure_ascii=False)

    def load(self, page):
        start = int(page) * 5
        end = 5
        rows = list(
            self.collection.aggregate([
                {'$sort':{"site":pymongo.ASCENDING, "crawled_time":pymongo.DESCENDING}},
                {'$group':
                    {
                        '_id': {'isbn':'$isbn', 'site':'$site'},
                        'books': {
                            '$push':
                            {
                                'title': '$title',
                                'category': '$category',
                                'price' : '$price',
                                'author' : '$author',
                                'publish' : '$publish',
                                'publish_date' : '$publish_date',
                                'img' : '$img',
                                'url' : '$url',
                                'crawled_time' : '$crawled_time'
                            }
                        }
                    }
                },
                {'$group':
                    {
                        '_id': {'isbn': '$_id.isbn'},
                        'bookList': { '$push' : {'site' : '$_id.site', 'books' : '$books'}}
                    }
                },
                {'$sort':{"bookList.books.publish_date":pymongo.DESCENDING}},
                {'$skip': start},
                {'$limit': end}
            ])
        )
        results = list(rows)
        self.dbclose()
        return json.dumps(results, default=json_util.default, ensure_ascii=False)

    def getCount(self):
        rows = self.collection.aggregate([
                                            {
                                                '$group':{
                                                    '_id': '$isbn'
                                                }
                                            },
                                            {
                                                '$group': {
                                                   '_id': 1,
                                                    'count' :{
                                                        '$sum' : 1
                                                    }
                                                }
                                            }
                                        ])
        count = list(rows)
        self.dbclose()
        return json.dumps(count, default=json_util.default, ensure_ascii=False)

    def getSearchCount(self, keyword):
        rows = list(
            self.collection.aggregate([
                        {'$match': {'title': {'$regex': keyword}}},
                        {
                            '$group':{
                                '_id': '$isbn'
                            }
                        },
                        {
                            '$group': {
                               '_id': 1,
                                'count' :{
                                    '$sum' : 1
                                }
                            }
                        }
                    ])
        )
        count = list(rows)
        print(count)
        self.dbclose()
        return json.dumps(count, default=json_util.default, ensure_ascii=False)

    def getBookCategory(self, category, page):
        start = int(page) * 5
        end = 5
        rows = list(
            self.collection.aggregate([
                {'$sort':{"site":pymongo.ASCENDING, "crawled_time":pymongo.DESCENDING}},
                {'$match':{'category' : category}},
                {'$group':
                    {
                        '_id': {'isbn':'$isbn', 'site':'$site'},
                        'books': {
                            '$push':
                            {
                                'title': '$title',
                                'category': '$category',
                                'price' : '$price',
                                'author' : '$author',
                                'publish' : '$publish',
                                'publish_date' : '$publish_date',
                                'img' : '$img',
                                'url' : '$url',
                                'crawled_time' : '$crawled_time'
                            }
                        }
                    }
                },
                {'$group':
                    {
                        '_id': {'isbn': '$_id.isbn'},
                        'bookList': { '$push' : {'site' : '$_id.site', 'books' : '$books'}}
                    }
                },
                {'$sort':{"bookList.books.publish_date":pymongo.DESCENDING}},
                {'$skip': start},
                {'$limit': end}
            ])
        )
        results = list(rows)
        self.dbclose()
        return json.dumps(results, default=json_util.default, ensure_ascii=False)