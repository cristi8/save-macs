#!/usr/bin/python

import json

WORST_ACCURACY = 30

class GPS(object):
    def __init__(self):
        self.pos = []
        with open('data/gps.log', 'r') as f:
            for line in f:
                e = json.loads(line)
                if float(e['accuracy']) > WORST_ACCURACY:
                    continue
                self.pos.append( (e['timestamp'], e['lat'], e['long']) )

    def get(self, ts):
        l = 0
        r = len(self.pos) - 1
        # pos[l].timestamp <= ts < pos[r].timestamp
        while l < r - 1:
            m = (l + r) / 2
            if self.pos[m][0] <= ts:
                l = m
            else:
                r = m
        lat1 = self.pos[l][1]
        long1 = self.pos[l][2]
        lat2 = self.pos[r][1]
        long2 = self.pos[r][2]

        return {'lat': (lat1 + lat2) / 2, 'long': (long1 + long2) / 2}

