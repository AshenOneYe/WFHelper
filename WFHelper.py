from Config import config
from utils.ADBUtil import adbUtil
from utils.ImageUtil import *
import sys
import getopt
import time
from utils.LogUtil import Log

class WFHelper():

    lastActionTime = int(time.time())
    isRunning = False

    def check(self,target,screen):
        tmp = screen.crop(target["area"])
        hash = getImageHash(image=tmp)
        # 写死0.9
        s = similarity(hash1=hash,hash2=target["hash"])
        if s >= 0.9:
            Log.info("{},识别相似度:{}".format(target["text"],s))
            return True
        return False

    def click(self,area):
        adbUtil.touchScreen(area)


    def getTargetFromName(self,targetName):
        for target in config.targets:
            if target["name"] == targetName:
                return target
      

    def waitFor(self,selfTarget,waitTargetName):
        Log.info("等待{}".format(waitTargetName))
        target = self.getTargetFromName(waitTargetName)

        startTime = int(time.time())

        while self.isRunning:
            screen = readImageFromBytes(adbUtil.getScreen())
            self.screen = screen
            adbUtil.touchScreen((0, 0, config.picSize[0]/2, 2))
            if self.check(selfTarget,screen):
                adbUtil.touchScreen(selfTarget["area"])
                
            if self.check(target,screen):
                self.doAction(target)
                break

            # 设置timeout防止卡死
            if int(time.time()) - startTime > 20:
                break

    def doAction(self,target):
        try:
            opts,args = getopt.getopt(target["action"], "c:w:s:")

            for o,a in opts:
                if o == "-c":
                    if a in (None,""," "):
                        self.click(target["area"])
                    else:
                        self.click(a)

                if o == "-w":
                    self.waitFor(target,a)

                if o == "-s":
                    time.sleep(int(a))

        except getopt.GetoptError:
            Log.error("配置文件中{}的action参数错误".format(target["name"]))
            sys.exit()


    def mainLoop(self):
        while self.isRunning:
            screen = readImageFromBytes(adbUtil.getScreen())
            t = int(time.time())

            for target in config.targets:
                if self.check(target,screen):
                    self.doAction(target)
                    self.lastActionTime = t
                    break

            #300秒未操作则随机点击一次
            if t - self.lastActionTime > 300:
                Log.info("长时间未操作，随机点击一次")
                adbUtil.touchScreen((0, 0, config.picSize[0]/2, 2))
                self.lastActionTime = t

        ## 当脚本被远程停止时，持续更新lastActionTime
        self.lastActionTime = int(time.time())


    def start(self):
        self.lastActionTime = int(time.time())
        self.isRunning = True

        try:
            while True:
                self.mainLoop()
        except KeyboardInterrupt:
            Log.critical("退出!!!")
        

    def stop(self):
        self.isRunning = False
        Log.info("停止自动脚本")

wfhelper = WFHelper()