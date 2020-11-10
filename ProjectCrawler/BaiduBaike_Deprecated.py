from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "https://baike.baidu.com/item/{}"


def crawlPeopleInfo(listFilePath: str):
    with open(listFilePath, "r", 8192, encoding="UTF-8") as file:
        for line in file:
            peopleName = line.strip()
            url = urlTemplate.format(peopleName)
            response = requests.get(url)
            response.encoding = "UTF-8"
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            if not check(soup):
                continue
            else:
                pass


def check(soup: BeautifulSoup) -> bool:
    """
    检查百度百科上是否存在某个词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="basic-info")):
        return True
    return False
