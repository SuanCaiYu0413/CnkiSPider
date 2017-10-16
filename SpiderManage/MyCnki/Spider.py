# -*- coding: utf-8 -*-
#调度器
import cookielib
import urllib2
import time
import Parser
from Auth import UserAuth
import DownLoad
from SaveDB import save
import Config

class CnkiSpider():

    def __init__(self,table):
        self.next_url = Config.Config().START_UTL
        self.download = DownLoad.download()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.dbconn = save()
        self.dbconn.conn('cnki' + table)

    def run(self,search_value):
        self.dbconn.update_stats(search_value,3)
        self.opener = UserAuth(search_value).Auth()
        while self.next_url:
            body = self.download.down(self.next_url,self.opener)
            result = Parser.HtmlParser().parser(body,self.dbconn)
            if result['flag'] == 'auth':
                self.opener = UserAuth(search_value).Auth()
                continue
            elif result['flag'] == 'end':
                break
            elif result['flag'] == 'pass':
                self.next_url = None
                self.next_url = result['next_url']
        self.dbconn.update_stats(search_value, 1)

if __name__ == "__main__":

    cnki = CnkiSpider('123')
    cnki.run('大数据')