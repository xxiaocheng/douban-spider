import requests
import re

class UserMoivesUrl(object):
    base_url='https://movie.douban.com/people/%(user_id)s/%(type)s'
    
    def __init__(self,user_id):
        self.user_id=user_id

    def get_index_url(self):
        '''返回用户电影主页url 
        例如:https://movie.douban.com/people/zhouxiaopo/
        '''
        return self.base_url % {'user_id':str(self.user_id),'type':''}

    def get_wish_url(self):
        '''用户想看的电影 url'''
        return self.base_url % {'user_id':str(self.user_id),'type':'wish'}
        
    def get_do_url(self):
        '''用户在看的电视剧 url'''
        return self.base_url % {'user_id':str(self.user_id),'type':'do'}

    def get_collect_url(self):
        '''用户看过的电影 url'''
        return self.base_url % {'user_id':str(self.user_id),'type':'collect'}

def get_response_text_by_url(url):
    '''返回指定url的字符类型响应'''
    response=requests.get(url=url)
    content=response.text
    return content

def get_moives_id_one_page(movie_url):
    '''返回当前页面的所有电影的唯一 id
    '''
    content = get_response_text_by_url(movie_url)
    #编译正则表达式
    re_str='https\:\/\/movie\.douban\.com\/subject\/([0-9]+)\/'
    re_compiled=re.compile(re_str)
    object_list=re_compiled.findall(content)
    #去重复
    return list(set(object_list))

def get_moives_count(current_user):
    ''' 返回用户看过，想看 ，在看的电影（电视剧数量）
    type(current_user)=UserMoivesUrl
    '''
    index_content=get_response_text_by_url(current_user.get_index_url())
    re_str='target\=\"\_self\"\>([0-9]+)部'
    re_compiled=re.compile(re_str)
    # 返回长度为3的列表 分别表示 ‘看过‘，’想看‘，’在看‘
    result_list=re_compiled.findall(index_content)
    assert len(result_list)==3

    return result_list

def get_all_page_moive_id(first_url,count):
    '''获取所有页面的moive id
    first_url: 第一页url
    count : 总个数
    return type: list
    '''
    first_url=first_url+'?start=%s'
    moives_id=[]
    for i in range(0,int(count),15):
        moives_id+=get_moives_id_one_page(first_url % str(i))
    return moives_id

def get_user_profile_moives(user_id=None):
    '''
    返回三个列表，分别包含看过，想看,  在看的电影id
    '''
    if user_id==None:
        return [],[],[]
    current_user=UserMoivesUrl(user_id)

    count_list=get_moives_count(current_user)
    collect_moives_count=count_list[0]
    wish_moives_count=count_list[1]
    do_moives_count=count_list[2]

    collect_moives=get_all_page_moive_id(current_user.get_collect_url(),collect_moives_count)
    wish_moives=get_all_page_moive_id(current_user.get_wish_url(),wish_moives_count)
    do_moives=get_all_page_moive_id(current_user.get_do_url(),do_moives_count)

    # assert len(collect_moives)==collect_moives_count
    # assert len(wish_moives)==wish_moives_count
    # assert len(do_moives)==do_moives_count

    return collect_moives,wish_moives,do_moives