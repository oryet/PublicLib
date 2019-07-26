#!/usr/bin/python3
# coding=utf-8

import pymysql
from PublicLib.MySqldb.MySqlApi import *

class Json2db():
    def __init__(self, dbip, dbname):
        self.ip = dbip
        self.dbname = dbname

    def insertlogin(self, addr, ip, port, rectime):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        sql = "INSERT INTO LoginHeart VALUES (\'%s\', \'%s\', %d, \'%s\')" % (addr, ip, port, rectime)
        sp.execut(sql)
        db.close()

    def updateheart(self, addr, ip, port, rectime):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        sql = "UPDATE LoginHeart SET ip = \'%s\' WHERE addr = \'%s\'" % (ip, addr)
        sp.execut(sql)
        sql = "UPDATE LoginHeart SET port = %d WHERE addr = \'%s\'" % (port, addr)
        sp.execut(sql)
        sql = "UPDATE LoginHeart SET rectime = \'%s\' WHERE addr = \'%s\'" % (rectime, addr)
        sp.execut(sql)
        sql = "SELECT * FROM LoginHeart WHERE addr like %s" % ('\'123%\'')
        sp.showaddrlist(sql)
        db.close()



if __name__ == '__main__':
    jdb = Json2db("192.168.127.200", "test")
    jdb.insertlogin('123456700004', '192.168.2.004', 12001, '2019-7-26 16:50:02')
    jdb.updateheart('123456700001', '192.168.2.005', 12005, '2019-7-26 17:07:01')