
import sqlite3
import time

DB_PATH = '/var/lib/macdump.db'

class MacDumpDB(object):
    def __init__(self, reuse_cursor=True):
        self.reuse_cursor = reuse_cursor
        self.sqlite_conn = sqlite3.connect(DB_PATH, timeout=2)
        self.init_cursor = self.sqlite_conn.cursor()
        try:
            self.init_cursor.execute('''CREATE TABLE seen (ts real, mac text, signal int)''')
            self.init_cursor.execute('''CREATE INDEX idx_ts ON seen (ts)''')
            self.init_cursor.execute('''CREATE INDEX idx_mac ON seen (mac)''')
        except sqlite3.OperationalError as ex:
            if 'already exists' not in str(ex):
                raise

    def get_cursor(self):
        if self.reuse_cursor:
            return self.init_cursor
        else:
            return self.sqlite_conn.cursor()

    def store_mac(self, ts, mac, signal):
        t0 = time.time()
        cursor = self.get_cursor()
        try:
            cursor.execute('INSERT INTO seen VALUES (?, ?, ?)', (ts, mac, signal))
            self.sqlite_conn.commit()
        finally:
            #if time.time() - t0 >= 0.5:
            print 'Insert took %.2f seconds' % (time.time()-t0,)

    def get_mac_history(self, mac):
        t0 = int(time.time() - (3600 * 24))
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM seen WHERE mac=? AND ts>? ORDER BY ts DESC', (mac, t0))
        results = []
        for entry in cursor:
            results.append({'ts': entry[0], 'signal': entry[2]})
        cursor.close()
        return results

    def get_latest_macs(self, top):
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM seen ORDER BY ts DESC')
        results = []
        seen_macs = set()
        for entry in cursor:
            if entry[1] in seen_macs:
                continue
            results.append({'ts': entry[0], 'mac': entry[1], 'signal': entry[2]})
            seen_macs.add(entry[1])
            if len(results) >= top:
                break
        cursor.close()
        return results

    def get_latest_macs_by_ts(self, latest_seconds):
        t0 = time.time() - latest_seconds;
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM seen ORDER BY ts DESC')
        results = []
        seen_macs = set()
        for entry in cursor:
            if entry[0] < t0:
                break
            if entry[1] in seen_macs:
                continue
            results.append({'ts': entry[0], 'mac': entry[1], 'signal': entry[2]})
            seen_macs.add(entry[1])
        
        cursor.close()
        return results
