#!/bin/python

import datetime
import sqlite3
from contextlib import closing
import sys

def strtodt(s):
    d=datetime.datetime(\
        int(s[0:4]),\
        int(s[4:6]),\
        int(s[6:8]),\
        int(s[8:10]),\
        int(s[10:12]),\
        int(s[12:14]))
    return d

pairlist=['audjpy','cadjpy','chfjpy','eurjpy','gbpjpy','nzdjpy']
args = sys.argv
pair = args[1]
if pair not in pairlist:
    print('pair:' + pair + " is not allowed.")
    exit(-1)

with closing(sqlite3.connect("data/" + pair + "_tick_60min.db")) as conn:
    sql = "select * from tick where open <> -1 order by dt asc"
    row = conn.execute(sql)
    for r in row:
        dt=strtodt(r[0])
        s=dt.strftime('%Y/%m/%d %H:%M:%S')\
          +',' + str(r[1])\
          +',' + str(r[2])\
          +',' + str(r[3])\
          +',' + str(r[4])
        print(s)
