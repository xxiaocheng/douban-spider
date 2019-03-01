# -*- coding: utf-8 -*-
import scrapy
import re
import json

from douban.items import MoiveItem,CelebrityItem,RatingItem

from douban.user_moives_profile import UserMoivesUrl
from douban_api import User,Subject


class MoivesSpider(scrapy.Spider):
    name = 'moives'

    def start_requests(self):
        uid='zhouxiaopo'
        user_url=UserMoivesUrl(uid)
        start_url=user_url.get_collect_url()

        yield scrapy.Request(url=start_url,callable=self.parse_rating)

    
    def parse_rating(self,response):
        # 解析评分数据
        uid=response.url.split('/')[-2]  # 当前爬取的用户uid

        #获取该用户粉丝 继续爬取
        user=User(uid)
        yield scrapy.Request(url=user.get_following(page=1,count=10000),callback=self.parse_followings)

        # 准备正则表达式
        re_url='href\=\".*?\"'
        re_url_compiled=re.compile(re_url)
        re_rating='rating([0-9])\-'
        re_rating_compiled=re.compile(re_rating)
        re_timestamp='date\"\>(.*?)\<\/span\>'
        re_timestamp_compiled=re.compile(re_timestamp)
        re_comment='comment\"\>(.*?)\<\/span\>'
        re_comment_compiled=re.compile(re_comment)
        re_tags='tags\"\>(.*?)\<\/span\>'
        re_tags_compiled=re.compile(re_tags)

        item_div_list=response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div')
        for item_div in item_div_list:
            html_str=item_div.get()
            url_list=re_url_compiled.findall(html_str)
            moive_id=url_list[0].split('/')[-2]  # 获取moive 🆔
            rating=re_rating_compiled.findall(html_str)[0] #获取 评分数据
            timestamp=re_timestamp_compiled.findall(html_str)[0] # 获取评分时间
            comment=re_comment_compiled.findall(html_str)[0]
            tags=re_tags_compiled.findall(html_str)[0].split(':')[1].split()

            item=RatingItem()
            item['id']=uid
            item['moive_id']=moive_id
            item['rating']=rating
            item['timestamp']=timestamp
            item['comment']=comment
            item['tags']=tags

            moive=Subject()
            yield scrapy.Request(url=moive.get_subject(),callback=self.parse_moive)

            yield item

        next_page=response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/span[4]/a/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_rating)

    def parse_followings(self,response):
        try:
            json_response=json.loads(response.body_as_unicode())
        except:
            scrapy.log.msg("Can't parse this response to json ,url:%s !" % response.url,level=scrapy.log.ERROR,spider=self)
        for t in json_response:
            user_url=UserMoivesUrl(t['id'])
            yield scrapy.Request(url=user_url.get_collect_url(),callable=self.parse_rating)

    def parse_moive(self,response):
        try:
            json_response=json.loads(response.body_as_unicode())
        except:
            scrapy.log.msg("Can't parse this response to json ,url:%s !" % response.url,level=scrapy.log.ERROR,spider=self)
        item=MoiveItem()
        attributes=[
            'id',
            'title',
            'subtype',
            'wish_count',
            'do_count',
            'collect_count',
            'year',
            'images',
            'seasons_count',
            'episodes_count',
            'countries',
            'genres',
            'current_season',
            'original_title',
            'summary',
            'comments_count',
            'ratings_count',
            'aka',
            'rating'
        ]
        for attribute in attributes:
            item[attribute]=json_response.get(attribute,None)
        item['rating']=json_response['rating']['average']

        # 获取directors 
        directors=[]
        for t in json_response['directors']:
            directors.append(t['id'])
            celebrity=Subject(t['id'],category='CELEBRITY')
            yield scrapy.Request(url=celebrity.get_subject(),callback=self.parse_celebrity)
        item['directors']=directors

        # 获取casts
        casts=[]
        for tt in json_response['casts']:
            casts.append(tt['id'])
            celebrity=Subject(tt['id'],category='CELEBRITY')
            yield scrapy.Request(url=celebrity.get_subject(),callback=self.parse_celebrity)
        item['casts']=casts
        yield item

    def parse_celebrity(self,response):
        try:
            json_response=json.loads(response.body_as_unicode())
        except:
            scrapy.log.msg("Can't parse this response to json ,url:%s !" % response.url,level=scrapy.log.ERROR,spider=self)

        item=CelebrityItem()
        item['id']=json_response['id']
        item['aka_en']=json_response['aka_en']
        item['name']=json_response['name']
        item['gender']=json_response['gender']
        item['avatars']=json_response['avatars']
        item['aka']=json_response['aka']
        item['name_en']=json_response['name_en']
        item['born_place']=json['born_place']

        yield item
        