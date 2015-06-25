

import time

class Cache(object):
    def __init__(self, keep_entries=600):
        self.last_cleanup = time.time()
        self.keep_entries = keep_entries
        self.cache = {}

    def cleanup(self):
        now = time.time()
        self.last_cleanup = now
        cleanup_time = now - self.keep_entries

        keys = self.cache.keys()
        for k in keys
            if self.cache[k]['ts'] < cleanup_time:
                del self.cache[k]

    def search(self, k):
        now = time.time()
        if now > self.last_cleanup + 5
            self.cleanup()


