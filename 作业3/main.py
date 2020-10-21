from flask import Flask, render_template
import os
import json

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
    for root, dirs, files in os.walk(r".\static\Library 1"):
        for file in files:
            dotIndex=file.find(".")
            id = file[:dotIndex]
            if id not in dict1:
                info = {}
                idDir = os.path.join(root, id)  # os.path.join合并路径
                info["idDir"] = idDir
                info["textContent"] = readJSON(idDir)
                dict1[id] = info
    for root, dirs, files in os.walk(r".\static\Library 2"):
        for file in files:
            dotIndex = file.find(".")
            id = file[:dotIndex]
            if id not in dict2:
                info = {}
                idDir = os.path.join(root, id)  # os.path.join合并路径
                info["idDir"] = idDir
                info["textContent"] = readJSON(idDir)
                dict2[id] = info
    dict["dict1"] = dict1
    dict["dict2"] = dict2
    return dict


def readJSON(idDir):
    jsonDir = idDir + ".json"
    file = open(jsonDir, encoding="UTF-8")
    jsonContent = file.read()
    dict = json.loads(jsonContent)
    text = "曲名：" + dict["title"] + "\n"
    text += "艺术家：" + dict["artist"] + "\n"
    text += "专辑：" + dict["albumTitle"] + "\n"
    text += "时长：" + dict["length"]
    return text


if __name__ == "__main__":
    app.run()
