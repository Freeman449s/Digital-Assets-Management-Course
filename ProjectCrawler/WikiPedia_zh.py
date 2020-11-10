from bs4 import BeautifulSoup
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "https://chi.jinzhao.wiki/wiki/{}"
headImgLibPath = "头像"
workImgLibPath = "作品图片"


def crawlPeopleInfo(name: str):
    try:
        url = urlTemplate.format(name)
        response = requests.get(url)
        response.encoding = "UTF-8"
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        if not checkPeople(soup): return
        dict = {}
        # 字典初始化
        dict["name"] = ""
        dict["nationality"] = ""
        dict["dateofbirth"] = "0"
        dict["dateofdeath"] = "0"
        dict["repwork"] = ""  # todo
        dict["majorAchv"] = ""
        dict["academy"] = ""
        dict["birthplace"] = ""
        dict["longitude"] = "0"  # todo
        dict["latitude"] = "0"  # todo
        dict["major"] = ""  # todo
        dict["gender"] = ""
        dict["introduction"] = ""  # todo
        dict["headimage"] = ""

        # todo: 格式化
        # 人物名
        tag = soup.find(class_="nickname")
        dict["name"] = tag.text
        # 生日
        tag = soup.find(class_="bday")
        # 生日样例：1853-03-30
        dict["dateofbirth"] = tag.text.split("-")[0]
        # 出生地
        tag = soup.find(class_="birthplace")
        dict["birthplace"] = tag.text
        # 逝世日期
        tag = soup.find(class_="dday")
        dict["dateofdeath"] = tag.text.split("-")[0]
        # 余下信息难以直接通过类解析，采用遍历方式进行解析
        vcard = soup.find(class_="vcard")
        tbody = vcard.find("tbody")
        # 遍历tbody的每个子节点
        for tr in tbody.children:
            th = tr.find("th")
            category = th.text
            if category == "国籍":
                dict["nationality"] = tr.find("td").text
            # todo: 为每部作品爬取图片
            elif category == "代表作" or category == "知名作品":
                td = tr.find("td")
                workDict = {}
                workNames = ""
                for index, tag in enumerate(td.find_all("a")):
                    workName = tag.text
                    workName = "《" + workName
                    workName += "》"
                    workNames += workName
                    workDict[workName] = tag["href"]
                dict["repwork"] = workNames
        # 下载人物头像
        headImgTag = tbody.find("img")
        headImgURL = headImgTag["src"]
        postfix = headImgURL.split(".")[-1]
        imgName = dict["name"] + postfix
        dict["headimage"] = "people\\images\\" + imgName
        imgPath = headImgLibPath + imgName
        downloadBinary(headImgURL, imgPath)
        # 为每部作品下载图片
    except Exception:
        traceback.print_exc()


def downloadBinary(url: str, path: str) -> None:
    # Response.content存储Response对象的二进制形式
    content = requests.get(url, headers=headers).content
    file = open(path, "wb")
    file.write(content)
    file.close()


def crawlPeopleWorks(workDict: dict) -> None:
    # todo
    pass


def checkPeople(soup: BeautifulSoup) -> bool:
    """
    检查维基百科上是否存在某个词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="vcard")):
        return True
    return False
