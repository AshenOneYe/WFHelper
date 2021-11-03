from io import BytesIO
from PIL import Image
import imagehash

def similarity(hash1,hash2):
    sim = 1 - (hash1 - hash2)/len(hash1.hash)**2
    return sim

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

def similarity(h1,h2):
    count = 0
    total = 0
    for hh1,hh2 in zip(h1,h2):
        for hhh1,hhh2 in zip(hh1,hh2):
            if hhh1 == hhh2:
                count += 1
            total += 1

    return count/total
