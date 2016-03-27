#!/usr/bin/env python

import sys
import json
import time
import datetime
import pcapy
import impacket
import logging
import Queue
import threading
from impacket import ImpactDecoder
from timedstrings import TimedStrings

logger = logging.getLogger('MacListener')


class MacListener(object):
    def __init__(self, iface='mon0', silence_mac_period=60):
        self.packet_queue = Queue.Queue(100000)
        self.running = True
        
        self.iface = iface
        if silence_mac_period:
            self.silenced_macs = TimedStrings(silence_mac_period)
        else:
            self.silenced_macs = None
        self.radio_tap_decoder = ImpactDecoder.RadioTapDecoder()
    
    def start(self, callback):
        self.callback = callback
        
        processing_thread = threading.Thread(target=self._processor_thread_start)
        processing_thread.daemon = True
        processing_thread.start()

        sniffer = pcapy.open_live(self.iface, 2000, 1, 50)
        sniffer.setfilter('')
        sniffer.loop(0, self._cb_packet)

    def _cb_packet(self, header, body):
        self.packet_queue.put(body)
    
    def _processor_thread_start(self):
        while True:
            try:
                body = self.packet_queue.get()
                dec = self.radio_tap_decoder.decode(body)
                self._on_packet(dec)
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                logger.error('Packet error: %s', str(ex))

    def _on_packet(self, pkt):
        data_frame = pkt.child().child()
        if data_frame.__class__ == impacket.dot11.Dot11DataFrame:
            src_b = data_frame.get_address2()
            dst_b = data_frame.get_address1()
        elif data_frame.__class__ == impacket.dot11.Dot11ManagementFrame:
            src_b = data_frame.get_source_address()
            dst_b = data_frame.get_destination_address()
        else:
            return
        
        src = self._str_mac(src_b)
        dst = self._str_mac(dst_b)

        if self.silenced_macs:
            if self.silenced_macs.is_stored(src):
                return
            self.silenced_macs.store(src)
        
        obs = {
            'src': src,
            'dst': dst,
            'signal': pkt.get_dBm_ant_signal(),
            'timestamp': time.time(),
            'packet': pkt,
            'queued_packets': self.packet_queue.qsize()
        }

        try:
            self.callback(obs)
        except Exception as ex:
            logger.error('Callback error: %s', str(ex))

    def _str_mac(self, b):
        return ':'.join('%02x'%i for i in b)




# Test and Debug

def _debug_callback(p):
    print '%s Found MAC %s' % (datetime.datetime.now(), p['src'])

if __name__ == '__main__':
    logging.basicConfig()
    a = MacListener()
    logger.info('Starting...')
    a.start(_debug_callback)

