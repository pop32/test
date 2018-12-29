#!/bin/python

import sys
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

try:
    condst = sqlite3.connect("data/gbpjpy_tick_60min.db")
    sql = "create table if not exists tick (dt text primary key, open real, end real, high real, low real)"
    condst.execute(sql)
    condst.execute("delete from tick")
    condst.execute(sql)

    mlist={}
    mlist['min60']=[0, 30]

    with closing(sqlite3.connect("data/gbpjpy_tick.db")) as conn:
        sql = "select min(dt),max(dt) from tick"
        row = conn.execute(sql)
        r = row.fetchone()
        mindt = strtodt(r[0])
        lastdt = strtodt(r[1])
        maxdt = datetime.datetime(mindt.year, mindt.month, mindt.day, mindt.hour, 0)\
            + datetime.timedelta(minutes=60)

        print(mindt)
        print(maxdt)
        print(lastdt)
        #exit(0)
        i = 0
        while mindt < lastdt:
            sql = "select * from tick "\
                  "where dt >= '" + mindt.strftime('%Y%m%d%H%M%S') + "'"\
                  "  and dt <  '" + maxdt.strftime('%Y%m%d%H%M%S') + "'"\
                  "order by dt"
            row = conn.execute(sql)
            rowdata = row.fetchall()

            dt = maxdt.strftime('%Y%m%d%H%M%S')
            maxrow = len(rowdata)
            if maxrow == 0:
                openp = -1
                endp = -1
                maxp = -1
                minp = -1
            else:
                openp = rowdata[0][1]
                endp = rowdata[len(rowdata)-1][1]
                maxp = 0
                minp = sys.maxsize

            for r in rowdata:
                if maxp < r[1]:
                    maxp = r[1]
                if minp > r[1]:
                    minp = r[1]
            
            print(dt)
            print(openp)
            print(endp)
            print(maxp)
            print(minp)

            inssql="insert into tick(dt,open,end,high,low) values ("\
                + "'" + dt + "',"\
                + str(openp) + ","\
                + str(endp) + ","\
                + str(maxp) + ","\
                + str(minp) + ")"

            #print(inssql)
            condst.execute(inssql)

            mindt = maxdt
            maxdt = maxdt  + datetime.timedelta(minutes=60)
            if i > 1000:
                condst.commit()

        condst.commit()

except Exception as ex:
    print(ex)
    
else:
    condst.close()

dbname=""
data=""

