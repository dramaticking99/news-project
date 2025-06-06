import scrapy
from news_scraper.items import NewsArticleItem
from news_scraper.extractors.field_extractors import extract_fields
from news_scraper.spiders.base_spider import BaseSpider


class NdtvSpider(BaseSpider):
    name = "ndtv"
    site_key = "ndtv"
    allowed_domains = ["ndtv.com"]
    start_urls = ["https://www.ndtv.com/india-news"]  # or whichever landing page

    def parse(self, response):
        # 1) List all article links on NDTV listing page
        for href in response.css("div#ins_storylist a::attr(href)").getall():
            yield response.follow(
                href,
                callback=self.parse_item,
                errback=self.errback_http,
                meta={"site_key": self.site_key},
            )

        # 2) NDTV pagination (if they have “Next”)
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        site_key = response.meta.get("site_key", self.site_key)
        data = extract_fields(response, site_key)
        data["url"] = response.url
        data["site_key"] = site_key
        yield NewsArticleItem(**data)
