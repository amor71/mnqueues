import pytest
import mnqueues as mnq


def test_setup():
    monitor = mnq.Monitor()
    queue = mnq.Queue(monitor)
