import re
import time
from os import path
from typing import Any, Dict, List
from asteval import Interpreter
from utils import Log, adbUtil
from .Global import GlobalConfig, GlobalState
from .Target import Target
import sys

aeval = Interpreter()


class ActionManager:
    def __init__(self, wfhelper):
        self.wfhelper = wfhelper

    def formatArg(self, arg):
        while isinstance(arg, str) and "$" in arg:
            argLeft = arg[: arg.rfind("$")]
            argRight = arg[arg.rfind("$") + 1:]
            if argLeft == "":
                tmp = GlobalState.getState(argRight)
                if tmp is None:
                    return None
                arg = tmp
            else:
                tmp = GlobalState.getState(argRight)
                if tmp is None:
                    return None
                arg = argLeft + GlobalState.getState(argRight)
        return arg

    def click(self, *args):
        target = args[0]  # type: Target
        area = GlobalConfig.screenSize
        if args[1] is None:
            if target.area is not None:
                area = target.area
        else:
            area = args[1][0]
        adbUtil.touchScreen(area)

    def sleep(self, *args):
        args = args[1]
        time.sleep(args[0])

    def state(self, *args):
        args = args[1]
        action, name, value = args

        name = self.formatArg(name)
        value = self.formatArg(value)
        if name is None:
            return

        if action == "set":
            GlobalState.setState(name, value)

        if action == "increase":
            if name == "无" or name is None:
                return
            if not GlobalState.has(name):
                GlobalState.setState(name, 0)
            value = int(value) + int(GlobalState.getState(name))
            GlobalState.setState(name, value)

    def changeTarget(self, *args):
        name, targetName = args
        targets = GlobalConfig.targetDict[name]

        return self.wfhelper.mainLoop(targets, targetName)

    def changeTargets(self, *args):
        args = args[1]
        if len(args) == 2:
            name, mode = args
        else:
            name, mode = args[0], "once"

        targets = GlobalConfig.targetDict[name]

        if mode == "loop":
            return GlobalState.setState("currentTargets", targets)

        if mode == "once":
            return self.changeTarget(name, None)

        return False

    def info(self, *args):
        args = args[1]
        if args is None:
            Log.error("`info` action的参数不能为空")
            return
        tmp = []
        for t in args:
            t = self.formatArg(t)
            tmp.append(t)
        if len(tmp) == 1:
            Log.info(tmp[0])
        else:
            Log.info(str(tmp[0]).format(*tmp[1:]))

    def getScreen(self, *args):
        args = args[1]
        if args[1] is None:
            savePath = path.join(
                str("./"),
                "temp/{}.png".format(int(time.time())),
            )
            adbUtil.getScreen(savePath)
        else:
            adbUtil.getScreen(args[0])

    def match(self, *args):
        target = args[0]  # type: Target
        exp, callbacks = args[1]

        func = exp

        match = re.compile(r"\$[\u4E00-\u9FA5A-Za-z0-9_+\[\]·]+")
        items = re.findall(match, func)

        for item in items:
            func = func.replace(item, str(self.formatArg(item)))

        result = str(aeval(func))

        Log.debug("判断“{}”结果为: {}".format(exp, result))

        actions = None

        if result in callbacks:
            actions = callbacks[result]

        if actions is not None:
            self.doActions(target, actions)

    def exit(self, *args):
        sys.exit()

    def doAction(self, target: Target, action: Dict[str, Any]):

        func = getattr(self, action["name"], None)
        if func is None:
            Log.error(
                "action:'{}'不存在! 请检查'{}'的配置文件".format(action["name"], target.name)
            )
        else:
            try:
                func(target, action.get("args"))
            except Exception:
                Log.error("{}执行失败，参数为: {}".format(action["name"], action.get("args")))

    def doActions(self, target: Target, actions: List[Any] = None):
        if actions is None:
            actions = target.actions
        for action in actions:
            self.doAction(target, action)
