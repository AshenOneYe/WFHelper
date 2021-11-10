import time
from State import State
from Config import Config
from utils.ADBUtil import adbUtil
from utils.ImageUtil import readImageFromBytes, similarity
from utils.LogUtil import Log
from Action import ActionManager


class WFHelper:

    actionManager = None
    config = Config()
    state = State()

    def check(self, target, screen):
        tmp = screen.crop(target["area"])
        s = similarity(tmp, target)
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

    def start(self):
        self.state.setState("isRunning", True)
        self.state.merge(self.config.summary)
        self.state.setState("startTime", int(time.time()))
        Log.info("开始自动脚本")
        while self.state.getState("isRunning"):
            targets = self.config.targetList[self.state.getState("currentTargets")]
            self.mainLoop(targets)
            time.sleep(self.config.loopDelay)

    def stop(self):
        self.state.setState("isRunning", False)
        self.state.setState("startTime", "")
        Log.info("停止自动脚本")

    def __init__(self, config):
        self.config = config
        self.actionManager = ActionManager(self)
