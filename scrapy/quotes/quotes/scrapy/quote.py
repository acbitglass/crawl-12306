# -*- coding: utf-8 -*-
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        response_next = response.css('.quote')
        print(response_next)
        for item in response_next:
            text = item.xpath('span[1]/text()').extract()
            author = item.xpath('span[2]/small/text()').extract()
            tags = item.xpath('div/a/text()').extract()
            # tags = item.xpath('div').re('a class="tag" href=".*?">(.*?)</a>')
            # tags = item.xpath('div[class="tag"]/a/text').extract()
            print(tags)
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }

        next_url = response.xpath('/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a/@href').extract()[0]
        url = 'http://quotes.toscrape.com'+next_url
        yield scrapy.Request(url, callback=self.parse)
