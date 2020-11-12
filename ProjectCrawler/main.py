from PeopleInfo import PeopleInfo

nameListPath = "人物列表\\诗（词）人列表 - 后期处理.txt"


def main():
    with open(nameListPath, "r", 8192) as nameListFile:
        for line in nameListFile:
            people = PeopleInfo(line.strip())
            people.crawl()
            people.write()


main()
