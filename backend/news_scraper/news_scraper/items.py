# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# myproject/items.py
import scrapy

class NewsArticleItem(scrapy.Item):
    site_key    = scrapy.Field()   # e.g. "ndtv", "siteB", so you know which site this came from
    title       = scrapy.Field()
    author      = scrapy.Field()
    published   = scrapy.Field()
    content     = scrapy.Field()
    url         = scrapy.Field()
    image_url   = scrapy.Field()   # Optional, if the article has an image