from multiprocessing import Process, Queue

import pytest

import mnqueues as mnq


class B:
    def f(self, x: int) -> int:
        return 2 * x


class A:
    def __init__(self):
        print(f"class {type(self).__name__} initiated")
        print(f"class {self.__class__}")

        self.b = B()

    def g(self, x: int) -> int:
        return 4 * x

    def __call__(self, *args, **kwargs):
        print(
            f"class {type(self).__name__} called w/ args={args} kwargs={kwargs}"
        )

    def __get__(self, obj, objtype=None):
        print(f"class {type(self).__name__} __get__ w/ {obj} and {objtype}")

    def __getattr__(self, attr):
        print(f"class {type(self).__name__}.__getattr__ called w/ {attr}")
        if attr not in self.__dict__:
            return self.b.__getattribute__(attr)


def test_init():
    a = A()

    return True


def test_get():
    a = A()
    print(a.f(8))
    print(a.g(8))
    return True
