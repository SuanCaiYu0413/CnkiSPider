# -*- coding: utf-8 -*-
import urllib2

import Singleton
import bs4
from SaveDB import save
from DownLoad import download

class HtmlParser(Singleton.singleton):

    def __init__(self):
        pass

    def parser(self,body,conn):
        select = bs4.BeautifulSoup(body['html'],'lxml')
        table = select.find('table',{'class':'GridTableContent'})
        next_node = select.find('a',{'id':'Page_next'})
        if table == None and next_node == None:
            #出验证
            return {'flag':'auth'}
        elif table != None and next_node == None:
            #结束了
            self.parser_list(select,conn)
            return {'flag':'end'}
        else:
            return {'flag':'pass','next_url':self.parser_list(select,conn)}


    def parser_list(self,select,conn):
        table = select.find_all('table', {'class': 'GridTableContent'})
        trs = table[0].find_all('tr')
        item = {}
        for tr in trs[1:]:
            tds = tr.find_all('td')
            item['title'] = tds[1].get_text().strip()
            item['author'] = tds[2].get_text().strip()
            item['source'] = tds[3].get_text().strip()
            item['datetime'] = tds[4].get_text().strip()
            item['downcount'] = tds[7].get_text().strip()
            item['url'] = tds[1].find_all('a')[0].attrs['href']
            item['url'] = 'http://kns.cnki.net/KCMS' + item['url'][-len(item['url']) + 4:]
            self.parser_content({'item':item,'html':download().down(item['url'],urllib2.build_opener())},conn)
        next_node = select.find('a', {'id': 'Page_next'})
        if next_node:
            return 'http://kns.cnki.net/kns/brief/brief.aspx' + next_node['href']
        else:
            return None

    def parser_content(self,body,conn):
        item = body['item']
        # for a in item:
        #     print '%s:%s'%(a,item[a])
        html = body['html']
        select = bs4.BeautifulSoup(html['html'],'lxml')
        #获取协助单位
        spans = select.find_all('div',{'class':'orgn'})[0].find_all('span')
        orgn = []
        for span in spans:
            orgn.append(span.get_text().strip())
        item['orgn'] = ';'.join(orgn)

        #获取摘要
        ChDivSummary = select.find('span', {'id': 'ChDivSummary'})
        if ChDivSummary:
            item['ChDivSummary'] = ChDivSummary.get_text().strip()

        #获取关键词
        keywords_node = select.find('label',{'id':'catalog_KEYWORD'})
        keywords = []
        if keywords_node:
            for a in keywords_node.parent.find_all('a'):
                keywords.append(a.get_text().strip())
        item['keywords'] = ''.join(keywords)

        #获取doi
        doi_node = select.find('label',{'id':'catalog_ZCDOI'})
        if doi_node:
            item['doi'] = doi_node.parent.get_text().strip()

        #获取分类号
        ztcls_node = select.find('label', {'id': 'catalog_ZTCLS'})
        if ztcls_node:
            item['ztcls'] = ztcls_node.parent.get_text().strip()

        #获取基金
        funds_node = select.find('label', {'id': 'catalog_KEYWORD'})
        funds = []
        if funds_node:
            for a in funds_node.parent.find_all('a'):
                funds.append(a.get_text().strip())
        item['funds'] = ''.join(funds)

        if '_id' in item:
            del(item['_id'])
        print item['title']
        conn.insert(item)