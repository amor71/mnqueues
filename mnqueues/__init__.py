from multiprocessing.queues import Queue

__version__ = "0.0.1"


class Monitor:
    def __init__(self):
        pass


class MNQueue(Queue):
    def __init__(self, monitor: Monitor, **kwargs):
        self.monitor = monitor
        super().__init__(kwargs)
