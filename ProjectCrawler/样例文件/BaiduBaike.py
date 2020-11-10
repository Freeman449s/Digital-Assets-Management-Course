from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def crawlBaiduBaike(dir, personName, personID):
    with open("百度百科爬取日志.txt", "a+", 8192) as log:
        try:
            url = "https://baike.baidu.com/item/" + personName
            data = requests.get(url, headers=headers)
            html = data.text
            soup = BeautifulSoup(html, 'lxml')
            nameList = []
            valueList = []
            jsonObject = {}
            # 组合查找：查找所有basicInfo-block类中，标签为dt的元素
            for i, each in enumerate(soup.select(".basicInfo-block dt")):
                content = each.text.replace("\xa0", "")
                content = content.replace("\n", "")
                nameList.append(content)
            for i, each in enumerate(soup.select(".basicInfo-block dd")):
                content = each.text.replace("\xa0", "")
                content = content.replace("\n", "")
                valueList.append(content)
            length = len(nameList)
            i = 0
        except Exception as e:
            print(e)
            log.write(e)
            log.write("\n")
        try:
            while (i < length):
                jsonObject[nameList[i]] = valueList[i]
                i = i + 1
            print("正在写入" + str(personName) + "补充百度百科json数据")
            log.write("正在写入" + str(personName) + "补充百度百科json数据" + '\n')
            f = open((dir + '/' + personID + '_' + personName + '_bk.json'), 'w+', encoding="utf-8")
            f.write(str(jsonObject).replace("\'", "\""))
            f.close()
        except Exception as e:
            print(e)
            log.write(e)
            log.write("\n")
