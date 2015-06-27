

from collections import deque
import time
import logging

logger = logging.getLogger("TimedStrings")

class TimedStrings(object):
    def __init__(self, timeout=600):
        self.timeout = timeout

        self.cache_set = set()  # strings    \
        self.cache_qs = deque() # strings     \___ same length
        self.cache_qt = deque() # timestamps  /
        self.count = 0


    def delete_old(self):
        delete_older_than = time.time() - self.timeout
        while self.count > 0 and self.cache_qt[0] < delete_older_than:
            s = self.cache_qs[0]
            logger.debug('Removing %s from the cached strings...' % (s,))
            self.cache_qt.popleft()
            self.cache_qs.popleft()
            self.cache_set.remove(s)
            self.count -= 1


    def is_stored(self, s):
        self.delete_old()
        return s in self.cache_set

    def store(self, s):
        self.delete_old()
        if s in self.cache_set:
            raise Exception("Updating an entry is not supported. Wait for it to expire")
        self.cache_qt.append(time.time())
        self.cache_qs.append(s)
        self.cache_set.add(s)
        self.count += 1


