import scrapy

# need splash for this - javascript is messing with the page
class DebtSpider(scrapy.Spider):
    name = "debt"
    allowed_domains = ["worldpopulationreview.com"]
    start_urls = [
        "https://worldpopulationreview.com/country-rankings/countries-by-national-debt/"
    ]

    def parse(self, response):
        rows = response.xpath("//tbody/tr")
        print(rows)
        for row in rows:
            country_name = row.xpath(".//td[1]/a/text()").get()
            debt_to_gdp = row.xpath(".//td[2]/text()").get()[:-1]
            yield {"country": country_name, "debt_to_gdp": debt_to_gdp}
