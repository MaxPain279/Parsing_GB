import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class Book24Spider(scrapy.Spider):
    name = 'book_24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D1%80%D0%BE%D0%BC%D0%B0%D0%BD%D1%8B']

    def parse(self, response: HtmlResponse):
        next_page = response.css('div.catalog-pagination__list a.catalog-pagination__item::attr(href)').extract_first()
        books_links = response.css('div.book__content a.book__title-link::attr(href)').extract()
        for links in books_links:
            yield response.follow(links, callback=self.books_parser)
        yield response.follow(next_page, callback=self.parse)

    def books_parser(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        authors = response.css('div.item-detail__tabs-box a.item-tab__chars-link::text').extract()
        price = response.css('div.item-actions__container div.item-actions__price-old::text').extract_first()
        discount_price = response.xpath(
            "//div[@class='item-actions__prices']//div[@class='item-actions__price']/b/text()").extract_first()
        rate = response.css("div.item-detail__informations-box span.rating__rate-value::text").extract_first()
        link = response.url
        print(name, authors, price, discount_price, rate, link)
        yield BooksParserItem(name=name, authors=authors, price=price,
                              discount_price=discount_price, rate=rate, link=link)
