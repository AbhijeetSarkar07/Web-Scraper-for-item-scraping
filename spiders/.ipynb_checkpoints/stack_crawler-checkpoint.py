import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from stack.items import StackItem  

class StackCrawlerSpider(CrawlSpider):
    name = "stack_crawler"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["https://stackoverflow.com/questions?pagesize=50&sort=newest&page=1"]
    page_count = 0  # Initialize a page count variable

    rules = [
        Rule(LinkExtractor(allow=r'questions\?pagesize=50&sort=newest&page=\d+'), 
             callback='parse_item', follow=True) 
    ]

    def parse_item(self, response):
        questions = response.xpath('//*[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a[@class="s-link"]/text()').get()
            item['url'] = question.xpath('a[@class="s-link"]/@href').get()
            if item['title'] and item['url']:
                item['url'] = response.urljoin(item['url'])
                yield item

        # Extract the "next" page link
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            self.page_count += 1  # Increment the page count
            if self.page_count <= 9:  # Check if the page count is less than or equal to 9
                yield response.follow(next_page, callback=self.parse_item)