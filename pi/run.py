#!/usr/bin/env python

import logging
from mac_listener import MacListener
import impacket
import time
from save_macs_db import SaveMacsDB

logger = logging.getLogger('main')

class SaveMacs(object):
    def __init__(self):
        self.db = SaveMacsDB()
    
    def start(self, iface):
        ml = MacListener(iface)
        ml.start(self.cb)
    
    def cb(self, p):
        self.db.store_mac(p['timestamp'], p['src'], p['signal'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    a = SaveMacs()
    a.start('mon0')

