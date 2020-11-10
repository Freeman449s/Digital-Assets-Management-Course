from YouhuaDaquan import crawlYouhuaDaquan
from MingrenJianli import crawlMinrenJianli
from TiantianToupiao import crawlTiantianToupiao
import GuShiwen
import json
import requests
from bs4 import BeautifulSoup
from PeopleInfo import PeopleInfo
import Util

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
# 解析位置函数
APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"
encoding = "UTF-8"

nameListPath = "人物列表\\画家名单.txt"
peopleFilePath = "PeopleInfo.json"
workFilePath = "WorkInfo.json"


def main():
    梵高 = PeopleInfo("梵高")
    梵高.crawl()
    梵高.write()


main()
