
import sqlite3

DB_PATH = '/var/lib/save_macs.db'

class SaveMacsDB(object):
    def __init__(self):
        self.sqlite_conn = sqlite3.connect(DB_PATH)
        self.cursor = self.sqlite_conn.cursor()
        try:
            self.cursor.execute('''CREATE TABLE seen (ts real, mac text, signal int)''')
            self.cursor.execute('''CREATE INDEX idx_ts ON seen (ts)''')
            self.cursor.execute('''CREATE INDEX idx_mac ON seen (mac)''')
        except sqlite3.OperationalError as ex:
            if 'already exists' not in str(ex):
                raise

    def store_mac(self, ts, mac, signal):
        self.cursor.execute('INSERT INTO seen VALUES (?, ?, ?)', (ts, mac, signal))
        self.sqlite_conn.commit()

    
