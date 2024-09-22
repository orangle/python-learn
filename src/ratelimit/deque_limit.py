# coding:utf-8
import unittest
from collections import deque
import time


class RateLimiter:
    """
    timeUnit 秒
    """
    def __init__(self, maxCount=5, timeUnit=1):
        self.timeUnit = timeUnit
        self.deque = deque(maxlen=maxCount)

    def __call__(self):
        if self.deque.maxlen == len(self.deque):
            cTime = time.time()
            if cTime - self.deque[0] > self.timeUnit:
                self.deque.append(cTime)
                return False
            else:
                return True
        self.deque.append(time.time())
        return False


def test():
    limiter = RateLimiter(maxCount=3, timeUnit=10)
    print(limiter())
    print(limiter())
    print(limiter())
    print(limiter())
    time.sleep(0.5)
    print(limiter())
    print(limiter())
    time.sleep(0.5)
    print(limiter())


if __name__ == '__main__':
    test()

