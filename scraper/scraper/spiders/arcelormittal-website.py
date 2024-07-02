import logging

from scrapy.spiders import SitemapSpider

logger = logging.getLogger(__name__)


class MySpider(SitemapSpider):
    name = "arcelormittal-website"
    sitemap_urls = ['https://corporate.arcelormittal.com/sitemap.xml']

    def sitemap_filter(self, entries):
        skip_patterns = ['/about/', '/investors/', '/media/']
        for entry in entries:
            loc = entry["loc"]
            if any(skip_pattern in loc for skip_pattern in skip_patterns):
                continue
            yield entry

    def parse(self, response):
        main_tag = response.css('main').extract_first()
        if main_tag:
            filename = response.url.replace('https://corporate.arcelormittal.com/', '').replace('/', '--')
            # main_tag = f"{response.url}\n{main_tag}"
            with open(f'data/website/{filename}.html', 'w', encoding='utf-8') as file:
                file.write(main_tag)
