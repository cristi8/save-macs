#!/usr/bin/env python

import sys
import json
import time
import pcapy
import impacket
from impacket import ImpactDecoder
g_decoder = ImpactDecoder.RadioTapDecoder()


ifc = 'mon0'

def str_mac(b):
    return ':'.join('%02x'%i for i in b)


def on_src_mac(mac):
    pass


def on_packet(pkt):
    data_frame = pkt.child().child()
    if data_frame.__class__ == impacket.dot11.Dot11DataFrame:
        src_b = data_frame.get_address2()
        dst_b = data_frame.get_address1()
    elif data_frame.__class__ == impacket.dot11.Dot11ManagementFrame:
        src_b = data_frame.get_source_address()
        dst_b = data_frame.get_destination_address()
    else:
        #print '......... %s' % data_frame.__class__
        return
    src = str_mac(src_b)
    dst = str_mac(dst_b)

    on_src_mac(src)

    sys.stdout.write('.')
    sys.stdout.flush()
    #print '##### %s --> %s    (%s)' % (src, dst, data_frame.__class__)

def cb_packet(header, body):
    try:
        dec = g_decoder.decode(body)
        on_packet(dec)
    except Exception as ex:
        print 'ERROR: ' + str(ex)


sniffer = pcapy.open_live(ifc, 1500, 1, 100)
sniffer.loop(0, cb_packet)


