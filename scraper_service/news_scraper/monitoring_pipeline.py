# news_scraper/monitoring_pipeline.py

class MonitoringPipeline:
    def process_item(self, item, spider):
        """
        This pipeline inspects each item to gather stats for the extension.
        It does NOT connect to the database.
        """
        # --- Calculate content length for averaging later ---
        body_text = item.get('body_text', '')
        spider.monitoring_stats['content_lengths'].append(len(body_text))

        # --- Count which fields have data ---
        for field in item.fields:
            if item.get(field):
                # We only need to count successes to calculate the percentage later
                spider.monitoring_stats['field_success_counts'][field] += 1
        
        return item