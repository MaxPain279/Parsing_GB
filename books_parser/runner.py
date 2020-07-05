from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from books_parser import settings
from books_parser.spiders.lab24 import Lab24Spider
from books_parser.spiders.book_24 import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Lab24Spider)
    process.crawl(Book24Spider)

    process.start()
