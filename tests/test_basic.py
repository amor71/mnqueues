import pytest
import mnqueues as mnq



def test_setup():
    monitor = mqn.Monitor()
    queue = mqn.Queue(monitor)

