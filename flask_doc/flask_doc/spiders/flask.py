# -*- coding: utf-8 -*-
import scrapy
from scrapy import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/0.12']

    rules = (
            Rule(LinkExtractor(allow=('/docs/0.12/',)), callback='parse_page')
            )


    def parse_page(self, response):
        item = PageItem()
        item['url'] = response.url
        item['text'] = response.css('p::text').extract()

        yield item
