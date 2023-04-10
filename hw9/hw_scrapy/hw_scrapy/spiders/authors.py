import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        author = response.xpath('/html//div[@class="author-details"]')
        yield {
            "fullname": author.xpath('h3[@class="author-title"]/text()').get().strip(),
            "born_date": author.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
            "born_location": author.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
            "description": author.xpath('div[@class="author-description"]/text()').get().strip()
        }
