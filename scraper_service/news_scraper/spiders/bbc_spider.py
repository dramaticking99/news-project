import scrapy
from news_scraper.items import NewsArticleItem
from scrapy_playwright.page import PageMethod
import re

def should_abort_request(request):
    """
    Helper function to decide if a request should be aborted.
    Blocks images, stylesheets, fonts, and tracking scripts for efficiency.
    """
    if request.resource_type in ("image", "stylesheet", "font"):
        return True
    # Block requests to common tracking/ad domains
    tracking_domains = [
        "google-analytics.com", "googletagmanager.com", "scorecardresearch.com",
        "chartbeat.com", "cxense.com", "adservice.google.com", "doubleclick.net"
    ]
    for domain in tracking_domains:
        if domain in request.url:
            return True
    return False


class BbcSpider(scrapy.Spider):
    """
    Spider to scrape articles from multiple BBC News sections.
    Uses Playwright to render the dynamically loaded list pages.
    """
    name = 'bbc'
    allowed_domains = ['bbc.com', 'bbc.co.uk']

    start_urls = [
        'https://www.bbc.com/news/world',
        'https://www.bbc.com/news/technology',
        'https://www.bbc.com/news/science_and_environment'
    ]

    async def start(self):
        """
        This method is called by Scrapy for each URL in start_urls.
        It creates a Playwright-enabled request for each section page.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("route", re.compile(r".*"), lambda route: route.abort() if should_abort_request(route.request) else route.continue_()),
                        PageMethod('wait_for_selector', 'div[data-testid="liverpool-card"]')
                    ],
                    errback=self.errback,
                )
            )

    async def parse(self, response):
        """
        This method finds article links on the current list page and yields
        requests for them.
        """
        page = response.meta.get("playwright_page")
        
        self.logger.info(f"Parsing list page: {response.url}")

        article_links = response.css('div[data-testid="liverpool-card"] a[data-testid="internal-link"]::attr(href)').getall()
        unique_links = list(set(article_links))

        if not unique_links:
            self.logger.warning(f"No article links found on page: {response.url}. The website layout may have changed.")
        else:
             self.logger.info(f"Found {len(unique_links)} unique article links to scrape from {response.url}")

        for link in unique_links:
            if link.startswith('/news/articles/'):
                 yield response.follow(link, callback=self.parse_article)

        if page:
            await page.close()
            self.logger.info(f"Finished parsing list page and closed Playwright page for {response.url}")


    def parse_article(self, response):
        """
        This method scrapes the data from an individual BBC article page.
        """
        self.logger.info(f"Scraping article: {response.url}")

        article = NewsArticleItem()
        article['url'] = response.url
        article['headline'] = response.css('div[data-component="headline-block"] h1::text').get('').strip()
        article['author'] = response.css('span[data-testid="byline-new-contributors"] span::text').get('').strip()
        article['publication_date'] = response.css('time[datetime]::attr(datetime)').get('').strip()
        
        body_paragraphs = response.css('div[data-component="text-block"] p::text').getall()
        article['body_text'] = " ".join(p.strip() for p in body_paragraphs).strip()
        
        article['source_site'] = 'BBC News'

        yield article

    async def errback(self, failure):
        """
        Handles errors that occur during the Playwright request.
        """
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        self.logger.error(f"Playwright request failed: {failure.value}")