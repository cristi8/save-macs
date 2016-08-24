#!/usr/bin/env python

import sys, os
import time, datetime
import logging
import json


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.normpath(os.path.join(FILE_DIR, '../pi'))
sys.path.append(APP_DIR)

from macdump_db import MacDumpDB



def main():
    db = MacDumpDB()
    c = db.create_cursor()
    c.execute('select mac, max(signal) sig, GROUP_CONCAT(ts) ts_list from seen group by mac order by min(ts) ASC')

    macs = []
    for o in c:
        mac, sig, ts_list_str = o
        ts_list = [int(float(x)) for x in ts_list_str.split(',')]
        ts_list = sorted(ts_list)
        
        hours_active = []
        for ts in ts_list:
            dt = datetime.datetime.fromtimestamp(ts)
            dt_str = dt.strftime('%Y-%m-%d %H:00:00')
            if dt_str not in hours_active:
                hours_active.append(dt_str)
        
        macs.append({'mac': mac, 'max_sig': sig, 'ts': ts_list, 'minutes_active': len(ts_list), 'hours_active': hours_active})
        
    macs = sorted(macs, key=lambda x: len(x['hours_active']), reverse=True)
    
    for mac in macs[:100]:
        print '%s - %s' % (mac['mac'], ' '.join([x.split(' ')[1] for x in mac['hours_active']]))


if __name__ == '__main__':
    main()
    
