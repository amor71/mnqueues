import pytest
from multiprocessing import Queue, Process
import mnqueues as mnq
from mnqueues.gcp_monitor import GCPMonitor
from time import sleep
import random


def test_gcp_monitor():
    g = GCPMonitor("name")
    return True


def consumer(q: mnq.MNQueue):
    try:
        for _ in range(10000):
            print(q.get())
            sleep(0.01)
    except Exception as e:
        print(f"[EXCEPTION] {e}")

    print("consumer: get done, giving grace")
    sleep(65)
    print("consumer completed")


def producer(q: mnq.MNQueue):
    for i in range(10000):
        q.put(f"testing {i}..")

    print("producer: put done, giving grace")
    sleep(65)
    print("producer completed")


def test_mp_basic():
    q = mnq.MNQueue(monitor=GCPMonitor("name"))
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()

    p.join()
    c.join()
