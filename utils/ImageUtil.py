from io import BytesIO
from PIL import Image
import imagehash
import math
import operator
from functools import reduce


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


def readImageFromBytes(bytes):
    bytes_stream = BytesIO(bytes)
    return Image.open(bytes_stream)


def getImageHash(image=None, path=None):
    if path is not None:
        image = Image.open(path)
    return imagehash.phash(image)


def getImageCrop(path, box):
    image = Image.open(path)
    return image.crop(box)




# img1 = getImageCrop("test.png", [318, 1574, 759, 1701])
# img2 = getImageCrop("test2.png", [318, 1574, 759, 1701])

# s1 = similarity(getImageHash(image=img1), getImageHash(image=img2))
# s2 = image_contrast(img1, img2)

# print("s1 : {} , s2 {}".format(s1, s2))
# print("avg : {}".format((9*s1+s2)/10))
