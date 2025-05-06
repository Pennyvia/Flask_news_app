import scrapy
from myproject.items import NewsSpiderItem


class CnbcSpider(scrapy.Spider):
    name = "cnbc"
    allowed_domains = ["cnbc.com"]
    start_urls = [
        "https://www.cnbc.com/business/",
        "https://www.cnbc.com/politics/",
        "https://www.cnbc.com/entertainment/",
        "https://www.cnbc.com/sports/"
    ]

    def parse(self, response):
        # Derive category from URL (e.g., business, politics, etc.)
        category = response.url.split("/")[-2]

        articles = response.css("a.Card-title")

        for article in articles:
            title = article.css("::text").get()
            link = article.css("::attr(href)").get()

            if title and link:
                item = NewsSpiderItem()
                item['title'] = title.strip()
                item['url'] = response.urljoin(link)
                item['category'] = category
                yield item
