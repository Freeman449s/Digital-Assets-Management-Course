from bs4 import BeautifulSoup
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "http://www.ttpaihang.com/vote/rank.php?voteid=1436&page={}"

def crawlTiantianToupiao():
    with open("人物列表\\外国文学家列表-天天投票网.txt", "a+", 8192, encoding="gb2312") as file:
        try:
            for i in range(1, 4):
                url = urlTemplate.format(str(i))
                print("开始从“天天投票网”爬取外国作家信息，第" + str(i) + "页...")
                response = requests.get(url, headers=headers)
                response.encoding = "gb2312"
                html = response.text
                soup = BeautifulSoup(html, "lxml")
                for index, tag in enumerate(soup.find_all("a", target="_blank", class_="clink")):
                    file.write(tag.text)
                    file.write("\n")
                print("完成")
        except Exception:
            traceback.print_exc()
