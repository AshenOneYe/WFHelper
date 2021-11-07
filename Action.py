
from utils.ADBUtil import adbUtil
import time
from utils.LogUtil import Log
from State import State


class ActionManager:
    wfhelper = None
    state = State()

    def formatArg(self, arg):
        while isinstance(arg, str) and '$' in arg:
            argLeft = arg[:arg.rfind("$")]
            argRight = arg[arg.rfind("$")+1:]
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

    def sleep(self, args):
        time.sleep(args[0])

    def accessState(self, args):
        action, name, value = args

        name = self.formatArg(name)
        value = self.formatArg(value)
        if name is None:
            return

        if action == 'set':
            self.state.setState(name, value)

        if action == 'increase':
            if not self.state.has(name):
                self.state.setState(name, 0)
            value = int(value) + int(self.state.getState(name))
            self.state.setState(name, value)

    def subTarget(self, args):
        targets = self.wfhelper.config.targetList[args[0]]
        self.wfhelper.mainLoop(targets)

    def getTargetFromName(self, targetName):
        for target in self.config.targets:
            if target["name"] == targetName:
                return target

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

    def doAction(self, target):
        actions = target["actions"]
        for action in actions:
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
            elif action["name"] == "state":
                self.accessState(action["args"])
            elif action["name"] == "subTargets":
                self.subTarget(action["args"])
            elif action["name"] == "info":
                self.info(action["args"])
            elif action["name"] == "exit":
                import sys
                sys.exit()
            else:
                Log.error(
                    "action:'{}'不存在！请检查'{}'的配置文件".format(
                        action["name"], target["name"])
                )

    def __init__(self, wfhelper):
        self.wfhelper = wfhelper
        self.state = wfhelper.state
