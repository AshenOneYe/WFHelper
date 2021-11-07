import time
from State import State
from Config import Config
from utils.ADBUtil import adbUtil
from utils.ImageUtil import getImageHash, readImageFromBytes, similarity
from utils.LogUtil import Log
from Action import ActionManager


class WFHelper:

    actionManager = None
    config = Config()
    state = State()

    def check(self, target, screen):
        tmp = screen.crop(target["area"])
        hash = getImageHash(image=tmp)
        s = similarity(hash1=hash, hash2=target["hash"])
        similarityThreshold = self.config.similarityThreshold
        if "similarityThreshold" in target:
            similarityThreshold = target["similarityThreshold"]
        if s >= similarityThreshold:
            Log.info("{} - 识别相似度：{}".format(target["text"], s))
            return True
        return False

    def mainLoop(self, targets):

        t = int(time.time())

        screen = readImageFromBytes(adbUtil.getScreen())

        for target in targets:
            if self.check(target, screen):
                self.actionManager.doAction(target)
                self.updateActionTime(t)
                break

        # 长时间未操作则随机点击一次
        if t - self.state.getState("lastActionTime") > self.config.randomClickDelay:
            Log.info("长时间未操作，随机点击一次")
            adbUtil.touchScreen(self.config.randomClickArea)
            self.updateActionTime(t)

    def updateActionTime(self, time):
        self.state.setState("lastActionTime", time)

    def run(self):
        self.start()

        try:
            while True:
                while self.state.getState("isRunning"):
                    targets = self.config.targetList[self.state.getState("currentTargets")]
                    self.mainLoop(targets)
                # 当脚本被远程停止时，持续更新lastActionTime
                    time.sleep(self.config.loopDelay)
                self.updateActionTime(int(time.time()))

        except KeyboardInterrupt:
            Log.critical("退出!!!")

    def start(self):
        self.state.setState("isRunning", True)
        self.state.merge(self.config.summary)
        self.state.setState("startTime", int(time.time()))
        Log.info("开始自动脚本")

    def stop(self):
        self.state.setState("isRunning", False)
        self.state.setState("startTime", "")
        Log.info("停止自动脚本")

    def __init__(self, config):
        self.config = config
        self.actionManager = ActionManager(self)
