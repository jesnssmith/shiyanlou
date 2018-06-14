# -*- coding: utf-8 -*-

import scrapy
from shiyanlou.items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):

    name = 'repositories'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com']


    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.css('li.d-block'):
            yield RepositoryItem({
                'name': repository.css('h3 a::text').extract_first().strip(),
                'update_time': repository.css('relative-time::attr(datetime)').extract_first()
                })
