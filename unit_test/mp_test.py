import os
import sys

sys.path.append("/home/kirito/life/badminton")
import time

from src.mp_tool import MP_Tool


def f(x):
    time.sleep(2)
    print(x)
    return x * x


def f_callback(x):
    print(f"end {x}")
    return x


if __name__ == "__main__":
    """Exmaple"""

    mp_tool = MP_Tool()
    results = []
    for i in range(20):
        results.append(mp_tool.create(f, False, i, callback_fn=f_callback))

    for result in results:
        result.wait()
