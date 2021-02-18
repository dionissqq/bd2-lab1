import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess

class FirstSpider(CrawlSpider):
    num_of_links = 0 
    images = []
    name = "first_spider"
    allowed_domains = ["xsport.ua"]
    start_urls = (
        'https://xsport.ua/',
    )
    rules = (Rule(LinkExtractor(allow=()), callback="parse_items", follow=False), ) 
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 20
    }

    def parse_items(self, response):
        content = Selector(response=response).xpath('//body')
        for nodes in content:

            FirstSpider.num_of_links += len(list(set(nodes.xpath('//a').getall())))

            texts = nodes.xpath('//div/text()').getall()
            texts = list(set([t.lstrip().rstrip().replace("\n", "") for t in list(set(texts))]))

            images = nodes.xpath('//img/@src').getall()
            images = list(set(images))
            
            page = {'url' : response.url}
            page['fragments'] = [{'type':'text','data':i} for i in texts] + [{'type':'image','data':i} for i in images]

            yield page

process = CrawlerProcess(settings={
    "FEEDS": {
        "results/elements.xml": {"format": "xml"},
    },
})

process.crawl(FirstSpider)
process.start()

print(FirstSpider.num_of_links)