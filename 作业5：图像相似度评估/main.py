import os
import numpy as np
from PIL import Image
import math
import time

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
        print("开始分析图像 " + imgPath + "。")
        print("分析颜色矩...")
        startTime = time.time()
        self.colorMomentVec = self.__colorMoments()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("已完成颜色矩分析，耗时" + str(duration) + "秒。颜色矩向量：" + str(self.colorMomentVec))
        print("分析对比度...")
        startTime = time.time()
        self.contrast = self.__contrast()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("已完成对比度分析，耗时" + str(duration) + "秒。对比度：" + str(self.contrast))
        print("分析朝向...")
        startTime = time.time()
        self.orientation = self.__orientation()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("已完成朝向分析，耗时" + str(duration) + "秒。朝向：" + str(self.orientation))
        print("开始分析粗糙度，这一步可能需要较长时间。")
        startTime = time.time()
        self.coarseness = self.__coarseness()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("已完成粗糙度分析，耗时" + str(duration) + "秒。粗糙度：" + str(self.coarseness))
        print("图像 " + imgPath + " 分析完毕。")

    def __colorMoments(self) -> np.array:
        """
        计算img成员的颜色矩，组成9维特征向量\n
        :return: 包含图像颜色矩信息的9维特征向量
        """
        pixels = np.array(self.img)  # 高*宽*通道数
        nPixels = np.size(pixels)
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
                RSum += math.pow(pixels[i][j][0] - RMean, 2)
                GSum += math.pow(pixels[i][j][1] - GMean, 2)
                BSum += math.pow(pixels[i][j][2] - BMean, 2)
        RVar = RSum / nPixels
        GVar = GSum / nPixels
        BVar = BSum / nPixels
        # 计算三阶矩
        RSum = 0
        GSum = 0
        BSum = 0
        for i in range(0, pixels.shape[0]):
            for j in range(0, pixels.shape[1]):
                RSum += math.pow(pixels[i][j][0] - RMean, 3)
                GSum += math.pow(pixels[i][j][1] - GMean, 3)
                BSum += math.pow(pixels[i][j][2] - BMean, 3)
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
        globalMaxK = min(math.floor(math.log(self.w - 1, 2) - 1), math.floor(math.log(self.h - 1, 2) - 1))
        means = np.zeros((self.h, self.w, globalMaxK), np.float64)
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        # 计算各不同中心、不同尺寸的窗口的均值
        # np.array()返回的矩阵尺寸为height*width
        # 边界像素不考虑
        startTime = time.time()
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                localMaxK = self.__maxK(j, i)
                for k in range(0, localMaxK):
                    means[i][j][k] = self.__calcWindowMean(j, i, k + 1, gsArr)
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print(" \t窗口均值计算完成，该过程耗时" + str(duration) + "秒。")
        bestKs = np.zeros((self.h, self.w), np.int32)
        # 为每个像素计算精细度
        startTime = time.time()
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                bestK = 1
                Max = -1
                localMaxK = self.__maxK(j, i)
                for k in range(0, localMaxK):
                    sumA = abs(means[i - 2 ** k][j + 2 ** k][k] - means[i + 2 ** k][j - 2 ** k][k])
                    sumB = abs(means[i - 2 ** k][j - 2 ** k][k] - means[i + 2 ** k][j + 2 ** k][k])
                    if max(sumA, sumB) > Max:
                        bestK = k + 1
                bestKs[i][j] = bestK
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print(" \t各像素精细度计算完成，该过程耗时" + str(duration) + "秒。")
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
        candiA = math.floor(math.log(x, 2))
        candiB = math.floor(math.log(self.w - x - 1, 2))
        candiC = math.floor(math.log(y, 2))
        candiD = math.floor(math.log(self.h - y - 1, 2))
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
        xMin = int(x - math.pow(2, k - 1))
        xMax = int(x + math.pow(2, k - 1))
        yMin = int(y - math.pow(2, k - 1))
        yMax = int(y + math.pow(2, k - 1))
        sum = 0
        # np.array()返回的矩阵尺寸为height*width
        for i in range(yMin, yMax + 1):
            for j in range(xMin, xMax + 1):
                sum += gsArr[i][j]
        return sum / math.pow(2 ** k + 1, 2)

    # todo nan问题
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
                yGradient = gsArr[i + 1][j - 1] + gsArr[i + 1][j] + gsArr[i + 1][j + 1] - \
                            gsArr[i - 1][j - 1] - gsArr[i - 1][j] - gsArr[i - 1][j + 1]
                gradient = (abs(xGradient) + abs(yGradient)) / 2
                if (gradient < threshold): continue
                rad = self.__calcNormalizeRad(xGradient, yGradient)
                nPixelVec[math.floor(rad / (math.pi / 4))] += 1
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
            (leftBound, rightBound) = self.__findTrough(peakIndex, HDVec)
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
        rightIndex = 7
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
    """
    基于图像的色彩、粗糙度、对比度和朝向，给出两幅图像的相似度的综合评分\n
    :param imgA: 图像A的ImageFeature对象
    :param imgB: 图像B的ImageFeature对象
    :return: float 两幅图像的相似度评分，在范围[0,1]内
    """
    eps = 0.000001
    if abs(np.linalg.norm(imgA.colorMomentVec)) < eps:
        # 纯黑图片
        if abs(np.linalg.norm(imgB.colorMomentVec)) < eps:
            colorFactor = 1
        else:
            colorFactor = 0
    else:
        # todo 内积
        colorFactor = np.dot(imgA.colorMomentVec, imgB.colorMomentVec) / \
                      np.linalg.norm(imgA.colorMomentVec) / np.linalg.norm(imgB.colorMomentVec)
    coarsenessA = imgA.coarseness
    coarsenessB = imgB.coarseness
    # 高精细度
    if abs(max(coarsenessA, coarsenessB)) < eps:
        coarsenessFactor = 1
    else:
        coarsenessFactor = min(coarsenessA, coarsenessB) / max(coarsenessA, coarsenessB)
    contrastA = imgA.contrast
    contrastB = imgB.contrast
    # 纯色图像
    if abs(max(contrastA, contrastB)) < eps:
        contrastFactor = 1
    else:
        contrastFactor = min(contrastA, contrastB) / max(contrastA, contrastB)
    orientationA = imgA.orientation
    orientationB = imgB.orientation
    if abs(max(orientationA, orientationB)) < eps:
        orientationFactor = 1
    else:
        orientationFactor = min(orientationA, orientationB) / max(orientationA, orientationB)
    return colorFactor * 0.25 + coarsenessFactor * 0.25 + contrastFactor * 0.25 + orientationFactor * 0.25


imgFeatA = ImageFeature(libPath + "\\1.jpg")
imgFeatB = ImageFeature(libPath + "\\2.jpg")
similarity = compare(imgFeatA, imgFeatB)
print("相似度：" + str(similarity))
