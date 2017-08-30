# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import cookielib

import redis
from lxml import etree
import pymongo


class Spider():
    '''
    爬虫初始化
    '''

    def __init__(self, search_value, db_name, collection_name, db_host='127.0.0.1', db_port=27017,cache_host='127.0.0.1',cache_port=6379):

        # 配置参数
        self.search_value = search_value  # 搜索关键词
        dbHost = db_host  # 数据库地址
        dbPort = db_port  # 数据库端口
        dbName = db_name  # 数据库名称
        collectionName = collection_name  # 数据表名称
        cacheHost = cache_host  # redis地址
        cachePort = cache_port  # redis端口

        # 初始化应用
        print '----初始化爬虫属性----'
        self.urls = []
        self.hos_urls = []
        self.items = []
        self.next_link = None
        self.try_except = False
        self.swicth = True
        self.body = ''
        self.opener = None
        self.cookie = None

        # 数据库操作
        print '----初始化数据库链接----'
        client = pymongo.MongoClient(host=dbHost, port=dbPort)
        tdb = client[dbName]
        self.post = tdb[collectionName]
        self.pagepost = tdb['pagesLink']
        self.yanzheng()

        # Redis连接池
        self.pool = redis.ConnectionPool(host=cacheHost, port=cachePort)
        # r = redis.Redis(connection_pool=self.pool)

    def quchu(self, str):
        str = str.replace("\r\n", '')
        str = str.replace(';', '')
        str = str.replace(u'；', '')
        str = str.strip()
        return str

    '''
        get_url方法获取每篇文章的url地址
        和下一页地址
    '''

    def get_url(self, page_url=None):
        if page_url == None:
            url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB'
        elif page_url == False:
            exit()
        else:
            url = page_url
        request = urllib2.Request(url)
        print url

        response = self.opener.open(request)
        html = response.read()
        self.body = html
        if html.find('CheckCode') != -1:
            return False
        self.pagepost.insert({'url': url, 'time': int(time.time())})
        Selecter = etree.HTML(html)
        urls = Selecter.xpath('//table[@class="GridTableContent"]/tr/td[2]/a/@href')
        for url in urls:
            self.urls.append(url)
        if len(urls) < 20:
            self.swicth = False
            return False
        next_url = Selecter.xpath('//div[@class="TitleLeftCell"]/a/@href')
        try:
            self.next_link = 'http://kns.cnki.net/kns/brief/brief.aspx' + next_url[len(next_url) - 1]
        except IndexError as e:
            self.try_except = True
        return True

    '''
        downLoad方法对爬取url进行读取并且
        取关键数据存放到items里面
    '''

    def downLoad(self, url=None):

        r = redis.Redis(connection_pool=self.pool)
        if r.hexists('his_url', url):
            return
        r.hset('his_url', url, int(time.time()))
        url = 'http://kns.cnki.net/KCMS' + url[-len(url) + 4:]

        request = urllib2.Request(url)
        response = self.opener.open(request)
        html = response.read()
        Selecter = etree.HTML(html)
        item = dict()
        item['body'] = html
        item['title'] = Selecter.xpath('//div[@class="wxTitle"]/h2/text()')
        item['author'] = ' '.join(Selecter.xpath('//div[@class="wxTitle"]/div[@class="author"]/span/a/text()'))
        item['source'] = Selecter.xpath('//div[@class="sourinfo"]/p[@class="title"]/a/text()')
        item['summary'] = Selecter.xpath('//span[@id="ChDivSummary"]/text()')
        if len(item['source']) > 0:
            item['source'] = item['source'][0]
        if len(item['summary']) > 0:
            item['summary'] = item['summary'][0]

        tag_p = Selecter.xpath('//div[@class="wxBaseinfo"]/p')
        al = tag_p[0].xpath('//label/@id')
        for i in range(len(tag_p) + 1):
            if al[i] == 'catalog_FUND':
                keywords = Selecter.xpath('//div[@class="wxBaseinfo"]/p[%d]/a/text()' % i)
                keywords = map(self.quchu, keywords)
                item['fund'] = ' '.join(keywords)
            elif al[i] == 'catalog_KEYWORD':
                keywords = Selecter.xpath('//div[@class="wxBaseinfo"]/p[%d]/a/text()' % i)
                keywords = map(self.quchu, keywords)
                item['keywords'] = ' '.join(keywords)
            elif al[i] == 'catalog_ZTCLS':
                keywords = Selecter.xpath('//div[@class="wxBaseinfo"]/p[%d]/text()' % i)
                if len(keywords) > 0:
                    item['classNum'] = keywords[0]
        item['url'] = response.geturl()
        print '-------------------------------------------------------------'
        if len(item['title']) > 0:
            item['title'] = item['title'][0]
            print item['title']
            self.items.append(item)
            print '已收录:' + str(r.hlen('his_url'))

    '''
        阶段性写入数据库
    '''

    def write_db(self):
        for db_item in self.items:
            self.post.insert(db_item)
        self.items = []

    '''
        用户验证
    '''

    def yanzheng(self):
        # 初始化Cookie
        print '----初始化Cookie对象----'
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

        # 游客登录
        print '----游客身份登录知网获取Cookie----'
        current_milli_time = lambda: int(round(time.time() * 1000))
        urls = [
            'http://www.cnki.net/',
            'http://kns.cnki.net/kns/Request/login.aspx?pt=1&p=/kns&td=' + str(current_milli_time())
        ]
        for url in urls:
            request = urllib2.Request(url)
            self.opener.open(request)

        # 资料查询
        print '----查询[%s]相关资料----' % self.search_value
        post_data = {
            'txt_1_sel': 'SU$%=|',
            'txt_1_value1': self.search_value,
            'txt_1_special1': '%',
            'txt_extension': '',
            'expertvalue': '',
            'cjfdcode': '',
            'currentid': 'txt_1_value1',
            'dbJson': 'coreJson',
            'dbPrefix': 'SCDB',
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND',
            'db_value': '',
            'hidTabChange': '',
            'hidDivIDS': '',
            'singleDB': 'SCDB',
            'db_codes': '',
            'singleDBName': '',
            'againConfigJson': 'false',
            'action': 'scdbsearch',
            'ua': '1.11',
        }
        url = 'http://kns.cnki.net/kns/brief/default_result.aspx'
        data = urllib.urlencode(post_data)
        request = urllib2.Request(url, data)
        self.opener.open(request)
        url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx?action=&NaviCode=*&ua=1.11&formDefaultResult=&PageName=ASP.brief_default_result_aspx&DbPrefix=SCDB&DbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&db_opt=CJFQ%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND&txt_1_sel=SU%24%25%3D%7C&txt_1_value1=' + urllib.quote(
            self.search_value) + '&txt_1_special1=%25&his=0&parentdb=SCDB'
        request = urllib2.Request(url)
        self.opener.open(request)
        print '----爬虫准备就绪----'

    '''
        爬虫主控方法
    '''

    def crawl(self):
        while self.swicth:
            flag = self.get_url(self.next_link)
            if flag == False:
                for url in self.urls:
                    self.downLoad(url)
                self.write_db()
                self.urls = []
                self.yanzheng()


if __name__ == '__main__':
    spider = Spider('大数据','Cnki','ahha')
    spider.crawl()
