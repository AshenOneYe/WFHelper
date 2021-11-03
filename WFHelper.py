from Config import config
from utils.ADBUtil import adbUtil
from utils.ImageUtil import getImageHash, similarity, readImageFromBytes
import time
from utils.LogUtil import Log


class WFHelper():

    lastActionTime = int(time.time())
    isRunning = False

    def check(self, target, screen):
        tmp = screen.crop(target["area"])
        hash = getImageHash(image=tmp)
        s = similarity(hash1=hash, hash2=target["hash"])
        similarityThreshold = config.similarityThreshold
        if "similarityThreshold" in target:
            similarityThreshold = target["similarityThreshold"]
        if s >= similarityThreshold:
            Log.info("{},识别相似度:{}".format(target["text"], s))
            return True
        return False

    def click(self, area):
        adbUtil.touchScreen(area)

    def sleep(self, args):
        time.sleep(args[0])

    def getTargetFromName(self, targetName):
        for target in config.targets:
            if target["name"] == targetName:
                return target

    # 该功能不稳定
    def waitFor(self, selfTarget, args):
        target = self.getTargetFromName(args[0])

        startTime = int(time.time())

        while self.isRunning:
            screen = readImageFromBytes(adbUtil.getScreen())
            self.screen = screen
            adbUtil.touchScreen((0, 0, config.screenSize[0]/2, 2))
            if self.check(selfTarget, screen):
                adbUtil.touchScreen(selfTarget["area"])

            if self.check(target, screen):
                break

            # 设置timeout防止卡死
            timeout = 20
            try:
                timeout = args[1]
            except IndexError:
                pass
            if int(time.time()) - startTime > timeout:
                break

    def doAction(self, target):
        actions = target["actions"]
        for action in actions:
            if "info" in action:
                Log.info(action["info"])
            if action["name"] == "click":
                if "args" not in action or \
                        len(action["args"]) == 0 or action["args"][0] is None:
                    self.click(target["area"])
                else:
                    self.click(action["args"][0])
            elif action["name"] == "sleep":
                self.sleep(action["args"])
            elif action["name"] == "waitFor":
                self.waitFor(target, action["args"])
            elif action["name"] == "pass":
                pass
            else:
                Log.error(
                    "action'{}'不存在！请检查'{}'的配置文件".format(
                        action["name"], target["name"]
                    )
                )

    def mainLoop(self):
        while self.isRunning:
            screen = readImageFromBytes(adbUtil.getScreen())
            t = int(time.time())

            for target in config.targets:
                if self.check(target, screen):
                    self.doAction(target)
                    self.lastActionTime = t
                    break

            # 300秒未操作则随机点击一次
            if t - self.lastActionTime > config.randomClickDelay:
                Log.info("长时间未操作，随机点击一次")
                adbUtil.touchScreen(config.randomClickArea)
                self.lastActionTime = t

        # 当脚本被远程停止时，持续更新lastActionTime
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
