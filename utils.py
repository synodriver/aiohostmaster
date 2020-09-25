# -*- coding: utf-8 -*-
from functools import wraps
import asyncio


def concurrency(con: int = 1):
    """
    你并发必超级打折
    :param con:
    :return:
    """
    loop = asyncio.get_running_loop()
    sem = asyncio.Semaphore(con, loop=loop)

    def deco(func):
        @wraps(func)
        async def inner(*args, **kw):
            async with sem:
                ret = await func(*args, **kw)
                return ret

        return inner

    return deco


def retry(*exceptions, retries: int = 5, cool_down: int = 1):
    """
    出现异常时进行重试，期待几秒后问题解决
    Args:
        exceptions (Tuple[Exception]) : 期待捕获的异常
        retries (int): 重试次数
        cool_down (int): 冷却时间
    """

    def wrap(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            retries_count = 0

            while True:
                try:
                    result = await func(*args, **kwargs)
                except exceptions as err:
                    retries_count += 1
                    if retries_count > retries:
                        raise err
                    if cool_down:
                        await asyncio.sleep(cool_down)
                else:
                    return result

        return inner

    return wrap
