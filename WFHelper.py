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
    screen = None

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

    def checkRequirement(self, requirement):
        if len(requirement) < 3:
            key = self.actionManager.formatArg(requirement[0])
            if self.state.getState(key) == 0:
                return False
            else:
                return True
        else:
            key = self.actionManager.formatArg(requirement[0])
            ope = requirement[1]
            lim = requirement[2]
            if ope == "==":
                return True if self.state.getState(key) == lim else False
            else:
                val = 0
                if not self.state.has(key):
                    self.state.setState(key, 0)
                else:
                    val = self.state.getState(key)
                try:
                    val = float(val)
                    lim = float(lim)
                    if ope == "<":
                        return True if val < lim else False
                    elif ope == "<=":
                        return True if val <= lim else False
                    elif ope == ">":
                        return True if val > lim else False
                    elif ope == ">=":
                        return True if val >= lim else False
                    else:
                        return False
                except TypeError as arg:
                    Log.error("错误的边界值 : {}".format(arg))
                    return False

    def mainLoop(self, targets):

        t = int(time.time())

        for target in targets:
            if "requirement" not in target or self.checkRequirement(target["requirement"]):
                if "hash" not in target or self.check(target, self.screen):
                    if "hash" not in target:
                        Log.info("{} - 直接操作".format(target["text"]))
                    self.actionManager.doAction(target)
                    self.updateActionTime(t)
                    return True

        # 长时间未操作则随机点击一次
        if t - self.state.getState("lastActionTime") > self.config.randomClickDelay:
            Log.info("长时间未操作，随机点击一次")
            adbUtil.touchScreen(self.config.randomClickArea)
            self.updateActionTime(t)
        return False

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
            self.screen = readImageFromBytes(adbUtil.getScreen())
            self.mainLoop(targets)
            time.sleep(self.config.loopDelay)

    def stop(self):
        self.state.setState("isRunning", False)
        self.state.setState("startTime", "")
        Log.info("停止自动脚本")

    def __init__(self, config):
        self.config = config
        self.actionManager = ActionManager(self)
