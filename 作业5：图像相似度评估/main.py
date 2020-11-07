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
        self.path = imgPath
        self.w = self.img.width
        self.h = self.img.height

    def analyze(self):
        """
        分析图像的颜色矩、对比度、朝向和粗糙度特征，结果保存为自身的成员
        """
        print("开始分析图像 " + self.path + "。")
        print("\t分析颜色矩...")
        startTime = time.time()
        self.colorMomentVec = self.__colorMoments()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("\t已完成颜色矩分析，耗时" + str(duration) + "秒。颜色矩向量：" + str(self.colorMomentVec))
        print("\t分析对比度...")
        startTime = time.time()
        self.contrast = self.__contrast()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("\t已完成对比度分析，耗时" + str(duration) + "秒。对比度：" + str(self.contrast))
        print("\t分析朝向...")
        startTime = time.time()
        self.orientation = self.__orientation()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("\t已完成朝向分析，耗时" + str(duration) + "秒。朝向：" + str(self.orientation))
        print("\t开始分析粗糙度，这一步可能需要较长时间。")
        startTime = time.time()
        self.coarseness = self.__coarseness()
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print("\t已完成粗糙度分析，耗时" + str(duration) + "秒。粗糙度：" + str(self.coarseness))
        print("图像 " + self.path + " 分析完毕。")

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
        globalMaxK = min(math.floor(math.log(self.w - 1, 2)), math.floor(math.log(self.h - 1, 2)))
        means = np.zeros((self.h, self.w, globalMaxK), np.float64)
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        # 为每个像素计算最大的k
        maxKs = np.zeros((self.w, self.h), np.int32)
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                maxKs[j][i] = self.__maxK(j, i)
        # Step 1：计算各不同中心、不同尺寸的窗口的均值
        # np.array()返回的矩阵尺寸为height*width
        # 边界像素不考虑
        startTime = time.time()
        # for i in range(2, self.h - 2):
        #     for j in range(2, self.w - 2):
        #         localMaxK = maxKs[j][i]
        #         for k in range(0, localMaxK):
        #             means[i][j][k] = self.__calcWindowMean(j, i, k + 1, gsArr)
        means = self.__calcWindowMeans(gsArr, globalMaxK, maxKs)
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print(" \t\t窗口均值计算完成，该过程耗时" + str(duration) + "秒。")
        bestKs = np.zeros((self.h, self.w), np.int32)
        # Step2：为每个像素计算精细度
        startTime = time.time()
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                bestK = 1
                Max = -1
                maxCoordinatedK = self.__maxCoordinatedK(j, i, maxKs)
                for k in range(1, maxCoordinatedK + 1):
                    sumA = abs(
                        means[i - 2 ** (k - 1)][j + 2 ** (k - 1)][k] - means[i + 2 ** (k - 1)][j - 2 ** (k - 1)][k])
                    sumB = abs(
                        means[i - 2 ** (k - 1)][j - 2 ** (k - 1)][k] - means[i + 2 ** (k - 1)][j + 2 ** (k - 1)][k])
                    if max(sumA, sumB) > Max:
                        Max = max(sumA, sumB)
                        bestK = k
                bestKs[i][j] = bestK
        endTime = time.time()
        duration = round(endTime - startTime, 2)
        print(" \t\t各像素精细度计算完成，该过程耗时" + str(duration) + "秒。")
        # Step 3：计算全局精细度
        sum = 0.0
        for i in range(2, self.h - 2):
            for j in range(2, self.w - 2):
                # 当**两边的运算数中的某个属于numpy中的类型时，返回的结果可能为numpy类型，而非内置类型。这可能导致越界。
                sum += math.pow(2, bestKs[i][j])
        return sum / (self.w - 2) / (self.h - 2)

    def __maxK(self, x: int, y: int) -> int:
        """
        求对一个像素(x,y)而言，在Step1中需要考虑的窗口等级k的最大值\n
        :param x: 像素的横坐标（以2起始）
        :param y: 像素的纵坐标（以2起始）
        :return: int 在Step1需要考虑的窗口等级k的最大值
        """
        candiA = math.floor(math.log(x, 2))
        candiB = math.floor(math.log(self.w - x - 1, 2))
        candiC = math.floor(math.log(y, 2))
        candiD = math.floor(math.log(self.h - y - 1, 2))
        return min(candiA, candiB, candiC, candiD) + 1

    def __maxCoordinatedK(self, x: int, y: int, maxKs: np.array) -> int:
        """
        求对一个像素(x,y)而言，在Step2中需要考虑的窗口等级k的最大值。\n
        请注意：该函数的返回值不同于__maxK()返回的值，该函数返回的值考虑了在窗口等级k0下，位于顶点的像素的最大k值。\n
        :param x: 像素的横坐标（以2起始）
        :param y: 像素的纵坐标（以2起始）
        :param maxKs: 存储了以各个像素为中心的窗口最大等级的矩阵
        :return: 在Step2中，此像素需要考虑的最大k值
        """
        maxKOfThis = maxKs[x][y]
        maxKCoordinated = 1
        # 对不同的k0，检查该尺度下窗口顶点的最大k值能否达到k0，从而确定在Step2下每个像素所需要考虑的最大k
        for i in range(1, maxKOfThis + 1):
            if maxKs[x - 2 ** (i - 1)][y - 2 ** (i - 1)] >= i \
                    and maxKs[x - 2 ** (i - 1)][y + 2 ** (i - 1)] >= i \
                    and maxKs[x + 2 ** (i - 1)][y - 2 ** (i - 1)] >= i \
                    and maxKs[x + 2 ** (i - 1)][y + 2 ** (i - 1)] >= i:
                maxKCoordinated = i
            else:
                break
        return maxKCoordinated

    # 因效率过低而弃用
    # def __calcWindowMean(self, x: int, y: int, k: int, gsArr: np.array) -> float:
    #     """
    #     计算以(x,y)为中心，2^k+1窗口内像素的平均值\n
    #     :param x: 窗口中心点的横坐标
    #     :param y: 窗口中心点的纵坐标
    #     :param k: 窗口大小等级
    #     :param gsArr: 灰度图像矩阵
    #     :return: float 窗口像素值的均值
    #     """
    #     xMin = int(x - math.pow(2, k - 1))
    #     xMax = int(x + math.pow(2, k - 1))
    #     yMin = int(y - math.pow(2, k - 1))
    #     yMax = int(y + math.pow(2, k - 1))
    #     sum = 0.0
    #     # np.array()返回的矩阵尺寸为height*width
    #     for i in range(yMin, yMax + 1):
    #         for j in range(xMin, xMax + 1):
    #             sum += gsArr[i][j]
    #     return sum / math.pow(2 ** k + 1, 2)

    def __calcWindowMeans(self, gsArr: np.array, globalMaxK: int, maxKs: np.array):
        """
        为各个像素，计算各尺寸窗口的均值\n
        :param gsArr: 灰度矩阵
        :param globalMaxK: k的全局最大值
        :param maxKs: 每个像素k的最大值
        :return: 存储了各个像素各尺寸窗口均值的矩阵
        """
        means = np.zeros((self.h, self.w, globalMaxK + 1), np.float64)
        # 0阶窗口均值等于自身像素值
        for i in range(0, self.h):
            for j in range(0, self.w):
                means[i][j][0] = gsArr[i][j]
        for k in range(1, globalMaxK + 1):
            for i in range(2, self.h - 2):
                for j in range(2, self.w - 2):
                    if k > maxKs[j][i]:
                        continue
                    if k == 1:
                        sum = means[i][j][0]
                    else:
                        # 读取k-1阶均值乘以(2^(k-1)+1)^2，作为中心k-1阶窗口值之和
                        sum = means[i][j][k - 1] * math.pow(math.pow(2, k - 1) + 1, 2)
                    minX = int(j - math.pow(2, k - 1))
                    maxX = int(j + math.pow(2, k - 1))
                    minY = int(i - math.pow(2, k - 1))
                    maxY = int(i + math.pow(2, k - 1))
                    # 考虑外围像素
                    for x in range(minX, maxX + 1):
                        sum += gsArr[minY][x]
                        sum += gsArr[maxY][x]
                    for y in range(minY + 1, maxY):
                        sum += gsArr[y][minX]
                        sum += gsArr[y][maxX]
                    means[i][j][k] = sum / math.pow(math.pow(2, k) + 1, 2)
        return means

    def __contrast(self) -> float:
        """
        计算图像的对比度\n
        :return: float 图像的对比度
        """
        grayscale = self.img.convert("L")
        gsArr = np.array(grayscale)
        sum = 0.0
        for i in range(0, gsArr.shape[0]):
            for j in range(0, gsArr.shape[1]):
                sum += gsArr[i][j]
        mean = sum / gsArr.size
        sum = 0.0
        for i in range(0, gsArr.shape[0]):
            for j in range(0, gsArr.shape[1]):
                sum += math.pow(gsArr[i][j], 4)
        mean_quad = sum / gsArr.size
        sum = 0.0
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
        HDVec = np.zeros(16, np.float64)
        nPixelVec = np.zeros(16, np.int32)  # 将朝向分为8个分区，nPixelVec记录了朝向在分区内的像素的个数
        for i in range(1, self.h - 1):
            for j in range(1, self.w - 1):
                xGradient = int(gsArr[i - 1][j + 1]) + int(gsArr[i][j + 1]) + int(gsArr[i + 1][j + 1]) - \
                            int(gsArr[i - 1][j - 1]) - int(gsArr[i][j - 1]) - int(gsArr[i + 1][j - 1])
                yGradient = int(gsArr[i + 1][j - 1]) + int(gsArr[i + 1][j]) + int(gsArr[i + 1][j + 1]) - \
                            int(gsArr[i - 1][j - 1]) - int(gsArr[i - 1][j]) - int(gsArr[i - 1][j + 1])
                gradient = (abs(xGradient) + abs(yGradient)) / 2
                if (gradient < threshold): continue
                rad = self.__calcNormalizeRad(xGradient, yGradient)
                nPixelVec[math.floor(rad / (math.pi / 8))] += 1
        sum = 0
        for i in range(0, 16):
            sum += nPixelVec[i]
        # 图像没有明显方向性
        if sum == 0:
            return math.inf
        for i in range(0, 16):
            HDVec[i] = nPixelVec[i] / sum
        peakIndices = []  # 记录HD极值点的横坐标
        for i in range(1, 15):
            if HDVec[i - 1] < HDVec[i] and HDVec[i + 1] < HDVec[i]:
                peakIndices.append(i)
        sumA = 0.0
        for i in range(0, len(peakIndices)):
            sumB = 0.0
            peakIndex = peakIndices[i]
            (leftBound, rightBound) = self.__findTrough(peakIndex, HDVec)
            for j in range(leftBound, rightBound + 1):
                phi = math.pi / 8 * j + math.pi / 16
                phi_p = math.pi / 8 * peakIndex + math.pi / 16
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
        rightIndex = 15
        for i in range(i - 1, 0, -1):
            if HDVec[i - 1] > HDVec[i] and HDVec[i + 1] > HDVec[i]:
                leftIndex = i
                break
        for i in range(i + 1, 15):
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
    return colorFactor * 0.4 + coarsenessFactor * 0.2 + contrastFactor * 0.2 + orientationFactor * 0.2


def main():
    for root, dirs, files in os.walk(libPath):
        benchmark = ImageFeature(os.path.join(root, files[0]))
        print("已选择 " + benchmark.path + " 作为基准。")
        imgList = []
        similarities = []
        files.sort()
        for i in range(1, len(files)):
            filename = files[i]
            imgList.append(ImageFeature(os.path.join(root, filename)))
        benchmark.analyze()
        for img in imgList:
            img.analyze()
        print("开始分析相似度。")
        mostSimilar = imgList[0]
        maxSimilarity = -1
        for img in imgList:
            similarity = compare(benchmark, img)
            if similarity > maxSimilarity:
                maxSimilarity = similarity
                mostSimilar = img
            print("基准 " + benchmark.path + " 与图像 " + img.path + " 的相似度为" + str(similarity))
        print("全部分析已结束，与基准 " + benchmark.path + " 最为相似的图片为 " + mostSimilar.path + "。")


main()
