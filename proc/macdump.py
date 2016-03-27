#!/usr/bin/env python

import time, datetime
import json
import sys
from PIL import Image, ImageDraw
from map_plot import image_filename, c2s_x, c2s_y
from gps import GPS
gps = GPS()
import random

def rcolor():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())


def t2str(t):
    #return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
    return datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S') + (' (%d)' % t)

mac2ts = {}

f = open('data/mac.log', 'r')
for line in f:
    (ts, mac) = line.split(' ')
    ts = int(ts)
    mac = mac.strip()
    if mac == '00:0d:a3:10:c7:30' or mac == '24:4b:81:69:b5:94':
        continue
    if ts < 1435424289 or ts > 1435439289:
        continue
    #if ts < 1435434878:
    #    continue

    if mac not in mac2ts:
        mac2ts[mac] = []
    mac2ts[mac].append(ts)
f.close()

macs = sorted(mac2ts.keys(), key=lambda x: min(mac2ts[x]), reverse=False)

pmacs = [mac for mac in macs if len(mac2ts[mac]) > 20]

print '%d interesting MACs' % len(pmacs)


RADIUS = 5
def shuffle(x, y):
    return (x + random.randint(-RADIUS, RADIUS), y + random.randint(-RADIUS, RADIUS))


IMGCOUNT = 0

def gen_img(mac):
    global IMGCOUNT
    img = Image.open('map_img/2x_' + image_filename)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    CSIZE = 1

    for (i,t) in enumerate(mac2ts[mac]):
        for dt in range(-30,30):
            pos = gps.get(t + dt)

            x = 2*c2s_x(pos['long'])
            y = 2*c2s_y(pos['lat'])
            x, y = shuffle(x, y)

            draw.ellipse((x - CSIZE, y - CSIZE, x + CSIZE, y + CSIZE), fill='red')

    #draw.text((10, i * 20), t2str(t), (0,0,0))


    istr = '%s' % (mac[:9] + 'XX:XX:XX',)
    draw.text((10, 1200), istr, (0,0,0))

    img.save('/tmp/img/%03d.png' % IMGCOUNT)
    IMGCOUNT += 1

#for mac in pmacs:
#    gen_img(mac)
gen_img(pmacs[9])
