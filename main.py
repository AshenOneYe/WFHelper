from Config import *
from utils.ADBUtil import *
from utils.ImageUtil import getImageHash, readImageFromBytes
import sys
import getopt
import time


def checkAndClick(target,screen,adb):
        tmp = screen.crop(target["area"])
        hash = getImageHash(image=tmp)
        if hash == target["hash"]:
            print(target["text"])
            adb.touchScreen(target["area"])
            return True
        return False


def main(adb,configPath=None):

    flag = True
    lastClick = int(time.time())

    config = Config(configPath)

    while flag:
        screen = readImageFromBytes(adb.getScreen())
        t = int(time.time())

        for target in config.targets:
            if checkAndClick(target,screen,adb):
                lastClick = t
                break

        #300秒未操作则随机点击一次
        if t - lastClick > 300:
            adb.touchScreen([0,0,config.picSize[0],config.picSize[1]])

if __name__ == '__main__':

    adb = ADBUtil()
    configPath = None

    try:
        opts,args = getopt.getopt(sys.argv[1:], "d:s:c:")
        
        for o,a in opts:
            if o == "-d":
                adb.setDevice(a)
            elif o == "-s":
                adb.getScreen(savePath=a)
                sys.exit()
            elif o == "-c":
                configPath = a

    except getopt.GetoptError:
        print("参数错误")

    main(adb,configPath)
        

    

