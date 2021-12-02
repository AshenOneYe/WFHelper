import random
import time

from Action import ActionManager
from Config import Config
from State import State
from utils.ADBUtil import adbUtil
from utils.ImageUtil import readImageFromBytes, similarity
from utils.LogUtil import Log


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
                if "text" in target:
                    Log.info("{} - 识别相似度：{}".format(target["text"], s))
                result = True
        finally:
            return result

    def checkRequire(self, require):
        if len(require) == 1:
            # *** 仅有一个参数时，将其当作变量名进行判断 ***
            key = self.actionManager.formatArg(require[0])
            val = self.state.getState(key)
            if val == 0 or val is None:
                return False
            else:
                return True
        else:
            statement = ""
            for arg in require:
                statement += "{}".format(self.actionManager.formatArg(arg))

            while True:
                try:
                    # FIXME eval 不安全，请使用 aeval 模块代替
                    return eval(statement, self.state.content)

                except NameError as e:

                    # *** 解析所缺变量名，写法待改进，大概在3.10可以直接用name？ ***
                    var = e.args[0]
                    var = var[var.find("'") + 1: var.rfind("'")]
                    # ***********************************************************

                    self.state.setState(var, 0)
                    Log.error("缺少变量 : {}. 已赋初值 0".format(var))

                except SyntaxError as e:
                    Log.error("语法错误 : {}".format(e))
                    return False

                except TypeError as e:
                    Log.error("类型错误 : {}".format(e))
                    return False

                except ArithmeticError as e:
                    Log.error("运算错误 : {}".format(e))
                    return False

                except Exception as e:
                    Log.error("其他错误 : {}".format(e))
                    return False

            # *** 以下为旧的硬编码实现方法 ***

            # key = self.actionManager.formatArg(require[0])
            # ope = require[1]
            # lim = require[2]
            # if ope == "==":
            #     return True if self.state.getState(key) == lim else False
            # else:
            #     val = 0
            #     if not self.state.has(key):
            #         self.state.setState(key, 0)
            #     else:
            #         val = self.state.getState(key)
            #     try:
            #         val = float(val)
            #         lim = float(lim)
            #         if ope == "<":
            #             return True if val < lim else False
            #         elif ope == "<=":
            #             return True if val <= lim else False
            #         elif ope == ">":
            #             return True if val > lim else False
            #         elif ope == ">=":
            #             return True if val >= lim else False
            #         else:
            #             return False
            #     except TypeError as arg:
            #         Log.error("错误的边界值 : {}".format(arg))
            #         return False

    def mainLoop(self, targets):

        t = int(time.time())

        for target in targets:
            if "require" in target and not self.checkRequire(target["require"]):
                continue

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

    def run(self, isDebug=False):
        if isDebug:
            Log.setDebugLevel()

        self.state.setState("isDebug", isDebug)
        self.start()

        while True:
            if not self.isIdle():
                targets = self.config.targetList[self.state.getState("currentTargets")]
                self.screen = readImageFromBytes(adbUtil.getScreen())
                self.mainLoop(targets)
                self.loopDelay()

    def start(self):
        self.state.merge(self.config.state)
        self.state.setState("isRunning", True)
        self.state.setState("startTime", int(time.time()))
        Log.info("开始自动脚本")

    def stop(self):
        self.state.setState("isRunning", False)
        self.state.setState("startTime", "")
        Log.info("停止自动脚本")

    def __init__(self, config):
        self.config = config
        self.actionManager = ActionManager(self)
