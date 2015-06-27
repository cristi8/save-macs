#!/usr/bin/env python


import json
import time
import sys
from PIL import Image, ImageDraw
from map_plot import image_filename, c2s_x, c2s_y


img = Image.open('map_img/' + image_filename)
draw = ImageDraw.Draw(img)

last_line = None
f = open('data/gps.log', 'r')
for crt_line_json in f:
    crt_line = json.loads(crt_line_json)
    if float(crt_line['accuracy']) > 30:
        continue
    if last_line is None:
        last_line = crt_line
        continue
    x0 = c2s_x(last_line['long'])
    y0 = c2s_y(last_line['lat'])
    x1 = c2s_x(crt_line['long'])
    y1 = c2s_y(crt_line['lat'])

    draw.line((x0, y0, x1, y1), fill=0, width=1)

    last_line = crt_line

img.show()



