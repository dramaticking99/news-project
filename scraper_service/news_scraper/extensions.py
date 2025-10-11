# news_scraper/extensions.py

import datetime
from collections import defaultdict
from pymongo import MongoClient
from scrapy import signals

class SpiderMonitoringExtension:

    def __init__(self, mongo_uri, mongo_db, stats):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.stats = stats
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri = crawler.settings.get('MONGO_URI')
        mongo_db = crawler.settings.get('MONGO_DATABASE_MONITORING', 'news_project_monitoring')
        ext = cls(mongo_uri, mongo_db, crawler.stats)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        return ext

    def spider_opened(self, spider):
        """ Initializes the stats collector when the spider starts. """
        spider.logger.info(f"===== Summary Report Monitoring Enabled for: {spider.name} =====")
        spider.monitoring_stats = {
            'dropped_item_count': 0,
            'content_lengths': [],
            'field_success_counts': defaultdict(int),
        }
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def item_dropped(self, item, response, exception, spider):
        """ Counts items that are dropped by any pipeline. """
        spider.monitoring_stats['dropped_item_count'] += 1

    def spider_closed(self, spider, reason):
        """ Calculates and saves the final summary report when the spider finishes. """
        spider.logger.info(f"===== Generating Summary Report for: {spider.name} =====")
        
        stats = spider.monitoring_stats
        scraped_count = self.stats.get_value('item_scraped_count', 0)
        dropped_count = stats['dropped_item_count']
        total_attempts = scraped_count + dropped_count

        # --- Calculate Overall Success/Failure Rates ---
        success_rate = (scraped_count / total_attempts * 100) if total_attempts > 0 else 0
        failure_rate = (dropped_count / total_attempts * 100) if total_attempts > 0 else 0

        # --- Calculate Field Fill Percentages ---
        field_percentages = {}
        if scraped_count > 0:
            for field, success_count in stats['field_success_counts'].items():
                percentage = (success_count / scraped_count) * 100
                field_percentages[field] = f"{percentage:.2f}%"

        # --- Calculate Average Content Length ---
        avg_content_length = 0
        if stats['content_lengths']:
            avg_content_length = sum(stats['content_lengths']) / len(stats['content_lengths'])

        # --- Build the final report document ---
        report = {
            'spider_name': spider.name,
            'end_time': datetime.datetime.utcnow(),
            'finish_reason': reason,
            'success_rate': f"{success_rate:.2f}%",
            'failure_rate': f"{failure_rate:.2f}%",
            'total_successful_scrapes': scraped_count,
            'field_data_in_successful_scrapes': field_percentages,
            'average_content_length': round(avg_content_length)
        }

        # Save the report to a new collection
        self.db['spider_summary_reports'].insert_one(report)
        spider.logger.info("Summary report saved to MongoDB.")
        self.client.close()