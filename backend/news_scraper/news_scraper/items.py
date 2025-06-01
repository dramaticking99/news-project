# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# myproject/items.py
import scrapy

class NewsArticleItem(scrapy.Item):
    url          = scrapy.Field()
    title        = scrapy.Field()
    content_html = scrapy.Field()
    author       = scrapy.Field()
    publish_date = scrapy.Field()
    tags         = scrapy.Field()
    image_url    = scrapy.Field()