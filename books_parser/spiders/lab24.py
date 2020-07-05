import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class Lab24Spider(scrapy.Spider):
    name = 'lab24'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%80%D0%BE%D0%BC%D0%B0%D0%BD/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        books_links = response.css('div.products-row div.card-column_gutter a.product-title-link::attr(href)').extract()
        for links in books_links:
            yield response.follow(links, callback=self.books_parser)
        yield response.follow(next_page, callback=self.parse)

    def books_parser(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        authors = response.css('div.product-description div.authors a.analytics-click-js::text').extract()
        price = response.css('div.product-description span.buying-priceold-val-number::text').extract_first()
        discount_price = response.css('div.product-description span.buying-pricenew-val-number::text').extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        link = response.url
        yield BooksParserItem(name=name, authors=authors, price=price,
                              discount_price=discount_price, rate=rate, link=link)
