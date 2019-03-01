# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MoiveItem(scrapy.Item):
    id=scrapy.Field()  # 豆瓣 🆔
    title=scrapy.Field()    # 标题
    subtype=scrapy.Field()  # 子类型，moive 或 tv    
    wish_count=scrapy.Field() # 想看的数目
    do_count=scrapy.Field() # 在看的数量
    collect_count=scrapy.Field()  # 看过的数量
    year=scrapy.Field() #年份
    images=scrapy.Field()   #封面图片地址，@字典形式
    seasons_count=scrapy.Field()    # 总季数
    episodes_count=scrapy.Field()   #集数
    countries=scrapy.Field()    # 国家 @列表形式
    genres=scrapy.Field()   #类型  @列表形式
    current_season=scrapy.Field()    #当前subject 季数
    original_title=scrapy.Field() # 原标题
    summary=scrapy.Field() # 摘要
    comments_count=scrapy.Field()   #评论数
    ratings_count=scrapy.Field()    #评分数目
    aka=scrapy.Field()  #其他标题  @列表形式

    rating=scrapy.Field() # 评分数据 
    directors=scrapy.Field()    #导演 @列表形式
    casts=scrapy.Field()    # 演员  @列表形式，包含列表id

class CelebrityItem(scrapy.Item):
    id=scrapy.Field()  #celebrity id
    aka_en=scrapy.Field() # 英文又名 @列表形式
    name=scrapy.Field() #中文名 
    gender=scrapy.Field()   #性别
    avatars=scrapy.Field() # 头像 
    aka=scrapy.Field()  #又名 @列表形式 
    name_en=scrapy.Field() # 英文名称   
    born_place=scrapy.Field()  #出生地

class RatingItem(scrapy.Item):
    id=scrapy.Field()  # 用户id
    moive_id=scrapy.Field()  #被评价的电影id
    rating=scrapy.Field() # 评分
    timestamp=scrapy.Field() # 时间戳 
    comment=scrapy.Field()# 评论数据
    tags=scrapy.Field()  # 用户对电影所打的标签 @列表