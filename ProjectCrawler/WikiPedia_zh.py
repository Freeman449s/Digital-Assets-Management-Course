from bs4 import BeautifulSoup
import bs4
import requests
import traceback
import Util
from PeopleInfo import PeopleInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "https://chi.jinzhao.wiki/wiki/{}"
headImgLibPath = "头像"
workImgLibPath = "作品图片"
encoding = "UTF-8"


def crawlPeopleInfo(peopleInfo: PeopleInfo, logPath: str) -> None:
    with open(logPath, "a+", 8192, encoding=encoding) as logFile:
        try:
            print("正在从维基百科为 " + peopleInfo.name + " 爬取信息...")
            logFile.write("正在从维基百科为 " + peopleInfo.name + " 爬取信息...\n")
            url = urlTemplate.format(peopleInfo.name)
            response = requests.get(url)
            response.encoding = encoding
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            if not checkPeople(soup): return
            worksDict = {}
            # 爬取人物信息
            # 人物名
            tag = soup.find(class_="nickname")
            if tag != None:
                peopleInfo.infoDict["name"] = tag.text
            # 生日
            tag = soup.find(class_="bday")
            if tag != None:
                # 生日样例：1853-03-30
                peopleInfo.infoDict["dateofbirth"] = tag.text.split("-")[0]
            # 出生地
            tag = soup.find(class_="birthplace")
            if tag != None:
                peopleInfo.infoDict["birthplace"] = tag.text
                # 解析经纬度
                posInfo = Util.parseCoordinate(peopleInfo.infoDict["birthplace"])
                if posInfo[0] == 0:
                    peopleInfo.infoDict["longitude"] = posInfo[1]["location"]["lng"]
                    peopleInfo.infoDict["latitude"] = posInfo[1]["location"]["lat"]
                # 解析失败，尝试利用地点词条解析
                aTag = tag.find_all("a")[-1]
                coordinate = crawlCoordinate(insertHead(aTag["href"]))
                peopleInfo.infoDict["longitude"] = coordinate[0]
                peopleInfo.infoDict["latitude"] = coordinate[1]
            # 逝世日期
            tag = soup.find(class_="dday")
            if tag != None:
                peopleInfo.infoDict["dateofdeath"] = tag.text.split("－")[0]
            # 简介
            tag = soup.find(class_="mw-parser-output")
            if tag != None:
                introduction = ""
                for child in tag.children:
                    if isinstance(child, bs4.NavigableString):
                        continue
                    # 遇到词条目录，简介部分到此结束
                    if "id" in child.attrs and child["id"] == "toc":
                        break
                    if child.name == "p":
                        introduction += child.text
                peopleInfo.infoDict["introduction"] = introduction
            # 余下信息难以直接通过类解析，采用遍历方式进行解析
            vcard = soup.find(class_="vcard")
            tbody = vcard.find("tbody")
            # 遍历tbody的每个子节点
            for tr in tbody.children:
                th = tr.find("th")
                if th == None:
                    continue
                category = th.text
                if category == "国籍":
                    peopleInfo.infoDict["nationality"] = tr.find("td").text
                elif category == "代表作" or category == "知名作品":
                    td = tr.find("td")
                    workNames = ""
                    for index, tag in enumerate(td.find_all("a")):
                        workName = tag.text
                        workName = "《" + workName
                        workName += "》"
                        workNames += workName
                        if "href" in tag.attrs:
                            worksDict[workName] = insertHead(tag["href"])
                        peopleInfo.infoDict["repwork"] = workNames
                elif category == "体裁" or category == "知名于":
                    peopleInfo.infoDict["major"] = tr.find("td").text
            # 下载人物头像
            headImgTag = tbody.find("img")
            if headImgTag != None:
                headImgURL = headImgTag["src"]
                postfix = "." + headImgURL.split(".")[-1]
                imgName = peopleInfo.name + postfix
                peopleInfo.infoDict["headimage"] = "people\\images\\" + imgName
                imgPath = headImgLibPath + "\\" + imgName
                headImgURL = insertHead(headImgURL)
                Util.downloadBinary(headImgURL, imgPath)
            # 为每部作品下载图片
            peopleInfo.workInfoList = crawlWorks(worksDict, peopleInfo.infoDict["name"])
            print("\t完成")
            logFile.write("\t完成\n")
        except Exception as ex:
            print("\t发生异常：")
            traceback.print_exc()
            logFile.write("\t发生异常：\n")
            logFile.write(ex)
            logFile.write("\n")


def crawlCoordinate(url: str) -> tuple:
    """
    根据地区词条的url，爬取词条上的经纬度信息\n
    :param url: 地区词条的url
    :return: 包含浮点型经度和纬度信息的元组
    """
    latitude = "0"
    longitude = "0"
    response = requests.get(url, headers=headers)
    response.encoding = encoding
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    latitudeTag = soup.find(class_="latitude")
    longitudeTag = soup.find(class_="longitude")
    # 将字符串形式的经纬度转为浮点型
    # 维度
    if latitudeTag != None:
        latitudeText = latitudeTag.text
        if latitudeText[-1] == "N":
            sign = 1
        else:
            sign = -1
        latitude = float(latitudeText.split("°")[0])
        latitude += float(latitudeText.split("°")[1][0:-2])
        latitude *= sign
    # 经度
    if longitudeTag != None:
        longitudeText = longitudeTag.text
        if longitudeText[-1] == "E":
            sign = 1
        else:
            sign = -1
        longitude = float(longitudeText.split("°")[0])
        longitude += float(longitudeText.split("°")[1][0:-2])
        longitude *= sign
    return (longitude, latitude)


def crawlWorks(worksDict: dict, authorName: str) -> list:
    workInfoList = []
    for workName, url in worksDict.items():
        # 不尝试在英文维基上爬取
        if "en.wikipedia" in url:
            continue
        workName = workName.replace("《", "")
        workName = workName.replace("》", "")
        response = requests.get(url)
        response.encoding = encoding
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        if not checkWork(soup): continue
        workDict = {}
        workDict["author"] = authorName
        workDict["title"] = workName
        table = soup.find(class_="vevent")
        imgTag = table.find("img")
        imgURL = imgTag["src"]
        postfix = "." + imgURL.split(".")[-1]
        imgName = authorName + "-" + workName + postfix
        workDict["image"] = "peopleworks\\images\\" + imgName
        workInfoList.append(workDict)
        imgURL = insertHead(imgURL)
        Util.downloadBinary(imgURL, workImgLibPath + "\\" + imgName)
    return workInfoList


def checkWork(soup: BeautifulSoup) -> bool:
    """
    检查维基百科上是否存在有关某部作品的词条，若有，进一步检查是否有作品图片
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有作品信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="vevent")):
        imgTag = soup.find("img")
        if imgTag != None:
            return True
    return False


def checkPeople(soup: BeautifulSoup) -> bool:
    """
    检查维基百科上是否存在有关某个人物的词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="vcard")):
        return True
    return False


def insertHead(url: str) -> str:
    # 不包含域名
    if "jinzhao.wiki" not in url and "https" not in url:
        return "https://chi.jinzhao.wiki" + url
    # 包含域名但缺失https
    elif "https:" not in url:
        return "https:" + url
    # url完整
    else:
        return url
