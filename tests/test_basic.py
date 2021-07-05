import pytest
import mnqueues as mnq
from multiprocessing import Queue, Process


def test_mqt_instantiate():
    queue = mnq.MNQueue()


def test_create_monitor():
    monitor = mnq.Monitor("name")


def producer(q: mnq.MNQueue):
    print(q.get())


def consumer(q: mnq.MNQueue):
    q.put("testing 123")


def test_mp_basic():
    q = mnq.MNQueue()
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()

    p.join()
    c.join()
