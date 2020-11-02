import os
import numpy as np
from PIL import Image
import math

libPath = "测试用图库"


class ImageFeature():
    """
    图像特征类，包含以下成员：
    img 代表图像的PIL.Image.Image对象\n
    w 图像的宽度\n
    h 图像的高度\n
    colorMomentVec 颜色矩向量\n
    coarseness 粗糙度\n
    contrast 对比度\n
    orientation 代表朝向的浮点值
    """

    def __init__(self, imgPath: str):
        """
        读取图片作为自身的img成员（PIL.Image.Image对象）\n
        :param imgPath: 图片的路径
        """
        self.img = Image.open(imgPath)
        self.w = self.img.width
        self.h = self.img.height
        self.colorMomentVec = self.__colorMoments()
        self.coarseness = self.__coarseness()
        self.contrast = self.__contrast()
        self.orientation = self.__orientation()

    def __colorMoments(self) -> np.array:
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
        return np.array([RMean, GMean, BMean, RVar, GVar, BVar, RSkew, GSkew, BSkew])

    def __coarseness(self) -> float:
        """
        计算图像的平均粗糙度。值越小表示图像细节越丰富。\n
        :return: float 图像的平均粗糙度
        """
        # 求全局的k最大值
        globalMaxK = min(floor((math.log(self.w - 1), 2) - 1), floor((math.log(self.h - 1), 2) - 1))
        means = np.zeros((self.h, self.w, globalMaxK), np.float64)
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        # 计算各不同中心、不同尺寸的窗口的均值
        # np.array()返回的矩阵尺寸为height*width
        # 边界像素不考虑
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                for k in range(0, self.__maxK(j, i)):
                    means[i][j][k] = self.__calcWindowMean(j, i, k, gsArr)
        bestKs = np.zeros((self.h, self.w), np.int32)
        # 为每个像素计算精细度
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                bestK = 1
                max = -1
                for k in range(0, self.__maxK(j, i)):
                    sumA = abs(means[i - 2 ** k][j + 2 ** k][k] - means[i + 2 ** k][j - 2 ** k][k])
                    sumB = abs(means[i - 2 ** k][j - 2 ** k][k] - means[i + 2 ** k][j + 2 ** k][k])
                    if (max(sumA, sumB) > max):
                        bestK = k + 1
                bestKs[i][j] = bestK
        # 计算全局精细度
        sum = 0
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                sum += bestKs[i][j]
        return sum / (self.w - 2) / (self.h - 2)

    def __maxK(self, x: int, y: int) -> int:
        """
        求对一个像素(x,y)而言，需要考虑的窗口大小等级k的最大值\n
        :param x: 像素的横坐标（以0起始）
        :param y: 像素的总坐标（以0起始）
        :return: int 需要考虑的窗口大小等级k的最大值
        """
        candiA = floor(math.log(x, 2))
        candiB = floor(math.log(self.w - x - 1, 2))
        candiC = floor(math.log(y, 2))
        candiD = floor(math.log(self.h - y - 1, 2))
        return min(candiA, candiB, candiC, candiD)

    def __calcWindowMean(self, x: int, y: int, k: int, gsArr: np.array) -> float:
        """
        计算以(x,y)为中心，2^k+1窗口内像素的平均值\n
        :param x: 窗口中心点的横坐标
        :param y: 窗口中心点的纵坐标
        :param k: 窗口大小等级
        :param gsArr: 灰度图像矩阵
        :return: float 窗口像素值的均值
        """
        xMin = x - math.pow(2, k - 1)
        xMax = x + math.pow(2, k - 1)
        yMin = y - math.pow(2, k - 1)
        yMax = y + math.pow(2, k - 1)
        sum = 0
        # np.array()返回的矩阵尺寸为height*width
        for i in range(yMin, yMax + 1):
            for j in range(xMin, xMax + 1):
                sum += gsArr[i][j]
        return sum / math.pow(2 ** k + 1, 2)

    def __contrast(self) -> float:
        """
        计算图像的对比度\n
        :return: float 图像的对比度
        """
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        sum = 0
        for i in range(0, gsArr.shape[0]):
            for j in range(0, gsArr.shape[1]):
                sum += gsArr[i][j]
        mean = sum / gsArr.size
        sum = 0
        for i in range(0, gsArr.shape[0]):
            for j in range(0, gsArr.shape[1]):
                sum += gsArr[i][j] ** 4
        mean_quad = sum / gsArr.size
        sum = 0
        for i in range(0, gsArr.shape[0]):
            for j in range(0, gsArr.shape[1]):
                sum += (gsArr[i][j] - mean) ** 4
        var_quad = sum / gsArr.size
        alpha = mean_quad / var_quad
        return var_quad ** (1 / 4) / (alpha ** (1 / 4))

    def __orientation(self) -> float:
        """
        计算图像的朝向\n
        :return: float 代表图像朝向的浮点值
        """
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        threshold = 12  # 梯度阈值。梯度过小代表方向性不明显，不予考虑
        HDVec = np.zeros(8, np.float64)
        nPixelVec = np.zeros(8, np.int32)  # 将朝向分为8个分区，nPixelVec记录了朝向在分区内的像素的个数
        for i in range(1, self.h - 1):
            for j in range(1, self.w - 1):
                xGradient = gsArr[i - 1][j + 1] + gsArr[i][j + 1] + gsArr[i + 1][j + 1] - \
                            gsArr[i - 1][j - 1] - gsArr[i][j - 1] - gsArr[i + 1][j - 1]
                yGradient = gsArr[i + 1][j - 1] + gsArr[i + 1][j] + gsArr[i + 1][j + 2] - \
                            gsArr[i - 1][j - 1] - gsArr[i - 1][j] - gsArr[i - 1][j + 1]
                gradient = (abs(xGradient) + abs(yGradient)) / 2
                if (gradient < threshold): continue
                rad = self.__calcNormalizeRad(xGradient, yGradient)
                nPixelVec[floor(rad / (math.pi / 4))] += 1
        sum = 0
        for i in range(0, 8):
            sum += nPixelVec[i]
        # 图像没有明显方向性
        if sum == 0:
            return math.inf
        for i in range(0, 8):
            HDVec[i] = nPixelVec[i] / sum
        peakIndices = []  # 记录HD极值点的横坐标
        for i in range(1, 7):
            if HDVec[i - 1] < HDVec[i] and HDVec[i + 1] < HDVec[i]:
                peakIndices.append(i)
        sumA = 0
        for i in range(0, len(peakIndices)):
            sumB = 0
            peakIndex = peakIndices[i]
            (leftBound, rightBound) = self.__findTrough()
            for j in range(leftBound, rightBound + 1):
                phi = math.pi / 4 * j + math.pi / 8
                phi_p = math.pi / 4 * peakIndex + math.pi / 8
                sumB += ((phi - phi_p) ** 2) * HDVec[j]
            sumA += sumB
        return sumA * len(peakIndices)

    def __calcNormalizeRad(self, deltaX: float, deltaY: float) -> float:
        """
        依据给定的横向和纵向跨度，计算向量的弧度并归一化到[0,2pi]之间\n
        :param deltaX: 向量的横向跨度
        :param deltaY: 向量的纵向跨度
        :return: float 归一化到[0,2pi]的向量弧度
        """
        if deltaX == 0:
            if deltaY > 0:
                rad = math.pi / 2
            elif deltaY == 0:
                return 0
            else:
                rad = math.pi / 2 * 3
        else:
            if deltaY == 0:
                return 0
            rad = math.atan(deltaY / deltaX)
            # 角度归一化到[0,2pi]
            if deltaX > 0 and deltaY > 0:
                rad = rad
            elif deltaX > 0 and deltaY < 0:
                rad = rad + 2 * math.pi
            elif deltaX < 0 and deltaY > 0:
                rad = rad + math.pi
            else:
                rad = rad + math.pi
        return rad

    def __findTrough(self, i: int, HDVec: list) -> tuple:
        """
        寻找HD函数中，横坐标为i的波峰的两侧波谷的横坐标\n
        :param i: 波峰的横坐标
        :param HDVec: HD函数在各个横坐标上的值
        :return: tuple 两侧波谷的横坐标
        """
        leftIndex = 0
        RightIndex = 7
        for i in range(i - 1, 0, -1):
            if HDVec[i - 1] > HDVec[i] and HDVec[i + 1] > HDVec[i]:
                leftIndex = i
                break
        for i in range(i + 1, 7):
            if HDVec[i - 1] > HDVec[i] and HDVec[i + 1] > HDVec[i]:
                rightIndex = i
                break
        return (leftIndex, rightIndex)


def compare(imgA: ImageFeature, imgB: ImageFeature) -> float:
    colorFactor = np.multiply(imgA.colorMomentVec, imgB.colorMomentVec) / \
                  np.linalg.norm(mgA.colorMomentVec) / np.linalg.norm(imgB.colorMomentVec)
    # todo
    pass
