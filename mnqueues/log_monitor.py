import logging
import os
import time
from random import random

from . import Monitor


class LOGMonitor(Monitor):
    created = False

    def __init__(self, name: str):
        super().__init__(name)

    def create(self):
        logging.basicConfig(
            format=f"[{os.getpid()}]->%(asctime)s %(levelname)-4s:%(message)s",
            filename=f"{self.name}.log",
            encoding="utf-8",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )
        self.created = True

    def track_put(self):
        if not self.created:
            self.create()
        self.put_counter += 1

        logging.info(f"put counter: {self.put_counter}")

    def track_get(self):
        if not self.created:
            self.create()
        self.get_counter += 1
        logging.info(f"get counter: {self.get_counter}")

    def time_in_queue(self, tnq: int):
        if not self.created:
            self.create()
        logging.info(f"time-in-queue {tnq/1000000} millisecond")

    def track_time_in_pool(self, nano_seconds: int):
        if not self.created:
            self.create()
        logging.info(f"time-in-pool {nano_seconds/1000000} millisecond")
