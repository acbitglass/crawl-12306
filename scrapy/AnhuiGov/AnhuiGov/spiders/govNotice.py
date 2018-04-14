# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from AnhuiGov.items import AnhuigovItem


class GovnoticeSpider(scrapy.Spider):
    name = 'govNotice'
    allowed_domains = ['ah.gov.cn']
    start_urls = ['http://www.ah.gov.cn/tmp/Nav_nav.shtml?SS_ID=8&tm=39520.27&Page=1']

    def parse(self, response):
        # page_total = response.xpath('//*[@id="mm2"]/div/font[2]/text()').extract()[0]
        base_url = response.url[:-1]
        for i in range(1, 3):
            url = base_url + str(i)
            yield Request(url, callback=self.get_context_url)

    def get_context_url(self, response):
        context_urls = response.xpath('//*[@id="mm2"]/ul/li/span[1]/a/@href').extract()
        for context_url in context_urls:
            yield Request(context_url, callback=self.get_text)

    def get_text(self, response):
        item = AnhuigovItem()
        item['title'] = response.xpath('//*[@id="color_printsssss"]/div/div/font/text()').extract()[0]
        item['source_publish_time'] = response.xpath('//div[@class="wzbjxx"]/p/text()[1]').extract()[0]
        item['source_url'] = response.url
        contexts = response.xpath('//*[@id="zoom"]/p/text()').extract()
        content = ''
        for context in contexts:
            content = content + context
        item['context'] = content
        item['info_source'] = response.xpath('//div[@class="wzbjxx"]/p/text()[3]').extract()[0]
        return item

