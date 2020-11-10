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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
# 解析位置函数
APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"


def main():
    BaiduBaike.crawlSuppleInfo(PeopleInfo("鲁迅"), "log.txt")


def check(soup: BeautifulSoup) -> bool:
    """
    检查百度百科上是否存在某个词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="basic-info")):
        return True
    return False


# 返回一个列表
# 第一个值为状态码：-1为查询失败，0为查询成功
# 第二个值为状态信息  若查询失败： 返回数据的提示信息
#                  若查询成功   返回数据的result查询结果
def interpret(pos):
    reply = requests.get("https://apis.map.qq.com/ws/geocoder/v1/?address=" + pos + "&key=" + APIKEY)
    jsondata = json.loads(reply.text)
    print("请求发送成功！")
    if (jsondata["status"] != 0):
        return [-1, jsondata["message"]]
    else:
        return [0, jsondata["result"]]


main()
