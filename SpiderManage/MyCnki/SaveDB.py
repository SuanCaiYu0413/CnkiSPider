# -*- coding: utf-8 -*-
import pymongo
from Config import Config
import Singleton

class save(Singleton.singleton):

    def __init__(self):
        pass

    def insert(self,item):
        self.post.insert(item)

    def conn(self,name):
        client = pymongo.MongoClient(host=Config().MONGODB['host'], port=Config().MONGODB['port'])
        tdb = client[Config().MONGODB['dbName']]
        self.post = tdb[name]