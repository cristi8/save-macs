#!/usr/bin/env python


import json
import time
import sys
from PIL import Image, ImageDraw
from map_plot import image_filename, c2s_x, c2s_y
from gps import GPS
gps = GPS()

CSIZE = 2
SEC = 60

img = Image.open('map_img/' + image_filename)
draw = ImageDraw.Draw(img)

t0 = 1435421469
t1 = 1435441950

for t in range(t0, t1, SEC):
    pos = gps.get(t)

    x = c2s_x(pos['long'])
    y = c2s_y(pos['lat'])

    draw.ellipse((x - CSIZE, y - CSIZE, x + CSIZE, y + CSIZE), outline=0)

img.show()



