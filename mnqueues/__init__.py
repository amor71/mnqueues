from multiprocessing import Queue
from typing import Optional

__version__ = "0.0.13"

from random import randint
import time
import copy


class Monitor:
    def __init__(self, name: str):
        self.name = name
        self.put_counter: int = 0
        self.get_counter: int = 0

    def track_put(self):
        pass

    def track_get(self):
        pass

    # tnq is measured in nano-seconds
    def time_in_queue(self, tnq: int):
        pass


class MNQueue:
    def __init__(self, monitor: Optional[Monitor] = None, maxsize=0):
        self.monitor = monitor
        self.queue = Queue(maxsize)

    def put(self, *args, **kwargs):
        if self.monitor:
            try:
                self.monitor.track_put()
                if randint(1, 20) == 1:
                    payload = {
                        "_signature": "mnqueue_tnq",
                        "tnq": time.time_ns(),
                    }
                    if "obj" in kwargs:
                        payload["obj"] = kwargs["obj"]
                        kwargs_copy = copy.deepcopy(kwargs)
                        kwargs_copy["obj"] = payload
                        return self.queue.put(**args, **kwargs_copy)
                    else:
                        payload["obj"] = args[0]
                        args_copy = list(args)
                        args_copy[0] = payload
                        args_copy = tuple(args_copy)
                        return self.queue.put(*args_copy, **kwargs)
            except Exception as e:
                print(f"failed to track put() with {e}")

        return self.queue.put(*args, **kwargs)

    def get(self, *args, **kwargs):
        rc = self.queue.get(*args, **kwargs)
        if self.monitor:
            try:
                self.monitor.track_get()
                if (
                    isinstance(rc, dict)
                    and "_signature" in rc
                    and rc["_signature"] == "mnqueue_tnq"
                ):
                    self.monitor.time_in_queue(time.time_ns() - int(rc["tnq"]))
                    rc = rc["obj"]
            except Exception as e:
                print(f"failed to track get() with {e}")

        return rc

    def qsize(self):
        return self.queue.qsize()

    def empty(self):
        return self.queue.empty()

    def full(self):
        return self.queue.full()

    def get_nowait(self):
        return self.get(False)

    def put_nowait(self, obj):
        return self.put(obj, False)

    def close(self):
        self.queue.close()

    def join_thread(self):
        self.queue.join_thread()

    def cancel_join_thread(self):
        self.queue.cancel_join_thread()
