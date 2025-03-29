import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
import logging

class NewsCrawlerSpider(CrawlSpider):
    name = 'news_crawler'
    allowed_domains = ['google.com']
    start_urls = ['https://news.google.com/']

    rules = (
        Rule(LinkExtractor(allow=r'\/news\/\d{4}\/\d{2}\/\d{2}\/'), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        item = {
            'url': response.url,
            'title': response.xpath('//h1/text()').get(),
            'content': response.xpath('//div[@class="article-content"]/text()').getall(),
            'author': response.xpath('//span[@class="author"]/text()').get(),
            'published_date': response.xpath('//time/@datetime').get(),
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': response.xpath('//meta[@property="og:site_name"]/@content').get(),
        }
        # Clean up any None Values
        item = {k: v for k, v in item.items() if v is not None}

        yield item