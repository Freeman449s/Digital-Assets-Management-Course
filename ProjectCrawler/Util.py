import requests
import json

APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"


def parsePos(pos: str) -> list:
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
