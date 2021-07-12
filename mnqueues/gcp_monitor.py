import time
from random import random

from opencensus.ext.stackdriver import stats_exporter
from opencensus.stats import aggregation, measure, stats, view

from . import Monitor


class GCPMonitor(Monitor):
    created = False

    def __init__(self, name: str):
        super().__init__(name)

    def _create_put_measure(self):
        self.m_put = measure.MeasureInt(f"mnqueues.put", "number of puts", "1")
        self.v_put = view.View(
            f"mnqueues.{self.name}.number_queue_put",
            "number of put() to queues",
            [],
            self.m_put,
            aggregation.CountAggregation(),
        )
        stats.stats.view_manager.register_view(self.v_put)

    def _create_get_measure(self):
        self.m_get = measure.MeasureInt("mnqueues.get", "number of gets", "1")
        self.v_get = view.View(
            f"mnqueues.{self.name}.number_queue_get",
            "number of get() to queues",
            [],
            self.m_get,
            aggregation.CountAggregation(),
        )
        stats.stats.view_manager.register_view(self.v_get)

    def _create_tnq_measure(self):
        self.m_tnq = measure.MeasureInt("mnqueues.mnq", "time in queue", "ms")
        self.v_tnq = view.View(
            f"mnqueues.{self.name}.time_in_queue_distribution",
            "The distribution of the queue latencies",
            [],
            self.m_tnq,
            aggregation.DistributionAggregation(
                [10, 50, 100, 500, 1000, 10000]
            ),
        )
        stats.stats.view_manager.register_view(self.v_tnq)

    def create(self):
        self.created = True

        self._create_put_measure()
        self._create_get_measure()
        self._create_tnq_measure()

        exporter = stats_exporter.new_stats_exporter()
        stats.stats.view_manager.register_exporter(exporter)

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

    def time_in_queue(self, tnq: int):
        if not self.created:
            self.create()
        mmap = stats.stats.stats_recorder.new_measurement_map()
        mmap.measure_int_put(self.m_tnq, tnq / 1000000)
        mmap.record()
