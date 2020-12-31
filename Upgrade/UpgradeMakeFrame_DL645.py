import sys
sys.path.append("..")
from PublicLib.Protocol.protocol import prtl2Make
from PublicLib.Protocol.protocol import judgePrtl
from PublicLib.Upgrade.UpgradeReadfile import UpgradeReadfile
import PublicLib.public as pfun
from PublicLib.Protocol.dl645 import *

'''
FILE_MANUIDEN = "594C"
FILE_DEV_TYPE = "03"
FILE_LEN = 0x000173ed
if FILE_LEN%128 == 0:
    FILE_PACK_NUM = hex((int)(FILE_LEN / 128))
else:
    FILE_PACK_NUM = hex((int)(FILE_LEN / 128) + 1)
FILE_PACK_NUM = str(FILE_PACK_NUM).replace("0x", "0000")[-4:]
FILE_LEN = hex(FILE_LEN).replace("0x", "00000000")[-8:]
FILE_CRC = "1a4c"
'''


class upgradeMakeFrame():
    def __init__(self, filename=None):
        if filename == None:
            filename = u'F:\\Work\\软件提交\\TLY2821\\TLY2821-03-UP0000-201211-00\\TLY2821-03-UP0000-201211-00.bin'
        rf = UpgradeReadfile()
        rf.ReadBinFile(filename, 128)
        self.FILE_MANUIDEN = "594C"
        self.FILE_DEV_TYPE = "03"
        self.flen = rf.flen
        self.packnum = rf.packnum
        self.FILE_LEN = hex(rf.flen).replace("0x", "").zfill(8)
        self.FILE_CRC = rf.fcrc
        self.FILE_PACK_NUM = hex(rf.packnum).replace("0x", "").zfill(4)
        self.flist = rf.flist
        self.addr = 'AAAAAAAAAAAA'
        self.FILEINFO = rf.FILEINFO
        self.password = '00000000'


    def upgradeCheckVision(self):
        data = pfun.strReverse("04A00101")
        data = Dl645DataAdd33(data)
        senddata = make645Frame('', self.addr, '11', data)
        return senddata


    def upgradeCheckPack(self):
        data = pfun.strReverse("04A00501")
        data = Dl645DataAdd33(data)
        senddata = make645Frame('', self.addr, '11', data)
        return senddata


    def upgradeStart(self):
        data = pfun.strReverse("04A00502")
        data += pfun.strReverse(self.password)
        # 产品类型 + 版本日期 + 软件版本 + 硬件版本 + 文件总长 + 总包数 + 包长度 + 文件CRC校验 + 升级模式字
        # value = "28210000#18121716#01010002#01000000#0001f9c1#03f4#80#75d3#0000"
        # value = "28210000#20121110#01031006#01030000#" + self.FILE_LEN + "#" +  self.FILE_PACK_NUM + "#" + "80" + "#" +  self.FILE_CRC + "#" + "0000"
        data += pfun.strReverse(self.FILEINFO['dwFileType'])
        data += pfun.strReverse(self.FILEINFO['dwDateTime'])
        data += pfun.strReverse(self.FILEINFO['dwSWVersion'])
        data += pfun.strReverse(self.FILEINFO['dwHWVersion'])
        data += pfun.strReverse(self.FILE_LEN)
        data += pfun.strReverse(self.FILE_PACK_NUM)
        data += '80'
        data += pfun.strReverse(self.FILE_CRC)
        data += '00'
        data += '00'
        data = Dl645DataAdd33(data)
        senddata = make645Frame('', self.addr, '14', data)
        return senddata


    def upgradeSendFile(self, i):
        sindex = hex(i+1).replace("0x", "0000")[-4:]
        data = pfun.strReverse("04A00501")
        data += pfun.strReverse(self.password)
        data += pfun.strReverse(self.FILE_MANUIDEN)
        data += pfun.strReverse(self.FILE_DEV_TYPE)
        data += pfun.strReverse(self.FILE_PACK_NUM)
        data += pfun.strReverse(sindex)
        data += self.flist[i]
        data = Dl645DataAdd33(data)
        senddata = make645Frame('', self.addr, '14', data)
        return senddata

if __name__ == '__main__':
    # filename = u'F:\\Work\\软件提交\\TLY2821\\TLY2821-03-UP0000-201211-00\\TLY2821-03-UP0000-201211-00.bin'
    filename = u'F:\Work\软件提交\TLY2821\V1.0.0.1\TLY2821-00-SW0000-190409-01\TLY2821-update-V01000099-190409.bin'
    upd = upgradeMakeFrame(filename)
    s = upd.upgradeCheckVision()
    print(s)
    s = upd.upgradeCheckPack()
    print(s)
    s = upd.upgradeStart()
    print(s)
    s = upd.upgradeSendFile(0)
    print(s)
