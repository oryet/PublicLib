import time
import datetime


class simrtc():
    def __init__(self, mage=0):
        self.sysClockTimer = int(time.time())
        if mage > 1:
            self.mage = mage
        else:
            self.mage = 1

    def gettime(self):
        if self.mage > 1:
            self.sysClockTimer += self.mage
            dt_obj = datetime.datetime.fromtimestamp(self.sysClockTimer)
        else:
            dt_obj = datetime.datetime.now()
        return dt_obj

    def gettick(self):
        if self.mage > 1:
            self.sysClockTimer += self.mage
            t = self.sysClockTimer
        else:
            t = int(time.time())
        return t

if __name__ == '__main__':
    rtc = simrtc()
    a = rtc.gettime()
    b = rtc.gettime(60*60*24)
    print(a, b)

    print(a.year, a.month, a.day, a.hour)
    print(b.year, b.month, b.day, b.hour)
