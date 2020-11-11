import BaiduBaike
import WikiPedia_zh

peopleFilePath = "PeopleInfo.json"
workFilePath = "WorkInfo.json"
encoding = "UTF-8"


class PeopleInfo():
    def __init__(self, name: str):
        self.name = name
        self.infoDict = {}
        # 字典初始化
        self.infoDict["name"] = name
        self.infoDict["nationality"] = ""
        self.infoDict["dateofbirth"] = "0"
        self.infoDict["dateofdeath"] = "0"
        self.infoDict["repwork"] = ""
        self.infoDict["majorAchv"] = ""
        self.infoDict["academy"] = ""
        self.infoDict["birthplace"] = ""
        self.infoDict["longitude"] = "0"
        self.infoDict["latitude"] = "0"
        self.infoDict["major"] = ""
        self.infoDict["gender"] = ""
        self.infoDict["introduction"] = ""
        self.infoDict["headimage"] = ""
        self.workInfoList = []

    def crawl(self):
        WikiPedia_zh.crawlPeopleInfo(self, "log.txt")
        BaiduBaike.crawlSuppleInfo(self, "log.txt")

    def write(self):
        with open(peopleFilePath, "a+", 8192, encoding=encoding) as peopleInfoFile, \
                open(workFilePath, "a+", 8192, encoding=encoding) as workInfoFile:
            peopleInfoFile.write(str(self.infoDict).replace("\'", "\""))
            peopleInfoFile.write("\n")
            for workInfoDict in self.workInfoList:
                workInfoFile.write(str(workInfoDict).replace("\'", "\""))
                workInfoFile.write("\n")
