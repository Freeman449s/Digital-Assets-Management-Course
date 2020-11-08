from bs4 import BeautifulSoup
import bs4
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}


def crawlMinrenJianli():
    with open("外国文学家列表-名人简历网.txt", "a+", 8192, encoding="gb2312") as file:
        try:
            url = "http://www.gerenjianli.com/Mingren/Tags/577/"
            response = requests.get(url, headers=headers)
            response.encoding = "gb2312"
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            print("开始从“名人简历网”写入外国作家信息...")
            for index, tag in enumerate(soup.find_all("a", target="_blank")):
                check = hasNoImgChildren(tag)
                if check:
                    file.write(tag.text)
                    file.write("\n")
                else:
                    continue
            print("完成")
        except Exception:
            traceback.print_exc()


def hasNoImgChildren(tag: bs4.element.Tag) -> bool:
    for child in tag.children:
        if child.name == "img":
            return False
    return True
