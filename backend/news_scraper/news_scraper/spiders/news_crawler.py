import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from news_scraper.items import NewsArticleItem

class NewsArticleSpider(CrawlSpider):
    name = 'news_scraper'
    allowed_domains = ['ndtv.com']
    start_urls = ['https://www.ndtv.com/india']

    rules = (
        Rule(LinkExtractor(allow=r'/india-news/.*-\d+$'),
             callback='parse_article',
             follow=True),
    )

    def parse_article(self, response):
        item = NewsArticleItem()

        # These XPaths match the current NDTV structure:
        item['url'] = response.url
        item['title'] = response.xpath(
            '//h1[@itemprop="headline"]/text()'
        ).get(default='').strip()

        # We store the entire <div itemprop="articleBody"> as 'content_html'
        # (so that later you can strip tags or render it in Django).
        paragraphs = response.xpath(
            '//div[@itemprop="articleBody"]//p'
        ).getall()
        item['content_html'] = ''.join(paragraphs).strip()

        item['author'] = response.xpath(
            '//span[@itemprop="author"]/text()'
        ).get(default='').strip()

        item['publish_date'] = response.xpath(
            '//span[@itemprop="dateModified"]/@content'
        ).get(default='')

        item['tags'] = response.xpath(
            '//meta[@name="keywords"]/@content'
        ).get(default='')

        item['image_url'] = response.xpath(
            '//meta[@property="og:image"]/@content'
        ).get(default='')

        yield item