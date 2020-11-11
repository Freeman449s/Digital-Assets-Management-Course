from PeopleInfo import PeopleInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
# 解析位置函数
APIKEY = "VNUBZ-K252F-2U4JO-NSF35-SKNJO-UEB37"
encoding = "UTF-8"

nameListPath = "人物列表\\画家名单.txt"
peopleFilePath = "PeopleInfo.json"
workFilePath = "WorkInfo.json"


def main():
    with open(nameListPath, "r", 8192) as nameListFile:
        for line in nameListFile:
            people = PeopleInfo(line.strip())
            people.crawl()
            people.write()


main()
