import random
import time

from wfhelper.Action import ActionManager
from wfhelper.Config import Config
from wfhelper.State import State
from utils.ADBUtil import adbUtil
from utils.ImageUtil import readImageFromBytes, similarity
from utils.LogUtil import Log


class WFHelper:

    actionManager = None
    config = Config()
    state = State()
    screen = None
    serial = None
    isDebug = False

    def check(self, target, screen):
        result = False

        try:
            tmp = screen.crop(target["area"])
            s = similarity(tmp, target)
            similarityThreshold = self.config.similarityThreshold
            if "similarityThreshold" in target:
                similarityThreshold = target["similarityThreshold"]
            if s >= similarityThreshold:
                if "text" in target:
                    Log.info("{} - 识别相似度：{}".format(target["text"], s))
                result = True
        finally:
            return result

    def mainLoop(self, targets, targetName=None):

        t = int(time.time())

        for target in targets:
            if targetName is not None:
                if target['name'] != targetName:
                    continue
            if "hash" not in target or self.check(target, self.screen):
                if "hash" not in target:
                    if "text" in target:
                        Log.info("{} - 直接操作".format(target["text"]))
                self.actionManager.doActions(target)
                self.updateActionTime(t)
                return True

        # 长时间未操作则随机点击一次
        if t - self.state.getState("lastActionTime") > self.config.randomClickDelay:
            Log.info("长时间未操作，随机点击一次")
            adbUtil.touchScreen(self.config.randomClickArea)
            self.updateActionTime(t)
        return False

    def loopDelay(self):
        a, b = self.config.loopDelay
        delay = random.uniform(a, b)
        time.sleep(delay)

    def isIdle(self):
        if self.state.getState("isRunning"):
            return False
        if self.state.getState("lastActionTime") + 10 > int(time.time()):
            return False
        return True

    def updateActionTime(self, time):
        self.state.setState("lastActionTime", time)

    def run(self):

        self.actionManager = ActionManager(self)

        if self.isDebug:
            Log.setDebugLevel()

        self.state.setState("isDebug", self.isDebug)
        self.start()

        try:
            while True:
                if not self.isIdle():
                    targets = self.config.targetList[self.state.getState("currentTargets")]
                    t = time.time()
                    self.updateScreen()
                    Log.debug("截图耗时: {}秒".format(time.time() - t))
                    t = time.time()
                    self.mainLoop(targets)
                    Log.debug("比对循环耗时: {}秒".format(time.time() - t))
                    self.loopDelay()
        except KeyboardInterrupt:
            import sys
            sys.exit()

    def updateScreen(self):
        frame = adbUtil.getScreen()
        screen = readImageFromBytes(frame)
        if screen is not None:
            self.screen = screen
            if self.screenUpdateCallback is not None:
                self.screenUpdateCallback(frame)

    def start(self):
        self.state.merge(self.config.state)
        self.state.setState("isRunning", True)
        self.state.setState("startTime", int(time.time()))
        Log.info("开始自动脚本")

    def stop(self):
        self.state.setState("isRunning", False)
        self.state.setState("startTime", "")
        Log.info("停止自动脚本")

    def setConfig(self, config):
        self.config = config

    def enableDebug(self, isDebug):
        self.isDebug = isDebug
