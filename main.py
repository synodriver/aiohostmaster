# -*- coding: utf-8 -*-
from typing import List
import sys
import json
import asyncio
from domain import Domain


def load_config() -> dict:
    with open("config.json") as f:
        congif = json.load(f)
    return congif


def load_prefix() -> str:
    with open("model.txt") as f:
        prefix = f.read()
    return prefix


async def main():
    prefix = load_prefix()
    config: dict = load_config()
    host_path: str = config.get("host_path", "C:\\Windows\\System32\\drivers\\etc\\hosts")  # host路径
    hosts: List[str] = config.get("domains", [])  # 要查询的域名
    if hosts:
        domains = [Domain(host) for host in hosts]
    [await domain.get_ip() for domain in domains]  # 取ip
    [await domain.check() for domain in domains]  # 检查ip
    for domain in domains:
        prefix += str(domain)
    with open(host_path, "w", encoding="utf8") as f:
        f.write(prefix)


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop.run_until_complete(main())
