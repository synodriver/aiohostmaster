# -*- coding: utf-8 -*-
import time
import json
import asyncio
from typing import List
from copy import deepcopy
import re
import aiohttp
from bs4 import BeautifulSoup
from utils import retry
from log import logger


header = {'Accept': '*/*',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Connection': 'keep-alive',
          'Host': 'site.ip138.com',
          # 'Referer': 'https://site.ip138.com/github.com/',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


@retry(Exception)
async def get_ip_2(session: aiohttp.ClientSession, host: str) -> List[str]:
    """输入域名找ip"""
    param = {"domain": host, "time": str(int(time.time() * 1000))}
    new_header = deepcopy(header)
    new_header["Refer"] = "https://site.ip138.com/" + host + "/"
    async with session.get("https://site.ip138.com/domain/read.do?", params=param, headers=new_header) as resp:
        data = await resp.text()
        data = json.loads(data)
        ip_list = [ip["ip"] for ip in data["data"]]
        return ip_list


@retry(Exception)
async def get_ip(session: aiohttp.ClientSession, host: str) -> List[str]:
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive', 'Host': 'www.ntunhs.net', 'Origin': 'http://www.ntunhs.net',
        'Referer': 'http://www.ntunhs.net/lang/GB/index-1.html', 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'}

    post_data = {"lang": "GB", "IP": host}
    async with session.post("http://www.ntunhs.net/cgi-bin/whois20_1.cgi", data=post_data, headers=header) as resp:
        html = await resp.text()
    soup = BeautifulSoup(html, "lxml")
    data = str(soup.find(name="font"))
    data = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", data)
    return data


@retry(Exception)
async def get_addr(session: aiohttp.ClientSession, ip: str) -> str:
    """
    输入ip找地址
    :param session:
    :param ip:
    :return:
    """
    param = {"ip": ip, "action": "2"}
    new_header = deepcopy(header)
    new_header[
        "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    new_header["Refer"] = "https://www.ip138.com/iplookup.asp?ip={0}&action=2".format(ip)
    new_header["Host"] = "www.ip138.com"
    new_header["Sec-Fetch-Dest"] = "document"
    new_header["Sec-Fetch-Mode"] = "navigate"
    new_header["Sec-Fetch-User"] = "?1"
    new_header["Upgrade-Insecure-Requests"] = "1"
    async with session.get("https://www.ip138.com/iplookup.asp?", params=param, headers=new_header) as resp:
        data = await resp.text()
        data = re.findall(r"(?<=归属地\":\").+?(?=\")", data)
        if not data:
            logger.error("Ohhhh查询 {0} 的位置的时候被反爬了".format(ip))
            return "未知"
        addr = data[0]
        return addr


if __name__ == "__main__":
    async def test_1():
        async with aiohttp.ClientSession() as sessoion:
            ips = await get_ip(sessoion, "conda.anaconda.org")
            print(ips)
        pass


    async def test_2():
        async with aiohttp.ClientSession() as sessoion:
            addr = await get_addr(sessoion, "27.10.240.65")
            print(addr)
        pass


    asyncio.run(test_1())
