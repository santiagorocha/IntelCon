from scrapy.spiders import CrawlSpider, Rule
from wikiCTI.items import WikictiItem
from scrapy.linkextractors import LinkExtractor

class ArticleSpider(CrawlSpider):
    name = "wikicti"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Cyber_threat_intelligence"]
    rules = [
        Rule(LinkExtractor(allow=('(/wiki/)((?!:).)*$'),), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = WikictiItem()
        title = response.xpath('//h1/text()')[0].extract()
        print("Articulo con contenido sobre: "+title)
        item['title'] = title
        return item