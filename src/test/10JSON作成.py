#!/bin/python

import datetime
import sqlite3
from contextlib import closing

def strtodt(s):
    d=datetime.datetime(\
        int(s[0:4]),\
        int(s[4:6]),\
        int(s[6:8]),\
        int(s[8:10]),\
        int(s[10:12]),\
        int(s[12:14]))
    return d

with closing(sqlite3.connect("data/gbpjpy_tick_1day.db")) as conn:
    sql = "select * from tick order by dt desc"
    row = conn.execute(sql)
    print("var testdata=[")
    for r in row:
        dt=strtodt(r[0])
        s='{dt:"' + dt.strftime('%Y/%m/%d')  + '"'\
          +',open:' + str(r[1])\
          +',end:' + str(r[2])\
          +',high:' + str(r[3])\
          +',low:' + str(r[4])\
          +'},'

        print(s)
    print("];")
