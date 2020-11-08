from bs4 import BeautifulSoup
import requests
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
urlTemplate = "http://www.shangshiwen.com/shiren_{1}_{0}.html"  # 参数0代表朝代，参数1代表这个朝代诗人列表的第几页


def crawlGuShiwen():
    # 不同朝代的诗人页数不一样，需要为每个朝代单独编写循环语句
    # 先秦
    url = urlTemplate.format("204", "1")
    crawlPage(url)
    # 两汉
    for i in range(1, 3):
        url = urlTemplate.format("205", str(i))
        crawlPage(url)
    # 魏晋
    for i in range(1, 3):
        url = urlTemplate.format("206", str(i))
        crawlPage(url)
    # 南北朝
    for i in range(1, 3):
        url = urlTemplate.format("207", str(i))
        crawlPage(url)
    # 隋
    url = urlTemplate.format("208", "1")
    crawlPage(url)
    # 唐
    for i in range(1, 55):
        url = urlTemplate.format("209", str(i))
        crawlPage(url)
    # 五代
    url = urlTemplate.format("210", "1")
    crawlPage(url)
    # 宋
    for i in range(1, 29):
        url = urlTemplate.format("211", str(i))
        crawlPage(url)
    # 金
    url = urlTemplate.format("212", "1")
    crawlPage(url)
    # 元
    for i in range(1, 9):
        url = urlTemplate.format("213", str(i))
        crawlPage(url)
    # 明
    for i in range(1, 5):
        url = urlTemplate.format("214", str(i))
        crawlPage(url)
    # 清
    for i in range(1, 7):
        url = urlTemplate.format("215", str(i))
        crawlPage(url)
    # 近现代
    url = urlTemplate.format("233", "1")
    crawlPage(url)


def crawlPage(url: str):
    pass
