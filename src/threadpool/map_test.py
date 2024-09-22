# coding:utf-8

from concurrent.futures import ThreadPoolExecutor
import time


def task(n):
    # print(f"Task {n} is running")
    time.sleep(2)  # 模拟耗时任务
    return n * n


def main():
    executor = ThreadPoolExecutor(max_workers=5)

    numbers = list(range(10))
    print("Submitting tasks to thread pool...")
    # 这行代码会阻塞主线程，直到所有任务完成
    results = executor.map(task, numbers)
    print("All tasks have completed.")
    results_tw = executor.map(task, numbers)
    print("All tw tasks have completed.")
    # 结果按顺序返回
    for result in results:
        print(f"Result: {result}")

    for result in results_tw:
        print(f"Result_tw: {result}")


if __name__ == "__main__":
    main()