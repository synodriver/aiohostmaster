# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import aiohttp


def test():
    data = aiohttp.FormData(boundary="---------------------------7e4813830f3c")
    f = open(r"F:\TIM图片20200508215118.jpg", "rb")
    data.add_field("file", f, filename="F:\TIM图片20200508215118.jpg", content_type="image/jpeg")
    print(str(data))


def main():
    with open("test.html", encoding="utf8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")
    a = soup.find(name="font")
    a = str(a)
    data = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", a)
    print(data)
    pass


if __name__ == "__main__":
    test()
