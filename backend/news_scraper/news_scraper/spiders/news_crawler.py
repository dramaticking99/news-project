import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

class NewsArticleSpider(CrawlSpider):
    name = 'news_scraper'
    allowed_domains = ['ndtv.com']
    start_urls = ['https://www.ndtv.com/india']

    rules = (
        Rule(LinkExtractor(allow=r'/india-news/.*-\d+$'), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        title = response.xpath('//h1[@itemprop="headline"]/text()').get()
        author = response.xpath('//span[@itemprop="author"]/text()').get()
        published_date = response.xpath('//span[@itemprop="dateModified"]/@content').get()
        content = response.xpath('//div[@itemprop="articleBody"]//p//text()').getall()
        source = response.url.split('/')[2]

        item = {
            'url': response.url,
            'title': title.strip() if title else '',
            'author': author.strip() if author else '',
            'published_date': published_date,
            'content': ' '.join(content).strip(),
            'source': source,
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        yield item
