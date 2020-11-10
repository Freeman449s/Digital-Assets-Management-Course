from bs4 import BeautifulSoup
import requests
import json

src = "./newresource/"
# 请求头可将请求伪装成是浏览器发出的，避免服务器拒绝访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


# 静态html页面（无音乐爬取）
def htmljx():
    # format函数将括号内的字符串依次填入大括号中
    urls = [
        "https://music.douban.com/top250?start={}".format(str(i)) for i in range(0, 250, 25)]
    index = 0
    for url in urls:
        # requests.get返回一个包含url对应的服务器资源的Response对象
        data = requests.get(url, headers=headers)
        # text成员储存Response对象的Unicode字符串形式
        html = data.text
        # 解析html文件并构造BeautifulSoup对象，后者将html文档组织成树形结构。lxml为使用的解析器的名称。
        soup = BeautifulSoup(html, 'lxml')
        # BeautifulSoup.select查找文档中的内容，查找方式类似于CSS，用.表示类，#表示id，没有.或#则表示标签
        # “.indent table”是复合查找，表明查找indent类元素下的table标签
        # select函数的返回值是bs4.element.ResultSet。enumerate函数将可遍历数据对象组织成索引序列，同时返回下标和对应的数据
        for ind, each in enumerate(soup.select(".indent table")):
            # 可以用点号(.)访问一个标签的子标签。可以越级访问，但只能访问第一个后裔标签。
            # 使用中括号访问标签的属性，此处each.img["src"]可以返回图片的url。
            downloadpic(index, each.img["src"])
            writetxt(index, '\"Title\":\"' +
                     str(each.img["alt"]) + '\",\"content\":\"' + str(each.div.p.text) + "\"}")
            index = index + 1
            print('歌曲名字：' + str(each.img["alt"]))
            print('图片地址：' + str(each.img["src"]))
            print('信息:' + str(each.div.p.text))


def writetxt(index, text):
    # 以UTF-8编码写入字符数据
    f = open((src + '{}.json').format(index), 'w+', encoding="utf-8")
    f.write(text)
    f.close()


def downloadpic(name, url):
    # content成员储存Response对象的二进制形式
    response = requests.get(url).content
    # 以二进制的形式写入文件中
    print("正在下载第：" + str(name) + "张图片")
    f = open((src + '{}.png').format(name), 'wb')
    f.write(response)
    f.close()


def download(name, url):
    response = requests.get(url).content
    # 以二进制的形式写入文件中
    print("正在下载第：" + name + "首歌曲")
    f = open((src + '{}.mp3').format(name), 'wb')
    f.write(response)
    f.close()


# 动态网页不会将资源以html形式返回，需要以其他方法爬取
def dynamicpage():
    # 此url返回一个json文件，包含了一系列专辑的信息。依据此id，可以包装一个url并向服务器请求音乐资源。
    url = "https://douban.fm/j/v2/songlist/explore?type=hot&genre=0&limit=20&sample_cnt=5"
    data = requests.get(url, headers=headers)
    # json.loads函数将json文件转为字典
    js = json.loads(data.text)
    idlist = []
    for each in js:
        idlist.append(each["id"])
    print(idlist)

    index = 0
    length = len(idlist)
    i = 0
    while (i < length):
        # 依据专辑id包装一个url，此url可以返回包含专辑内歌曲信息的json文件。
        url = "https://douban.fm/j/v2/songlist/" + \
              str(idlist[i]) + "/?kbps=128"
        print(url)
        try:
            data = requests.get(url, headers=headers)
            js = json.loads(data.text)
            for each in js["songs"]:
                # each["url"]为歌曲的url
                print(each["url"])
                picurl = each["picture"]
                print(picurl)
                downloadpic(str(index), picurl)
                artist = each["artist"]
                title = each["release"]["title"]
                albumtitle = each["albumtitle"]
                writetxt(str(index), "{\"artist\":\"" + artist + "\",\"title\":\"" +
                         title + "\",\"albumtitle\":\"" + albumtitle + "\"}")
                download(str(index), each["url"])
                index = index + 1
        except Exception as e:
            print(e)

        index = index + 1
        i = i + 1


# htmljx()
dynamicpage()
