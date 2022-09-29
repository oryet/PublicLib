import random
import numpy as np
from PublicLib.ACModule.simCurrent import ACsampling

POS = 0
NEG = 1

POSACT = 0
NEGACT = 1
QUADRE1 = 2
QUADRE2 = 3
QUADRE3 = 4
QUADRE4 = 5

TEST_EN = 1

DemandWindows = 15


class energy():
    def __init__(self, phaseNum=1):
        if phaseNum == 1 or phaseNum == 3:
            self.phaseNum = phaseNum
        else:
            self.phaseNum = 3  # 默认三相表

        self.RATE_DEFAULT_NUM = 3  # 默认记录在三费率
        self.RATE_MAX_NUM = 4

        self.energy = np.zeros([4, 6, 9], dtype=float)  # (总ABC) （正/反/I/II/III/IV）(总1~8费率)
        self.demand = np.zeros([4, 6, 9], dtype=float)  # (总ABC) （正/反/I/II/III/IV）(总1~8费率)

    def rate(self):
        if TEST_EN == 0:
            return random.randint(1, self.RATE_MAX_NUM)
        else:
            return self.RATE_DEFAULT_NUM

    def demandrun(self, ac, t, n):
        for i in range(1, self.phaseNum + 1):
            if t < DemandWindows:
                rate1 = t / DemandWindows
                rate2 = 1 - rate1
            else:
                rate1 = 1
                rate2 = 0

            if ac[3][i] >= 0:
                dpos = ac[3][i]
                dnge = 0
            else:
                dpos = 0
                dnge = ac[3][i]

            dpos = self.demand[i][POSACT][0] * rate2 + dpos * rate1
            self.demand[i][POSACT][n] = dpos  # 正向有功
            self.demand[0][POSACT][n] = dpos
            self.demand[i][POSACT][0] = dpos
            self.demand[0][POSACT][0] = dpos

            dnge = abs(self.demand[i][NEGACT][0] * rate2 + dnge * rate1)
            self.demand[i][NEGACT][n] = dnge
            self.demand[0][NEGACT][n] = dnge
            self.demand[i][NEGACT][0] = dnge
            self.demand[0][NEGACT][0] = dnge

            if 0 <= ac[2][i] <= 90:
                dqua1 = ac[4][i]
                dqua2 = 0
                dqua3 = 0
                dqua4 = 0
            elif 90 < ac[2][i] <= 180:
                dqua1 = 0
                dqua2 = ac[4][i]
                dqua3 = 0
                dqua4 = 0
            elif 180 < ac[2][i] <= 270:
                dqua1 = 0
                dqua2 = 0
                dqua3 = ac[4][i]
                dqua4 = 0
            elif 270 < ac[2][i] <= 360:
                dqua1 = 0
                dqua2 = 0
                dqua3 = 0
                dqua4 = ac[4][i]
            else:
                dqua1 = 0
                dqua2 = 0
                dqua3 = 0
                dqua4 = 0

            dqua1 = abs(self.demand[i][QUADRE1][0] * rate2 + dqua1 * rate1)
            self.demand[i][QUADRE1][n] = dqua1
            self.demand[0][QUADRE1][n] = dqua1
            self.demand[i][QUADRE1][0] = dqua1
            self.demand[0][QUADRE1][0] = dqua1

            dqua2 = abs(self.demand[i][QUADRE2][0] * rate2 + dqua2 * rate1)
            self.demand[i][QUADRE2][n] = dqua2
            self.demand[0][QUADRE2][n] = dqua2
            self.demand[i][QUADRE2][0] = dqua2
            self.demand[0][QUADRE2][0] = dqua2

            dqua3 = abs(self.demand[i][QUADRE3][0] * rate2 + dqua3 * rate1)
            self.demand[i][QUADRE3][n] = dqua3
            self.demand[0][QUADRE3][n] = dqua3
            self.demand[i][QUADRE3][0] = dqua3
            self.demand[0][QUADRE3][0] = dqua3

            dqua4 = abs(self.demand[i][QUADRE4][0] * rate2 + dqua4 * rate1)
            self.demand[i][QUADRE4][n] = dqua4
            self.demand[0][QUADRE4][n] = dqua4
            self.demand[i][QUADRE4][0] = dqua4
            self.demand[0][QUADRE4][0] = dqua4

    def energyrun(self, ac, t, n):
        for i in range(1, self.phaseNum + 1):
            if ac[3][i] >= 0:
                d = ac[3][i] * t / 3600
                self.energy[i][POSACT][n] += d  # 正向有功
                self.energy[0][POSACT][n] += d
                self.energy[i][POSACT][0] += d
                self.energy[0][POSACT][0] += d
            else:
                d = abs(ac[3][i] * t / 3600)
                self.energy[i][NEGACT][n] += d
                self.energy[0][NEGACT][n] += d
                self.energy[i][NEGACT][0] += d
                self.energy[0][NEGACT][0] += d

            if 0 <= ac[2][i] <= 90:
                d = abs(ac[4][i] * t / 3600)
                self.energy[i][QUADRE1][n] += d
                self.energy[0][QUADRE1][n] += d
                self.energy[i][QUADRE1][0] += d
                self.energy[0][QUADRE1][0] += d
            elif 90 < ac[2][i] <= 180:
                d = abs(ac[4][i] * t / 3600)
                self.energy[i][QUADRE2][n] += d
                self.energy[0][QUADRE2][n] += d
                self.energy[i][QUADRE2][0] += d
                self.energy[0][QUADRE2][0] += d
            elif 180 < ac[2][i] <= 270:
                d = abs(ac[4][i] * t / 3600)
                self.energy[i][QUADRE3][n] += d
                self.energy[0][QUADRE3][n] += d
                self.energy[i][QUADRE3][0] += d
                self.energy[0][QUADRE3][0] += d
            elif 270 < ac[2][i] <= 360:
                d = abs(ac[4][i] * t / 3600)
                self.energy[i][QUADRE4][n] += d
                self.energy[0][QUADRE4][n] += d
                self.energy[i][QUADRE4][0] += d
                self.energy[0][QUADRE4][0] += d

    def run(self, ac, t):
        n = self.rate()
        self.energyrun(ac, t, n)
        self.demandrun(ac, t, n)  # 需量计算

    def eprint(self):
        for i in range(6):
            print("%d, energy total: %.2f, a: %.2f, b: %.2f, c: %.2f" % (
                i, self.energy[0][i][0], self.energy[1][i][0], self.energy[2][i][0], self.energy[3][i][0]))
            print("%d, demand total: %.2f, a: %.2f, b: %.2f, c: %.2f" % (
                i, self.demand[0][i][0], self.demand[1][i][0], self.demand[2][i][0], self.demand[3][i][0]))
        print("\r\n")


if __name__ == '__main__':
    eng = energy(3)
    ins = ACsampling()
    for i in range(32):
        ins.run()
        eng.run(ins.ac, 5)
        eng.eprint()
