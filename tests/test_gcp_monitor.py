import multiprocessing as mp
import random
from multiprocessing import Process, Queue
from queue import Empty
from time import sleep

import pytest

import mnqueues as mnq
from mnqueues.gcp_monitor import GCPMonitor


def test_gcp_monitor():
    g = GCPMonitor("test")
    return True


def consumer(q: mnq.MNQueue):
    for _ in range(10000):
        try:
            print(q.get(block=True, timeout=1))
            sleep(0.01)
        except Empty:
            print("Empty queue, quiting")
            break

    print("consumer: get done, giving grace")
    sleep(65)
    print("consumer completed")


def producer(q: mnq.MNQueue):
    for i in range(10000):
        q.put(f"testing {i}..")

    print("producer: put done, giving grace")
    sleep(65)
    print("producer completed")


@pytest.mark.devtest
def test_mp_basic():
    q = mnq.MNQueue(monitor=GCPMonitor("test"))
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()

    p.join()
    c.join()


@pytest.mark.devtest
def test_mp_2():
    q = mnq.MNQueue(monitor=GCPMonitor("test"))
    p = Process(target=producer, args=(q,))
    c1 = Process(target=consumer, args=(q,))
    c2 = Process(target=consumer, args=(q,))

    p.start()
    c1.start()
    c2.start()

    p.join()
    c1.join()
    c2.join()


def consumer_no_delay(q: mnq.MNQueue):
    for _ in range(10000):
        try:
            print(q.get(block=True, timeout=1))
        except Empty:
            print("Empty queue, quiting")
            break

    print("consumer_no_delay: get done, giving grace")
    sleep(65)
    print("consumer_no_delay completed")


@pytest.mark.devtest
def test_mp_3():
    print("grace before starting test_mp_3")
    sleep(65)
    q = mnq.MNQueue(monitor=GCPMonitor("test"))
    p = Process(target=producer, args=(q,))
    c1 = Process(target=consumer_no_delay, args=(q,))
    c2 = Process(target=consumer_no_delay, args=(q,))

    p.start()
    c1.start()
    c2.start()

    p.join()
    c1.join()
    c2.join()
