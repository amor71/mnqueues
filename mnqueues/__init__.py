from multiprocessing import Pool, Queue
from typing import Optional

__version__ = "0.0.16"

import copy
import time
from random import randint


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

    def track_time_in_pool(self, nano_seconds: int):
        pass


class MNQueue:
    def __init__(self, monitor: Optional[Monitor] = None, maxsize=0):
        self.monitor = monitor
        self.queue: Queue = Queue(maxsize)

    def put_w_tnq(self, *args, **kwargs):
        payload = {
            "_signature": "mnqueue_tnq",
            "tnq": time.time_ns(),
        }
        if "obj" in kwargs:
            payload["obj"] = kwargs["obj"]
            kwargs["obj"] = payload
        else:
            payload["obj"] = args[0]
            args = list(args)
            args[0] = payload
            args = tuple(args)

        return self.queue.put(*args, **kwargs)

    def should_send_tnq(self) -> bool:
        return randint(1, 20) == 1  # nosec

    def put(self, *args, **kwargs):
        if self.monitor:
            self.monitor.track_put()
            if self.should_send_tnq():
                return self.put_w_tnq(*args, **kwargs)

        return self.queue.put(*args, **kwargs)

    def extract_tnq(self, queue_content):
        if (
            isinstance(queue_content, dict)
            and queue_content.get("_signature", "") == "mnqueue_tnq"
        ):
            self.monitor.time_in_queue(
                time.time_ns() - int(queue_content["tnq"])
            )
            return queue_content["obj"]
        return queue_content

    def get(self, *args, **kwargs):
        rc = self.queue.get(*args, **kwargs)
        if self.monitor:
            self.monitor.track_get()
            rc = self.extract_tnq(rc)

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


class MNPool:
    def __init__(self, *args, monitor=None, **kwargs):
        self.monitor = monitor
        self.pool: Pool = Pool(*args, **kwargs)
        self.tnp: int

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return self.pool.__getattribute__(attr)

    def __enter__(self):
        if self.monitor:
            self.tnp = time.time_ns()

        return self.pool.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        _exit = self.pool.__exit__(exc_type, exc_val, exc_tb)

        if self.monitor:
            self.monitor.track_time_in_pool(time.time_ns() - self.tnp)

        return _exit
