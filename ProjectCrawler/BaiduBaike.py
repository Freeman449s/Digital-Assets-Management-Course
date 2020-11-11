from bs4 import BeautifulSoup
import requests
import traceback
import Util

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "https://baike.baidu.com/item/{}"
headImgLibPath = "头像"
workImgLibPath = "作品图片"
encoding = "UTF-8"


def crawlSuppleInfo(peopleName: str, infoDict: dict, workInfoList: list, logPath: str) -> None:
    with open(logPath, "a+", 8192, encoding=encoding) as logFile:
        try:
            print("正在从百度百科为 " + peopleName + " 爬取补充信息...")
            logFile.write("正在从百度百科为 " + peopleName + " 爬取补充信息...\n")
            url = urlTemplate.format(peopleName)
            response = requests.get(url, headers=headers)
            response.encoding = encoding
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            if not checkPeople(soup):
                print("\t没有此人物的词条")
                logFile.write("\t没有此人物的词条\n")
                return
            # 检查是否已有人物头像
            if infoDict["headimage"] == "":
                summaryPic = soup.find(class_="summary-pic")
                if summaryPic != None:
                    imgTag = summaryPic.find("img")
                    if imgTag != None:
                        imgURL = imgTag["src"]
                        postfix = "." + imgURL.split("_")[-1]
                        imgName = peopleName + postfix
                        imgPath = headImgLibPath + "\\" + imgName
                        Util.downloadBinary(imgURL, imgPath)
                        infoDict["headimage"] = "people\\images\\" + imgName
            # 将人物信息中的条目名和条目内容分别存入两个列表
            keyList = []
            valueList = []
            basicInfo = soup.find(class_="basicInfo-left")
            for index, tag in enumerate(basicInfo.find_all("dt")):
                key = tag.text
                key = key.replace("\xa0", "")
                key = key.replace("\n", "")
                keyList.append(key)
            for index, tag in enumerate(basicInfo.find_all("dd")):
                value = tag.text
                value = value.replace("\xa0", "")
                value = value.replace("\n", "")
                valueList.append(value)
            basicInfo = soup.find(class_="basicInfo-right")
            for index, tag in enumerate(basicInfo.find_all("dt")):
                key = tag.text
                key = key.replace("\xa0", "")
                key = key.replace("\n", "")
                keyList.append(key)
            for index, tag in enumerate(basicInfo.find_all("dd")):
                value = tag.text
                value = value.replace("\xa0", "")
                value = value.replace("\n", "")
                valueList.append(value)
            # 遍历键值列表，填充信息
            for i in range(0, len(keyList)):
                if keyList[i] == "国籍" and infoDict["nationality"] == "":
                    infoDict["nationality"] = valueList[i]
                elif keyList[i] == "出生地" and infoDict["birthplace"] == "":
                    infoDict["birthplace"] = valueList[i]
                    # 解析经纬度
                    posInfo = Util.parseCoordinate(infoDict["birthplace"])
                    if posInfo[0] == 0:
                        infoDict["longitude"] = posInfo[1]["location"]["lng"]
                        infoDict["latitude"] = posInfo[1]["location"]["lat"]
                elif (keyList[i] == "出生日期" or keyList[i] == "出生时间") and infoDict["dateofbirth"] == "0":
                    infoDict["dateofbirth"] = valueList[i].split("年")[0]
                elif (keyList[i] == "逝世日期" or keyList[i] == "去世时间") and infoDict["dateofdeath"] == "0":
                    infoDict["dateofdeath"] = valueList[i].split("年")[0]
                elif keyList[i] == "毕业院校" and infoDict["academy"]:
                    infoDict["academy"] = valueList[i]
                elif keyList[i] == "职业" and infoDict["major"] == "":
                    infoDict["major"] = valueList[i]
                elif keyList[i] == "主要成就" and infoDict["majorAchv"] == "":
                    infoDict["majorAchv"] = valueList[i]
                elif keyList[i] == "性别" and infoDict["gender"] == "":
                    infoDict["gender"] = valueList[i]
                elif keyList[i] == "主要作品" or keyList[i] == "代表作品":
                    valueList[i] = valueList[i].replace("等", "")
                    if infoDict["repwork"] == "":
                        infoDict["repwork"] = valueList[i]
                    if len(workInfoList) == 0:
                        workNameList = valueList[i].split("《")
                        # 格式化作品名
                        for j in range(0, len(workNameList)):
                            workNameList[j] = workNameList[j].replace("》", "")
                        crawlWorks(workNameList, workInfoList, peopleName)
            print("\t完成")
            logFile.write("\t完成\n")
        except Exception as ex:
            print("\t发生异常：")
            traceback.print_exc()
            logFile.write("\t发生异常：\n")
            logFile.write(str(ex))
            logFile.write("\n")


def crawlWorks(workNameList: list, workInfoList: list, authorName: str) -> None:
    """
    依据传入的作品名称列表，爬取作品图片，并将作者-作品名-图片名封装为字典传入workInfoList。
    通常而言，只在workInfoList为空时调用此函数。\n
    :param workNameList: 作品名称列表。这些作品应该具有共同的作者，即传入的author。
    :param workInfoList: 作品信息列表。函数不会读取其中的信息，而只会向列表中填充信息。
    :param authorName: 作者名
    :return: 无返回值
    """
    for workName in workNameList:
        url = urlTemplate.format(workName)
        response = requests.get(url, headers=headers)
        response.encoding = encoding
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        if not checkWork(soup): continue
        summaryPic = soup.find(class_="summary-pic")
        imgTag = summaryPic.find("img")
        if imgTag == None: continue
        workDict = {}
        workDict["author"] = authorName
        workDict["title"] = workName
        imgURL = imgTag["src"]
        postfix = "." + imgURL.split("_")[-1]
        imgName = authorName + "-" + workName + postfix
        workDict["image"] = "peopleworks\\images\\" + imgName
        workInfoList.append(workDict)
        imgPath = workImgLibPath + "\\" + imgName
        Util.downloadBinary(imgURL, imgPath)


def checkWork(soup: BeautifulSoup) -> bool:
    """
    检查百度百科上是否存在某部作品的词条；若存在，进一步解析是否有作品图片\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有作品则返回True，否则返回False
    """
    basicInfo = soup.find(class_="basic-info")
    if basicInfo == None:
        return False
    pic = soup.find(class_="summary-pic")
    if pic == None:
        return False
    return True


def checkPeople(soup: BeautifulSoup) -> bool:
    """
    检查百度百科上是否存在某个人物的词条；若存在，进一步解析是否有人物信息\n
    :param soup: 根据对词条包装而成的url的响应构造的BeautifulSoup对象
    :return: 如果词条存在，并且有人物信息则返回True，否则返回False
    """
    for index, tag in enumerate(soup.find_all(class_="basic-info")):
        return True
    return False
