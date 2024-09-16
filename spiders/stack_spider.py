from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem
import logging

class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["https://stackoverflow.com/questions?pagesize=50&sort=newest&page=1"]

    def parse(self, response):
        questions = Selector(response).xpath('//*[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a[@class="s-link"]/text()').extract()[0]
            item['url'] = question.xpath('a[@class="s-link"]/@href').extract()[0]
            yield item
