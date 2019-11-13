import time
import datetime


class simrtc():
    def __init__(self):
        self.sysClockTimer = int(time.time())

    def gettime(self, x=1):
        if x > 1:
            self.sysClockTimer += x
            dt_obj = datetime.datetime.fromtimestamp(self.sysClockTimer)
        else:
            dt_obj = datetime.datetime.now()
        return dt_obj

if __name__ == '__main__':
    rtc = simrtc()
    a = rtc.gettime()
    b = rtc.gettime(60*60*24)
    print(a, b)

    print(a.year, a.month, a.day, a.hour)
    print(b.year, b.month, b.day, b.hour)
