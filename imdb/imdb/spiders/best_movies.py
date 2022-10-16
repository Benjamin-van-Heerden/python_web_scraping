import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating",
            headers={"User-Agent": self.user_agent},
        )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"),
            callback="parse_item",
            follow=True,
            process_request="set_user_agent",
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"
            ),
            process_request="set_user_agent",
        ),
    )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath(
                "//h1[@data-testid='hero-title-block__title']/text()"
            ).get(),
            "year": response.xpath(
                "//ul[@data-testid='hero-title-block__metadata']/li[1]/a/text()"
            ).get(),
            "duration": "".join(
                response.xpath(
                    "(//ul[@data-testid='hero-title-block__metadata'])[1]/li[3]/text()"
                ).getall()
            ),
            "genre": response.xpath("//span[@class='ipc-chip__text'][1]//text()").get(),
            "url": response.url,
            "user_agent": str(response.request.headers["User-Agent"]),
        }
