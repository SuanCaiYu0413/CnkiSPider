# -*- coding:utf-8 -*-
import threadpool

from MyCnki.Spider import CnkiSpider
from threading import Timer
from MongoDB import DBConn




class manage():

    def __init__(self):
        self.dbconn = DBConn()
        self.dbconn.conn()
        self.thpool = threadpool.ThreadPool(5)



    def Task(self,dic):
        cnki = CnkiSpider(dic['table'])
        cnki.run(dic['keyword'])


    def run(self):
        keywords = self.dbconn.find_keyword()
        if len(keywords) > 0:
            requests = threadpool.makeRequests(self.Task, keywords)
            [self.thpool.putRequest(req) for req in requests]
            self.thpool.wait()
        self.timer = Timer(900, self.run)
        self.timer.start()


    def check_out(self):
        self.timer = Timer(1, self.run)
        self.timer.start()


if __name__ == "__main__":

    man = manage()
    man.check_out()