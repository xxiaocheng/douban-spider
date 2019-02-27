
BASE_API='https://api.douban.com/%s'

class User(object):

    def __init__(self,uid):
        self.uid=uid

    def get_me(self):
        return BASE_API % 'v2/user/%s' % self.uid

    def get_following(self,page=1,count=20):
        return BASE_API%'shuo/v2/users/%s/following%s' % (self.uid ,'?page=%s&count=%s') % (str(page),str(count))
    
    def get_followers(self,page=1,count=20):
        return BASE_API%'shuo/v2/users/%s/followers%s' % (self.uid ,'?page=%s&count=%s') % (str(page),str(count))

    def __repr__(self):
        return '<User Api %s>' % self.uid

class Subject(object):

    categories={
            'CELEBRITY':'celebrity',
            'IMDB':'imdb',
            'SUBJECT':'subject'
        }

    def __init__(self,id,category='SUBJECT'):
        self.id=id
        assert category in self.categories
        self.category=category
    
    def get_subject(self):
        return BASE_API % 'v2/movie/%s/%s' % (self.categories[self.category],self.id)
    
    def __repr__(self):
        return '<%s Api %s>' % (self.category,self.id)

class Cinema(object):

    base_api=BASE_API %'v2/movie/%s?city=%s&start=%s&count=%s'

    def __init__(self,city=''):
        self.city=city

    def nowplaying(self,start=0,count=100):
        return self.base_api %('in_theaters',self.city,str(start),str(count))

    def coming(self,start=0,count=100):
        return self.base_api %('coming_soon',self.city,str(start),str(count))

    def __repr__(self):
        return '<%s Cinema info>' % self.city    
