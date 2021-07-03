__version__ = "0.0.1"


class Monitor:
    def __init__(self):
        pass


class Queue:
    def __init__(self, monitor: Monitor):
        self.monitor = monitor
