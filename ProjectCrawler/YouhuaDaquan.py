from bs4 import BeautifulSoup
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def crawlYouhuaDaquan():
    with open("人物列表\\画家名单.txt", "a+", 8192, encoding="UTF-8") as file:
        try:
            url = "http://www.youhuadaquan.org/top-artist.html"
            print("开始爬取画家信息...")
            response = requests.get(url, headers=headers)
            response.encoding = "UTF-8"
            html = response.text
            bs = BeautifulSoup(html, "lxml")
            for index, tag in enumerate(bs.select("span")):
                file.write(tag.text)
                file.write("\n")
            print("完成")
        except Exception:
            traceback.print_exc()
