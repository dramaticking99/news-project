import scrapy
from news_scraper.items import NewsArticleItem
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
import asyncio

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


class RepublicWorldSpider(scrapy.Spider):
    """
    Spider to scrape articles from the Republic World homepage.
    Uses Playwright and handles infinite scroll.
    """
    name = 'republic_world'
    allowed_domains = ['republicworld.com']
    
    SCROLL_COUNT = 3

    async def start(self):
        """
        This is the entry point for the spider. It generates the first request for the homepage.
        """
        url = 'https://www.republicworld.com'
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("route", re.compile(r".*"), lambda route: route.abort() if should_abort_request(route.request) else route.continue_()),
                    PageMethod("wait_for_load_state", "networkidle")
                ],
                errback=self.errback,
            )
        )

    async def parse(self, response):
        """
        This method handles infinite scroll, finds article links, filters out video links,
        and yields requests for them.
        """
        page = response.meta.get("playwright_page")
        
        self.logger.info(f"Parsing list page and handling infinite scroll: {response.url}")

        for i in range(self.SCROLL_COUNT):
            self.logger.info(f"Scrolling down... ({i + 1}/{self.SCROLL_COUNT})")
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await page.wait_for_timeout(3000)

        final_html = await page.content()
        selector = Selector(text=final_html)

        # Use a flexible selector that works on both homepage and category pages
        article_links = selector.css('div.hr-card-box > a::attr(href), div.hrcards a::attr(href)').getall()

        if not article_links:
            self.logger.warning(f"No article links found on page: {response.url}. The website layout may have changed.")
        else:
             self.logger.info(f"Found {len(article_links)} potential links to scrape after scrolling.")

        for link in article_links:
            # Filter for article links AND explicitly ignore video links.
            if link and link.count('/') >= 2 and '/videos' not in link:
                 yield response.follow(link, callback=self.parse_article)
        
        if page:
            await page.close()

    def parse_article(self, response):
        """
        This method scrapes the data from an individual article page.
        """
        self.logger.info(f"Scraping article: {response.url}")

        article = NewsArticleItem()
        article['url'] = response.url
        
        article['headline'] = response.css('div.storyTitle h1::text').get('').strip()

        # Improved author scraping: Try the first format, if it fails, try the second.
        author = response.css('div.storyEditor a::text').get('').strip()
        if not author:
            published_by_text = response.css('p:contains("Published By :")::text').get('').strip()
            if "Published By :" in published_by_text:
                author = published_by_text.replace('Published By :', '').strip()
        article['author'] = author
        
        # Get publication date
        published_text = response.css('p:contains("Published On:")::text').get('')
        if not published_text:
            published_text = response.css('p.svelte-m7a8h8:contains("Updated")::text').get('')
        article['publication_date'] = published_text.replace('Published On:', '').replace('Updated', '').strip()
        
        body_paragraphs = response.css('div.storyContent p ::text').getall()
        article['body_text'] = " ".join(p.strip() for p in body_paragraphs if p.strip()).strip()
        
        article['source_site'] = 'Republic World'

        yield article

    async def errback(self, failure):
        """
        Handles errors that occur during the Playwright request.
        """
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        self.logger.error(f"Playwright request failed: {failure.value}")