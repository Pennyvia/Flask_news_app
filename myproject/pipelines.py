# pipelines.py
import csv

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open(f"{spider.name}_news.csv", 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['title','url','category'])

    def process_item(self, item, spider):
        self.writer.writerow([item['title'], item['url'], item['category']])
        return item

    def close_spider(self, spider):
        self.file.close()
