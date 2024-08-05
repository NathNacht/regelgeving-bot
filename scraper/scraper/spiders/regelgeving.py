import scrapy

class RegelgevingSpider(scrapy.Spider):
    name = "regelgeving_spider"
    start_urls = ['https://www.vlaanderen.be/lokaal-bestuur/regelgeving?order_publicationdate=desc']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        # Select the links to the 'regelgeving' pages
        regelgeving_links = response.css('a.vl-spotlight__link-wrapper.vl-link::attr(href)').getall()
        # regelgeving_links = response.css('a.::attr(href)').getall()


        for link in regelgeving_links:
            # Absolute URL
            absolute_url = response.urljoin(link)
            yield {'url': absolute_url}

        # If there's pagination, find the next page link and follow it
        next_page = response.css('a.vl-pager__element__cta.vl-link.vl-link--bold::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse, meta={"playwright": True})

