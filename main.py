from Config import Config
from utils.ADBUtil import *
from utils.ImageUtil import getImageHash, readImageFromBytes



flag = True
# flag = False

# getScreen("images\\tmp6.png")

# from PIL import Image
# pic = Image.open("template\\tmp6.png")
# pic.crop((322,1089,794,1250)).save("images\shengji.png")


# lastScreen = None


while flag:
    screen = readImageFromBytes(getScreen())

    tmp = screen.crop(Config.lingdangArea)
    hash = getImageHash(image=tmp)
    if hash == Config.lingdangHash:
        print("有铃铛")
        touchScreen(Config.lingdangPos)
        continue

    tmp = screen.crop(Config.canjiaArea)
    hash = getImageHash(image=tmp)
    if hash == Config.canjiaHash:
        print("参加")
        touchScreen(Config.canjiaPos)
        continue


    tmp = screen.crop(Config.zhunbeiArea)
    hash = getImageHash(image=tmp)
    if hash == Config.zhunbeiHash:
        print("准备")
        touchScreen(Config.zhunbeiPos)
        continue


    tmp = screen.crop(Config.yijingkaishiOKArea)
    hash = getImageHash(tmp)
    if hash == Config.yijingkaishiOKHash:
        print("已经开始")
        touchScreen(Config.yijingkaishiOKPos)
        continue


    tmp = screen.crop(Config.manyuanOKArea)
    hash = getImageHash(tmp)
    if hash == Config.manyuanOKHash:
        print("满员了")
        touchScreen(Config.manyuanOKPos)
        continue


    tmp = screen.crop(Config.jixuArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuHash:
        print("继续")
        touchScreen(Config.jixuPos)
        continue


    tmp = screen.crop(Config.likaiArea)
    hash = getImageHash(tmp)
    if hash == Config.likaiHash:
        print("离开房间")
        touchScreen(Config.likaiPos)
        continue


    tmp = screen.crop(Config.jixuguankaArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuguankaHash:
        print("继续关卡")
        touchScreen(Config.jixuguankaPos)
        continue


    tmp = screen.crop(Config.shengjiArea)
    hash = getImageHash(tmp)
    if hash == Config.shengjiHash:
        print("升级了")
        touchScreen(Config.shengjiPos)
        continue
