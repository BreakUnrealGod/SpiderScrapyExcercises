# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient

# 文件保存
class DushuprojectPipeline(object):

    def open_spider(self, spider):
        self.fp = open("books.txt", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.fp.close()

    def process_item(self, item, spider):
        wString = json.dumps(dict(item)) + "\n"
        self.fp.write(wString)
        return item

# 数据库存储
class MongoPipleline(object):
    def open_spider(self, spider):
        # 数据库的连接
        self.conn = MongoClient("127.0.0.1", 27002)
        # 构建数据库
        self.db = self.conn["bookStore"]
        self.collection = self.db["bookList"]


    def close_spider(self, spider):
        # 数据库的关闭
        # 清理跟对象没关的资源
        self.conn.close()

    def process_item(self, item, spider):
        # 写入数据库操作
        self.collection.insert(item)
        return item

# class MysqlPipeline(object):
#
#     def open_spider(self, spider):
#         # mysql本地配置
#         pass
#
#     def close_spider(self, spider):
#         # mysql关闭
#         pass
#
#     def process_item(self, item, spider):
#         # 入库操作
#         return item