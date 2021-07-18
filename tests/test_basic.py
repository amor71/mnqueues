from multiprocessing import Process, Queue

import pytest

import mnqueues as mnq


def test_mqt_instantiate():
    queue = mnq.MNQueue()


def test_create_monitor():
    monitor = mnq.Monitor("test")


def consumer(q: mnq.MNQueue):
    print(q.get())


def producer(q: mnq.MNQueue):
    q.put("testing 123")


def test_mp_basic():
    q = mnq.MNQueue()
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()

    p.join()
    c.join()
