# coding:utf-8
import time


class RateLimiter:
    """
    固定窗口的限流算法
    """
    def __init__(self, maxCount=5, timeUnit=1):
        self.start_time = time.time()
        self.req_count = 0
        self.max_count = maxCount
        self.time_unit = timeUnit

    def is_rate_limited(self):
        current_time = time.time()
        if current_time - self.start_time > self.time_unit:
            self.start_time = current_time
            self.req_count = 0

        if self.req_count >= self.max_count:
            return True
        else:
            self.req_count += 1
            return False


def test():
    limiter = RateLimiter(maxCount=3, timeUnit=5)
    time.sleep(4)
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())
    time.sleep(1)
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())
    print(limiter.is_rate_limited())


if __name__ == '__main__':
    test()
