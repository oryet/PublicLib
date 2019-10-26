import random
from PublicLib.ACModule.simCurrent import ACsampling

POS = 0
NEG = 1

POSACT = 0
NEGACT = 1
QUADRE1 = 2
QUADRE2 = 3
QUADRE3 = 4
QUADRE4 = 5

RATE_FUN = 1  # 默认记录在三费率
RATE_DEFT_NUM = 3 + 1
RATE_MAX_NUM = 4 + 1

class energy():
    def __init__(self):
        self.POS = 0
        self.NEG = 1

        self.POSACT = 0
        self.NEGACT = 1
        self.QUADRE1 = 2
        self.QUADRE2 = 3
        self.QUADRE3 = 4
        self.QUADRE4 = 5

        self.PhaseTotal = 0
        self.PhaseA = 1
        self.PhaseB = 2
        self.PhaseC = 3

        self.RATE_FUN = 1  # 默认记录在三费率
        self.RATE_DEFT_NUM = 3 + 1
        self.RATE_MAX_NUM = 4 + 1

        self.energy = [[[0]*9 for i in range(6) ] for i in range(4)]  # 8费率 6种组合 3个相位

    def rate(self):
        return random.randint(1, 4)

    def run(self, ac, t):
        n = self.rate()
        for i in range(1,4):
            if ac.Power[POS][i] >= 0:
                d = ac.Power[POS][i] * t / 3600
                self.energy[i][POSACT][n] += d# 正向有功
                self.energy[0][POSACT][n] += d
                self.energy[i][POSACT][0] += d
                self.energy[0][POSACT][0] += d
            else:
                d = abs(ac.Power[POS][i] * t / 3600)
                self.energy[i][NEGACT][n] += d
                self.energy[0][NEGACT][n] += d
                self.energy[i][NEGACT][0] += d
                self.energy[0][NEGACT][0] += d

            if 0 <= ac.A[i] <= 90:
                d = abs(ac.Power[NEG][i] * t / 3600)
                self.energy[i][QUADRE1][n] += d
                self.energy[0][QUADRE1][n] += d
                self.energy[i][QUADRE1][0] += d
                self.energy[0][QUADRE1][0] += d
            elif 90 < ac.A[i] <= 180:
                d = abs(ac.Power[NEG][i] * t / 3600)
                self.energy[i][QUADRE2][n] += d
                self.energy[0][QUADRE2][n] += d
                self.energy[i][QUADRE2][0] += d
                self.energy[0][QUADRE2][0] += d
            elif 180 < ac.A[i] <= 270:
                d = abs(ac.Power[NEG][i] * t / 3600)
                self.energy[i][QUADRE3][n] += d
                self.energy[0][QUADRE3][n] += d
                self.energy[i][QUADRE3][0] += d
                self.energy[0][QUADRE3][0] += d
            elif 270 < ac.A[i] <= 360:
                d = abs(ac.Power[NEG][i] * t / 3600)
                self.energy[i][QUADRE4][n] += d
                self.energy[0][QUADRE4][n] += d
                self.energy[i][QUADRE4][0] += d
                self.energy[0][QUADRE4][0] += d

    def eprint(self):
        for i in range(6):
            print("%d, total: %.2f, a: %.2f, b: %.2f, c: %.2f"%(i, self.energy[0][i][0], self.energy[1][i][0], self.energy[2][i][0], self.energy[3][i][0]))
        print("\r\n")


if __name__ == '__main__':
    eng = energy()
    ac = ACsampling()
    for i in range(10):
        ac.run()
        eng.run(ac, 3600)
        eng.eprint()
