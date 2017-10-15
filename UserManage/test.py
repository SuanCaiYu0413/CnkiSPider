# -*- coding: utf-8 -*-
import pymongo
import re

from config import Config
client = pymongo.MongoClient(host=Config().MONGODB['host'], port=Config().MONGODB['port'])
tdb = client[Config().MONGODB['dbName']]
post = tdb ['cnki_keyword']

post.insert({'keyword':u'大数据','stats':'2','rand_table':'1231241'})
post.insert({'keyword':u'电网','stats':'2','rand_table':'546546'})