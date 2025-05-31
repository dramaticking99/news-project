# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')  # Use the appropriate settings file (e.g., dev or prod)
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from news.models import Article
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewsScraperPipeline:
    def process_item(self, item, spider):
       try:
           published_date = datetime.fromisoformat(item['published_date'])
           scraped_date = datetime.fromisoformat(item['scraped_date'])
           
           article, created = Article.objects.get_or_create(
               url = item['url'],
               defaults={
                   'title': item['title'],
                   'content': item['content'],
                   'author': item['author'],
                   'published_date': published_date,
                   'scraped_date': scraped_date,
                    'source': item['source'],
               }
           )

           if not created:
               spider.logger.info(f"Article already exists: {item['url']}")
           else:
               spider.logger.info(f"Article created: {item['url']}")
      
       except Exception as e:
              spider.logger.error(f"Error processing item: {e}")
              return None
       
       return item
