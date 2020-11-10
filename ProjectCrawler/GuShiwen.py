from bs4 import BeautifulSoup
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "http://www.shangshiwen.com/shiren_{1}_{0}.html"  # 参数0代表朝代，参数1代表这个朝代诗人列表的第几页


def crawlGuShiwen():
    # 不同朝代的诗人页数不一样，需要为每个朝代单独编写循环语句
    urls = []
    # 先秦
    url = urlTemplate.format("204", "1")
    urls.append(url)
    # 两汉
    for i in range(1, 3):
        url = urlTemplate.format("205", str(i))
        urls.append(url)
    # 魏晋
    for i in range(1, 3):
        url = urlTemplate.format("206", str(i))
        urls.append(url)
    # 南北朝
    for i in range(1, 3):
        url = urlTemplate.format("207", str(i))
        urls.append(url)
    # 隋
    url = urlTemplate.format("208", "1")
    urls.append(url)
    # 唐
    for i in range(1, 55):
        url = urlTemplate.format("209", str(i))
        urls.append(url)
    # 五代
    url = urlTemplate.format("210", "1")
    urls.append(url)
    # 宋
    for i in range(1, 29):
        url = urlTemplate.format("211", str(i))
        urls.append(url)
    # 金
    url = urlTemplate.format("212", "1")
    urls.append(url)
    # 元
    for i in range(1, 9):
        url = urlTemplate.format("213", str(i))
        urls.append(url)
    # 明
    for i in range(1, 5):
        url = urlTemplate.format("214", str(i))
        urls.append(url)
    # 清
    for i in range(1, 7):
        url = urlTemplate.format("215", str(i))
        urls.append(url)
    # 近现代
    url = urlTemplate.format("233", "1")
    urls.append(url)
    crawlPages(urls)


def crawlPages(urls: list):
    with open("人物列表\\诗（词）人列表.txt", "a+", 8192, encoding="UTF-8") as file:
        for url in urls:
            try:
                print("正在从 " + url + " 爬取诗（词）人列表...")
                response = requests.get(url, headers=headers)
                response.encoding = "UTF-8"
                html = response.text
                soup = BeautifulSoup(html, "lxml")
                for index, tag in enumerate(soup.select("b")):
                    if tag.text == "诗人列表":
                        continue
                    file.write(tag.text)
                    file.write("\n")
                print("完成")
            except Exception:
                traceback.print_exc()


def postProcess():
    print("后期处理...")
    with open("人物列表\\诗（词）人列表.txt", "r", 8192) as srcFile, \
            open("人物列表\\诗（词）人列表 - 后期处理.txt", "w", 8192) as targetFile:
        for line in srcFile:
            if line == "诗人列表\n":
                continue
            else:
                targetFile.write(line)
    print("完成")
