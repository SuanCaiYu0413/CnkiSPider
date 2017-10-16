# -*- coding: utf-8 -*-
import Singleton

class Config(Singleton.singleton):

    def __init__(self):


        #MongoDB数据库配置
        self.MONGODB = {}
        self.MONGODB['host'] = '127.0.0.1'
        self.MONGODB['port'] = 27017
        self.MONGODB['pwd'] = None
        self.MONGODB['dbName'] = 'Cnki'


