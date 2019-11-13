import numpy as np


defultcfg = {'day': 62, 'month': 12, 'hour': 24}

class freeze():
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = defultcfg
        if 0 < cfg['day'] <= 62:
            self.day = np.zeros([cfg['day'], 4, 6, 9], dtype=float)
        else:
            self.day = np.zeros([62, 4, 6, 9], dtype=float)

        if 0 < cfg['month'] <= 12:
            self.mon = np.zeros([cfg['month'], 4, 6, 9], dtype=float)
        else:
            self.mon = np.zeros([12, 4, 6, 9], dtype=float)

        if 0 < cfg['hour'] <= 24:
            self.hour = np.zeros([cfg['hour'], 4, 6, 9], dtype=float)
        else:
            self.hour = np.zeros([24, 4, 6, 9], dtype=float)

    def FreezeData(self, type, eng):
        if type == 'month':
            self.mon = np.append(self.mon, [eng], axis=0)
            self.mon = np.delete(self.mon, 0, 0)
        elif type == 'day':
            self.day = np.append(self.day, [eng], axis=0)
            self.day = np.delete(self.day, 0, 0)
        elif type == 'hour':
            self.hour = np.append(self.hour, [eng], axis=0)
            self.hour = np.delete(self.hour, 0, 0)

    # test fun
    def FreezeRun(self, cfg, eng, ins):
        mon = cfg['month']
        day = cfg['day']
        hour = cfg['hour']

        daym = int(day / 30)
        hourd = int(hour / 24)

        if mon >= daym:
            mon = mon - daym
        else:
            mon = 0

        if day >= hourd:
            day = day - hourd
        else:
            day = 0

        for i in range(mon):
            ins.run()
            eng.run(ins.ac, 3600 * 24 * 30)
            self.FreezeData('month', eng.energy)

        for i in range(day):
            ins.run()
            eng.run(ins.ac, 3600 * 24)
            self.FreezeData('day', eng.energy)
            if i % 30 == 29:
                fz.FreezeData('month', eng.energy)

        for i in range(hour):
            ins.run()
            eng.run(ins.ac, 3600)
            self.FreezeData('hour', eng.energy)
            if i % 24 == 23:
                fz.FreezeData('day', eng.energy)

if __name__ == '__main__':
    import sys

    sys.path.append('../')
    from PublicLib.ACModule.simEnergy import energy
    from PublicLib.ACModule.simCurrent import ACsampling


    eng = energy(3)
    ins = ACsampling()
    fz = freeze(defultcfg)

    mon = defultcfg['month']
    day = defultcfg['day']
    hour = defultcfg['hour']

    daym = int(day/30)
    hourd = int(hour/24)

    if mon >= daym:
        mon = mon - daym
    else:
        mon = 0

    if day >= hourd:
        day = day - hourd
    else:
        day = 0


    for i in range(mon):
        ins.run()
        eng.run(ins.ac, 3600*24*30)
        fz.FreezeData('month', eng.energy)

    for i in range(day):
        ins.run()
        eng.run(ins.ac, 3600*24)
        fz.FreezeData('day', eng.energy)
        if i % 30  == 29:
            fz.FreezeData('month', eng.energy)

    for i in range(hour):
        ins.run()
        eng.run(ins.ac, 3600)
        fz.FreezeData('hour', eng.energy)
        if i % 24  == 23:
            fz.FreezeData('day', eng.energy)
