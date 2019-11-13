import random
import math
import numpy as np

volfluctu = 5
curfluctu = 5
PhaseA = 0
PhaseB = 1
PhaseC = 2
PhaseTotal = 3

U = 0
I = 1
A = 2
P = 3
Q = 4

TEST_EN = 0

class ACsampling():
    def __init__(self):
        self.ac = np.zeros([5, 4], dtype=float)  # 总/A/B/C   U/I/A/P/Q
        self.ac[U] = 220

    def vol(self):
        for i in range(3):
            if TEST_EN:
                self.ac[U][i] = 220
            else:
                self.ac[U][i] = 220 + random.uniform(0, volfluctu)

    def cur(self):
        self.ac[I] = 0
        for i in range(3):
            if TEST_EN:
                self.ac[I][i] = curfluctu
            else:
                self.ac[I][i] = random.uniform(0, curfluctu)
            self.ac[I][PhaseTotal] += self.ac[I][i]

    def angle(self):
        for i in range(3):
            if TEST_EN:
                self.ac[A][i] = 0
            else:
                self.ac[A][i] = random.randint(0, 360)

    def power(self):
        self.ac[P] = 0
        self.ac[Q] = 0
        for i in range(3):
            self.ac[P][i] = self.ac[U][i] * self.ac[I][i] * math.cos(math.radians(self.ac[A][i])) * 1e-3
            self.ac[P][PhaseTotal] += self.ac[P][i]

            self.ac[Q][i] = self.ac[U][i] * self.ac[I][i] * math.sin(math.radians(self.ac[A][i])) * 1e-3
            self.ac[Q][PhaseTotal] += self.ac[Q][i]

    def run(self):
        self.vol()
        self.cur()
        self.angle()
        self.power()

    def printAC(self):
        print("Ua:%.1f,Ub:%.1f,Uc:%.1f" % (self.ac[U][PhaseA], self.ac[U][PhaseB], self.ac[U][PhaseC]))
        print("Ia:%.4f,Ib:%.4f,Ic:%.4f,Iabc:%.4f" % (self.ac[I][PhaseA], self.ac[I][PhaseB], self.ac[I][PhaseC], self.ac[I][PhaseTotal]))
        print("Pa:%.2f,Pb:%.2f,Pc:%.2f,Pabc:%.2f" % (self.ac[P][PhaseA], self.ac[P][PhaseB], self.ac[P][PhaseC], self.ac[P][PhaseTotal]))
        print("Qa:%.2f,Qb:%.2f,Qc:%.2f,Qabc:%.2f" % (self.ac[Q][PhaseA], self.ac[Q][PhaseB], self.ac[Q][PhaseC], self.ac[Q][PhaseTotal]))
        print("\r\n")


if __name__ == '__main__':
    ac = ACsampling()
    ac.printAC()
    ac.run()
    ac.printAC()

    '''
    ac2 = ACsampling()
    ac2.printAC()
    ac2.vol()
    ac2.cur()
    ac2.power()
    ac2.printAC()
    '''
