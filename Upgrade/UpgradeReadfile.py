#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import PublicLib.public as pfun


class UpgradeReadfile():
    def __init__(self):
        self.flen = 0
        self.fcrc = '0xffff'
        self.packnum = 0
        self.flist = []

    def ReadBinFile(self, file):
        # 打开文件
        # file = u'F:\Work\TLY2826 Cat1\升级测试程序\IotMeter.bin'
        if file == None:
            file = u'F:\\Work\\软件提交\\TLY2821\\升级包-200911\\TLY2821-03-UP0000-200911-00.bin'
        fo = open(file, "rb")  # 读取二进制文件用 rb
        print ("文件名为: ", fo.name)

        try:
            while 1:
                c = fo.read(128)
                if not c:
                    break
                else:
                    strsend = self.ByteToHex(c)
                    # print(strsend)
                    self.flist += [strsend]
                    self.flen += len(c)
                    self.fcrc = pfun.crc16hex(int(self.fcrc, 16), strsend, False)
        finally:
            fo.close()
            self.fcrc = self.fcrc[2:] + self.fcrc[:2]
            self.packnum = len(self.flist)


    def ByteToHex(self, bins):
        return ''.join(["%02X" % x for x in bins]).strip()

if __name__ == '__main__':
    file = u'F:\Work\软件提交\TLY2821\V1.0.0.1\TLY2821-00-SW0000-190409-01\TLY2821-update-V01000099-190409.bin'
    filelen = 0

    rf = UpgradeReadfile()

    # 读升级bin文件
    rf.ReadBinFile(file)
    #for i in range(len(rf.flist)):
    #    filelen += len(rf.flist[i])
    print(hex(rf.flen), rf.fcrc, rf.packnum)
