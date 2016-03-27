#!/usr/bin/env python


import json
import time, datetime
import sys
from PIL import Image, ImageDraw, ImageFont

import numpy
import matplotlib.pyplot
import matplotlib.image

matplotlib.pyplot.ion()
figure = matplotlib.pyplot.figure("plot", figsize=(9,9))
matplotlib.pyplot.axis('off')

from map_plot import image_filename, c2s_x, c2s_y
from gps import GPS
gps = GPS()

CSIZE = 2
SEC = 120

img = Image.open('map_img/' + image_filename)
img = img.convert('RGB')

t0 = 1435424289
t1 = 1435439289

matplot_img = None

for t in range(t0, t1, SEC):
    pos = gps.get(t)

    x = c2s_x(pos['long'])
    y = c2s_y(pos['lat'])

    fimg = img.copy()
    draw = ImageDraw.Draw(fimg)
    draw.ellipse((x - CSIZE, y - CSIZE, x + CSIZE, y + CSIZE), outline=0)
    t_str = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
    draw.text((10, 600), t_str, (0,0,0))

    npimg = numpy.asarray(fimg)
    if matplot_img is None:
        matplot_img = matplotlib.pyplot.imshow(npimg)
    else:
        matplot_img.set_array(npimg)

    matplotlib.pyplot.draw()
    print "Plotting frame for %d " % (t,)


