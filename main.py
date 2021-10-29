from Config import Config
from ADBUtil import *
from ImageUtil import getImageHash, readImageFromBytes



flag = True
# flag = False

# getScreen("images\\tmp6.png")
# from PIL import Image
# pic = Image.open("images\\tmp6.png")
# pic.crop((322,1089,794,1250)).save("images\shengji.png")


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

    tmp = screen.crop(Config.shengjiArea)
    hash = getImageHash(tmp)
    if hash == Config.shengjiHash:
        touchScreen(Config.shengjiPos)