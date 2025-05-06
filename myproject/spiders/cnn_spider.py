# myproject/spiders/cnn_spider.py
import scrapy
from myproject.items import NewsSpiderItem

class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["cnn.com", "edition.cnn.com"]
    start_urls = [
        "https://edition.cnn.com/business",
        "https://edition.cnn.com/politics",
        "https://edition.cnn.com/entertainment",
        "https://edition.cnn.com/sport"
    ]

    def parse(self, response):
        category_map = {
            "business": "Business",
            "politics": "Politics",
            "entertainment": "Arts/Culture/Celebrities",
            "sport": "Sports"
        }
        slug = response.url.split("/")[-1]
        category = category_map.get(slug, "Other")

        # Updated selector for CNN main headlines (as of May 2025)
        articles = response.css("a[href*='/2025/']")

        for article in articles:
            title = article.css("span::text").get()
            url = article.attrib["href"]

            if title and url:
                item = NewsSpiderItem()
                item["title"] = title.strip()
                item["url"] = response.urljoin(url)
                item["category"] = category
                yield item
