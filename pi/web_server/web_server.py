#!/usr/bin/env python

import sys, os
import cherrypy
import time
import json
import logging
logger = logging.getLogger('web_server')

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.normpath(os.path.join(FILE_DIR, '..'))
sys.path.append(APP_DIR)

from macdump_db import MacDumpDB

class SaveMacsDashboard(object):
    def __init__(self):
        self.db = MacDumpDB()
    
    @cherrypy.expose
    def latest(self):
        latest = self.db.get_latest_macs(10)
        return '<br />'.join('%.1d sec ago - %s (%d)' % (time.time() - x['ts'], x['mac'], x['signal']) for x in latest)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cherrypy.quickstart(SaveMacsDashboard(), '/', os.path.join(FILE_DIR, 'cherrypy.conf'))

