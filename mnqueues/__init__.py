from multiprocessing import Queue
from typing import Optional

__version__ = "0.0.1"


class Monitor:
    def __init__(self, name: str):
        self.name = name

    def track_put(self):
        pass

    def track_get(self):
        pass


class MNQueue:
    def __init__(self, monitor: Optional[Monitor] = None, maxsize=0):
        self.monitor = monitor
        self.queue = Queue(maxsize)

    def put(self, *args, **kwargs):
        if self.monitor:
            self.monitor.track_put()
        return self.queue.put(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.monitor:
            self.monitor.track_get()
        return self.queue.get(*args, **kwargs)

    def qsize(self):
        return self.queue.qsize()

    def empty(self):
        return self.queue.empty()

    def full(self):
        return self.queue.full()

    def get_nowait(self):
        return self.queue.get(False)

    def put_nowait(self, obj):
        return self.queue.put(obj, False)

    def close(self):
        self.queue.close()

    def join_thread(self):
        self.queue.join_thread()

    def cancel_join_thread(self):
        self.queue.cancel_join_thread()
