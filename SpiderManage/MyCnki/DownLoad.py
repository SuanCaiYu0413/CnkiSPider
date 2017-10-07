# -*- coding: utf-8 -*-
import urllib2

import Singleton

class download(Singleton.singleton):


    def down(self,url,opener):
        request = urllib2.Request(url)
        response = opener.open(request)
        return {'html':response.read(),'length':response.info()['Content-Length'],'url':response.geturl()}