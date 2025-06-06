import scrapy

class BaseSpider(scrapy.Spider):
    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "RETRY_TIMES": 2,
    }

    def errback_http(self, failure):
        self.logger.error(f"Request failed: {repr(failure)}")
