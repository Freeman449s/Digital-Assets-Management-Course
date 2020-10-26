from PIL import Image
from PIL.Image import ANTIALIAS
import numpy as np

srcImg = Image.open("Source.jpg")
srcM = np.asarray(srcImg)
wmImg = Image.open("Watermark.jpg")
wmImg.resize(srcImg.size, ANTIALIAS)  # 将水印图尺寸调整到与原图一致
wmM = np.asarray(wmImg)
