import pytest
from multiprocessing import Queue, Process


def producer(q: Queue):
    print(q.get())


def consumer(q: Queue):
    q.put("testing 123")


def test_mp_basic():
    q = Queue()
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()

    p.join()
    c.join()
