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

    def find_keyword(self):
        post = self.tdb['cnki_keyword']
        keyword_list = []
        for row in post.find({'stats':'2'}):
            keyword_list.append({'keyword':row['keyword'].encode('utf-8'),'table':row['rand_table']})
        return keyword_list

if __name__ == "__main__":

    a = DBConn()
    a.conn()
    print a.find_keyword()

