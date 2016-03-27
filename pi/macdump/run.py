#!/usr/bin/env python

import sys, os
import logging
from mac_listener import MacListener
import impacket
import time

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.normpath(os.path.join(FILE_DIR, '..'))
sys.path.append(APP_DIR)

from macdump_db import MacDumpDB

logger = logging.getLogger('main')

class SaveMacs(object):
    def __init__(self):
        self.db = MacDumpDB()
    
    def start(self, iface):
        ml = MacListener(iface)
        ml.start(self.cb)
    
    def cb(self, p):
        self.db.store_mac(p['timestamp'], p['src'], p['signal'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    a = SaveMacs()
    a.start('mon0')

