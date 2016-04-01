#!/usr/bin/env python

import sys, os
import cherrypy
import time
import json
import logging
import hashlib, identicon, StringIO
logger = logging.getLogger('web_server')

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.normpath(os.path.join(FILE_DIR, '..'))
sys.path.append(APP_DIR)

from macdump_db import MacDumpDB

class SaveMacsDashboard(object):
    def __init__(self):
        self.db = MacDumpDB()
    
    @cherrypy.expose
    def get_icon(self, s='test'):
        h = hashlib.md5(s.encode('utf-8')).hexdigest()
        img = identicon.render_identicon(int(h[:8], 16), 20)
        cherrypy.response.headers['Content-Type'] = "image/png"
        cherrypy.response.headers['Cache-Control'] = '31536000'
        cherrypy.response.headers['ETag'] = s
        buf = StringIO.StringIO()
        img.save(buf, 'PNG')
        return buf.getvalue()

    @cherrypy.expose
    def latest(self):
        latest = self.db.get_latest_macs_by_ts(600)
        return json.dumps(latest)
        #return '<br />'.join('%.1d sec ago - %s (%d)' % (time.time() - x['ts'], x['mac'], x['signal']) for x in latest)

    @cherrypy.expose
    def mac_history(self, mac=''):
        mac_hist = self.db.get_mac_history(mac)
        mac_hist_text = ''
        for x in mac_hist:
            s = '%.3f hours ago (%06.1f min ago) - signal %d' % (
                (time.time() - x['ts']) / 3600.0,
                (time.time() - x['ts']) / 60.0,
                x['signal']
            )
            mac_hist_text += s + '\n'
        return '<html><body><h1><a href="/"><img src="/get_icon?s=%s"></a> %s</h1><pre>%s</pre></body></html>' % (mac, mac, mac_hist_text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cherrypy.quickstart(SaveMacsDashboard(), '/', os.path.join(FILE_DIR, 'cherrypy.conf'))

