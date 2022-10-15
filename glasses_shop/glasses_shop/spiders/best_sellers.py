import scrapy


class BestSellersSpider(scrapy.Spider):
    name = "best_sellers"
    allowed_domains = ["www.glassesshop.com"]
    start_urls = ["http://www.glassesshop.com/bestsellers"]

    def parse(self, response):
        current_page = response.xpath(
            "//li[@class='page-item active'][1]/span/text()"
        ).get()
        for title_div, price_div in zip(
            response.xpath("//div[@class='p-title']"),
            response.xpath("//div[@class='p-price']"),
        ):
            title = (title_div.xpath(".//a[1]/text()").get().strip(),)
            price = (price_div.xpath(".//div[1]/span/text()").get(),)
            yield {
                "title": title,
                "price": price,
                "current_page": current_page,
            }

        next_page = response.xpath(
            "//a[@class='page-link' and @rel='next']/@href"
        ).get()

        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
