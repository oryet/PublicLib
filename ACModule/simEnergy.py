from PublicLib.ACModule.simCurrent import ACsampling

POS = 0
NEG = 1

POSACT = 0
NEGACT = 1
QUADRE1 = 2
QUADRE2 = 3
QUADRE3 = 4
QUADRE4 = 5


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

        self.energy = [[0] * 4, [0] * 4, [0] * 4, [0] * 4, [0] * 4, [0] * 4]

    def run(self, ac, t):
        for i in range(3):
            if ac.Power[POS][i] >= 0:
                self.energy[POSACT][i] += ac.Power[POS][i] * t / 3600
            else:
                self.energy[NEGACT][i] += ac.Power[POS][i] * t / 3600

            if 0 <= ac.A[i] <= 90:
                self.energy[QUADRE1][i] += ac.Power[NEG][i] * t / 3600
            elif 90 < ac.A[i] <= 180:
                self.energy[QUADRE2][i] += ac.Power[NEG][i] * t / 3600
            elif 180 < ac.A[i] <= 270:
                self.energy[QUADRE3][i] += ac.Power[NEG][i] * t / 3600
            elif 270 < ac.A[i] <= 360:
                self.energy[QUADRE4][i] += ac.Power[NEG][i] * t / 3600

    def eprint(self):
        for i in range(6):
            print("%d, a: %.2f, a: %.2f, a: %.2f, a: %.2f"%(i, self.energy[i][0], self.energy[i][1], self.energy[i][2], self.energy[i][3]))
        print("\r\n")


if __name__ == '__main__':
    eng = energy()
    ac = ACsampling()
    for i in range(10):
        ac.run()
        eng.run(ac, 3600)
        eng.eprint()
