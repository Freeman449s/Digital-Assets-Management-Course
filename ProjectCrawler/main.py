from YouhuaDaquan import crawlYouhuaDaquan
from MingrenJianli import crawlMinrenJianli
from TiantianToupiao import crawlTiantianToupiao
import GuShiwen
import BaiduBaike
import WikiPedia_zh
import json
import requests
from bs4 import BeautifulSoup
from PeopleInfo import PeopleInfo
import Util

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
# 解析位置函数
APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"


def main():
    print("Hello"[0:-1])


def check(soup: BeautifulSoup) -> bool:
    """
    检查百度百科上是否存在某个词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="basic-info")):
        return True
    return False


main()
