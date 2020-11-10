class PeopleInfo():
    def __init__(self, name: str):
        self.name = name
        self.infoDict = {}
        # 字典初始化
        self.infoDict["name"] = ""
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
