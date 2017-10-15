# coding:utf-8

#状态说明：
#   1.爬取完成
#   2.待爬取
#   3.爬取中
#   0.待审核

import pymongo
import re
import time
from config import Config
import Singleton

class DBConn(Singleton.singleton):

    def __init__(self):
        pass


    def conn(self):
        client = pymongo.MongoClient(host=Config().MONGODB['host'], port=Config().MONGODB['port'])
        self.tdb = client[Config().MONGODB['dbName']]


    def find_cache(self,keyword):
        post = self.tdb['cnki_keyword']
        keyword_dict = []
        for keyword_value in post.find({'keyword':re.compile(keyword)}):
            if keyword_value['stats'] == '1':
                temp = {'keyword':keyword_value['keyword'],'table':keyword_value['rand_table']}
                keyword_dict.append(temp)
        return keyword_dict


    def find_keyword(self,keyword_dict):
        post = self.tdb[keyword_dict['table']]
        article_list = []
        for article in post.find():
            article_list.append(article)
        return article_list

    def insert_keyword(self,keyword):

        post = self.tdb['cnki_keyword']
        row = post.find_one({'keyword':keyword})
        if row == None:
            post.insert({'keyword': keyword, 'stats': '2', 'rand_table': str(int(time.time()))})
            return True
        else:
            return False

if __name__ == "__main__":

    a = DBConn()
    a.conn()
    print a.find_cache(u'电网')
