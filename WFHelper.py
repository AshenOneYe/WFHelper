import time

from utils.ADBUtil import adbUtil
from utils.ImageUtil import getImageHash, readImageFromBytes, similarity
from utils.LogUtil import Log


class WFHelper:

    lastActionTime = int(time.time())
    isRunning = False
    config = None
    summary = None

    def check(self, target, screen):
        try:
            tmp = screen.crop(target["area"])
            hash = getImageHash(image=tmp)
            s = similarity(hash1=hash, hash2=target["hash"])
            similarityThreshold = self.config.similarityThreshold
            if "similarityThreshold" in target:
                similarityThreshold = target["similarityThreshold"]
            if s >= similarityThreshold:
                Log.info("{} - 识别相似度：{}".format(target["text"], s))
                return True
        except SyntaxError:
            pass
        return False

    def click(self, area):
        adbUtil.touchScreen(area)

    def sleep(self, args):
        time.sleep(args[0])

    def updateSummary(self, args):
        name, action, value = args

        if isinstance(value, str) and value.startswith('$'):
            value = getattr(self, value[1:])

        if name not in self.summary:
            self.summary[name] = ""

        if action == 'replace':
            self.summary[name] = value

        if action == 'increase':
            self.summary[name] = int(self.summary[name]) + int(value)

    def count(self, target):
        if "count" not in target:
            target["count"] = 0
        target["count"] = target["count"] + 1
        Log.info("已完成`{}`{}次".format(target["name"], target["count"]))
        # Log.info(args[0].format(args[1:]))

    def getTargetFromName(self, targetName):
        for target in self.config.targets:
            if target["name"] == targetName:
                return target

    # 该功能不稳定
    def waitFor(self, selfTarget, args):
        target = self.getTargetFromName(args[0])

        startTime = int(time.time())

        while self.isRunning:
            screen = readImageFromBytes(adbUtil.getScreen())
            adbUtil.touchScreen((0, 0, self.config.screenSize[0] / 2, 2))
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
                if (
                    "args" not in action
                    or len(action["args"]) == 0
                    or action["args"][0] is None
                ):
                    self.click(target["area"])
                else:
                    self.click(action["args"][0])
            elif action["name"] == "sleep":
                self.sleep(action["args"])
            elif action["name"] == "summary":
                self.updateSummary(action["args"])
            elif action["name"] == "waitFor":
                self.waitFor(target, action["args"])
            elif action["name"] == "count":
                self.count(target)
            elif action["name"] == "pass":
                pass
            elif action["name"] == "exit":
                import sys
                sys.exit()
            else:
                Log.error(
                    "action:'{}'不存在！请检查'{}'的配置文件".format(
                        action["name"], target["name"])
                )

    def mainLoop(self):
        while self.isRunning:
            t = int(time.time())

            screen = readImageFromBytes(adbUtil.getScreen())

            for target in self.config.targets:
                if self.check(target, screen):
                    self.doAction(target)
                    self.updateActionTime(t)
                    break

            # 长时间未操作则随机点击一次
            if t - self.lastActionTime > self.config.randomClickDelay:
                Log.info("长时间未操作，随机点击一次")
                adbUtil.touchScreen(self.config.randomClickArea)
                self.updateActionTime(t)

            time.sleep(self.config.loopDelay)

        # 当脚本被远程停止时，持续更新lastActionTime
        self.updateActionTime(int(time.time()))

    def updateActionTime(self, time):
        self.lastActionTime = time
        self.updateSummary(["lastActionTime", "replace", time])

    def init(self):
        self.start()

        try:
            while True:
                self.mainLoop()
        except KeyboardInterrupt:
            Log.critical("退出!!!")

    def start(self):
        self.isRunning = True
        self.summary = self.config.summary
        self.updateSummary(["startTime", "replace", int(time.time())])
        Log.info("开始自动脚本")

    def stop(self):
        self.isRunning = False
        self.updateSummary(["startTime", "replace", ""])
        Log.info("停止自动脚本")

    def __init__(self, config):
        self.config = config
