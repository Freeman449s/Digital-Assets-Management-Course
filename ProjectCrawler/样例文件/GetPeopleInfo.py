import os
import json
import shutil
#########################################################################################################
import requests
import json
#解析位置函数
APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"

#返回一个列表
# 第一个值为状态码：-1为查询失败，0为查询成功
# 第二个值为状态信息  若查询失败： 返回数据的提示信息
#                   若查询成功   返回数据的result查询结果
def interpret(pos):
    reply = requests.get("https://apis.map.qq.com/ws/geocoder/v1/?address="+pos+"&key="+APIKEY)
    jsondata = json.loads(reply.text)
    print("请求发送成功！")
    if(jsondata["status"] !=0):
        return [-1,jsondata["message"]]
    else:
        return [0,jsondata["result"]]

#########################################################################################################

image_count = 1

folderPath = "C:/Users/14012/Desktop/媒体资源管理大作业/AllData"
folderList = os.listdir(folderPath)
f = open(r"C:\Users/14012\Desktop\媒体资源管理大作业\people_info.json", 'w+', encoding='UTF-8')
status = 0
infolist = []

# 读取从主要网站上爬取的人物信息，构建json对象
for folder in folderList:
    filelist = os.listdir(folderPath + '\\' + folder)
    for file in filelist:
        object = {}
        if file.endswith('.json'):
            if len(file.split('_')) == 3:
                ff = open(folderPath + '/' + folder + '/' + file,'r+',encoding='UTF-8')
                a = ff.readline()
                # 从一行文字中解析json信息
                info = json.loads(a)
                if("中文名" in info):
                    object['name'] = info["中文名"]
                else:
                    if("姓名" in info):
                        object['name'] = info["姓名"]
                    else:
                        object['name'] = ""

                if ("国籍" in info):
                    object['nationality'] = info["国籍"]
                else:
                    object['nationality'] = ""

                if ("出生日期" in info):
                    object['dateofbirth'] = info["出生日期"].split('年')[0]
                    if len(object['dateofbirth'].split('元')) == 2:
                        object['dateofbirth'] = object['dateofbirth'].split('元')[1]
                else:
                    object['dateofbirth'] = 0

                if ("逝世日期" in info):
                    object['dateofdeath'] = info["逝世日期"].split('年')[0]
                else:
                    object['dateofdeath'] = 0

                if ("代表作品" in info):
                    object['repwork'] = info["代表作品"]
                else:
                    object['repwork'] = ""

                if ("主要成就" in info):
                    object['majorAchv'] = info["主要成就"]
                else:
                    object['majorAchv'] = ""

                if ("毕业院校" in info):
                    object['academy'] = info["毕业院校"]
                else:
                    object['academy'] = ""

                # if ("出生地" in info):
                #     object['birthplace'] = info["出生地"]
                #     code,res = interpret(object['birthplace'])
                #     if code == -1:
                #         object['longitude'] = 0
                #         object['latitude'] = 0
                #     else:
                #         object['longitude'] = res["location"]["lng"]
                #         object['latitude'] = res["location"]["lat"]
                # else:
                #     object['birthplace'] = ""
                #     object['longitude'] = 0
                #     object['latitude'] = 0
                # if object["name"] != "":
                #     print(object)
                #     infolist.append(object)

length = len(infolist)


for folder in folderList:
    filelist = os.listdir(folderPath + '\\' + folder)
    for file in filelist:
        if file.endswith('.json'):
            if len(file.split('_')) == 2:
                k = 0
                while(k<length):
                    # print("原文件名",file)
                    # print("文件名",(file.split('_')[1]).split('.')[0])
                    # print("比较",infolist[k]['name'])
                    if((file.split('_')[1]).split('.')[0] == infolist[k]['name']):
                        ff = open(folderPath + '/' + folder + '/' + file, 'r+', encoding='UTF-8')
                        a = ff.readline()
                        info = json.loads(a)
                        infolist[k]["major"] = info["zhuanye"]
                        infolist[k]["gender"] = info["sex"]
                        infolist[k]["introduction"] = info["jianjie"]
                        break
                    k = k + 1

# 更新人物头像的json信息，并移动头像
i = 0
for folder in folderList:
    filelist = os.listdir(folderPath + '\\' + folder)
    for file in filelist:
        if file.endswith('.png') and len(file.split('_')) == 2:
            k = 0
            while (k < length):
                if ((file.split('_')[1]).split('.')[0] == infolist[k]['name']):
                    infolist[k]["headimage"] = "people/images/" + str(i) + '.png'
                    newfilename = str(i) + ".png"
                    shutil.copyfile(folderPath + '/' + folder + '/' + file,
                                    "C:/Users/14012/Desktop/媒体资源管理大作业/peoplehead/" + newfilename)
                    # print(infolist[k])
                    i = i + 1
                    break
                k = k + 1

fff = open("../data/people_info.json", 'w+', encoding='UTF-8')
for each in infolist:
    fff.write(json.dumps(each) + '\n')
