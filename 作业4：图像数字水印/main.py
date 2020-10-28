from PIL import Image
from PIL.Image import ANTIALIAS
import numpy as np
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
srcPath = "Source.bmp"
markPath = "Watermark.bmp"
markedPath = "Image with Watermark.bmp"
extractedPath = "Extracted Watermark.bmp"

originalSize = (3072, 2048)  # 水印图的原始尺寸


@app.route("/")
def home():
    return render_template("home.html")


# localhost:5000/fuse只接受post方法
@app.route("/fuseResult", methods=["post"])
def fuse():
    srcImg = request.files["srcImg"]
    srcImg.save(srcPath)
    watermark = request.files["watermark"]
    watermark.save(markPath)
    print("来自用户的图片已经保存到本地")
    addWatermark(srcPath, markPath)
    return send_from_directory("./", markedPath, as_attachment=True)  # as_attachment设为True时，文件将作为下载项返回


@app.route("/extract")
def extract_home():
    return render_template("extract.html")


@app.route("/extractResult", methods=["post"])
def extract():
    global originalSize
    originalSize = (int(request.form["width"]), int(request.form["height"]))
    markedImg = request.files["markedImg"]
    markedImg.save(markedPath)
    extractWatermark(markedPath)
    return send_from_directory("./", extractedPath, as_attachment=True)


def addWatermark(srcPath, markPath):
    srcImg = Image.open(srcPath)
    srcM = np.array(srcImg)  # 尺寸为height * width * channels
    srcM.flags.writeable = True
    watermark = Image.open(markPath)
    # originalSize = watermark.size
    watermark = watermark.resize(srcImg.size, ANTIALIAS)  # 将水印图尺寸调整到与原图一致
    markM = np.array(watermark)
    markM.flags.writeable = True
    # 水印图像素值除以85
    # 原图像素值右移位后与归一化后的水印图像素值相加
    for i in range(0, markM.shape[0]):
        for j in range(0, markM.shape[1]):
            for k in range(0, markM.shape[2]):
                markM[i][j][k] = round(markM[i][j][k] / 85)
                srcM[i][j][k] = srcM[i][j][k] >> 2
                srcM[i][j][k] = srcM[i][j][k] << 2
                srcM[i][j][k] += markM[i][j][k]
    markedImg = Image.fromarray(srcM)
    markedImg.save(markedPath)


def extractWatermark(markedImgPath):
    markedImg = Image.open(markedImgPath)
    markedM = np.array(markedImg)
    markedM.flags.writeable = True
    # 提取每个像素的低2位，乘以85
    for i in range(0, markedM.shape[0]):
        for j in range(0, markedM.shape[1]):
            for k in range(0, markedM.shape[2]):
                tmp = markedM[i][j][k] >> 2
                tmp = tmp << 2
                markedM[i][j][k] = (markedM[i][j][k] - tmp) * 85
    extractedImg = Image.fromarray(markedM)
    extractedImg.resize(originalSize, ANTIALIAS)
    extractedImg.save(extractedPath)


# addWatermark("Source.bmp", "Watermark.bmp")
# extractWatermark("Image with Watermark.bmp")

if __name__ == "__main__":
    app.run()
