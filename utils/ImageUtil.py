from io import BytesIO
from PIL import Image, UnidentifiedImageError
import imagehash
import math
import operator
from functools import reduce
import cv2
import numpy as np


# 这个函数可能要继续优化
def similarity(img, target):
    hash1 = getImageHash(image=img)
    hash2 = target["hash"]
    sim1 = 1 - (hash1 - hash2)/len(hash1.hash)**2
    if "histogram" in target:
        h1 = img.histogram()
        h2 = target["histogram"]
        tmp = list(map(lambda a, b: (a-b)**2, h1, h2))
        tmp = reduce(operator.add, tmp)
        sim2 = math.sqrt(tmp)/(img.size[0] * img.size[1]*4)
        sim2 = (0.5 - sim2)*2
        colorRatio = target["colorRatio"]
        return (1 - colorRatio) * sim1 + colorRatio * sim2
    return sim1


def locateImage(test_pic, sample_pic):
    w, h = test_pic.size
    res = None

    sample_pic_gray = np.array(sample_pic.convert('L'))
    res = cv2.matchTemplate(sample_pic_gray, np.array(test_pic.convert('L')), cv2.TM_CCOEFF_NORMED)
    score = np.max(res)
    loc = np.where(res == score)
    return [loc[1], loc[0], loc[1] + w, loc[0] + h], score


def readImageFromBytes(bytes):
    bytes_stream = BytesIO(bytes)
    try:
        img = Image.open(bytes_stream)
    except UnidentifiedImageError:
        return None
    return img


def getImageHash(image=None, path=None):
    if path is not None:
        image = Image.open(path)
    return imagehash.phash(image)


def getImageCrop(path, box):
    image = Image.open(path)
    return image.crop(box)
