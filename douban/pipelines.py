# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import redis
from scrapy import log

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    # collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #不同类型item 写入不同的collection
        collection_name=type(item).__name__.lower()

        #插入新的数据
        #self.db[collection_name].insert_one(dict(item))

        #更新数据，避免插入重复数据
        self.db[collection_name].update({'id': item['id']},dict(item),True)
        
        # print logs on the console
        log.msg('Item added to MongoDB database!',level=log.DEBUG,spider=spider) 
        return item


class InsertRedisPipeline(object):
    """将item 唯一标示id插入Redis 中，以set形式存储，用来避免下载重复的网页
    """
    def __init__(self,redis_host,redis_port,redis_password,redis_db):
        self.redis_host=redis_host
        self.redis_port=redis_port
        self.redis_password=redis_password
        self.db=redis_db
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST','127.0.0.1'),
            redis_port=crawler.settings.get('REDIS_PORT','6379'),
            redis_password=crawler.settings.get('REDIS_PASSWORD'),
            redis_db=crawler.settings.get('REDIS_DB','0')
        )
    
    def open_spider(self,spider):
        self.client=redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
    
    def close_spider(self,spider):
        pass
    
    def process_item(self,item,spider):
        redis_key=type(item).__name__.lower()
        self.client.sadd(redis_key,item['id'])
        log.msg('Ignore add the item id to redis!',level=log.DEBUG,spider=spider)

        return item
