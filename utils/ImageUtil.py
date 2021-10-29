from io import BytesIO
from PIL import Image
from utils.ADBUtil import getScreen
import imagehash


def readImageFromBytes(bytes):
    bytes_stream = BytesIO(getScreen(None))
    return Image.open(bytes_stream)

def getImageHash(image=None,path=None):

    if path != None:
        image = Image.open(path)
    
    return imagehash.phash(image)

