# coding:utf-8
import asyncio


def print_stat(loop):
    print(loop.is_running())


async def stop(loop):
    await asyncio.sleep(10)
    print_stat(loop)
    loop.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.call_later(5, print_stat, loop)
    loop.run_until_complete(stop(loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
