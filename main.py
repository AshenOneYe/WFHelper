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
        touchScreen(Config.lingdangArea)
        continue

    tmp = screen.crop(Config.canjiaArea)
    hash = getImageHash(image=tmp)
    if hash == Config.canjiaHash:
        print("参加")
        touchScreen(Config.canjiaArea)
        continue


    tmp = screen.crop(Config.zhunbeiArea)
    hash = getImageHash(image=tmp)
    if hash == Config.zhunbeiHash:
        print("准备")
        touchScreen(Config.zhunbeiArea)
        continue


    tmp = screen.crop(Config.yijingkaishiOKArea)
    hash = getImageHash(tmp)
    if hash == Config.yijingkaishiOKHash:
        print("已经开始")
        touchScreen(Config.yijingkaishiOKArea)
        continue


    tmp = screen.crop(Config.manyuanOKArea)
    hash = getImageHash(tmp)
    if hash == Config.manyuanOKHash:
        print("满员了")
        touchScreen(Config.manyuanOKArea)
        continue


    tmp = screen.crop(Config.jixuArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuHash:
        print("继续")
        touchScreen(Config.jixuArea)
        continue


    tmp = screen.crop(Config.likaiArea)
    hash = getImageHash(tmp)
    if hash == Config.likaiHash:
        print("离开房间")
        touchScreen(Config.likaiArea)
        continue


    tmp = screen.crop(Config.jixuguankaArea)
    hash = getImageHash(tmp)
    if hash == Config.jixuguankaHash:
        print("继续关卡")
        touchScreen(Config.jixuguankaArea)
        continue


    tmp = screen.crop(Config.shengjiArea)
    hash = getImageHash(tmp)
    if hash == Config.shengjiHash:
        print("升级了")
        touchScreen(Config.shengjiArea)
        continue
