#!/bin/python

import sqlite3
from contextlib import closing
import glob

files = glob.glob('data/gbpjpy/*.db')
#print (files)

try:
    condst = sqlite3.connect("data/gbpjpy_tick.db")
    sql = "create table if not exists tick (dt text primary key, ask real, bit real)"
    condst.execute(sql)
    condst.execute("delete from tick")

    for fs in files:
        #print(fs)
        conn = sqlite3.connect(fs)
        sql = "select * from gbpjpy_tick"
        row = conn.execute(sql)
        for r in row:
            #print(r)
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

