import pymongo
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import logging

logger = logging.getLogger(__name__)

class MongoDBPipeline(object):

    def __init__(self, settings):
        self.mongo_uri = settings.get('MONGODB_SERVER')
        self.mongo_port = settings.get('MONGODB_PORT')
        self.mongo_db = settings.get('MONGODB_DB')
        self.mongo_collection = settings.get('MONGODB_COLLECTION')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update_one(
            {'url': item['url']},
            {'$set': dict(item)},
            upsert=True
        )
        logger.info(f"Question added to MongoDB database! {item}")
        return item
