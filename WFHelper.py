import time, random
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
        result = False
        
        try:
            # FIXME 有几率报错 broken PNG file
            tmp = screen.crop(target["area"])
            s = similarity(tmp, target)
            similarityThreshold = self.config.similarityThreshold
            if "similarityThreshold" in target:
                similarityThreshold = target["similarityThreshold"]
            if s >= similarityThreshold:
                Log.info("{} - 识别相似度：{}".format(target["text"], s))
                result = True
        finally:
            return result

    def mainLoop(self, targets):

        t = int(time.time())

        screen = readImageFromBytes(adbUtil.getScreen())

        for target in targets:
            if self.check(target, screen):
                self.actionManager.doAction(target)
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
        self.start()

        while True:
            if not self.isIdle():
                targets = self.config.targetList[self.state.getState("currentTargets")]
                self.mainLoop(targets)
                self.loopDelay()

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
