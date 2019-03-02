# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import logging
import redis

class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self,redis_host,redis_port,redis_password,redis_db):
        self.redis_host=redis_host
        self.redis_port=redis_port
        self.redis_password=redis_password
        self.db=redis_db

        self.client=redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(
            redis_host=crawler.settings.get('REDIS_HOST','127.0.0.1'),
            redis_port=crawler.settings.get('REDIS_PORT','6379'),
            redis_password=crawler.settings.get('REDIS_PASSWORD'),
            redis_db=crawler.settings.get('REDIS_DB','0')
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        """判断将要下载的页面是否已经请过，通过url中唯一标识符是否已经在redis set中来判断
        """
        request_url=str(request.url)
        # 判断是否为用户看过的电影 url，避免只抓取到一页数据
        if 'collect' in request_url and '?' in request_url:
            return  None

        if '?' in request_url:
            request_url=request_url.split('?')[0]
        splited_url=request_url.split('/')
        if request_url[-1]=='/':
            id=splited_url[-2]
            cate=splited_url[-3]
            if cate=='subject':
                redis_key='MoiveItem'.lower()
            else:
                redis_key='CelebrityItem'.lower()
        else:
            if 'people' in request_url:
                id =splited_url[-2]
                redis_key='RatingItem'.lower()
            else:
                id=splited_url[-1]
                cate=splited_url[-2]
                if cate=='subject':
                    redis_key='MoiveItem'.lower()
                else:
                    redis_key='CelebrityItem'.lower()
        
        # 判断url 中唯一标识符是否已经在redis中
        if self.client.sadd(redis_key,id):
            return None
        else:
            logging.debug("IgnoreRequest : %s" % request.url)
            raise IgnoreRequest("IgnoreRequest : %s" % request.url)


        #return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
