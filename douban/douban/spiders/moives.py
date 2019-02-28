# -*- coding: utf-8 -*-
import scrapy


class MoivesSpider(scrapy.Spider):
    name = 'moives'
    start_urls = ['http://douban.com/']

    def parse(self, response):
        pass
