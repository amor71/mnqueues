import pytest
import mnqueues as mnq


def test_mqt_instantiate():
    queue = mnq.MNQueue()


def test_create_monitor():
    monitor = mnq.Monitor("name")
