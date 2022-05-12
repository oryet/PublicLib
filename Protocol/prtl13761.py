from PublicLib.public import calcCheckSum


class prtl3761():
    def __init__(self):
        self.frame = {}

    def Data2Fun(self, d1, d2):
        for i in range(8):
            if d1 >> i:
                return d2 * 8 + i
        return 0

    def Fun2Data(self, fun):
        d2 = fun / 8
        d1 = fun % 8
        return int(d1), int(d2)

    def deal3761Frame(self, frame):
        for i in range(0, len(frame), 2):
            if frame[i:i + 2] == '68' and frame[i + 10:i + 12] == '68':
                framelen = int(frame[i + 4:i + 6] + frame[i + 2:i + 4], 16) >> 2
                self.frame['end'] = frame[i + 12 + framelen * 2 + 2:i + 12 + framelen * 2 + 4]
                self.frame['crc'] = frame[i + 12 + framelen * 2 + 0:i + 12 + framelen * 2 + 2]
                crc = calcCheckSum(frame[i + 12:i + 12 + framelen * 2])
                if crc != self.frame['crc'].lower():
                    return False
                self.frame['ctrl'] = frame[i + 12:i + 14]
                addr = {}
                addr['A1'] = frame[i + 14:i + 18]
                addr['A2'] = frame[i + 18:i + 22]
                addr['A3'] = frame[i + 22:i + 24]
                self.frame['Addr'] = addr
                self.frame['AFN'] = frame[i + 24:i + 26]
                self.frame['SEQ'] = frame[i + 26:i + 28]
                DA = {}
                DA['DA1'] = frame[i + 28:i + 30]
                DA['DA2'] = frame[i + 30:i + 32]
                DA['pn'] = self.Data2Fun(int(DA['DA1'], 16), int(DA['DA2'], 16))
                self.frame['DA'] = DA
                DT = {}
                DT['DT1'] = frame[i + 30:i + 32]
                DT['DT2'] = frame[i + 32:i + 34]
                DT['Fn'] = self.Data2Fun(int(DT['DT1'], 16), int(DT['DT2'], 16))
                self.frame['DT'] = DT
                return True
        return False

    def frameAFN00(self, fn):
        self.frame['AFN'] = '00'
        dt1, dt2 = self.Fun2Data(fn)
        self.frame['DT']['DT1'] = hex(dt1).replace('0x', '00')[-2:]
        self.frame['DT']['DT2'] = hex(dt2).replace('0x', '00')[-2:]

    def make3761Frame(self, du):
        self.frame['ctrl'] = '40'
        datastr = self.frame['ctrl'] + self.frame['Addr']['A1'] + self.frame['Addr']['A2'] + self.frame['Addr']['A3']
        datastr += self.frame['AFN'] + self.frame['SEQ']
        datastr += self.frame['DA']['DA1'] + self.frame['DA']['DA2']
        datastr += self.frame['DT']['DT1'] + self.frame['DT']['DT2']
        datastr += du  # 数据单元

        self.frame['crc'] = calcCheckSum(datastr)

        datalen = int(len(datastr) / 2)
        datalenstr = hex(datalen << 2).replace('0x', '00')[-2:] + '00'
        self.frame['len'] = datalenstr[-4:]

        frame = '68' + self.frame['len'] + self.frame['len'] + '68' + datastr + self.frame['crc'] + '16'
        return frame

    def LoginHeartFrame(self, frame):
        if self.deal3761Frame(frame):
            if self.frame['AFN'] == "02" and (self.frame['DT']['Fn'] == 0 or self.frame['DT']['Fn'] == 3):
                self.frameAFN00(0)
                return self.make3761Frame(date='')
        return None


if __name__ == '__main__':
    # frame = u"683200320068c95507070000027100000100a016"
    frame = u'6839013901684B02438B07140D6F02010114251211020104142512110401011425121104010414251211080101142512110801041425121110010114251211100104142512112001011425121120010414251211E916'
    p = prtl3761()
    p.deal3761Frame(frame)
    print(p.frame)

    p.frameAFN00(0)
    f = p.make3761Frame(date='')
    print(f)
