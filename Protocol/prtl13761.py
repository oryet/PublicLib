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
        return d1, d2

    def deal3761Frame(self, frame):
        for i in range(0, len(frame), 2):
            if frame[i:i + 2] == '68' and frame[i + 10:i + 12] == '68':
                framelen = int(frame[i + 4:i + 6] + frame[i + 2:i + 4], 16) >> 2
                self.frame['end'] = frame[i + 12 + framelen * 2 + 2:i + 12 + framelen * 2 + 4]
                self.frame['crc'] = frame[i + 12 + framelen * 2 + 0:i + 12 + framelen * 2 + 2]
                if calcCheckSum(frame[i + 12:i + 12 + framelen * 2]) != self.frame['crc']:
                    return False
                self.frame['ctrl'] = frame[i + 12:i + 14]
                self.frame['A1'] = frame[i + 14:i + 18]
                self.frame['A2'] = frame[i + 18:i + 22]
                self.frame['A3'] = frame[i + 22:i + 24]
                self.frame['AFN'] = frame[i + 24:i + 26]
                self.frame['SEQ'] = frame[i + 26:i + 28]
                self.frame['DA1'] = frame[i + 28:i + 30]
                self.frame['DA2'] = frame[i + 30:i + 32]
                self.frame['pn'] = self.Data2Fun(int(self.frame['DA1'], 16), int(self.frame['DA2'], 16))
                self.frame['DT1'] = frame[i + 30:i + 32]
                self.frame['DT2'] = frame[i + 32:i + 34]
                self.frame['Fn'] = self.Data2Fun(int(self.frame['DT1'], 16), int(self.frame['DT2'], 16))
                return True
        return False

    def make3761Frame(self):
        pass


if __name__ == '__main__':
    frame = u"683200320068c95507070000027100000100a016"
    p = prtl3761()
    p.deal3761Frame(frame)
