#!/usr/bin/env python

import logging
from mac_listener import MacListener
import time
import impacket


logger = logging.getLogger('main')

logging.basicConfig(level=logging.INFO)

def cb(p):
    pkt = p['packet']
    data_frame = pkt.child().child()
    if data_frame.__class__ == impacket.dot11.Dot11DataFrame:
        pass
    elif data_frame.__class__ == impacket.dot11.Dot11ManagementFrame:
        pass
    else:
        print '......... %s' % data_frame.__class__
        return

    print '[%3d] %s -> %s (%s)' % (p['queued_packets'], p['src'], p['dst'], p['signal'])


ml = MacListener('mon0')
ml.start(cb)

