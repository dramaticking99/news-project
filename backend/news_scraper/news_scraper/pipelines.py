# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import redis
import scrapy

class ValidationPipeline:
    def process_item(self, item, spider):
        # Ensure title + content exist; if not, drop
        if not item.get("title") or not item.get("content"):
            raise scrapy.exceptions.DropItem(f"Missing field in {item}")
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open(f"{spider.name}_{spider.site_key}.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

class RedisPushPipeline:
    def __init__(self, redis_url):
        self.redis_conn = redis.Redis.from_url(redis_url)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(redis_url=crawler.settings.get("REDIS_URL"))

    def process_item(self, item, spider):
        self.redis_conn.lpush("news_items", json.dumps(dict(item), ensure_ascii=False))
        return item
