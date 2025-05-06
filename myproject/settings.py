# settings.py

BOT_NAME = "myproject"

SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"

# Don’t obey robots.txt (you already had this)
ROBOTSTXT_OBEY = False

# Allow inspecting HTTP 451 if needed
HTTPERROR_ALLOWED_CODES = [451]

# Use asyncio reactor (required by scrapy-playwright)
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# ------------------------------------------------------------
# Playwright Configuration
# ------------------------------------------------------------
# Delegate all downloads through Playwright so JS gates are solved
DOWNLOAD_HANDLERS = {
    "http":  "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Launch headless Chromium
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    # Optional tweaks:
    # "timeout": 30000,
    # "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
# ------------------------------------------------------------

# Feed export encoding
FEED_EXPORT_ENCODING = "utf-8"

# User agent override
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)

# Your existing pipelines
ITEM_PIPELINES = {
    "myproject.pipelines.CsvPipeline": 300,
}

# If you want a single CSV output via Scrapy’s feed exporter:
FEEDS = {
    "reuters_news.csv": {
        "format": "csv",
        "encoding": "utf8",
        "fields": ["title", "url","category",],  # adjust to your item’s fields
    }
}

# Optional: HTTP proxy support (unrelated to Playwright)
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 750,
}
HTTP_PROXY = "http://your_proxy_here:port"
