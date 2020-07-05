import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f"https://www.leroymerlin.ru/search/?q={search}"]

    def parse(self, response: HtmlResponse):
        next_page = response.css('div.list-paginator div.next-paginator-button-wrapper a::attr(href)').extract_first()
        products_link = response.css('div.ui-sorting-cards div.product-name a::attr(href)').extract()
        for link in products_link:
            yield response.follow(link, callback=self.products_parser)
        yield response.follow(next_page, self.parse)

    def products_parser(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath("photos", "//picture[contains(@slot, 'pictures')]/source/@srcset")
        # photos = response.xpath("//picture[contains(@slot, 'pictures')]/source/@srcset").extract()
        loader.add_xpath("name", "//h1/text()")
        # name = response.xpath("//h1/text()").extract_first()
        loader.add_value("link", response.url)
        # link = response.url
        loader.add_xpath("params",
                         "//div[contains(@class, 'def-list__group')]/dt/text() | //div[contains(@class, 'def-list__group')]/dd/text()")
        # params = response.xpath(
        #     "//div[contains(@class, 'def-list__group')]/dt/text() | //div[contains(@class, 'def-list__group')]/dd/text()").extract()
        loader.add_xpath("price", "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        # price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span/text()").extract_first()
        # yield LeroymerlinItem(name=name, photos=photos, params=params, price=price, link=link)
        yield loader.load_item()
