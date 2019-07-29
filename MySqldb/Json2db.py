#!/usr/bin/python3
# coding=utf-8

import pymysql
from PublicLib.MySqldb.MySqlApi import *


class Json2db():
    def __init__(self, dbip, dbname):
        self.ip = dbip
        self.dbname = dbname

    # 插入心跳登陆地址信息
    def insertlogin(self, addr, ip, port, rectime):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        sql = "INSERT INTO LoginHeart VALUES (\'%s\', \'%s\', %d, \'%s\')" % (addr, ip, port, rectime)
        ret = sp.execut(sql)
        if ret == 0:
            self.updateheart(addr, ip, port, rectime)
        # test print
        # sql = "SELECT * FROM LoginHeart WHERE addr like %s" % ('\'123%\'')
        # sp.showaddrlist(sql)
        db.close()

    # 更新登陆地址信息
    def updateheart(self, addr, ip, port, rectime):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        sql = "UPDATE LoginHeart SET ip = \'%s\' WHERE addr = \'%s\'" % (ip, addr)
        sp.execut(sql)
        sql = "UPDATE LoginHeart SET port = %d WHERE addr = \'%s\'" % (port, addr)
        sp.execut(sql)
        sql = "UPDATE LoginHeart SET rectime = \'%s\' WHERE addr = \'%s\'" % (rectime, addr)
        sp.execut(sql)
        db.close()

    def ip2addr(self, sp, ip):
        sql = "SELECT * FROM LoginHeart WHERE ip = \'%s\'" % (ip)
        addr = sp.selectip2addr(sql)
        return addr

    # 电压
    def insertvol(self, ip, rectime, curvetime, volta, voltb, voltc):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO volt VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f)" % (
            addr, rectime, curvetime, volta, voltb, voltc)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM volt WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM volt"
        sp.showdata(sql)
        db.close()

    # 电流
    def insertcur(self, ip, rectime, curvetime, cura, curb, curc):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO cur VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f)" % (
            addr, rectime, curvetime, cura, curb, curc)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM volt WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM cur"
        sp.showdata(sql)
        db.close()

    # 正向有功功率
    def insertinsq(self, ip, rectime, curvetime, insqsum, insqa, insqb, insqc):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO insq VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f)" % (
            addr, rectime, curvetime, insqsum, insqa, insqb, insqc)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM volt WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM insq"
        sp.showdata(sql)
        db.close()

    # 反向有功功率
    def insertinsp(self, ip, rectime, curvetime, inspsum, inspa, inspb, inspc):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO insp VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f)" % (
            addr, rectime, curvetime, inspsum, inspa, inspb, inspc)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM volt WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM insp"
        sp.showdata(sql)
        db.close()

    # 功率因素
    def insertpwrf(self, ip, rectime, curvetime, pwrfsum, pwrfa, pwrfb, pwrfc):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO pwrf VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f)" % (
            addr, rectime, curvetime, pwrfsum, pwrfa, pwrfb, pwrfc)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM volt WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM pwrf"
        sp.showdata(sql)
        db.close()

    # 正向有功电能量
    def insertposeng(self, ip, rectime, curvetime, posengsum, poseng1, poseng2, poseng3, poseng4, poseng5, poseng6,
                     poseng7, poseng8):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO poseng VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f, %f, %f, %f, %f, %f, %f)" % (
            addr, rectime, curvetime, posengsum, poseng1, poseng2, poseng3, poseng4, poseng5, poseng6,
            poseng7, poseng8)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM poseng WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM poseng"
        sp.showdata(sql)
        db.close()

    # 反向有功电能量
    def insertnegeng(self, ip, rectime, curvetime, negengsum, negeng1, negeng2, negeng3, negeng4, negeng5, negeng6,
                     negeng7, negeng8):
        db = pymysql.connect(self.ip, "root", "123456", self.dbname)
        sp = MySqlApi(db)
        addr = self.ip2addr(sp, ip)
        sql = "INSERT INTO negeng VALUES (\'%s\', \'%s\', \'%s\', %f, %f, %f, %f, %f, %f, %f, %f, %f)" % (
            addr, rectime, curvetime, negengsum, negeng1, negeng2, negeng3, negeng4, negeng5, negeng6,
            negeng7, negeng8)
        ret = sp.execut(sql)
        # test print
        # sql = "SELECT * FROM negeng WHERE curvetime = \'%s\'" % (curvetime)
        sql = "SELECT * FROM negeng"
        sp.showdata(sql)
        db.close()


if __name__ == '__main__':
    jdb = Json2db("192.168.127.200", "test")
    # jdb.insertvol('123456700005', '2019-7-29 08:43:09', '2019-7-29 08:43:09', 223.2, 232.1, 111.1)
    # jdb.insertcur('192.168.2.005', '2019-7-29 12:43:13', '2019-7-29 12:45:13', 0.561239, 0.123456,  0.014741)
    # jdb.insertnegeng('192.168.2.005', '2019-7-29 12:43:13', '2019-7-29 12:45:13', 123456.78, 0, 0, 123456.78, 0, 0, 0, 0, 0)
