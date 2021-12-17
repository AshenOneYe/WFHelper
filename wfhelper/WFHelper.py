import random
import time
from typing import Any, Dict, List

from PIL.Image import Image
from utils import Log, adbUtil, readImageFromBytes, similarity

from .Action import ActionManager
from .Global import GlobalState, GlobalConfig


class WFHelper:
    def __init__(self):
        self.actionManager = None
        self.lastFrame = None
        self.screen = None

    def check(self, target: Dict[str, Any], screen: Image):
        result = False

        try:
            tmp = screen.crop(target["area"])
            s = similarity(tmp, target)
            similarityThreshold = GlobalConfig.similarityThreshold
            if "similarityThreshold" in target:
                similarityThreshold = target["similarityThreshold"]
            if s >= similarityThreshold:
                if "text" in target:
                    Log.info("{} - 识别相似度：{}".format(target["text"], s))
                result = True
        finally:
            return result

    def mainLoop(self, targets: List[Any], targetName: str = None):

        t = int(time.time())
        screen = readImageFromBytes(self.lastFrame)

        for target in targets:
            if targetName is not None:
                if target["name"] != targetName:
                    continue
            if "hash" not in target or self.check(target, screen):
                if "hash" not in target:
                    if "text" in target:
                        Log.info("{} - 直接操作".format(target["text"]))
                self.actionManager.doActions(target)
                self.updateActionTime(t)
                return True

        # 长时间未操作则随机点击一次
        if t - GlobalState.getState("lastActionTime") > GlobalConfig.randomClickDelay:
            Log.info("长时间未操作，随机点击一次")
            adbUtil.touchScreen(GlobalConfig.randomClickArea)
            self.updateActionTime(t)
        return False

    def loopDelay(self):
        a, b = GlobalConfig.loopDelay
        delay = random.uniform(a, b)
        time.sleep(delay)

    def isIdle(self):
        if GlobalState.getState("isRunning"):
            return False
        if GlobalState.getState("lastActionTime") + 10 > int(time.time()):
            return False
        return True

    def updateActionTime(self, time):
        GlobalState.setState("lastActionTime", time)

    def run(self):

        self.actionManager = ActionManager(self)

        self.start()

        try:
            while True:
                if not self.isIdle():
                    targets = GlobalConfig.targetList[GlobalState.getState("currentTargets")]
                    t = time.time()
                    self.mainLoop(targets)
                    Log.debug("比对循环耗时: {}秒".format(time.time() - t))
                    self.loopDelay()
        except KeyboardInterrupt:
            import sys

            sys.exit()

    def start(self):
        GlobalState.merge(GlobalConfig.state)
        GlobalState.setState("isRunning", True)
        GlobalState.setState("startTime", int(time.time()))
        Log.info("开始自动脚本")

    def stop(self):
        GlobalState.setState("isRunning", False)
        GlobalState.setState("startTime", "")
        Log.info("停止自动脚本")
