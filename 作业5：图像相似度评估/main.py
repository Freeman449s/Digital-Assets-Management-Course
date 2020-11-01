import os
import numpy as np
from PIL import Image

libPath = "测试用图库"


class ImageFeature():
    def __init__(self, imgPath):
        """
        读取图片作为自身的img成员（PIL.Image.Image对象）\n
        :param imgPath: 图片的路径
        """
        self.img = Image.open(imgPath)
        self.colorMomentVec = self.__colorMoments()

    def __colorMoments(self):
        """
        计算img成员的颜色矩，组成9维特征向量\n
        :return: 包含图像颜色矩信息的9维特征向量
        """
        pixels = np.array(self.img)  # 高*宽*通道数
        nPixels = np.size()
        # 计算一阶矩
        RSum = 0
        GSum = 0
        BSum = 0
        for i in range(0, pixels.shape[0]):
            for j in range(0, pixels.shape[1]):
                RSum += pixels[i][j][0]
                GSum += pixels[i][j][1]
                BSum += pixels[i][j][2]
        RMean = RSum / nPixels
        GMean = GSum / nPixels
        BMean = BSum / nPixels
        # 计算二阶矩
        RSum = 0
        GSum = 0
        BSum = 0
        for i in range(0, pixels.shape[0]):
            for j in range(0, pixels.shape[1]):
                RSum += power(pixels[i][j][0] - RMean, 2)
                GSum += power(pixels[i][j][1] - GMean, 2)
                BSum += power(pixels[i][j][2] - BMean, 2)
        RVar = RSum / nPixels
        GVar = GSum / nPixels
        BVar = BSum / nPixels
        # 计算三阶矩
        RSum = 0
        GSum = 0
        BSum = 0
        for i in range(0, pixels.shape[0]):
            for j in range(0, pixels.shape[1]):
                RSum += power(pixels[i][j][0] - RMean, 3)
                GSum += power(pixels[i][j][1] - GMean, 3)
                BSum += power(pixels[i][j][2] - BMean, 3)
        RSkew = RSum / nPixels
        GSkew = GSum / nPixels
        BSkew = BSum / nPixels
        return np.array(RMean, GMean, BMean, RVar, GVar, BVar, RSkew, GSkew, BSkew)
