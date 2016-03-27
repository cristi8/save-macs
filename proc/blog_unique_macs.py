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
    r = lambda: random.randint(100,155)
    return '#%02X%02X%02X' % (r(),r(),r())

mac2ts = {}

f = open('data/mac.log', 'r')
for line in f:
    (ts, mac) = line.split(' ')
    ts = int(ts)
    mac = mac.strip()
    if mac == '00:0d:a3:10:c7:30' or mac == '24:4b:81:69:b5:94':
        continue
    #if ts < 1435424289 or ts > 1435439289:
    #    continue
    #if ts < 1435434878:
    #    continue

    if mac not in mac2ts:
        mac2ts[mac] = []
    mac2ts[mac].append(ts)
f.close()

ts_list = [min(mac2ts[mac]) for mac in mac2ts.keys()]
ts_list = sorted(ts_list)

print len(ts_list)

CSIZE = 1

img = Image.open('map_img/2x_dim_' + image_filename)
draw = ImageDraw.Draw(img)

RADIUS = 5

def shuffle(x, y):
    return (x + random.randint(-RADIUS, RADIUS), y + random.randint(-RADIUS, RADIUS))

for t in ts_list:
    pos = gps.get(t)

    x = 2 * c2s_x(pos['long'])
    y = 2 * c2s_y(pos['lat'])
    x, y = shuffle(x, y)

    draw.point((x, y), 'red')

img.save('blog_unique_macs.png')
img.show()

