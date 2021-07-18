import multiprocessing
import os
import random
import sys
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


@pytest.mark.devtest
def test_pool_2_logmonitor():
    print("test_pool_2_logmonitor")
    mon = GCPMonitor("test")
    # start 4 worker processes
    with mnq.MNPool(processes=4, monitor=mon) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f2(20)" asynchronously
        res = pool.apply_async(f2, (20,))  # runs in *only* one process
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

    print("give grace")
    sleep(65)
    print("completed")


#
# Functions used by test code
#


def calculate(func, args):
    result = func(*args)
    return "%s says that %s%s = %s" % (
        multiprocessing.current_process().name,
        func.__name__,
        args,
        result,
    )


def calculatestar(args):
    return calculate(*args)


def mul(a, b):
    time.sleep(0.5 * random.random())  # nosec
    return a * b


def plus(a, b):
    time.sleep(0.5 * random.random())  # nosec
    return a + b


def f2(x):
    return 1.0 / (x - 5.0)


def pow3(x):
    return x ** 3


def noop(x):
    pass


#
# Test code
#
def test_mnpool_example():
    print("test_mnpool_example")
    mon = GCPMonitor("test")
    PROCESSES = 4
    print("Creating pool with %d processes\n" % PROCESSES)

    with mnq.MNPool(PROCESSES, monitor=mon) as pool:
        #
        # Tests
        #

        TASKS = [(mul, (i, 7)) for i in range(10)] + [
            (plus, (i, 8)) for i in range(10)
        ]

        results = [pool.apply_async(calculate, t) for t in TASKS]
        imap_it = pool.imap(calculatestar, TASKS)
        imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

        print("Ordered results using pool.apply_async():")
        for r in results:
            print("\t", r.get())
        print()

        print("Ordered results using pool.imap():")
        for x in imap_it:
            print("\t", x)
        print()

        print("Unordered results using pool.imap_unordered():")
        for x in imap_unordered_it:
            print("\t", x)
        print()

        print("Ordered results using pool.map() --- will block till complete:")
        for x in pool.map(calculatestar, TASKS):
            print("\t", x)
        print()

        #
        # Test error handling
        #

        print("Testing error handling:")

        try:
            print(pool.apply(f2, (5,)))
        except ZeroDivisionError:
            print("\tGot ZeroDivisionError as expected from pool.apply()")
        else:
            raise AssertionError("expected ZeroDivisionError")

        try:
            print(pool.map(f2, list(range(10))))
        except ZeroDivisionError:
            print("\tGot ZeroDivisionError as expected from pool.map()")
        else:
            raise AssertionError("expected ZeroDivisionError")

        try:
            print(list(pool.imap(f2, list(range(10)))))
        except ZeroDivisionError:
            print("\tGot ZeroDivisionError as expected from list(pool.imap())")
        else:
            raise AssertionError("expected ZeroDivisionError")

        it = pool.imap(f2, list(range(10)))
        for i in range(10):
            try:
                x = next(it)
            except ZeroDivisionError:
                if i == 5:
                    pass
            except StopIteration:
                break
            else:
                if i == 5:
                    raise AssertionError("expected ZeroDivisionError")

        if i != 9:
            raise AssertionError("i == 9")
        print("\tGot ZeroDivisionError as expected from IMapIterator.next()")
        print()

        #
        # Testing timeouts
        #

        print("Testing ApplyResult.get() with timeout:", end=" ")
        res = pool.apply_async(calculate, TASKS[0])
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write("\n\t%s" % res.get(0.02))
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write(".")
        print()
        print()

        print("Testing IMapIterator.next() with timeout:", end=" ")
        it = pool.imap(calculatestar, TASKS)
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write("\n\t%s" % it.next(0.02))
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write(".")
        print()
        print()

    print("give grace")
    sleep(65)
    print("completed")
