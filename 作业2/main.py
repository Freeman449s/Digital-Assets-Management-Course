from flask import Flask, render_template
import os
import math

app = Flask(__name__)


@app.route('/')
def main():
    dict = scan()
    dict1 = dict["dict1"]
    dict2 = dict["dict2"]
    return render_template("homePage.html", dict1=dict1, dict2=dict2)


def scan():
    dict = {}
    dict1 = {}
    dict2 = {}
    # root 根目录路径
    # dirs 根目录下直接子目录的目录名（列表）
    # file 根目录下文件的文件名（列表）
    for root, dirs, files in os.walk(r".\static\Male Artists"):
        for file in files:
            id = file[:-4]
            if id not in dict1:
                info = {}
                idDir = os.path.join(root, id)  # os.path.join合并路径
                info["idDir"] = idDir
                info["textContent"] = readText(idDir)
                dict1[id] = info
    for root, dirs, files in os.walk(r".\static\Female Artists"):
        for file in files:
            id = file[:-4]
            if id not in dict2:
                info = {}
                idDir = os.path.join(root, id)  # os.path.join合并路径
                info["idDir"] = idDir
                info["textContent"] = readText(idDir)
                dict2[id] = info
    dict["dict1"] = dict1
    dict["dict2"] = dict2
    return dict


def readText(idDir):
    textDir = idDir + ".txt"
    file = open(textDir, encoding="UTF-8")
    content = file.read().strip(" \n")  # read方法一次性读取全部内容
    return content


if __name__ == "__main__":
    app.run()
