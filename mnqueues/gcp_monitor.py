from random import random
import time

from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view

from . import Monitor


class GCPMonitor(Monitor):
    created = False

    def __init__(self, name: str):
        self.put_counter: int
        self.get_counter: int
        super().__init__(name)

    def create(self):
        self.created = True

        self.m_put = measure.MeasureInt(f"mnqueues.put", "number of puts", "1")
        self.m_get = measure.MeasureInt("mnqueues.get", "number of gets", "1")
        self.v_put = view.View(
            "mnqueues.number_queue_put",
            "number of put() to queues",
            [],
            self.m_put,
            aggregation.CountAggregation(),
        )
        self.v_get = view.View(
            "mnqueues.number_queue_get",
            "number of get() to queues",
            [],
            self.m_get,
            aggregation.CountAggregation(),
        )
        stats.stats.view_manager.register_view(self.v_put)
        stats.stats.view_manager.register_view(self.v_get)
        exporter = stats_exporter.new_stats_exporter()
        stats.stats.view_manager.register_exporter(exporter)

        self.put_counter = 0
        self.get_counter = 0

    def track_put(self):
        if not self.created:
            self.create()
        self.put_counter += 1
        mmap = stats.stats.stats_recorder.new_measurement_map()
        mmap.measure_int_put(self.m_put, self.put_counter)
        mmap.record()

    def track_get(self):
        if not self.created:
            self.create()
        self.get_counter += 1
        mmap = stats.stats.stats_recorder.new_measurement_map()
        mmap.measure_int_put(self.m_get, self.get_counter)
        mmap.record()
