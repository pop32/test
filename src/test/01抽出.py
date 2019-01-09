#!/bin/python

import sqlite3
from contextlib import closing
import glob
import datetime
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
print (args)

if pair not in pairlist:
    print('pair:' + pair + " is not allowed.")
    exit(-1)

files = glob.glob('data/tmp/' + pair + '*.db')
#print (files)

try:
    condst = sqlite3.connect("data/" + pair + "_tick.db")
    sql = "create table if not exists tick (dt text primary key, ask real, bit real)"
    condst.execute(sql)
    condst.execute("delete from tick")

    for fs in files:
        #print(fs)
        conn = sqlite3.connect(fs)
        sql = "select * from " + pair + "_tick"
        row = conn.execute(sql)
        for r in row:
            #print(r)
            dt = strtodt(r[0])
            wd = dt.weekday()
            tm = dt.strftime('%H%M%S')

            #日曜日
            if wd == 6:
                continue
            #月曜日
            if wd == 0:
                if tm < '070000':
                    continue
            #土曜日
            if wd == 5:
                if tm > '070000':
                    continue

            inssql="insert into tick(dt,ask,bit) values ("\
                + "'" + r[0] + "',"\
                + str(r[1]) + ","\
                + str(r[2]) + ")"
            #print(inssql)
            condst.execute(inssql)
        
        condst.commit()
        #print(row)

except Exception as ex:
    print(ex)
    
else:
    conn.close()
    condst.close()

dbname=""
data=""

