from PIL import Image
from PIL.Image import ANTIALIAS
import numpy as np


def addWatermark(srcPath, markPath):
    srcImg = Image.open(srcPath)
    srcM = np.array(srcImg)  # 尺寸为height * width * channels
    srcM.flags.writeable = True
    markImg = Image.open(markPath)
    markImg = markImg.resize(srcImg.size, ANTIALIAS)  # 将水印图尺寸调整到与原图一致
    markM = np.array(markImg)
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
    markedImg.save("Image with Watermark.bmp")


addWatermark("Source.jpg", "Watermark.jpg")
