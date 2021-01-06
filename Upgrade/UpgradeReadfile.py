#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import PublicLib.public as pfun

nextflag = 0

class UpgradeReadfile():
    def __init__(self):
        self.flen = 0
        self.fcrc = '0xffff'
        self.packnum = 0
        self.flist = []
        self.FILEINFO = {}


    def ReadBinFile(self, file, readlen=128):
        datastr = ''

        try:
            fo = open(file, "rb")  # 读取二进制文件用 rb
            print ("文件名为: ", fo.name)
        except:
            print('open file err!')
            return

        try:
            while 1:
                c = fo.read(readlen)
                if not c:
                    break
                else:
                    strsend = self.ByteToHex(c)
                    datastr += self.FindFileInfo(strsend)
                    # print(strsend)
                    self.flist += [strsend]
                    self.flen += len(c)
                    self.fcrc = pfun.crc16hex(int(self.fcrc, 16), strsend, False)
        finally:
            fo.close()
            self.fcrc = self.fcrc[2:] + self.fcrc[:2]
            self.packnum = len(self.flist)
            self.FILEINFO = self.GetFileInfo(datastr)
            # print FILEINFO
            for key, value in self.FILEINFO.items():
                print(key, value)

    def FindFileInfo(self, s):
        # dwSignature = 'feef04fb'
        # dwSignature = 'C37F0100'
        global nextflag
        dwSignature = 'FB04EFFE'# 'fb04effe'  # fb 04 ef fe
        ret = s.find(dwSignature)
        if ret >= 0 or nextflag == 1:
            # print(ret, s)
            if ret >= 0:
                nextflag = 1
                return s[ret:]
            else:
                nextflag = 0
                # 找到第二帧
                return s
        return ''

    def GetFileInfo(self, s):
        fileinfo = {}
        if len(s) >= 88 and s[:8] == 'FB04EFFE':
            l = []
            for i in range(0, 88, 8):
                ls = s[i:i+8]
                l += [pfun.strReverse(ls)]

            fileinfo['dwSignature'] = l[0]
            fileinfo['dwSize'] = l[1]
            fileinfo['dwFileOS'] = l[2]
            fileinfo['dwFileType'] = l[3]
            fileinfo['dwChipType'] = l[4]
            fileinfo['dwRFChipType'] = l[5]
            fileinfo['dwSWVersion'] = l[6]
            fileinfo['dwDateTime'] = l[7]
            fileinfo['dwProReleaseTime'] = l[8]
            fileinfo['dwProRecordTime'] = l[9]
            fileinfo['dwHWVersion'] = l[10]
        return fileinfo


    def ByteToHex(self, bins):
        return ''.join(["%02X" % x for x in bins]).strip()

if __name__ == '__main__':
    # file = u'F:\Work\软件提交\TLY2821\V1.0.0.1\TLY2821-00-SW0000-190409-01\TLY2821-update-V01000099-190409.bin'
    file = u'F:\\Work\\软件提交\\TLY2821\\TLY2821-03-UP0000-201211-00\\TLY2821-03-UP0000-201211-00.bin'
    filelen = 0

    rf = UpgradeReadfile()

    # 读升级bin文件
    rf.ReadBinFile(file, 200)
    #for i in range(len(rf.flist)):
    #    filelen += len(rf.flist[i])
    print(hex(rf.flen), rf.fcrc, rf.packnum, rf.FILEINFO)
