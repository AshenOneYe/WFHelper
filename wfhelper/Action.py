import random
import re
import time
from os import path

from asteval import Interpreter
from mergedeep import merge, Strategy

from .State import State
from utils import adbUtil
from utils import Log

aeval = Interpreter()


class ActionManager:
    wfhelper = None
    state = State()

    def eval(self, arg):
        if isinstance(arg, str) and "$" in arg:
            func = arg

            while isinstance(func, str) and "$" in func:
                match = re.compile(r"\$[\u4E00-\u9FA5A-Za-z0-9_+·]+")
                items = re.findall(match, func)

                for item in items:
                    func = func.replace(item, str(self.state.getState(item[1:])))

            result = aeval(func)

            Log.debug('计算"{}"结果为: {}'.format(arg, result))

        else:
            result = arg

        return result

    def formatArg(self, arg):
        while isinstance(arg, str) and "$" in arg:
            argLeft = arg[: arg.rfind("$")]
            argRight = arg[arg.rfind("$") + 1:]
            if argLeft == "":
                tmp = self.state.getState(argRight)
                if tmp is None:
                    return None
                arg = tmp
            else:
                tmp = self.state.getState(argRight)
                if tmp is None:
                    return None
                arg = argLeft + self.state.getState(argRight)
        return arg

    def click(self, area):
        adbUtil.touchScreen(area)

    def swipe(self, args):
        x1, y1, x2, y2 = args
        adbUtil.swipeScreen(x1, y1, x2, y2)

    def delay(self, args):
        if len(args) > 1:
            delay = random.uniform(args[0], args[1])
        else:
            delay = args[0]
        time.sleep(delay)

    def accessState(self, args):
        action, name, value = args

        name = self.formatArg(name)
        value = self.eval(value)

        if name is None:
            return

        if action == "set":
            self.state.setState(name, value)

        if action == "merge":
            state = self.state.getState(name)

            if not isinstance(state, dict):
                return

            self.state.setState(name, merge(state, value, strategy=Strategy.ADDITIVE))

        if action == "increase":
            if name == "无":
                return

            if self.state.has(name):
                value = int(value) + int(self.state.getState(name))

            self.state.setState(name, value)

    def changeTarget(self, args):
        name, targetName = args
        targets = self.wfhelper.config.targetList[name]

        return self.wfhelper.mainLoop(targets, targetName)

    def changeTargets(self, args):
        if len(args) == 2:
            name, mode = args
        else:
            name, mode = args[0], "once"

        if mode == "loop":
            return self.state.setState("currentTargets", name)

        if mode == "once":
            return self.changeTarget([name, None])

        return False

    def info(self, args):
        if len(args) == 0:
            Log.error("`info` action的参数不能为空")
            return
        tmp = []
        for t in args:
            t = self.formatArg(t)
            tmp.append(t)
        if len(tmp) == 1:
            Log.info(tmp[0])
        else:
            Log.info(tmp[0].format(*tmp[1:]))

    def getScreen(self, savePath):
        adbUtil.getScreen(savePath)

    def match(self, target, args):
        exp, callbacks = args

        result = str(self.eval(exp))

        actions = None

        if result in callbacks:
            actions = callbacks[result]

        if actions is not None:
            self.doActions(target, actions)

    def doAction(self, target, action):
        if action["name"] == "click":
            if "args" not in action:
                if "area" in target:
                    self.click(target["area"])
                else:
                    self.click(self.wfhelper.config.screenSize)
            else:
                self.click(action["args"])
        elif action["name"] == "swipe":
            self.swipe(action["args"])
        elif action["name"] == "delay" or action["name"] == "sleep":
            self.delay(action["args"])
        elif action["name"] == "state":
            self.accessState(action["args"])
        elif action["name"] == "changeTargets":
            self.changeTargets(action["args"])
        elif action["name"] == "changeTarget":
            self.changeTarget(action["args"])
        elif action["name"] == "info":
            self.info(action["args"])
        elif action["name"] == "exit":
            import sys

            sys.exit()
        elif action["name"] == "getScreen":
            if "args" not in action:
                savePath = path.join(
                    self.wfhelper.config.configDir,
                    "temp/{}.png".format(int(time.time())),
                )
                self.getScreen(savePath)
            else:
                self.getScreen(action["args"])
        elif action["name"] == "match":
            self.match(target, action["args"])
        else:
            Log.error(
                "action:'{}'不存在！请检查'{}'的配置文件".format(action["name"], target["name"])
            )

    def doActions(self, target, actions=None):
        if actions is None:
            actions = target["actions"]
        for action in actions:
            self.doAction(target, action)

    def __init__(self, wfhelper):
        self.wfhelper = wfhelper
        self.state = wfhelper.state
