from Config import Config
from ADBUtil import *
from ImageUtil import getImageHash, readImageFromBytes
# from PIL import Image


flag = True
# flag = False

# getScreen("images\\tmp5.png")
# pic = Image.open("images\manyuan.png")
# pic.crop((316,1422,760,1528)).save("images\manyuanOK.png")


while flag:
    screen = readImageFromBytes(getScreen())

    tmp = screen.crop(Config.lingdangArea)
    hash = getImageHash(image=tmp)
    if hash == Config.lingdangHash:
        touchScreen(Config.lingdangPos)

    tmp = screen.crop(Config.canjiaArea)
    hash = getImageHash(image=tmp)
    if hash == Config.canjiaHash:
        touchScreen(Config.canjiaPos)

    tmp = screen.crop(Config.zhunbeiArea)
    hash = getImageHash(image=tmp)
    if hash == Config.zhunbeiHash:
        touchScreen(Config.zhunbeiPos)

    tmp = screen.crop(Config.yijingkaishiOKArea)
    hash = getImageHash(tmp)
    if hash == Config.yijingkaishiOKHash:
        touchScreen(Config.yijingkaishiOKPos)

    tmp = screen.crop(Config.manyuanOKArea)
    hash = getImageHash(tmp)
    if hash == Config.manyuanOKHash:
        touchScreen(Config.manyuanOKPos)

    tmp = screen.crop(Config.jixuArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuHash:
        touchScreen(Config.jixuPos)

    tmp = screen.crop(Config.likaiArea)
    hash = getImageHash(tmp)
    if hash == Config.likaiHash:
        touchScreen(Config.likaiPos)

    tmp = screen.crop(Config.jixuguankaArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuguankaHash:
        touchScreen(Config.jixuguankaPos)