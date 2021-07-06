import pytest
from multiprocessing import Queue, Process
import mnqueues as mnq
from mnqueues.gcp_monitor import GCPMonitor
from queue import Empty, Full
from time import sleep
import random


def test_empty():
    q = mnq.MNQueue(monitor=GCPMonitor("name"))
    try:
        _ = q.get(block=False)
    except Empty:
        print("got empty exception, good!")
        return True
    raise AssertionError("non-blocking get() did not get Empty exception")


def test_no_full():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    try:
        _ = q.put(
            "aaa",
            block=False,
        )
    except Full:
        print("got full exception, bad!")
        raise AssertionError("put on queue w/ short-size  got wrong Full exception")

    q.get()
    return True


def test_full():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    try:
        _ = q.put(
            "aaa",
            block=False,
        )

        if not q.full():
            raise Exception("expected queue to be full")
        else:
            print("q is full, as expected")
        _ = q.put(
            "aaa",
            block=False,
        )
    except Full:
        print("got full exception, good!")
        return True

    raise AssertionError("put on queue w/ short-size, expected Full exception")


def test_timeout():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    try:
        _ = q.put("aaa")
        _ = q.put("aaa", block=True, timeout=5)
    except Full:
        print(f"got Full exception, after timeout, good!")
        return True

    raise AssertionError("expected Full exception")


def test_put_nowait():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    try:
        _ = q.put_nowait("aaa")
        _ = q.put_nowait("aaa")
    except Full:
        print(f"got Full exception, good!")
        return True

    raise AssertionError("expected Full exception")


def test_get_nowait():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    try:
        _ = q.get_nowait()
    except Empty:
        print(f"got Empty exception, good!")
        return True

    raise AssertionError("expected Empty exception")


def test_close():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    q.close()
    try:
        _ = q.get()
    except ValueError as e:
        print(f"got {e} exception, good!")
        return True

    raise AssertionError("expected exception")


def test_empty():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    if q.empty():
        print("queue is empty, good!")
        return True

    raise AssertionError("expected empty queue")


def test_join():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    q.close()
    q.join_thread()
    return True


def test_join():
    q = mnq.MNQueue(maxsize=1, monitor=GCPMonitor("name"))
    q.close()
    q.cancel_join_thread()
    return True
