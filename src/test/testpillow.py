#!/usr/bin/env python3.6

from PIL import Image, ImageDraw
import datetime
import sqlite3
from contextlib import closing

#あ
class Chart:
    def __init__(self):
        self.tick = []
        self.max = -1
        self.min = 9999999
        self.pixrate = 70

    def strtodt(self,s):
        d=datetime.datetime(\
            int(s[0:4]),\
            int(s[4:6]),\
            int(s[6:8]),\
            int(s[8:10]),\
            int(s[10:12]),\
            int(s[12:14]))
        return d

    def append(self,dic):
        self.tick.append(dic)
        if dic['high'] < 0:
            return
        if self.max < dic['high']:
            self.max = dic['high']
        if self.min > dic['low']:
            self.min = dic['low']

    def drawChart(self):

        self.setup()

        im = Image.new("RGB", (self.canvas_width, self.canvas_height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
    
        for xscale in self.canvas_xscales:
            y = (self.base - xscale) * self.pixrate + self.canvas_hmid
            x = 0
            cl = 98
            w = 2
            if (xscale % 2) == 0:
                cl = 45
                w = 4

            while x < self.canvas_width:
                xe = x + 10
                if xe > self.canvas_width:
                    xe = self.canvas_width
                draw.line((x, y, xe, y), fill=(cl, cl, cl), width=w)
                x = xe + 10

        x = 1
        for i in range(self.tick_count):
            t1 = self.tick[i]

            dt = self.strtodt(t1['dt'])
            wd = dt.weekday()
            tm = dt.strftime('%H%M%S')
            # 月曜日 用修正
            if wd == 0 and tm == '070000':
                cl = 98
                draw.line((x, 0, x, self.canvas_height), fill=(cl, cl, cl), width=2)

            if t1['high'] < 0:
                x = x + 4
                continue
            hly1 = (self.base - t1['high']) * self.pixrate + self.canvas_hmid
            hly2 = (self.base - t1['low']) * self.pixrate + self.canvas_hmid
            oey1 = (self.base - t1['open']) * self.pixrate + self.canvas_hmid
            oey2 = (self.base - t1['end']) * self.pixrate + self.canvas_hmid

            if t1['open'] < t1['end']:
                draw.line((x, hly1, x, hly2), fill=(0, 0, 255), width=1)
                draw.line((x, oey1, x, oey2), fill=(0, 0, 255), width=3)
            else:
                draw.line((x, hly1, x, hly2), fill=(255, 0, 0), width=1)
                draw.line((x, oey1, x, oey2), fill=(255, 0, 0), width=3)

            x = x + 4

        im.save('test.png')

    def dump(self):
        self.setup()
        print('max:' + str(self.max))
        print('min:' + str(self.min))
        print('count:' + str(self.tick_count))
        print('base:' + str(self.base))
        print('pixrate:' + str(self.pixrate))
        print('canvas_height:' + str(self.canvas_height))
        print('canvas_hmid:' + str(self.canvas_hmid))
        print('canvas_width:' + str(self.canvas_width))
        print('canvas_xscales:' + str(self.canvas_xscales))

    def setup(self):
        self.base = (self.max + self.min) / 2
        self.tick_w = 3
        self.tick_space = 1
        self.tick_startpos = 2
        self.tick_count = len(self.tick)
        self.canvas_height = int((self.max - self.min) * self.pixrate) + 20
        self.canvas_hmid = self.canvas_height / 2
        self.canvas_width = self.tick_count * 4 + 20
        self.canvas_xscales = []
        tmp = int(self.max)
        while tmp > self.min:
            self.canvas_xscales.append(tmp)
            tmp = tmp - 1


if __name__ == '__main__':

    try:
        conn = sqlite3.connect("data/gbpjpy_tick_240min.db")
        sql = "select dt,open,end,high,low from tick order by dt"
        row = conn.execute(sql)
        char = Chart()
        for r in row:
            char.append({"dt":r[0],"open":r[1],"end":r[2],"high":r[3],"low":r[4]})
        conn.close()

        char.dump()
        char.drawChart()

        #im = Image.new("RGB", (512, 512), (255, 255, 255))
        #draw = ImageDraw.Draw(im)
        #draw.rectangle((100, 100, 200, 200), fill=(0, 0, 255))
        #drawChart(draw, ctlist)

        #draw.line((0, im.height, im.width, 0), fill=(255, 0, 0), width=8)
        #draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
        #draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))
        #im.show()
        #im.save('test.jpg', quality=95)
        #im.save('test.png')

    except Exception as ex:
        print(ex)
