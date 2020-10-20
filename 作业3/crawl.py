import requests
import json

# 请求头，将请求伪装成由浏览器发出
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
albumListURL = "https://douban.fm/j/v2/songlist/explore?type=hot&genre=0&limit=20&sample_cnt=5"
# 需要填充专辑ID
songListURLTemplate = "https://douban.fm/j/v2/songlist/{}/?kbps=192"
libOnePath = "Music Library 1"
libTwoPath = "Music Library 2"


# 爬虫函数
def crawl():
    # 获取专辑信息列表
    albumListResponse = requests.get(albumListURL, headers=headers)
    albumList = json.loads(albumListResponse.text)
    count = 0
    # 处理每张专辑
    for i in range(0, len(albumList)):
        # 最多下载202首歌
        if count >= 202:
            break
        albumID = albumList[i]["id"]
        # 获取歌曲信息列表
        songListURL = songListURLTemplate.format(str(albumID))
        songListResponse = requests.get(songListURL, headers=headers)
        songListDict = json.loads(songListResponse.text)
        songList = songListDict["songs"]
        # 获取歌曲信息
        for songInfoDict in songList:
            songID = "{:0>3d}"  # 数字不足3位时，左边补零
            if count <= 100:
                libDir = libOnePath
                songID = songID.format(count)
            else:
                libDir = libTwoPath
                songID = songID.format(count - 101)
            isSuccessful = True
            print("Downloading song NO." + str(count))
            try:
                downloadSong(songInfoDict, songID, libDir)
            except Exception as ex:
                print("\tDownload failed. Error Message:")
                print("\t" + repr(ex))
                isSuccessful = False
            if isSuccessful:
                print("\tSuccessful")
            count += 1
            if (count >= 200):
                break


def downloadSong(dict, id, libDir):
    pictureURL = dict["picture"]
    songURL = dict["url"]
    downloadBinary(songURL, libDir + "\\" + id + ".mp3")
    downloadBinary(pictureURL, libDir + "\\" + id + ".jpg")
    jsonDict = {}
    jsonDict["artist"] = dict["artist"]
    jsonDict["kbps"] = dict["kbps"]
    jsonDict["title"] = dict["title"]
    jsonDict["albumTitle"] = dict["albumtitle"]
    jsonDict["length"] = formatTime(dict["length"])
    writeJSON(jsonDict, libDir + "\\" + id + ".json")


def formatTime(length):
    minute = int(length / 60)
    second = length - minute * 60
    time = "{}:{:0>2d}"
    return time.format(minute, second)


def downloadBinary(url, path):
    # Response.content存储Response对象的二进制形式
    content = requests.get(url, headers=headers).content
    file = open(path, "wb")
    file.write(content)
    file.close()


def downloadASCII(url, path):
    content = requests.get(url, headers=headers).text
    file = open(path, "w", encoding="UTF-8")
    file.write(content)
    file.close()


def writeJSON(dict, path):
    file = open(path, "w", encoding="UTF-8")
    file.write("{\n")
    count = 0
    length = len(dict)
    for key, value in dict.items():
        line = "    \"{}\":"
        # value为整数时，不需要加引号；为字符串时，需要加引号
        if isinstance(value, int):
            line += "{}"
        else:
            line += "\"{}\""
        line = line.format(key, value)
        if (count != length - 1):
            line += ","
        line += "\n"
        file.write(line)
        count += 1
    file.write("}")
    file.close()


crawl()
