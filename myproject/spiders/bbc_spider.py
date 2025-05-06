# myproject/spiders/bbc_spider.py
import scrapy
from myproject.items import NewsSpiderItem

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = [
        "https://www.bbc.com/news/business",
        "https://www.bbc.com/news/politics",
        "https://www.bbc.com/culture/entertainment-news",
        "https://www.bbc.com/sport"
    ]

    def parse(self, response):
        # Map URL keywords to categories
        category_map = {
            "business": "Business",
            "politics": "Politics",
            "entertainment-news": "Arts/Culture/Celebrities",
            "sport": "Sports"
        }
        cat_slug = response.url.split("/")[-1]
        category = category_map.get(cat_slug, "Other")

        # This selector targets BBC headlines reliably as of May 2025
        articles = response.css("a[href*='/news/']:has(h2), a[href*='/sport/']:has(h3)")

        for article in articles:
            title = article.css("h2::text, h3::text").get()
            url = article.css("::attr(href)").get()

            if title and url:
                item = NewsSpiderItem()
                item["title"] = title.strip()
                item["url"] = response.urljoin(url)
                item["category"] = category
                yield item
