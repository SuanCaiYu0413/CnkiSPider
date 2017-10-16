# -*- coding: utf-8 -*-
import pymongo
from Config import Config
import Singleton

class save():

    def __init__(self):
        pass

    def insert(self,item):
        self.post.insert(item)

    def conn(self,name):
        client = pymongo.MongoClient(host=Config().MONGODB['host'], port=Config().MONGODB['port'])
        self.tdb = client[Config().MONGODB['dbName']]
        self.post = self.tdb[name]

    def update_stats(self,keyword,stats):
        post = self.tdb['cnki_keyword']
        post.update({'keyword':keyword},{"$set":{"stats":str(stats)}})