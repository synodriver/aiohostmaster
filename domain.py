# -*- coding: utf-8 -*-
import asyncio
import sys
from typing import List
import aiohttp
from claw import get_addr, get_ip
from log import logger


async def _check(ip: str, count: int = 1):
    p = await asyncio.create_subprocess_shell("ping {0} -n {1}".format(ip, count), stdout=asyncio.subprocess.DEVNULL)
    await p.wait()
    return p.returncode == 0


class IP:
    def __init__(self, val, addr):
        """

        :param val: ipaddress
        :param addr: 地理位置
        """
        self.value = val
        self.addr = addr  # 地理位置
        self.able = None  # 可以ping

    def __str__(self):
        return f"# {self.addr}" + "\n" + self.value

    async def check(self, count: int = 1) -> bool:
        """
        检查ip是否可以ping
        :return:
        """
        self.able = await _check(self.value, count)
        return self.able


class Domain:
    def __init__(self, host: str, *ip: IP):
        """

        :param host: 域名
        :param ip: 拥有的ip 多个 实例化的时候可以不传入
        """
        self.host = host
        self.ips: List[IP] = list(ip)

    async def get_ip(self):
        """根据自己的域名自动填充ip地址"""
        print("正在为 {0} 查询ip地址".format(self.host))
        async with aiohttp.ClientSession() as session:
            ips: List[str] = await get_ip(session, self.host)
            tasks = [asyncio.create_task(get_addr(session, ip)) for ip in ips]
            addrs: List[str] = await asyncio.gather(*tasks)
            self.ips = [IP(*_) for _ in zip(ips, addrs)]

    async def check(self):
        print("正在为 {0} 检查可用ip地址".format(self.host))
        tasks = [asyncio.create_task(ip.check(4)) for ip in self.ips]
        results: List[bool] = await asyncio.gather(*tasks)
        self.ips: List[IP] = [data[0] for data in filter(lambda x: x[1], zip(self.ips, results))]
        if not self.ips:
            logger.warning("震惊：{0} 找不到可用的ip".format(self.host))

    def __str__(self):
        """
        格式化成要输入host的数据
        :return: str
        """
        return "".join(f"{str(ip)} {self.host}" + "\n" for ip in self.ips)


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


    async def main():
        ip1 = IP("1.1.1.1", "精神病院")
        ip2 = IP("140.82.112.4", "美国")
        ip3 = IP("192.168.0.1", "美国")
        github = Domain("github.com")
        await github.get_ip()
        await github.check()
        print(github)


    a = loop.run_until_complete(main())
