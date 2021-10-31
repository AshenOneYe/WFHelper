from io import BytesIO
from PIL import Image
import imagehash


def readImageFromBytes(bytes):  
    bytes_stream = BytesIO(bytes)
    return Image.open(bytes_stream)

def getImageHash(image=None,path=None):

    if path != None:
        image = Image.open(path)

    return imagehash.phash(image)

def getImageCrop(path,box):
    image = Image.open(path)
    return image.crop(box)


