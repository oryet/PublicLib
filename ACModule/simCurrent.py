import random
import math

volfluctu = 20
curfluctu = 20
PhaseA = 0
PhaseB = 1
PhaseC = 2
PhaseTotal = 3

POS = 0
NEG = 1


class ACsampling():
    def __init__(self):
        self.I = [0]*4
        self.A = [0] * 4
        self.U = [220]*3
        self.Power = [[0] * 4, [0] * 4]  # 总/A/B/C

    def vol(self):
        for i in range(3):
            self.U[i] = 220 + random.uniform(0, volfluctu)

    def cur(self):
        for i in range(3):
            self.I[i] = random.uniform(0, curfluctu)
            self.I[PhaseTotal] += self.I[i]

    def angle(self):
        for i in range(3):
            self.A[i] = random.randint(0, 360)

    def power(self):
        self.Power[POS][PhaseTotal] = 0
        self.Power[NEG][PhaseTotal] = 0
        for i in range(3):
            self.Power[POS][i] = self.U[i] * self.I[i] * math.cos(math.radians(self.A[i])) * 1e-4
            self.Power[POS][PhaseTotal] += self.Power[POS][i]

            self.Power[NEG][i] = self.U[i] * self.I[i] * math.sin(math.radians(self.A[i])) * 1e-4
            self.Power[NEG][PhaseTotal] += self.Power[NEG][i]

    def run(self):
        self.vol()
        self.cur()
        self.angle()
        self.power()

    def printAC(self):
        print("Ua:%.1f,Ub:%.1f,Uc:%.1f" % (self.U[PhaseA], self.U[PhaseB], self.U[PhaseC]))
        print("Ia:%.4f,Ib:%.4f,Ic:%.4f,Iabc:%.4f" % (self.I[PhaseA], self.I[PhaseB], self.I[PhaseC], self.I[PhaseTotal]))
        print("Pacta:%.2f,Pactb:%.2f,Pactc:%.2f,Pactabc:%.2f" % (self.Power[POS][PhaseA], self.Power[POS][PhaseB], self.Power[POS][PhaseC], self.Power[POS][PhaseTotal]))
        print("Preaa:%.2f,Preab:%.2f,Preac:%.2f,Preaabc:%.2f" % (self.Power[NEG][PhaseA], self.Power[NEG][PhaseB], self.Power[NEG][PhaseC], self.Power[NEG][PhaseTotal]))
        print("\r\n")


if __name__ == '__main__':
    ac = ACsampling()
    ac.printAC()
    ac.vol()
    ac.cur()
    ac.power()
    ac.printAC()

    '''
    ac2 = ACsampling()
    ac2.printAC()
    ac2.vol()
    ac2.cur()
    ac2.power()
    ac2.printAC()
    '''
