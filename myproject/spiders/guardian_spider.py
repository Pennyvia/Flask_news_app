# myproject/spiders/guardian_spider.py
import scrapy
from myproject.items import NewsSpiderItem


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = [
        "https://www.theguardian.com/uk/business",
        "https://www.theguardian.com/politics",
        "https://www.theguardian.com/uk/culture",
        "https://www.theguardian.com/uk/sport"
    ]

    def parse(self, response):
        category_map = {
            "business": "Business",
            "politics": "Politics",
            "culture": "Arts/Culture/Celebrities",
            "sport": "Sports"
        }
        # Extract slug (last path segment) to determine category
        slug = response.url.rstrip("/").split("/")[-1]
        category = category_map.get(slug, "Other")

        # The Guardian publishes articles with date in the URL, e.g. /2025/may/05/...
        # Select all links whose href contains '/2025/'
        articles = response.css("a[href*='/2025/']")

        for article in articles:
            # Use headline text inside the link
            title = article.css("::text").get()
            url = article.attrib.get("href")

            if not title or not url:
                continue

            item = NewsSpiderItem()
            item["title"] = title.strip()
            item["url"] = response.urljoin(url)
            item["category"] = category
            yield item
