import time
import datetime


def timeStr2stamp(date_str, format="%Y-%m-%d %H:%M:%S"):
    dt_obj = datetime.datetime.strptime(date_str, format)  # "%Y-%m-%d %H:%M:%S"
    # print("dt_obj:", dt_obj)
    # dt_obj: 2016-11-30 14:12:49

    # dt obj --> time obj1
    time_tuple = dt_obj.timetuple()
    # print("time_tuple:", time_tuple)
    # time_tuple: time.struct_time(tm_year=2016, tm_mon=11, tm_mday=30, tm_hour=14, tm_min=12, tm_sec=49, tm_wday=2, tm_yday=335, tm_isdst=-1)

    # time obj --> timestamp
    timestamp = time.mktime(time_tuple)
    # print("timestamp:", timestamp)
    # timestamp: 1480486369.0
    return timestamp