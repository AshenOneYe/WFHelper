from io import BytesIO
from typing import Any, List
from PIL import Image, UnidentifiedImageError
import imagehash
import math
import operator
from functools import reduce


# 这个函数可能要继续优化
def similarity(img, target: Any):
    hash1 = getImageHash(image=img)
    hash2 = target.hash
    sim1 = 1 - (hash1 - hash2) / len(hash1.hash) ** 2
    if target.histogram is not None:
        h1 = img.histogram()
        h2 = target.histogram
        tmp = list(map(lambda a, b: (a - b) ** 2, h1, h2))
        result = reduce(operator.add, tmp)
        sim2 = math.sqrt(result) / (img.size[0] * img.size[1] * 4)
        sim2 = (0.5 - sim2) * 2
        colorRatio = target.colorRatio
        return (1 - colorRatio) * sim1 + colorRatio * sim2
    return sim1


def readImageFromBytes(bytes: bytes):
    bytes_stream = BytesIO(bytes)
    try:
        img = Image.open(bytes_stream)
    except UnidentifiedImageError:
        return None
    return img


def getImageHash(image: Image = None, path: str = None):
    if path is not None:
        image = Image.open(path)
    return imagehash.phash(image)


def getImageCrop(path: str, box: List[int]):
    image = Image.open(path)
    return image.crop(box)
