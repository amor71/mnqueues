import os
import time
from multiprocessing import TimeoutError
from time import sleep

import pytest

import mnqueues as mnq
from mnqueues.gcp_monitor import GCPMonitor
from mnqueues.log_monitor import LOGMonitor


def f(x):
    return x * x


def test_create_mnpool():
    with mnq.MNPool(5) as p:
        print(p.map(f, [1, 2, 3]))


def test_create_mnpool_logmonitor():
    mon = LOGMonitor("name")

    for _ in range(5):
        with mnq.MNPool(5, monitor=mon) as p:
            print(p.map(f, [1, 2, 3]))


@pytest.mark.devtest
def test_create_mnpool_gcpmonitor():
    print("test_create_mnpool_gcpmonitor")
    mon = GCPMonitor("test")

    for _ in range(5):
        with mnq.MNPool(5, monitor=mon) as p:
            print(p.map(f, [1, 2, 3]))

    print("give grace")
    sleep(65)
    print("completed")


def test_pool_2_logmonitor():
    print("test_pool_2_logmonitor")
    mon = LOGMonitor("name")
    # start 4 worker processes
    with mnq.MNPool(processes=4, monitor=mon) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20,))  # runs in *only* one process
        print(res.get(timeout=1))  # prints "400"

        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ())  # runs in *only* one process
        print(res.get(timeout=1))  # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
