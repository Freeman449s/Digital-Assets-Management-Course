import requests
import json

APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def parseCoordinate(pos: str) -> list:
    """
    根据给定的地址字符串解析经纬度\n
    by Lvkesheng Shen\n
    :param pos: 代表位置的字符串。
    :return: 列表。第一个值为状态码：-1为查询失败，0为查询成功。第二个值为信息，若查询成功则返回查询结果，否则返回错误信息。
    """
    reply = requests.get("https://apis.map.qq.com/ws/geocoder/v1/?address=" + pos + "&key=" + APIKEY)
    jsonData = json.loads(reply.text)
    if (jsonData["status"] != 0):
        return [-1, jsonData["message"]]
    else:
        return [0, jsonData["result"]]


def parseCoordinate_foreign(pos):
    try:
        url =  "https://api.pickpoint.io/v1//forward?q=" + pos + "&key=VAYNFrz3NsN9sYAFpFUr"
        reply = requests.get(url)
        a = json.loads(reply.text)
        lat = a[0]["lat"]
        long = a[0]["lon"]
        print(lat,long)
        return [0,{"location":{"lng":long,"lat":lat}}]
    except Exception as e:
        return [-1,e]

def downloadBinary(url: str, path: str) -> None:
    # Response.content存储Response对象的二进制形式
    content = requests.get(url, headers=headers).content
    file = open(path, "wb")
    file.write(content)
    file.close()
