from io import BytesIO
from typing import List
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as ImageClass
import imagehash
import math
import operator
from functools import reduce


def similarity(
    img: ImageClass,
    hash: imagehash.ImageHash = None,
    histogram: List[int] = None,
    colorRatio: float = 0,
):
    if hash is None:
        raise Exception
    elif histogram is None:
        return hashSimilarity(img, hash)
    elif colorRatio == 0:
        raise Exception
    else:
        sim1 = hashSimilarity(img, hash)
        sim2 = colorSimilarity(img, histogram)
        return (1 - colorRatio) * sim1 + colorRatio * sim2


def hashSimilarity(img: ImageClass, hash: imagehash.ImageHash):
    hash1 = getImageHash(image=img)
    hash2 = hash
    sim = 1 - (hash1 - hash2) / len(hash1.hash) ** 2
    return sim


def colorSimilarity(img: ImageClass, histogram: List[int]):
    h1 = img.histogram()
    h2 = histogram
    tmp = list(map(lambda a, b: (a - b) ** 2, h1, h2))
    result = reduce(operator.add, tmp)
    sim = math.sqrt(result) / (img.size[0] * img.size[1] * 4)
    sim = (0.5 - sim) * 2
    return sim


def readImageFromBytes(bytes: bytes) -> ImageClass:
    bytes_stream = BytesIO(bytes)
    try:
        img = Image.open(bytes_stream)
    except UnidentifiedImageError:
        return None
    return img


output_buffer = BytesIO()


def img2bytes(img: ImageClass) -> bytes:
    output_buffer = BytesIO()
    img.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


def getImageHash(image: ImageClass = None, path: str = None) -> imagehash.ImageHash:
    if path is not None:
        image = Image.open(path)
    return imagehash.phash(image)


def getImageCrop(path: str, box: List[int]):
    image = Image.open(path)
    return image.crop(box)
