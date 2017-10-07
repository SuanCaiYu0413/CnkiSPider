# -*- coding: utf-8 -*-
import cookielib
import urllib
import urllib2

import time


class UserAuth(object):

    def __init__(self,search_value):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.search_value = search_value


    def Auth(self):
        current_milli_time = lambda: int(round(time.time() * 1000))
        urls = [
            'http://www.cnki.net/',
            'http://kns.cnki.net/kns/Request/login.aspx?pt=1&p=/kns&td=' + str(current_milli_time())
        ]
        for url in urls:
            request = urllib2.Request(url)
            self.opener.open(request)

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

        return self.opener