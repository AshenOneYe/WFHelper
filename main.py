from Config import *
from server.Server import Server
from utils.ADBUtil import *
from utils.ImageUtil import getImageHash, readImageFromBytes
import sys
import getopt
import time
import threading


class Main():

    adb = None
    config = None
    lastActionTime = int(time.time())
    lastLog = ""
    isRunning = False
    serverThread = None

    def log(self,log):
        print(log)
        self.lastLog = log

    def check(self,target,screen):
        tmp = screen.crop(target["area"])
        hash = getImageHash(image=tmp)
        if hash == target["hash"]:
            self.log(target["text"])
            return True
        return False

    def click(self,area):
        self.adb.touchScreen(area)


    def getTargetFromName(self,targetName):
        for target in self.config.targets:
            if target["name"] == targetName:
                return target
      

    def waitFor(self,selfTarget,waitTargetName):
        self.log("等待{}".format(waitTargetName))
        target = self.getTargetFromName(waitTargetName)

        while True:
            screen = readImageFromBytes(self.adb.getScreen())
            self.adb.touchScreen((0,0,self.config.picSize[0],2))
            if self.check(selfTarget,screen):
                self.adb.touchScreen(selfTarget["area"])
                
            if self.check(target,screen):
                self.doAction(target)
                break


    def doAction(self,target):
        try:
            opts,args = getopt.getopt(target["action"], "c:w:")
            
            for o,a in opts:
                if o == "-c":
                    if a==None:
                        self.click(target["area"])
                    else:
                        self.click(a)

                if o == "-w":
                    self.waitFor(target,a)

        except getopt.GetoptError:
            print("配置文件中{}的action参数错误".format(target["name"]))
            sys.exit()


    def start(self):

        self.isRunning = True
        self.lastActionTime = int(time.time())

        try:
            while self.isRunning:
                screen = readImageFromBytes(self.adb.getScreen())
                t = int(time.time())

                for target in self.config.targets:
                    if self.check(target,screen):
                        self.doAction(target)
                        self.lastActionTime = t
                        break

                #300秒未操作则随机点击一次
                if t - self.lastActionTime > 300:
                    self.log("长时间未操作，随机点击一次")
                    self.adb.touchScreen((0,0,self.config.picSize[0],2))
                    self.lastActionTime = t
        except KeyboardInterrupt:
            print("退出")
            sys.exit()


    def startServer(self):
        self.server.startServer()

    def __init__(self,argv) -> None:

        self.adb = ADBUtil()
        configPath = None

        try:
            opts,args = getopt.getopt(argv, "d:s:c:")
            
            for o,a in opts:
                if o == "-d":
                    self.log("设备名 : {}".format(a))
                    self.adb.setDevice(a)
                elif o == "-s":
                    self.log("截图保存至 : {}".format(a))
                    self.adb.getScreen(savePath=a)
                    sys.exit()
                elif o == "-c":
                    configPath = a

                # TODO -v 参数打印log信息

        except getopt.GetoptError:
            print("参数错误")

        self.config = Config(configPath)
        self.server = Server(self)

        self.serverThread = threading.Thread(target=self.server.startServer)
        # 设置主线程退出时同时关闭Server
        self.serverThread.setDaemon(True)
        self.serverThread.start()



if __name__ == '__main__':
    main = Main(sys.argv)
    main.start()