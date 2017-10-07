# -*- coding: utf-8 -*-
import Singleton

class Config(Singleton.singleton):

    def __init__(self):

        #Redis数据库配置
        self.REDIS = {}
        self.REDIS['host'] = '127.0.0.1'
        self.REDIS['port'] = 6379
        self.REDIS['pwd'] = None


        #MongoDB数据库配置
        self.MONGODB = {}
        self.MONGODB['host'] = '127.0.0.1'
        self.MONGODB['port'] = 27017
        self.MONGODB['pwd'] = None
        self.MONGODB['dbName'] = 'Cnki'


        #开始地址
        self.START_UTL = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB'
