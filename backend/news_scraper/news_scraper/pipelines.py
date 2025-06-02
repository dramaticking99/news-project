# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class NewsScraperPipeline:
    def process_item(self, item, spider):

       return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        # Called when the spider opens. We open a file handle to write JSON array.
        self.file = open('articles.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def close_spider(self, spider):
        # When spider closes, finish the JSON array and close file handle.
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        # Called for each item yielded by the spider.
        line = json.dumps(dict(item), ensure_ascii=False)
        if self.first_item:
            self.first_item = False
            self.file.write(line)
        else:
            self.file.write(',\n' + line)
        return item
    
    
